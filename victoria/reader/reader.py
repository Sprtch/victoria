from victoria.schema.message import VictoriaPrintMessage
from abc import ABC
from redis import Redis
from redis.exceptions import ConnectionError
import logging
import time

logger = logging.getLogger()

# TODO Write the type definition of the expected messages we would receive from
# redis/stdin

class MsgReader(ABC):
    channel: str

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
                logger.warning("Redis server retry attempt nº%i." % retry_number)
                retry_number += 1
            time.sleep(min(retry_number, MAX_RETRY))

    def read(self) -> VictoriaPrintMessage:
        raise NotImplementedError

    def read_loop(self):
        while 1:
            message = self.read()

            if message and (message['type'] == 'message'
                            or message['type'] == 'pmessage'):
                yield message['data']
            elif message:
                logger.debug(str(message))

            time.sleep(0.1)


class MsgReaderRedis(MsgReader):
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

    def read(self):
        while 1:
            # TODO Handle change of redis channel during the read loop.
            # TODO Handle disconnection of the reading channel
            try:
                return self.p.get_message()
            except ConnectionError:
                logger.warning("Redis server disconnected. Retrying.")
                self.retry_connection(self.channel)

            time.sleep(0.1)

class MsgReaderStdin(MsgReader):
    def read(self):
        # TODO read from stdin and make it look like the other messages
        pass
