from victoria.config.config import (
    Config,
    ConfigDevice,
    ConfigPrinter,
    ConfigPrinterPublisher,
    ConfigPrinterReader,
    ConfigPrinterTemplate,
)
import pytest


class TestConfigDataclasses:
    def test_config_printer_reader_defaults(self):
        r = ConfigPrinterReader(type="stdin")
        assert r.type == "stdin"
        assert r.path is None
        assert r.device_id is None
        assert r.host == "localhost"
        assert r.port == 6379
        assert r.channel == "victoria"
        assert r.db == 0

    def test_config_printer_reader_custom(self):
        r = ConfigPrinterReader(
            type="redis", host="10.0.0.1", port=6380, channel="mychan", db=2
        )
        assert r.host == "10.0.0.1"
        assert r.port == 6380
        assert r.channel == "mychan"
        assert r.db == 2

    def test_config_printer_publisher_defaults(self):
        p = ConfigPrinterPublisher()
        assert p.type == "redis"
        assert p.host == "localhost"
        assert p.port == 6379
        assert p.channel == "victoria"
        assert p.db == 0

    def test_config_printer_publisher_custom(self):
        p = ConfigPrinterPublisher(type="stdout")
        assert p.type == "stdout"

    def test_config_printer_template(self):
        t = ConfigPrinterTemplate(dialect="zpl", width=100, height=150)
        assert t.dialect == "zpl"
        assert t.width == 100
        assert t.height == 150

    def test_config_printer_type_default(self):
        p = ConfigPrinter()
        assert p.type == "redis"

    def test_config_printer_type_static(self):
        p = ConfigPrinter(type="static")
        assert p.type == "static"

    def test_config_defaults(self):
        c = Config()
        assert c.name == "victoria"
        assert c.debug is False
        assert c.nodaemon is False
        assert c.logfile is None
        assert c.pidfile is None
        assert isinstance(c.publisher, ConfigPrinterPublisher)
        assert c.printers == []


class TestConfigFromDict:
    def test_from_dict_minimal(self):
        data = {"victoria": {}}
        c = Config.from_dict(data)
        assert c.name == "victoria"
        assert c.debug is False
        assert c.printers == []

    def test_from_dict_debug_mode(self):
        data = {"victoria": {"debug": True}}
        c = Config.from_dict(data)
        assert c.debug is True

    def test_from_dict_nodaemon(self):
        data = {"victoria": {"nodaemon": True}}
        c = Config.from_dict(data)
        assert c.nodaemon is True

    def test_from_dict_with_printer(self):
        data = {
            "victoria": {
                "printers": [
                    {
                        "name": "test-printer",
                        "reader": {"type": "stdin"},
                        "template": {"dialect": "json", "width": 100, "height": 150},
                        "printer": {"type": "stdout"},
                    }
                ]
            }
        }
        c = Config.from_dict(data)
        assert len(c.printers) == 1
        dev = c.printers[0]
        assert isinstance(dev, ConfigDevice)
        assert dev.name == "test-printer"
        assert dev.reader.type == "stdin"
        assert dev.template.dialect == "json"
        assert dev.template.width == 100
        assert dev.template.height == 150
        assert dev.printer.type == "stdout"

    def test_from_dict_multiple_printers(self):
        data = {
            "victoria": {
                "printers": [
                    {
                        "name": "p1",
                        "reader": {"type": "stdin"},
                        "template": {"dialect": "json", "width": 80, "height": 100},
                        "printer": {"type": "stdout"},
                    },
                    {
                        "name": "p2",
                        "reader": {"type": "redis", "channel": "ch2"},
                        "template": {"dialect": "zpl", "width": 200, "height": 300},
                        "printer": {"type": "static"},
                    },
                ]
            }
        }
        c = Config.from_dict(data)
        assert len(c.printers) == 2
        assert c.printers[0].name == "p1"
        assert c.printers[1].name == "p2"
        assert c.printers[1].reader.channel == "ch2"

    def test_from_dict_default_publisher_applies(self):
        data = {
            "victoria": {
                "publisher": {"type": "redis", "channel": "default-ch"},
                "printers": [
                    {
                        "name": "p1",
                        "reader": {"type": "stdin"},
                        "template": {"dialect": "json", "width": 80, "height": 100},
                        "printer": {"type": "stdout"},
                    }
                ],
            }
        }
        c = Config.from_dict(data)
        assert c.publisher["channel"] == "default-ch"
        assert isinstance(c.printers[0].publisher, ConfigPrinterPublisher)
        assert c.printers[0].publisher.channel == "default-ch"

    def test_from_dict_printer_overrides_default_publisher(self):
        data = {
            "victoria": {
                "publisher": {"type": "redis", "channel": "default-ch"},
                "printers": [
                    {
                        "name": "p1",
                        "reader": {"type": "stdin"},
                        "template": {"dialect": "json", "width": 80, "height": 100},
                        "printer": {"type": "stdout"},
                        "publisher": {"type": "redis", "channel": "custom-ch"},
                    }
                ],
            }
        }
        c = Config.from_dict(data)
        assert c.publisher["channel"] == "default-ch"
        assert c.printers[0].publisher.channel == "custom-ch"

    def test_from_dict_kwargs_override(self):
        data = {"victoria": {}}
        c = Config.from_dict(data, debug=True, nodaemon=True)
        assert c.debug is True
        assert c.nodaemon is True

    def test_from_dict_kwargs_none_ignored(self):
        data = {"victoria": {"debug": True}}
        c = Config.from_dict(data, debug=None)
        assert c.debug is True

    def test_from_dict_redis_reader(self):
        data = {
            "victoria": {
                "printers": [
                    {
                        "name": "redis-dev",
                        "reader": {
                            "type": "redis",
                            "host": "10.0.0.1",
                            "port": 6380,
                            "channel": "mychan",
                            "db": 3,
                        },
                        "template": {"dialect": "zpl", "width": 100, "height": 150},
                        "printer": {"type": "static"},
                    }
                ]
            }
        }
        c = Config.from_dict(data)
        r = c.printers[0].reader
        assert r.type == "redis"
        assert r.host == "10.0.0.1"
        assert r.port == 6380
        assert r.channel == "mychan"
        assert r.db == 3


class TestConfigFromYaml:
    def test_from_yaml(self, tmp_path):
        yaml_content = """\
victoria:
    name: "test-app"
    debug: true
    publisher:
      type: "redis"
      channel: "test-out"
    printers:
        - name: "dev1"
          reader:
            type: "stdin"
          template:
            dialect: "json"
            width: 100
            height: 150
          printer:
            type: "stdout"
"""
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        c = Config.from_yaml(str(f))
        assert c.name == "test-app"
        assert c.debug is True
        assert c.publisher["channel"] == "test-out"
        assert len(c.printers) == 1
        assert c.printers[0].name == "dev1"
        assert c.printers[0].reader.type == "stdin"
        assert c.printers[0].template.dialect == "json"

    def test_from_yaml_with_kwargs(self, tmp_path):
        yaml_content = """\
victoria:
    name: "test-app"
"""
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        c = Config.from_yaml(str(f), debug=True)
        assert c.debug is True
        assert c.name == "test-app"

    def test_from_yaml_empty(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text("")
        c = Config.from_yaml(str(f))
        assert c.name == "victoria"
        assert c.printers == []
