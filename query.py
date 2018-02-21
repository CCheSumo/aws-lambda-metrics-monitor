class Query(object):

    def __init__(self, start_time, end_time, body, time_range):
        self.start_time = start_time
        self.end_time = end_time
        self.body = body
        self.time_range = time_range

    def latency(self):
        return self.end_time - self.start_time

class Index(object):
    def __init__(self, index, time_range):
        self.index = index
        self.time_range = time_range
