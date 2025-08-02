import asyncio
from util import delay


async def main():
    task = asyncio.create_task(delay(10))
    shielded_task = asyncio.shield(task)
    try:
        await asyncio.wait_for(shielded_task, 5)
    except asyncio.exceptions.TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await task  # do not await shielded_task
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
