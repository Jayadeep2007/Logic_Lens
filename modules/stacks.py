
# modules/stacks.py

class Stack:

    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity

    # PUSH
    def push(self, value):

        if self.is_full():
            raise OverflowError("Stack Overflow! Stack is full.")

        self.items.append(value)

        return self.items.copy()

    # POP
    def pop(self):

        if self.is_empty():
            raise IndexError("Stack Underflow! Stack is empty.")

        removed = self.items.pop()

        return removed, self.items.copy()

    # PEEK
    def peek(self):

        if self.is_empty():
            raise IndexError("Stack is empty.")

        return self.items[-1]

    # IS EMPTY
    def is_empty(self):
        return len(self.items) == 0

    # IS FULL
    def is_full(self):
        return len(self.items) >= self.capacity

    # GET SIZE
    def size(self):
        return len(self.items)

    # CLEAR STACK
    def clear(self):
        self.items = []

    # GET STACK
    def get_stack(self):
        return self.items.copy()

    # GET TOP
    def get_top(self):

        if self.is_empty():
            return None

        return self.items[-1]
