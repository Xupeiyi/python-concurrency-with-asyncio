import logging
import asyncio
from aiohttp import ClientSession
from util import async_timed
from chapter04 import fetch_status


@async_timed
async def main():
    async with ClientSession() as session:
        good_request = fetch_status(session, "https://www.google.com")
        bad_request = fetch_status(session, "invalid_url")

        done, pending = await asyncio.wait([
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request)
        ])

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error(
                    "Request got an exception",
                    exc_info=done_task.exception()
                )


asyncio.run(main())
