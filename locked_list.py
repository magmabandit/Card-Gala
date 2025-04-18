import threading

class LockedList():
    """
    class LockedList
    Thread-safe lists
    """
    def __init__(self):
        """
        Initializes class variables
        self.lock is the lock that is used to enforce exclusive access
        to the list when it is accessed by a thread
        """
        self.list = []
        self.lock = threading.Lock()

    def append(self, value):
        """
        Appends an element with the specified value to the end of the list
        Returns: None
        """
        with self.lock:
            self.list.append(value)

    def update(self, index, value):
        """
        Updates the value of the element at the specified index
        Returns: None
        """
        with self.lock:
            self.list[index] = value
    
    def remove(self, value):
        """
        Removes the first occurrence of the specified value from a list
        Returns: None
        """
        with self.lock:
            self.list.remove(value)

    def get(self, index):
        """
        Returns: the item at the specified list index
        """
        with self.lock:
            return self.list[index]
        
    def get_list(self):
        """
        Returns: the list
        Note: the returned list is no longer thread-safe
        """
        return self.list
    
    def get_length(self):
        """
        Returns: the length of the list
        """
        with self.lock:
            return len(self.list)
        
    def __iter__(self):
        """
        Returns: an iterator over a **shallow copy** of the list to ensure thread safety.
        """
        with self.lock:
            return iter(self.list.copy())