import asyncio
from asyncio import Transport, Future, AbstractEventLoop
from typing import Optional


# Protocol methods are called when an event occurs
class HTTPGetClientProtocol(asyncio.Protocol):

    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host: str = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    async def get_response(self):
        # await the internal future until we get a response from the server
        return await self._future

    def _get_requests_bytes(self) -> bytes:
        # create the HTTP request
        request = (
            "GET / HTTP/1.1\r\n"
            "Connection: close\r\n"
            f"Host: {self._host}\r\n\r\n"
        )
        return request.encode()

    def connection_made(self, transport: Transport):
        print(f"Connection made to {self._host}")
        self._transport = transport
        # use the transport to send the request once we've established a connection
        self._transport.write(self._get_requests_bytes())

    def data_received(self, data):
        print(f'Data received!')
        # save data to internal buffer once we have it
        self._response_buffer = self._response_buffer + data

    def eof_received(self) -> Optional[bool]:
        # complete the buffer once the connection closes
        self._future.set_result(self._response_buffer.decode())
        return False

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc is None:
            # do nothing if the connection closes with no error
            print('Connection closed without error.')
        else:
            # complete the future with an exception
            self._future.set_exception(exc)
