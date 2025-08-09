import asyncio
from aiohttp import ClientSession
from util import async_timed
from chapter04 import fetch_status


@async_timed
async def main():
    async with ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://www.google.com")),
            asyncio.create_task(fetch_status(session, "https://www.google.com")),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)


asyncio.run(main())