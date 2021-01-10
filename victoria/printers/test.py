from victoria.printers.printer import Printer
from despinassy.Printer import PrinterTypeEnum
import json
import dataclasses


@dataclasses.dataclass
class ReaderTest():
    messages: list = dataclasses.field(default_factory=list)

    def set_messages(self, msgs):
        self.messages = msgs

    def read_loop(self):
        for msg in self.messages:
            yield msg


class PrinterTest(Printer):
    out: list = list()
    isavailable: bool = True
    PRINTER_TYPE: PrinterTypeEnum = PrinterTypeEnum.TEST

    def set_reader(self):
        return ReaderTest(messages=[])

    def set_messages(self, msgs):
        self.get_reader().set_messages(msgs)

    def get_result(self):
        out = self.out
        self.out = []
        return out

    def export_config(self):
        return json.dumps({})

    def available(self):
        return self.isavailable

    def print(self, content: str):
        self.out.append(content)
