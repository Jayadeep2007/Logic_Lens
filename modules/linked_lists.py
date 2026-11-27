
# modules/linked_lists.py

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:

    def __init__(self, list_type="Singly"):

        self.list_type = list_type
        self.head = None
        self.tail = None
        self.nodes = []

    # --------------------------------
    # REBUILD POINTER CONNECTIONS
    # --------------------------------

    def rebuild_links(self):

        self.head = self.nodes[0] if self.nodes else None
        self.tail = self.nodes[-1] if self.nodes else None

        for i, node in enumerate(self.nodes):

            # Doubly linked list previous pointer
            if self.list_type == "Doubly" and i > 0:
                node.prev = self.nodes[i - 1]
            else:
                node.prev = None

            # Next pointer
            if i < len(self.nodes) - 1:
                node.next = self.nodes[i + 1]

            elif self.list_type == "Circular" and self.nodes:
                node.next = self.head

            else:
                node.next = None

    # --------------------------------
    # CREATE LINKED LIST
    # --------------------------------

    def create(self, values):

        self.nodes = [Node(value) for value in values]

        self.rebuild_links()

    # --------------------------------
    # INSERT AT BEGINNING
    # --------------------------------

    def insert_beginning(self, value):

        self.nodes.insert(0, Node(value))

        self.rebuild_links()

    # --------------------------------
    # INSERT AT END
    # --------------------------------

    def insert_end(self, value):

        self.nodes.append(Node(value))

        self.rebuild_links()

    # --------------------------------
    # INSERT AT POSITION
    # --------------------------------

    def insert_position(self, position, value):

        if position < 0 or position > len(self.nodes):
            raise IndexError("Invalid insertion position")

        self.nodes.insert(position, Node(value))

        self.rebuild_links()

    # --------------------------------
    # DELETE BY POSITION
    # --------------------------------

    def delete_position(self, position):

        if position < 0 or position >= len(self.nodes):
            raise IndexError("Invalid deletion position")

        deleted_value = self.nodes[position].data

        self.nodes.pop(position)

        self.rebuild_links()

        return deleted_value

    # --------------------------------
    # DELETE BY VALUE
    # --------------------------------

    def delete_value(self, value):

        for i, node in enumerate(self.nodes):

            if node.data == value:

                self.nodes.pop(i)

                self.rebuild_links()

                return True

        return False

    # --------------------------------
    # SEARCH
    # --------------------------------

    def search(self, value):

        steps = []

        for i, node in enumerate(self.nodes):

            steps.append({
                "values": self.to_list(),
                "highlight": i,
                "message": (
                    f"Checking node {i} "
                    f"with value {node.data}."
                )
            })

            if node.data == value:
                return i, steps

        return -1, steps

    # --------------------------------
    # REVERSE
    # --------------------------------

    def reverse(self):

        self.nodes.reverse()

        self.rebuild_links()

    # --------------------------------
    # CONVERT TO PYTHON LIST
    # --------------------------------

    def to_list(self):

        return [node.data for node in self.nodes]

    # --------------------------------
    # LENGTH
    # --------------------------------

    def length(self):

        return len(self.nodes)

    # --------------------------------
    # GET POINTER INFORMATION
    # --------------------------------

    def get_pointer_info(self):

        result = []

        for i, node in enumerate(self.nodes):

            result.append({
                "data": node.data,
                "previous": (
                    node.prev.data
                    if node.prev else "NULL"
                ),
                "next": (
                    node.next.data
                    if node.next else "NULL"
                )
            })

        return result
