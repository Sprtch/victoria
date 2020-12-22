from victoria.printers.test import PrinterTest
from victoria.template import Template, DialectEnum
from despinassy.ipc import IpcPrintMessage
import unittest
import json


class TestPrinter(unittest.TestCase):
    def test_printer_msg(self):
        printer = PrinterTest(
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
