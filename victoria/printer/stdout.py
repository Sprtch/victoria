from victoria.printer.base import Printer
from victoria.schema.type import PrinterTypeEnum
import dataclasses

@dataclasses.dataclass
class StdoutPrinter(Printer):
    @property
    def type(self):
        return PrinterTypeEnum.STDOUT

    def available(self):
        return True

    def print(self, content: str, number=1):
        for _ in range(number):
            print(content)
