class Sessions(object):

    def __init__(self):
        self.pending = {}
        self.completed = 0

    def add(self, key, val):
        self.pending[key] = val

    def delete(self, key):
        del self.pending[key]

    def complete(self):
        self.completed += 1

