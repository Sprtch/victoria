from victoria.printers.printer import Printer
from victoria.reader import MsgReader
from despinassy.Printer import PrinterTypeEnum
import json


class StdoutPrinter(Printer):
    PRINTER_TYPE: PrinterTypeEnum = PrinterTypeEnum.STDOUT

    def set_reader(self):
        return MsgReader(self.redis)

    def export_config(self):
        return json.dumps({})

    def available(self):
        return True

    def print(self, content: str):
        print(content)
