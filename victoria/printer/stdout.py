from victoria.printers.printer import Printer
import dataclasses

@dataclasses.dataclass
class StdoutPrinter(Printer):
    @property
    def type(self):
        return PrinterTypeEnum.STDOUT

    def available(self):
        return True

    def print(self, content: str, number=1):
        print(content)
