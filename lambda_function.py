import time
import logging

from config import Config
from monitor import Monitor
from feeder import Feeder

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    id = context.aws_request_id
    logger.info('started lambda_handler with id %s' % id)
    monitor = Monitor(event['query_url'], event['access_id'], event['access_key'])
    while not monitor.done():
        time.sleep(Config.sleep_interval)
    feeder = Feeder(event['send_url'], monitor.performance)
    feeder.send()
    return "finished lambda_handler with id %s" % id
