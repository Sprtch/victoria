import unittest
import unittest.mock
import builtins
import json
from despinassy.ipc import IpcPrintMessage
from victoria.printers.printer import Printer
from victoria.template import Template, DialectEnum


class StdoutPrinter(Printer):
    def __init__(self, name, redis, template):
        super().__init__(name, redis, template)
        self.out = None

    def available(self):
        return True

    def print(self, content: str):
        self.out = content


class TestPrinter(unittest.TestCase):
    def test_printer_msg(self):
        printer = StdoutPrinter(
            "test_printer", "test",
            Template(width=70, height=50, dialect=DialectEnum.TEST_JSON))

        msg = IpcPrintMessage(barcode="foo", name="bar")._asdict()
        msg_str = json.dumps(msg)
        self.assertEqual(printer.available(), True)
        printer.handle_msg_reception(msg_str)
        out = json.loads(printer.out)
        self.assertEqual(out['barcode'], msg['barcode'])
        self.assertEqual(out['name'], msg['name'])


if __name__ == '__main__':
    unittest.main()
