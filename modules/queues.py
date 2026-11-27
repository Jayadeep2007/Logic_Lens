
# modules/queues.py

class Queue:

    def __init__(self, capacity=10, queue_type="Simple"):
        self.items = []
        self.capacity = capacity
        self.queue_type = queue_type

    # CHECK EMPTY
    def is_empty(self):
        return len(self.items) == 0

    # CHECK FULL
    def is_full(self):
        return len(self.items) >= self.capacity

    # GET SIZE
    def size(self):
        return len(self.items)

    # ENQUEUE
    def enqueue(self, value, priority=1):

        if self.is_full():
            raise OverflowError("Queue Overflow! Queue is full.")

        if self.queue_type == "Priority":

            self.items.append({
                "value": value,
                "priority": priority
            })

            # Smaller priority number means higher priority.
            self.items.sort(
                key=lambda item: item["priority"]
            )

        else:
            self.items.append(value)

        return self.items.copy()

    # DEQUEUE
    def dequeue(self):

        if self.is_empty():
            raise IndexError("Queue Underflow! Queue is empty.")

        removed = self.items.pop(0)

        return removed, self.items.copy()

    # PEEK FRONT
    def peek(self):

        if self.is_empty():
            raise IndexError("Queue is empty.")

        return self.items[0]

    # INSERT AT FRONT - DEQUE
    def insert_front(self, value):

        if self.is_full():
            raise OverflowError("Deque is full.")

        self.items.insert(0, value)

        return self.items.copy()

    # INSERT AT REAR - DEQUE
    def insert_rear(self, value):

        if self.is_full():
            raise OverflowError("Deque is full.")

        self.items.append(value)

        return self.items.copy()

    # DELETE FROM FRONT - DEQUE
    def delete_front(self):

        if self.is_empty():
            raise IndexError("Deque is empty.")

        removed = self.items.pop(0)

        return removed, self.items.copy()

    # DELETE FROM REAR - DEQUE
    def delete_rear(self):

        if self.is_empty():
            raise IndexError("Deque is empty.")

        removed = self.items.pop()

        return removed, self.items.copy()

    # CLEAR QUEUE
    def clear(self):
        self.items = []

    # GET QUEUE
    def get_queue(self):
        return self.items.copy()

    # GET FRONT
    def get_front(self):

        if self.is_empty():
            return None

        return self.items[0]

    # GET REAR
    def get_rear(self):

        if self.is_empty():
            return None

        return self.items[-1]
