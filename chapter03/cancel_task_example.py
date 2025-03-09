import asyncio, signal
from asyncio import AbstractEventLoop
from util.delay_functions import delay


def cancel_tasks():
    print('Got a SIGINT signal. Cancelling tasks...')
    for task in asyncio.all_tasks():
        task.cancel()


async def main():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    await delay(10)

asyncio.run(main())