from config import Config


class Query(object):

    def __init__(self, start_time, end_time, body, time_range, data_points, quantization):
        self.start_time = start_time
        self.end_time = end_time
        self.body = body
        self.time_range = time_range
        self.data_points = data_points
        self.quantization = quantization

    def latency(self):
        return self.end_time - self.start_time

    def max_data_points(self):
        return int(self.time_range / (self.quantization * 1000))

    def availability(self):
        if len(self.data_points) > 0:
            return 100.0
        else:
            return 0.0

    def data_loss(self):
        data = self.data_points
        if not data:
            return 0

        if self.quantization != 1:
            return 0

        loss = 0.0
        for i in range(len(data) - 1):
            item_first = data[i]
            item_second = data[i + 1]
            if (item_second > item_first):
                if item_second - item_first > 1:
                    loss += item_second - item_first
        return (loss / self.max_data_points()) * 100

    def data_duplication(self):
        data = self.data_points
        if not data:
            return 0

        if self.quantization != 1:
            return 0

        duplication = 0.0
        for i in range(len(data) - 1):
            item_first = data[i]
            item_second = data[i + 1]
            if (item_second == item_first):
                duplication += 1
        return (duplication / self.max_data_points()) * 100

    def data_completeness(self):
        return (len(self.data_points) / self.max_data_points()) * 100


class Index(object):
    def __init__(self, index, time_range):
        self.index = index
        self.time_range = time_range
