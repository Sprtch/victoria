from victoria.printers.test import PrinterTest
from victoria.template import Template
from despinassy.Printer import Printer as PrinterTable, PrinterTransaction, PrinterDialectEnum
from despinassy.ipc import IpcPrintMessage
from despinassy.db import db
import unittest
import json


class TestPrinter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        db.init_app(config={
            'uri': 'sqlite://',
        })
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(self):
        db.drop_all()

    def tearDown(self):
        PrinterTable.query.delete()
        PrinterTransaction.query.delete()

    def test_printer_msg(self):
        printer = PrinterTest(
            "test_printer", "test",
            Template(width=70, height=50,
                     dialect=PrinterDialectEnum.TEST_JSON))

        msg = IpcPrintMessage(barcode="foo", name="bar")._asdict()
        msg_str = json.dumps(msg)
        printer.set_messages([msg_str])
        self.assertEqual(printer.available(), True)
        self.assertEqual(len(printer.get_result()), 0)
        printer.listen()
        list_out = printer.get_result()
        self.assertEqual(len(list_out), 1)
        out = json.loads(list_out[0])
        self.assertEqual(out['barcode'], msg['barcode'])
        self.assertEqual(out['name'], msg['name'])

        self.assertEqual(PrinterTable.query.count(), 1)
        p = PrinterTable.query.get(1)
        self.assertIsNotNone(p)
        self.assertEqual(p.type, printer.get_type())
        self.assertEqual(p.dialect, printer.template.dialect)
        self.assertEqual(p.name, printer.name)
        self.assertEqual(p.width, printer.template.width)
        self.assertEqual(p.height, printer.template.height)
        self.assertEqual(p.settings, printer.export_config())
        self.assertEqual(p.available, True)
        self.assertEqual(PrinterTransaction.query.count(), 1)

    def test_printer_not_available(self):
        printer = PrinterTest(
            "test_printer", "test",
            Template(width=70, height=50,
                     dialect=PrinterDialectEnum.TEST_JSON))

        msg = IpcPrintMessage(barcode="foo", name="bar")._asdict()
        msg_str = json.dumps(msg)
        printer.set_available(False)
        printer.set_messages([msg_str])
        printer.listen()
        self.assertEqual(len(printer.get_result()), 0)


if __name__ == '__main__':
    unittest.main()
