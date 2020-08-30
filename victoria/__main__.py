from daemonize import Daemonize
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import uuid
import logging
import argparse
import redis
import time
import json

APPNAME = "victoria"

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)

logger = logging

def retry():
    MAX_RETRY = 30
    retry_number = 1
    while retry_number:
        time.sleep(min(retry_number, MAX_RETRY))
        try:
            p.subscribe('printer')
            return
        except redis.exceptions.ConnectionError:
            logger.warning("Redis server retry attempt nº%i." % retry_number)
            retry_number += 1
            continue

def main():
    try:
        p.subscribe('printer')
    except redis.exceptions.ConnectionError:
        logger.warning("Failed to connect to redis server. Retrying.")
        retry()

    while True:
        try:
            message = p.get_message()
        except redis.exceptions.ConnectionError:
            logger.warning("Redis server disconnected. Retrying.")
            retry()
        if message and (message['type'] == 'message' or message['type'] == 'pmessage'):
            try:
                info = json.loads(message['data'])
            except json.decoder.JSONDecodeError as e:
                logger.error("Failed to decode json data from redis: %s" % e)
                continue

            try:
                template = env.get_template('productbarcode40x100.zpl')
            except TemplateNotFound:
                logger.error("Template not found")
                continue

            filename = '/tmp/%s-%s.zpl' % (APPNAME, str(uuid.uuid4()))
            try:
                f = open(filename, 'w')
            except OSError:
                logger.error("Error opening the filename '%s'" % filename)
                continue
            with f:
                # TODO Get part name from database and do verification.
                f.write(str(template.render(name=info.get('name', ''), number=info['barcode'])))

            logger.info("Launching the print of the barcode: %s" % (info['barcode']))

            # sp.check_output(['lpr', '-P', 'zebra', '-o', 'raw', filename])
        elif message:
            logger.debug(str(message))
        time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--no-daemon', dest='nodaemon', action='store_true', help='Does not start the program as a daemon')
    parser.add_argument('--logfile', dest='logfile', type=str, help='Log destination', default=("/var/log/%s.log" % APPNAME))
    parser.add_argument('--pid', dest='pid', type=str, help='Pid destination', default=("/tmp/%s.pid" % APPNAME))

    args = parser.parse_args()

    if args.nodaemon:
        logger.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        main()
    else:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        fh = logging.FileHandler(args.logfile, "w")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        keep_fds = [fh.stream.fileno()]

        daemon = Daemonize(app=APPNAME, logger=logger, pid=args.pid, action=main, keep_fds=keep_fds)
        daemon.start()
