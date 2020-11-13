from victoria.ipc import r, p, redis_retry_connection
from victoria.logger import logger
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from redis.exceptions import ConnectionError
import json
import os
import time

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)

class Printer():
    def __init__(self, name, redis):
        self.name = name
        self.redis = redis

    def warning(self, msg):
        logger.warning("[warn:%s] %s" % (self.name, msg))

    def error(self, msg):
        logger.error("[err:%s] %s" % (self.name, msg))

    def info(self, msg):
        logger.info("[info:%s] %s" % (self.name, msg))

    def debug(self, msg):
        logger.debug("[dbg:%s] %s" % (self.name, msg))

    def print(self, content):
        raise NotImplementedError

    def print_filename(self, filename):
        with open(filename, "rb") as fn:
            self.print(fn.read())

    def launch_print(self, content, number=1):
        try:
            for _ in range(number):
                self.print(content)
        except OSError as e:
            logger.error(e)

    def handle_print_msg(self, content):
        try:
            template = env.get_template('productbarcode70x50.zpl')
        except TemplateNotFound:
            self.error("Template not found")
            return

        self.info("Launching the print of the barcode: %s" % (content['barcode']))
        rendered_print = str(template.render(name=content.get('name', ''), number=content['barcode']))
        self.launch_print(rendered_print, content.get('number', 1))

    def handle_msg_reception(self, content):
        try:
            info = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            self.error("Failed to decode json data from redis: %s" % e)
            return
        # TODO Handle the parsing of the incoming message. Verify it follows
        # the BarcodeMsg template. Redirect the message to handle the print or
        # to reconfigure the printer to use different configuration.
        self.handle_print_msg(info)

    def listen(self):
        try:
            p.subscribe(self.redis)
        except ConnectionError:
            self.warning("Failed to connect to redis server. Retrying.")
            redis_retry_connection(self.redis)

        while True:
            try:
                message = p.get_message()
            except ConnectionError:
                self.warning("Redis server disconnected. Retrying.")
                redis_retry_connection(self.redis)
            if message and (message['type'] == 'message' or message['type'] == 'pmessage'):
                self.handle_msg_reception(message['data'])
            elif message:
                self.debug(str(message))
            time.sleep(0.01)
