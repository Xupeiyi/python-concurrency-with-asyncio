import asyncio
from util import delay


def call_later():
    print("I'm being called in the future!")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_later(delay=0, callback=call_later)
    await delay(1)


if __name__ == '__main__':
    # output on the console:
    # sleeping for 1 second(s)
    # I'm being called in the future!
    # finished sleeping for 1 second(s)
    asyncio.run(main())
