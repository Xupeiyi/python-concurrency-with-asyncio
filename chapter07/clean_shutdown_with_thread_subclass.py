import socket
from threading import Thread


class ClientEchoThread(Thread):

    def __init__(self, socket_):
        super().__init__()
        self.connected_socket = socket_

    def run(self):
        try:
            while True:
                data = self.connected_socket.recv(2048)

                # when connection was closed by the client or shut down by ourselves
                if not data:   
                    raise BrokenPipeError('Connection Closed!')
                
                print(f"Received: {data.decode()}, sending!")
                self.connected_socket.sendall(data)

        # thrown from sendall() when the client closed the connection
        except OSError as e:
            print(f"Thread interrupted by {e} exception, shutting down!")
        
    def close(self):
        # if the run() method is still running
        # the run() method won't be running if the client has already closed the connection
        if self.is_alive():
            self.connected_socket.sendall("Shutting down!\n".encode())
            # shutdown for read and write
            self.connected_socket.shutdown(socket.SHUT_RDWR)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(('127.0.0.1', 8000))
    listening_socket.listen()
    connection_threads = []

    try:
        while True:
            connected_socket, addr = listening_socket.accept()
            thread = ClientEchoThread(connected_socket)
            connection_threads.append(thread)
            thread.start()      
    except KeyboardInterrupt:
        print("Server shutting down!")
        for thread in connection_threads:
            thread.close()
