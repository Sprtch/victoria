from victoria.config import Config
from victoria.printers import StaticAddressPrinter, StdoutPrinter, PrinterTest
from despinassy import Printer as PrinterTable
import unittest


class TestConfig(unittest.TestCase):
    def test_config_test_printer(self):
        config_dict = {
            "victoria": {
                "redis": "victoria",
                "printers": [{
                    "main": {
                        "type": "test",
                    }
                }]
            }
        }

        conf = Config.from_dict(config_dict)
        self.assertEqual(conf.redis, 'victoria')
        self.assertFalse(conf.debug)
        self.assertEqual(len(conf.printers), 1)
        printer = conf.printers[0]
        self.assertTrue(isinstance(printer, PrinterTest))
        self.assertEqual(printer.name, 'main')
        self.assertEqual(printer.redis, 'victoria')

        self.assertEqual(PrinterTable.query.count(), 1)
        p = PrinterTable.query.get(1)
        self.assertIsNotNone(p)
        self.assertEqual(p.type, printer.get_type())
        self.assertEqual(p.dialect, printer.template.dialect)
        self.assertEqual(p.name, printer.name)
        self.assertEqual(p.width, printer.template.width)
        self.assertEqual(p.height, printer.template.height)
        self.assertEqual(p.settings, printer.export_config())

    def test_config_stdout_printer(self):
        config_dict = {
            "victoria": {
                "redis":
                "victoria",
                "printers": [{
                    "test": {
                        "type": "stdout",
                        "redis": "test_redis",
                        "height": 100,
                        "width": 100,
                    }
                }]
            }
        }

        conf = Config.from_dict(config_dict)
        self.assertEqual(conf.redis, 'victoria')
        self.assertFalse(conf.debug)
        self.assertEqual(len(conf.printers), 1)
        printer = conf.printers[0]
        self.assertTrue(isinstance(printer, StdoutPrinter))
        self.assertEqual(printer.name, 'test')
        self.assertEqual(printer.redis, 'test_redis')
        self.assertEqual(printer.template.width, 100)
        self.assertEqual(printer.template.height, 100)

        self.assertEqual(PrinterTable.query.count(), 1)
        p = PrinterTable.query.get(1)
        self.assertIsNotNone(p)
        self.assertEqual(p.type, printer.get_type())
        self.assertEqual(p.dialect, printer.template.dialect)
        self.assertEqual(p.name, printer.name)
        self.assertEqual(p.width, printer.template.width)
        self.assertEqual(p.height, printer.template.height)
        self.assertEqual(p.settings, printer.export_config())

    def test_config_static_printer(self):
        config_dict = {
            "victoria": {
                "redis":
                "victoria",
                "debug":
                True,
                "printers": [{
                    "test": {
                        "type": "static",
                        "redis": "test_redis",
                        "address": "192.168.0.1",
                        "port": 8080,
                        "height": 100,
                        "width": 100,
                    }
                }]
            }
        }

        conf = Config.from_dict(config_dict)
        self.assertEqual(conf.redis, 'victoria')
        self.assertTrue(conf.debug)
        self.assertEqual(len(conf.printers), 1)
        printer = conf.printers[0]
        self.assertTrue(isinstance(printer, StaticAddressPrinter))
        self.assertEqual(printer.name, 'test')
        self.assertEqual(printer.redis, 'test_redis')
        self.assertEqual(printer.port, 8080)
        self.assertEqual(printer.address, "192.168.0.1")
        self.assertEqual(printer.template.width, 100)
        self.assertEqual(printer.template.height, 100)

        self.assertEqual(PrinterTable.query.count(), 1)
        p = PrinterTable.query.get(1)
        self.assertIsNotNone(p)
        self.assertEqual(p.type, printer.get_type())
        self.assertEqual(p.dialect, printer.template.dialect)
        self.assertEqual(p.name, printer.name)
        self.assertEqual(p.width, printer.template.width)
        self.assertEqual(p.height, printer.template.height)
        self.assertEqual(p.settings, printer.export_config())


if __name__ == '__main__':
    unittest.main()
