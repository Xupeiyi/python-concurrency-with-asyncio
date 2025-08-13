import asyncio
from asyncio import AbstractEventLoop
from threading import Thread
from chapter07.gui_with_asyncio.load_tester_gui import LoadTester


class ThreadedEventLoop(Thread):

    def __init__(self, event_loop: AbstractEventLoop):
        super().__init__()
        self._loop = event_loop

        # automatically finished when the main thread for the GUI APP has finished
        self.daemon = True

    def run(self):
        self._loop.run_forever()


loop = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
asyncio_thread.start()

app = LoadTester(loop)
app.mainloop()

