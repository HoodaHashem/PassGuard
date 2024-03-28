import hashlib

class HashGen:
    def __init__(self):
        self.hash = hashlib.sha256()

    def update(self, data):
        self.hash.update(data)

    def digest(self):
        return self.hash.digest()

    def hexdigest(self):
        return self.hash.hexdigest()

    def reset(self):
        self.hash = hashlib.sha256()

    def copy(self):
        new_hash = HashGen()
        new_hash.hash = self.hash.copy()
        return new_hash

    def __str__(self):
        return self.hash.hexdigest()

    def __repr__(self):
        return self.hash.hexdigest()

    def __eq__(self, other):
        return self.hash.digest() == other.hash.digest()

    def __ne__(self, other):
        return self.hash.digest() != other.hash.digest()

    def __lt__(self, other):
        return self.hash.digest() < other.hash.digest()

    def __le__(self, other):
        return self.hash.digest() <= other.hash.digest()

    def __gt__(self, other):
        return self.hash.digest() > other.hash.digest()

    def __ge__(self, other):
        return self.hash.digest() >= other.hash.digest()

    def __add__(self, other):
        new_hash = HashGen()
        new_hash.hash = self.hash.copy()
        new_hash.hash.update(other.hash.digest())
        return new_hash

    def __iadd__(self, other):
        self.hash.update(other.hash.digest())
        return self

    def __xor__(self, other):
        new_hash = HashGen()
        new_hash.hash = self.hash.copy()
        new_hash.hash.update(other.hash.digest())
        return new_hash

    def __ixor__(self, other):
        self.hash.update(other.hash.digest())
        return self

    def __hash__(self):
        return hash(self.hash.digest())

    def __len__(self):
        return len(self.hash.digest())

    def __getitem__(self, index):
        return self.hash.digest()[index]

    def __setitem__(self, index, value):
        raise TypeError("hash object does not support item assignment")

    def __delitem__(self, index):
        raise TypeError("hash object does not support item deletion")

    def __iter__(self):
        return iter(self.hash.digest())

    def __contains__(self, item):
        return item in self.hash.digest()

    def __reversed__(self):
        return reversed(self.hash.digest())
