import os
import asyncio
import functools
import hashlib
from concurrent.futures.thread import ThreadPoolExecutor
import random
import string

from util import async_timed


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))


passwords = [random_password(10) for _ in range(10000)]


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


@async_timed
async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:

        tasks = []
        for password in passwords:
            hash_password = functools.partial(hash, password)
            task = loop.run_in_executor(pool, hash_password)
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
