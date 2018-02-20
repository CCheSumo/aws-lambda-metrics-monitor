class Performance(object):

    def __init__(self):
        self.latency = {}

    def add(self, key, val):
        self.latency[key] = val