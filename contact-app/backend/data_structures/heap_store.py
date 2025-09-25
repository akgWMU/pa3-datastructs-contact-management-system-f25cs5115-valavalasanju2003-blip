from .contact import Contact
import heapq

class HeapStore:
    def __init__(self):
        self.heap = []

    def insert(self, contact: Contact):
        heapq.heappush(self.heap, (contact.name, contact))

    def search(self, name):
        for _, c in self.heap:
            if c.name == name:
                return c
        return None

    def delete(self, name):
        for i, (_, c) in enumerate(self.heap):
            if c.name == name:
                self.heap.pop(i)
                heapq.heapify(self.heap)
                return c
        return None

    def list_all(self):
        return [vars(c) for _, c in self.heap]
