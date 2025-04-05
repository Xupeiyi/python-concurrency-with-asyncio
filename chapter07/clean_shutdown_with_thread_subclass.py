import socket
from threading import Thread


class ClientEchoThread(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)

                # when connection was closed by the client or shut down
                if not data:   
                    raise BrokenPipeError('Connection Closed!')
                
                print(f"Received: {data.decode()}, sending!")
                self.client.sendall(data)

        # thrown from sendall() when the client closed the connection
        except OSError as e:
            print(f"Thread interrupted by {e} excpetion, shutting down!")
        
    def close(self):
        # if the run() method is still running
        if self.is_alive():
            self.client.sendall(bytes("Shutting down!", encoding="utf-8"))
            # shutdown for read and write
            self.client.shutdown(socket.SHUT_RDWR)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen()
    connection_threads = []

    try:
        while True:
            connection, addr = server.accept()
            thread = ClientEchoThread(connection)
            connection_threads.append(thread)
            thread.start()      
    except KeyboardInterrupt:
        print("Server shutting down!")
        for thread in connection_threads:
            thread.close()
