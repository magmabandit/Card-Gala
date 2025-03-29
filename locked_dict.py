import threading

class LockedDict():
    def __init__(self):
        self.dict = {}
        self.lock = threading.Lock()

    # Add a new key-value or update an existing one
    def update(self, key, value):
        with self.lock:
            self.dict[key] = value
    
    def remove(self, key):
        with self.lock:
            self.dict.pop(key)

    def get(self, key):
        with self.lock:
            return self.dict[key]
        
    def get_dict(self):
        with self.lock:
            return self.dict