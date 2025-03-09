import asyncio
from asyncio import CancelledError
from util.delay_functions import delay


async def main():
    long_task = asyncio.create_task(delay(10))

    seconds = 0
    while not long_task.done():
        print(f"Task is running for {seconds} seconds")
        await asyncio.sleep(1)
        seconds += 1
        if seconds == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print('Task was cancelled')


asyncio.run(main())
