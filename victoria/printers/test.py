from victoria.printers.printer import Printer


class PrinterTest(Printer):
    def __init__(self, name, redis, template):
        super().__init__(name, redis, template)
        self.out = None

    def available(self):
        return True

    def print(self, content: str):
        self.out = content
