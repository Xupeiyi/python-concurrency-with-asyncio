import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    while response := await stream_reader.readline():
        print("received data")
        yield response.decode()


async def main():
    host: str = "www.google.com"
    request: str = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n\r\n"
        "Connection: close\r   \n"
    )

    stream_reader, stream_writer = await asyncio.open_connection(host, 80)

    try:
        stream_writer.write(request.encode())
        await stream_writer.drain()  # block until all queued data gets sent to the socket

        responses = [response async for response in read_until_empty(stream_reader)]

        print("".join(responses))
    finally:
        # close the writer and wait for it to finish closing
        stream_writer.close()
        await stream_writer.wait_closed()


asyncio.run(main())
