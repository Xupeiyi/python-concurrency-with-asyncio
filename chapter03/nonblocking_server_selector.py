import selectors
import socket
from selectors import SelectorKey

selector = selectors.DefaultSelector()

listening_socket = socket.socket()
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8000)
listening_socket.setblocking(False)
listening_socket.bind(server_address)
listening_socket.listen()

selector.register(listening_socket, selectors.EVENT_READ)

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print('No events, waiting a bit more...')
    
    for event, _ in events:
        event_socket = event.fileobj

        # event_socket is the listening socket
        if event_socket == listening_socket:
            connection, address = listening_socket.accept()
            connection.setblocking(False)
            print(f'I got a connection from {address}!')
            selector.register(connection, selectors.EVENT_READ)

        # event_socket is a connected socket
        else:
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)
