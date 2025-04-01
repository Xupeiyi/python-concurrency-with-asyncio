import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def count(to: int) -> int:
    counter = 0
    while counter < to:
        counter += 1
    return counter


async def main():
    with ProcessPoolExecutor() as executor:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [100000000, 10000000, 3, 5, 1, 3, 5]
        calls: list[partial[int]] = [partial(count, num) for num in nums]
        coros = [loop.run_in_executor(executor, call) for call in calls]

        for result in asyncio.as_completed(coros):
            print(await result)


if __name__ == "__main__":
    asyncio.run(main())