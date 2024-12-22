class MyQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        # Custom implementation to add an item at the end of the list
        self.items.insert(len(self.items), item)

    def dequeue(self):
        if not self.is_empty():
            # Custom implementation to remove an item from the front of the list
            item = self.items[0]
            self.items = self.items[1:]
            return item
        else:
            raise IndexError("Dequeue from an empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
