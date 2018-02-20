class Query(object):

    def __init__(self, start_time, end_time, body):
        self.start_time = start_time
        self.end_time = end_time
        self.body = body

    def latency(self):
        return self.end_time - self.start_time
