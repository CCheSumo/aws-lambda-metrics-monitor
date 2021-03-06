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
    logger.info('finished monitor query')
    feeder = Feeder(event['send_url'], event['deployment'], monitor.performance)
    feeder.send()
    logger.info('finished monitor send')
    return "finished lambda_handler with id %s" % id
