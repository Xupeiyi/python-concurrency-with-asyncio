import socket

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ("127.0.0.1", 8000)
listening_socket.bind(address)
listening_socket.listen()

connections = []

try:
    while True:
        connected_socket, client_address = listening_socket.accept()
        print(f'I got a connection from {client_address}!')
        connections.append(connected_socket)

        for connected_socket in connections:
            buffer = b''

            while buffer[-2:] != b'\r\n':
                data = connected_socket.recv(2)
                if not data:
                    break
                else:
                    print(f'I got data: {data}')
                    buffer = buffer + data
            
            print(f"All the data is: {buffer}")
            connected_socket.sendall(f"response from server: {buffer}".encode())
finally:
    listening_socket.close()

