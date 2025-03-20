import aiohttp
import asyncio
import logging
from chapter04 import fetch_status
from util import async_timed


@async_timed
async def main():
    async with aiohttp.ClientSession() as session:
        args = [
            ("invalid_url", 0),
            ("https://www.google.com", 3),
            ("https://www.google.com", 3),
        ]
        fetchers = [
            asyncio.create_task(fetch_status(session, url, delay))
            for url, delay in args
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception", exc_info=done_task.exception())

        for pending_task in pending:
            pending_task.cancel()


asyncio.run(main())
