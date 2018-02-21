import logging
import zlib
from botocore.vendored import requests
from config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Feeder(object):

    def __init__(self, url, performance):
        self.url = url
        self.performance = performance

    def encode(self, body):
        return zlib.compress(body.encode('utf-8'))

    def build_log_body(self, key, query):
        return "request_number=%d %s start_time=%f latency=%f" % \
               (int(key),
                Config.metric_query + "_latency",
                query.start_time,
                query.latency())

    def build_metric_body(self, key, query):
        return "%s  %f %d" % (Config.metric_query + "_latency", query.latency(), int(query.start_time))

    def send_logs(self):
        body = [self.build_log_body(key, query) for key, query in self.performance.latency.items()]
        body_str = '\n'.join(body)
        logger.info("sending logs request %s", body)
        response = requests.post(self.url, data=self.encode(body_str), headers=Config.send_logs_headers)
        logger.info("finishing logs request %s with %s", body, str(response))

    def send_metrics(self):
        body = [self.build_metric_body(key, query) for key, query in self.performance.latency.items()]
        body_str = '\n'.join(body)
        logger.info("sending metrics request %s", body)
        response = requests.post(self.url, data=self.encode(body_str), headers=Config.send_metrics_headers)
        logger.info("finishing metrics request %s with %s", body, str(response))

    def send(self):
        self.send_logs()
        self.send_metrics()
