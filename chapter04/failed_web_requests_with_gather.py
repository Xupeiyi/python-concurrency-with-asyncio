import asyncio
from aiohttp import ClientSession
from chapter04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with ClientSession() as session:
        urls = ['https://www.google.com', 'invalid_url']
        requests = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)

        exceptions = [result for result in results if isinstance(result, Exception)]
        status_codes = [result for result in results if not isinstance(result, Exception)]

        print(f'All results: {results}')
        print(f'Status codes: {status_codes}')
        print(f'Exceptions: {exceptions}')

asyncio.run(main())
