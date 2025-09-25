from .contact import Contact

class Node:
    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None

class BSTStore:
    def __init__(self):
        self.root = None

    def insert(self, contact: Contact):
        def _insert(node, contact):
            if not node:
                return Node(contact)
            if contact.name < node.contact.name:
                node.left = _insert(node.left, contact)
            else:
                node.right = _insert(node.right, contact)
            return node
        self.root = _insert(self.root, contact)

    def search(self, name):
        cur = self.root
        while cur:
            if name == cur.contact.name:
                return cur.contact
            cur = cur.left if name < cur.contact.name else cur.right
        return None

    def delete(self, name):
        def _delete(node, name):
            if not node:
                return None, None
            if name < node.contact.name:
                node.left, deleted = _delete(node.left, name)
            elif name > node.contact.name:
                node.right, deleted = _delete(node.right, name)
            else:
                deleted = node.contact
                if not node.left: return node.right, deleted
                if not node.right: return node.left, deleted
                # replace with min from right subtree
                succ = node.right
                while succ.left: succ = succ.left
                node.contact = succ.contact
                node.right, _ = _delete(node.right, succ.contact.name)
            return node, deleted
        self.root, deleted = _delete(self.root, name)
        return deleted

    def list_all(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(vars(node.contact))
                inorder(node.right)
        inorder(self.root)
        return result
