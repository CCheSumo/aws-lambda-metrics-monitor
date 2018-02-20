import logging
import zlib
from botocore.vendored import requests
from config import Config
from header import Header

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Feeder(object):

    def __init__(self, url, performance):
        self.url = url
        self.performance = performance

    def encode(self, body):
        return zlib.compress(body.encode('utf-8'))

    def build_body(self, key, query):
        return "request_number=%d %s  %s=%s %s=%s %s=%s start_time=%f latency=%f" % \
               (int(key),
                Config.metric_query,
                Header.x_sumo_category, Config.x_sumo_category,
                Header.x_sumo_host, Config.x_sumo_host,
                Header.x_sumo_source, Config.x_sumo_source,
                query.start_time,
                query.latency())

    def send(self):
        body = [self.build_body(key, query) for key, query in self.performance.latency.items()]
        body_str = '\n'.join(body)
        logger.info("sending request %s", body)
        response = requests.post(self.url, data=self.encode(body_str), headers=Config.send_headers)
        logger.info("finishing request %s with %s", body, str(response))
