import asyncio
import aiohttp
from chapter04 import fetch_status
from util import async_timed


@async_timed
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.google.com"
        pending = [
            asyncio.create_task(fetch_status(session, url))
            for _ in range(3)
        ]

        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f'Done task count: {len(done)}')
            print(f'Pending task count: {len(pending)}')

            for done_task in done:
                print(done_task.result())


asyncio.run(main())
