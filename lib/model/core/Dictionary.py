import threading

from oset import oset


class Dictionary:
    def __init__(self):
        self.entries = []
        self.condition = threading.Lock()
        self.current = 0

    def append_from_wordlist(self, wordlist):
        self.entries = list(oset(self.entries + wordlist.process()))

    def get_with_index(self):
        self.condition.acquire()
        result = None
        try:
            result = self.entries[self.current]
        except IndexError:
            raise StopIteration
        else:
            self.current = self.current + 1
            current = self.current
            return current, result
        finally:
            self.condition.release()

    def reset(self):
        self.condition.acquire()
        self.current = 0
        self.condition.release()

    def get(self):
        _, result = self.get_with_index()
        return result

    def __next__(self):
        return self.get()

    def __len__(self):
        return len(self.entries)
