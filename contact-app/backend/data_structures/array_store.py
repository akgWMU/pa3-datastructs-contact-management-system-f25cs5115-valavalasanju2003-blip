from data_structures.contact import Contact

class ArrayStore:
    def __init__(self):
        self.contacts = []

    def insert(self, contact: Contact):
        self.contacts.append(contact)

    def search(self, name):
        name = name.lower()
        for c in self.contacts:
            if c.name.lower() == name:
                return c
        return None

    def delete(self, name):
        name = name.lower()
        for i, c in enumerate(self.contacts):
            if c.name.lower() == name:
                return self.contacts.pop(i)
        return None

    def list_all(self):
        # return raw Contact objects (not dicts)
        return self.contacts
