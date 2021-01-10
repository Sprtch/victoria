from victoria.template import Template
from victoria.db import db
from victoria.reader import MsgReader
from despinassy.ipc import IpcPrintMessage, ipc_create_print_message
from despinassy import Printer as PrinterTable
import logging
import dataclasses
import json

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Printer():
    name: str
    redis: str
    template: Template

    def __post_init__(self):
        self._reader = self.set_reader()

    def save_printer(self):
        q = PrinterTable.query.filter(PrinterTable.name == self.name)
        if q.count():
            self._entry = q.first()
        else:
            self._entry = PrinterTable(type=self.get_type(),
                                       width=self.template.width,
                                       height=self.template.height,
                                       dialect=self.template.dialect,
                                       name=self.name,
                                       redis=self.redis,
                                       settings=self.export_config())
            db.session.add(self._entry)
            db.session.commit()

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

    def set_reader(self):
        raise NotImplementedError

    def get_reader(self):
        return self._reader

    def export_config(self):
        raise NotImplementedError

    def available(self) -> bool:
        raise NotImplementedError

    def check_availability(self):
        ret = self.available()
        self._entry.available = ret
        db.session.commit()
        return ret

    def print(self, content):
        raise NotImplementedError

    def render(self, message: IpcPrintMessage):
        return self.template.render_barcode(message)

    def print_filename(self, filename):
        with open(filename, "rb") as fn:
            self.print(fn.read())

    def launch_print(self, content, number=1):
        if self.check_availability():
            for _ in range(number):
                self.print(content)
        else:
            self.debug("\n" + content)

    def log_printer_transaction(self, msg: IpcPrintMessage):
        db.session.add(self._entry.add_transaction(**msg._asdict()))
        db.session.commit()

    def handle_print_msg(self, printmsg: IpcPrintMessage):
        self.info("Launching the print of the barcode :%s" %
                  (printmsg._asdict()))
        self.log_printer_transaction(printmsg)
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
        self.save_printer()

        for msg in self.get_reader().read_loop():
            self.handle_msg_reception(msg)
