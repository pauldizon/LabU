
class Queue:
    def __init__(self, capacity=10):
        # Initialize an empty queue with a maximum capacity.
        self.items = []
        self.capacity = capacity

    def is_empty(self):
        # Return True if the queue has no elements.
        return len(self.items) == 0

    def is_full(self):
        # Check whether the queue reached its capacity.
        return len(self.items) >= self.capacity

    def enqueue(self, item):
        # ENQUEUE: Add a new element at the rear of the queue.
        if self.is_full():
            raise OverflowError("Queue is full.")

        self.items.append(item)

    def dequeue(self):
        # DEQUEUE: Remove the oldest element from the front.
        if self.is_empty():
            raise IndexError("Queue is empty.")

        return self.items.pop(0)

    def peek(self):
        # View the front element without removing it.
        if self.is_empty():
            raise IndexError("Queue is empty.")

        return self.items[0]

    def display(self):
        # Return a copy to protect the original queue.
        return self.items.copy()

    def size(self):
        # Return the current number of elements.
        return len(self.items)
