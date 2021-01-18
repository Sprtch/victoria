from victoria.ipc import p, redis_retry_connection
from redis.exceptions import ConnectionError
import logging
import time

logger = logging.getLogger(__name__)


class MsgReader():
    def __init__(self, channel):
        self.channel = channel

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

    def read_loop(self):
        while not self.channel:
            self.warning("No channel set")
            time.sleep(0.1)

        while 1:
            try:
                message = p.get_message()
            except ConnectionError:
                self.warning("Redis server disconnected. Retrying.")
                redis_retry_connection(self.channel)
                continue
            if message and (message['type'] == 'message'
                            or message['type'] == 'pmessage'):
                yield message['data']
            elif message:
                self.debug(str(message))

            time.sleep(0.1)
