import logging
import asyncio
import socket
from asyncio import AbstractEventLoop
import signal


async def echo(connected_socket: socket.socket, event_loop: AbstractEventLoop) -> None:
    try:
        # This await can raise a CancelledError if there's a remaining task
        # when the application is being shut down by asyncio.run
        while data := await event_loop.sock_recv(connected_socket, 1024):
            print(f"I got data: {data.decode()}")

            if data == b'boom\r\n':
                raise Exception("Boom!")

            await event_loop.sock_sendall(
                connected_socket,
                f"response from server: {data}".encode()
            )
    # Since we are not awaiting the echo task, the exception is not thrown up the call stack.
    # We need to handle the exception in the coroutine itself.
    except Exception as e:
        logging.exception(e)
    finally:
        connected_socket.close()


ECHO_TASKS = []


async def listen_for_connection(server_socket: socket.socket, event_loop: AbstractEventLoop):
    while True:
        # create one connected socket at a time - use coroutine
        connected_socket, address = await event_loop.sock_accept(server_socket)
        connected_socket.setblocking(False)
        print(f"Got a connection from {address}")

        # read and write multiple connected sockets - use task
        task = asyncio.create_task(echo(connected_socket, event_loop))
        ECHO_TASKS.append(task)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def main():
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    listening_socket.setblocking(False)
    listening_socket.bind(server_address)
    listening_socket.listen()

    for signal_name in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            sig=getattr(signal, signal_name),
            callback=shutdown
        )

    await listen_for_connection(listening_socket, loop)


async def close_tasks(tasks: list[asyncio.Task]):
    # Drawback 1: After we created the waiters list,
    # if a new connection comes in (because the listening socket is not closed),
    # there's no way to wrap it in asyncio.wait_for and add it to waiters
    waiters = [asyncio.wait_for(task, 2) for task in tasks]
    for task in waiters:
        try:
            await task
        # Drawback 2: not handling other type of errors
        except asyncio.exceptions.TimeoutError:
            pass


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
except GracefulExit:
    # Give the echo tasks a few more seconds to keep running before shutting down.
    loop.run_until_complete(close_tasks(ECHO_TASKS))
finally:
    loop.close()
