from redis import Redis
from redis.exceptions import ConnectionError
import logging
import time

logger = logging.getLogger(__name__)

class MsgReaderBase():
    channel: str

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

    def disconnect(self, channel):
        """Disconnect from the currently in use channel

        :param channel: Channel to disconnect from.
        """
        raise NotImplementedError

    def connect(self, channel):
        """Connect to the channel to read message from.

        :param channel: Channel to connect to.
        """
        raise NotImplementedError

    def retry_connection(self, channel, MAX_RETRY=30):
        """Infinitely attempt a connection to a remote channel

        :param channel: Channel name to connect to.
        :param MAX_RETRY: Maximal time to wait to retry a connection.
        """
        retry_number = 1
        while retry_number:
            try:
                self.connect(channel)
                return
            except ConnectionError:
                self.warning("Redis server retry attempt nº%i." % retry_number)
                retry_number += 1
            time.sleep(min(retry_number, MAX_RETRY))

    def read_loop(self):
        raise NotImplementedError
 

class MsgReader(MsgReaderBase):
    """
    The `MsgReader` class intercept incoming messages.

    This class is made to abstract the complexity of listening incoming
    print job messages on a specific channel.
    The class is used by :class`victoria.Printer` to give away a simple API to
    receive new message based on python iterators.
    For now only redis channel are supported but this can be extended in the
    future.
    """

    # channel: str
    # host: str = "localhost"
    # port: int = 6379
    # redis: Redis

    def __init__(self, channel, host='localhost', port=6379):
        self.channel = channel
        self.redis = Redis(host=host, port=port, db=0)
        self.p = self.redis.pubsub()

    def __enter__(self):
        self.retry_connection(self.channel)
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect(self.channel)
        return self

    def disconnect(self, channel):
        """Disconnect from the currently in use redis channel

        :param channel: Channel to disconnect from.
        """
        self.p.unsubscribe(channel)

    def connect(self, channel):
        """Connect to the redis channel to read message from.

        :param channel: Channel to connect to.
        """
        self.p.subscribe(channel)

    def read_loop(self):
        # TODO Handle change of redis channel during the read loop.
        # TODO Handle disconnection of the reading channel
        while 1:
            try:
                message = self.p.get_message()
            except ConnectionError:
                self.warning("Redis server disconnected. Retrying.")
                self.retry_connection(self.channel)
                continue

            if message and (message['type'] == 'message'
                            or message['type'] == 'pmessage'):
                yield message['data']
            elif message:
                self.debug(str(message))

            time.sleep(0.1)
