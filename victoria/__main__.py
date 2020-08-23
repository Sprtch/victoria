from time import sleep
from daemonize import Daemonize
from aioconsole import ainput
from evdev import InputDevice, categorize, ecodes
from jinja2 import Environment, PackageLoader
import uuid
import signal
import asyncio
import logging
import argparse
import redis
import time
import json

pid = "/tmp/victoria.pid"
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

# Jinja2 Init
env = Environment(
    loader=PackageLoader(__name__, 'templates')
)


def main():
    p.subscribe('printer')

    while True:
        message = p.get_message()
        if message and message['type'] != 'subscribe':
            info = json.loads(message['data'])
            template = env.get_template('productbarcode40x100.zpl')

            filename = '/tmp/%s.zpl' % (str(uuid.uuid4()))
            file = open(filename, 'w')
            # Get part name from database.
            file.write(str(template.render(name=info.get('name', ''), number=info['barcode'])))
            file.close()

            logging.info("Launching the print of the barcode: %s" % (info['barcode']))

            # sp.check_output(['lpr', '-P', 'zebra', '-o', 'raw', filename])
        time.sleep(0.01)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--no-daemon', dest='nodaemon', action='store_true', help='Does not start the program as a daemon')
    args = parser.parse_args()

    if args.nodaemon:
        logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        main()
    else:
        logging.basicConfig(filename='/var/log/victoria.log', format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        daemon = Daemonize(app="erie", pid=pid, action=main)
        daemon.start()
