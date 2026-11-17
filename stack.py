
class Stack:
    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity

    # Check whether the stack is empty
    def is_empty(self):
        return len(self.items) == 0

    # Check whether the stack is full
    def is_full(self):
        return len(self.items) >= self.capacity

    # Add an element to the top
    def push(self, item):
        if self.is_full():
            raise OverflowError("Stack is full.")

        self.items.append(item)

    # Remove the top element
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty.")

        return self.items.pop()

    # View the top element without removing it
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty.")

        return self.items[-1]

    # Return all stack elements
    def display(self):
        return self.items.copy()

    # Return the current number of elements
    def size(self):
        return len(self.items)
