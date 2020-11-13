from victoria.logger import logger
from redis import Redis
from redis.exceptions import ConnectionError
import time

r = Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

def redis_retry_connection(channel):
    MAX_RETRY = 30
    retry_number = 1
    while retry_number:
        time.sleep(min(retry_number, MAX_RETRY))
        try:
            p.subscribe(channel)
            return
        except ConnectionError:
            logger.warning("Redis server retry attempt nº%i." % retry_number)
            retry_number += 1
            continue

