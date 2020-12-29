from victoria.ipc import p, redis_retry_connection
from victoria.template import Template
from despinassy.ipc import IpcPrintMessage, ipc_create_print_message
from redis.exceptions import ConnectionError
import logging
import dataclasses
import json
import time

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Printer():
    name: str
    redis: str
    template: Template

    def warning(self, msg):
        logger.warning("[warn:%s] %s" % (self.name, msg))

    def error(self, msg):
        logger.error("[err:%s] %s" % (self.name, msg))

    def info(self, msg):
        logger.info("[info:%s] %s" % (self.name, msg))

    def debug(self, msg):
        logger.debug("[dbg:%s] %s" % (self.name, msg))

    def get_type(self):
        return self.PRINTER_TYPE

    def export_config(self):
        raise NotImplementedError

    def available(self):
        raise NotImplementedError

    def print(self, content):
        raise NotImplementedError

    def render(self, message: IpcPrintMessage):
        return self.template.render_barcode(message)

    def print_filename(self, filename):
        with open(filename, "rb") as fn:
            self.print(fn.read())

    def launch_print(self, content, number=1):
        if self.available():
            for _ in range(number):
                self.print(content)
        else:
            self.debug("\n" + content)

    def handle_print_msg(self, printmsg: IpcPrintMessage):
        self.info("Launching the print of the barcode :%s" %
                  (printmsg._asdict()))
        rendered_print = self.render(printmsg)
        self.launch_print(rendered_print, printmsg.number)

    def handle_msg_reception(self, content):
        try:
            info = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            self.error("Failed to decode json data from redis: %s" % e)
            return

        try:
            self.handle_print_msg(ipc_create_print_message(info))
        except TypeError as e:
            self.error("Invalid message format: %s" % e)

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
            if message and (message['type'] == 'message'
                            or message['type'] == 'pmessage'):
                self.handle_msg_reception(message['data'])
            elif message:
                self.debug(str(message))
            time.sleep(0.1)
