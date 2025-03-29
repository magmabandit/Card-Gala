import threading

class LockedList():
    def __init__(self):
        self.list = []
        self.lock = threading.Lock()

    def append(self, value):
        with self.lock:
            self.list.append(value)

    def update(self, index, value):
        with self.lock:
            self.list[index] = value
    
    def remove(self, value):
        with self.lock:
            self.list.remove(value)

    def get(self, index):
        with self.lock:
            return self.list[index]