from redis import Redis
from redis.exceptions import ConnectionError
import logging
import time

logger = logging.getLogger(__name__)


class MsgReader():
    def __init__(self, channel, host='localhost', port=6379):
        self.channel = channel
        self.redis = Redis(host=host, port=port, db=0)
        self.p = self.redis.pubsub()

    def __enter__(self):
        self.redis_retry_connection(self.channel)
        return self

    def __exit__(self, type, value, traceback):
        self.p.unsubscribe(self.channel)
        return self

    def warning(self, msg):
        logger.warning("[warn:%s] %s" % (self.channel, msg))

    def error(self, msg):
        logger.error("[err:%s] %s" % (self.channel, msg))

    def info(self, msg):
        logger.info("[info:%s] %s" % (self.channel, msg))

    def debug(self, msg):
        logger.debug("[dbg:%s] %s" % (self.channel, msg))

    def set_channel(self, chan):
        self.channel = chan

    def redis_retry_connection(self, channel):
        MAX_RETRY = 30
        retry_number = 1
        while retry_number:
            try:
                self.p.subscribe(channel)
                return
            except ConnectionError:
                self.warning("Redis server retry attempt nº%i." % retry_number)
                retry_number += 1
            time.sleep(min(retry_number, MAX_RETRY))

    def read_loop(self):
        while 1:
            try:
                message = self.p.get_message()
            except ConnectionError:
                self.warning("Redis server disconnected. Retrying.")
                self.redis_retry_connection(self.channel)
                continue

            if message and (message['type'] == 'message'
                            or message['type'] == 'pmessage'):
                yield message['data']
            elif message:
                self.debug(str(message))

            time.sleep(0.1)
