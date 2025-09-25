from .contact import Contact

class Node:
    def __init__(self, contact):
        self.contact = contact
        self.next = None

class LinkedListStore:
    def __init__(self):
        self.head = None

    def insert(self, contact: Contact):
        node = Node(contact)
        node.next = self.head
        self.head = node

    def search(self, name):
        cur = self.head
        while cur:
            if cur.contact.name == name:
                return cur.contact
            cur = cur.next
        return None

    def delete(self, name):
        cur = self.head
        prev = None
        while cur:
            if cur.contact.name == name:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return cur.contact
            prev, cur = cur, cur.next
        return None

    def list_all(self):
        result = []
        cur = self.head
        while cur:
            result.append(vars(cur.contact))
            cur = cur.next
        return result
