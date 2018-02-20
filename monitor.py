import time
import logging
from botocore.vendored import requests
from header import Header
from config import Config
from timer import Timer
from sessions import Sessions
from performance import Performance

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Monitor(object):

    def __init__(self, url, access_id, access_key):
        self.timer = Timer(Config.request_interval, self.task)
        self.sessions = Sessions()
        self.performance = Performance()
        self.url = url +  Config.endpoint
        self.auth = (access_id, access_key)
        self.timestamp = int(time.time())
        self.start()

    def __del__(self):
        self.stop()

    def start(self):
        self.timer.start_timer()

    def stop(self):
        self.timer.cancel_timer()

    def done(self):
        return Config.number_requests == self.sessions.completed and (not self.sessions.pending)

    def build_body(self, start_time, end_time):
        return '{"%s":[{"%s":"%s","%s":"%s"}],"%s": %d,"%s":%d, "%s": %d, "%s": %d}' % \
               (Header.query, Header.query,
                Config.metric_query,
                Header.row_id, Config.row_id,
                Header.start_time, start_time,
                Header.end_time, end_time,
                Header.requested_data_points, Config.requested_data_points,
                Header.max_data_points, Config.max_data_points)

    def task(self):
        if self.sessions.completed < Config.number_requests:
            self.send()
        else:
            self.stop()

    def send(self):
        index = self.sessions.completed
        end_time = int(self.timestamp + index) * 1000
        body = self.build_body(end_time - Config.time_range, end_time)
        logger.debug("sending request %s ", body)
        self.sessions.add(index, body)
        perf_start = time.time()
        response = requests.post(self.url, data=body, headers=Config.headers, auth=self.auth)
        perf_end = time.time()
        self.performance.add(index, perf_end - perf_start)
        self.sessions.delete(index)
        logger.info("finishing request %d %s %s with %s in %f seconds", index, str(Config.headers), body, str(response), (perf_end - perf_start))
