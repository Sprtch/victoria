from victoria.printers.printer import Printer
from despinassy.Printer import PrinterTypeEnum
from typing import Optional
import json


class PrinterTest(Printer):
    out: Optional[str]
    PRINTER_TYPE: PrinterTypeEnum = PrinterTypeEnum.TEST

    def export_config(self):
        return json.dumps({})

    def available(self):
        return True

    def print(self, content: str):
        self.out = content
