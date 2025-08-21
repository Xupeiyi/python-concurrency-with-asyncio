import asyncio
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute


class UserCounter(WebSocketEndpoint):

    encoding = 'text'
    sockets = []

    async def _send_count(self):
        if len(self.sockets) > 0:
            count_str = str(len(self.sockets))

            task_to_socket = {}
            for socket in self.sockets:
                task = asyncio.create_task(socket.send_text(count_str))
                task_to_socket[task] = socket

            done, pending = await asyncio.wait(task_to_socket)
            for task in done:
                if task.exception() is not None and task_to_socket[task] in self.sockets:
                    self.sockets.remove(task_to_socket[task])

    async def on_connect(self, websocket):
        await websocket.accept()
        self.sockets.append(websocket)
        await self._send_count()

    async def on_disconnect(self, websocket, close_code):
        self.sockets.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket, data):
        pass


app = Starlette(routes=[WebSocketRoute('/counter', UserCounter)])
