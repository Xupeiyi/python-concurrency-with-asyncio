import asyncio
from aiohttp import ClientSession
from chapter04 import fetch_status
from util import async_timed


@async_timed
async def main():
    async with ClientSession() as session:
        urls = ['https://www.google.com' for _ in range(5)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

asyncio.run(main())
