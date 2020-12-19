from victoria.printers.printer import Printer

class StdoutPrinter(Printer):
    def __init__(self, name, redis, template):
        super().__init__(name, redis, template)

    def available(self):
        return True

    def print(self, content: str):
        print(content)
