from .contact import Contact

class HashMapStore:
    def __init__(self):
        self.store = {}

    def insert(self, contact: Contact):
        self.store[contact.name] = contact

    def search(self, name):
        return self.store.get(name, None)

    def delete(self, name):
        return self.store.pop(name, None)

    def list_all(self):
        return [vars(c) for c in self.store.values()]
