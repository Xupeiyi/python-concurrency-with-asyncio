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
        # by default, we are using return_when = asyncio.ALL_COMPLETED.
        # the pending set will always be empty
        done, pending = await asyncio.wait(fetchers)

    print(f'Done task count: {len(done)}')
    print(f'Pending task count: {len(pending)}')

    for done_task in done:
        # if any task went wrong, the exception is raised here
        # rather than at await asyncio.wait
        result = await done_task
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
