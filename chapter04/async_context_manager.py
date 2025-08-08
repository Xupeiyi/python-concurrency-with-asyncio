import asyncio
import socket
from types import TracebackType
from typing import Optional, Type


class ConnectedSocket:

    def __init__(self, listening_socket):
        self._listening_socket = listening_socket
        self._connected_socket = None

    async def __aenter__(self):
        print('Entering context manager, waiting for connection')
        loop = asyncio.get_running_loop()
        connected_socket, address = await loop.sock_accept(self._listening_socket)
        self._connected_socket = connected_socket
        print(f'Accepted connection from {address}')
        return self._connected_socket
    
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        print('Exiting context manager')
        self._connected_socket.close()
        print('Closed connection')
    

async def main():
    listening_socket = socket.socket()
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    listening_socket.setblocking(False)
    listening_socket.bind(server_address)
    listening_socket.listen()

    async with ConnectedSocket(listening_socket) as connected_socket:
        loop = asyncio.get_running_loop()
        data = await loop.sock_recv(connected_socket, 1024)
        print(f"I got data: {data}")


if __name__ == '__main__':
    asyncio.run(main())
