import logging
import zlib
from botocore.vendored import requests
from config import Config
from metric import Metric

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Feeder(object):

    def __init__(self, url, performance):
        self.url = url
        self.performance = performance

    def encode(self, body):
        return zlib.compress(body.encode('utf-8'))


    def build_log_body(self, key, metric, start_time, value):
        return "request_number=%d request_time_range=%d start_time=%f %s=%f" % \
               (int(key.index),
                (int(key.time_range)),
                int(start_time),
                metric,
                value)

    def build_metric_body(self, key, metric, start_time, value):
        return "metric=%s time_range=%d  %f %d" % (metric, int(key.time_range), value, int(start_time))

    def send_logs(self):
        query_latency_body = [self.build_log_body(key, Metric.query_latency, query.start_time, query.latency()) for key, query in self.performance.query.items()]
        data_availability_body = [self.build_log_body(key, Metric.data_availability, query.start_time, query.availability()) for key, query in self.performance.query.items()]
        data_loss_body = [self.build_log_body(key, Metric.data_loss, query.start_time, query.data_loss()) for key, query in self.performance.query.items()]
        data_dupliation_body = [self.build_log_body(key, Metric.data_duplication, query.start_time, query.data_duplication()) for key, query in self.performance.query.items()]
        data_completeness_body = [self.build_log_body(key, Metric.data_completeness, query.start_time, query.data_completeness()) for key, query in self.performance.query.items()]

        body = query_latency_body + data_availability_body + data_loss_body + data_dupliation_body + data_completeness_body
        body_str = '\n'.join(body)
        logger.info("sending logs request ...")
        response = requests.post(self.url, data=self.encode(body_str), headers=Config.send_logs_headers)
        logger.info("finishing logs request %s with %s", body_str, str(response))

    def send_metrics(self):
        query_latency_body = [self.build_metric_body(key, Metric.query_latency, query.start_time, query.latency()) for key, query in self.performance.query.items()]
        data_availability_body = [self.build_metric_body(key, Metric.data_availability, query.start_time, query.availability()) for key, query in self.performance.query.items()]
        data_loss_body = [self.build_metric_body(key, Metric.data_loss, query.start_time, query.data_loss()) for key, query in self.performance.query.items()]
        data_dupliation_body = [self.build_metric_body(key, Metric.data_duplication, query.start_time, query.data_duplication()) for key, query in self.performance.query.items()]
        data_completeness_body = [self.build_metric_body(key, Metric.data_completeness, query.start_time, query.data_completeness()) for key, query in self.performance.query.items()]

        body = query_latency_body + data_availability_body + data_loss_body + data_dupliation_body + data_completeness_body
        body_str = '\n'.join(body)
        logger.info("sending metrics request ...")
        response = requests.post(self.url, data=self.encode(body_str), headers=Config.send_metrics_headers)
        logger.info("finishing metrics request %s with %s", body_str, str(response))

    def send(self):
        self.send_logs()
        self.send_metrics()
