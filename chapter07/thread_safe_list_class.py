from threading import RLock


class IntListThreadsafe:

    def __init__(self, wrapped_list: list[int]):
        self._lock = RLock()  # this is a reentrant lock
        self._inner_list = wrapped_list

    def indices_of(self, to_find: int) -> list[int]:
        with self._lock:
            return [index for index, value in enumerate(self._inner_list) if value == to_find]

    def find_and_replace(self, to_find: int, replace_with: int) -> None:
        with self._lock:
            # self.indices_of need to acquire the same lock again from the same thread
            for index in self.indices_of(to_find):
                self._inner_list[index] = replace_with


threadsafe_list = IntListThreadsafe([1, 2, 1, 2, 1])
threadsafe_list.find_and_replace(1, 2)
