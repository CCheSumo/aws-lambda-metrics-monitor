import time
import logging

from config import Config
from monitor import Monitor

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    id = context.aws_request_id
    logger.info('started lambda_handler with id %s' % id)
    monitor = Monitor(event['url'], event['access_id'], event['access_key'])
    while not monitor.done():
        time.sleep(Config.sleep_interval)
    return "finished lambda_handler with id %s" % id
