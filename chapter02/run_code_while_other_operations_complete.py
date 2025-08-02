import asyncio
from util import delay


async def say_hello():
    for i in range(2):
        await asyncio.sleep(1)
        print(f'Hello {i}!')


async def main():
    task1 = asyncio.create_task(delay(3))
    task2 = asyncio.create_task(delay(3))
    await say_hello()  # need to await say_hello first
    await task1
    await task2


if __name__ == '__main__':
    asyncio.run(main())