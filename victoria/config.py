from victoria.printers import StaticAddressPrinter, StdoutPrinter, PrinterTest
from victoria.template import Template
from victoria.db import init_db, db
from victoria.logger import init_log
from typing import Optional
import dataclasses
import os
import yaml


class InvalidConfigFile(Exception):
    pass


@dataclasses.dataclass
class DbConfig:
    uri: str = 'sqlite://'


@dataclasses.dataclass
class Config:
    APPNAME = "victoria"
    redis: str = "victoria"
    printers: list = dataclasses.field(default_factory=list)
    debug: bool = False
    logfile: Optional[str] = None
    pidfile: Optional[str] = None
    nodaemon: bool = False

    def __post_init__(self):
        init_log(self)
        printers = []
        for dev in self.printers:
            name, content = list(dev.items())[0]
            devicetype = content.get('type')
            if devicetype == 'static':
                dev = StaticAddressPrinter(
                    name=name,
                    address=content.get('address'),
                    port=content.get('port'),
                    redis=content.get('redis', self.redis),
                    template=Template(
                        width=content.get('width', 50),
                        height=content.get('height', 70),
                        dialect=content.get('dialect', 'zpl'),
                    ))
            elif devicetype == 'stdout':
                dev = StdoutPrinter(name=name,
                                    redis=content.get('redis', self.redis),
                                    template=Template(
                                        width=content.get('width', 50),
                                        height=content.get('height', 70),
                                        dialect=content.get('dialect', 'zpl'),
                                    ))
            elif devicetype == 'test':
                dev = PrinterTest(name=name,
                                  redis=content.get('redis', self.redis),
                                  template=Template(
                                      width=content.get('width', 50),
                                      height=content.get('height', 70),
                                      dialect=content.get('dialect', 'zpl'),
                                  ))
            else:
                raise InvalidConfigFile("Type '%s' not supported" %
                                        (content.get('type')))

            printers.append(dev)

        self.printers = printers

    @staticmethod
    def from_dict(raw, **kwargs):
        victoria_args = {**kwargs, **raw[Config.APPNAME]}
        raw[Config.APPNAME] = victoria_args
        if raw.get('despinassy') is not None:
            dbconfig = DbConfig(**raw['despinassy'])
            init_db(dbconfig)
        else:
            dbconfig = DbConfig()
            init_db(dbconfig)
            db.create_all()

        if raw.get(Config.APPNAME) is not None:
            config = raw[Config.APPNAME]
        else:
            raise InvalidConfigFile("No '%s' field in the config file." %
                                    (Config.APPNAME))

        return Config(**config)

    @staticmethod
    def from_yaml_file(filename, **kwargs):
        if os.path.isfile(filename):
            raw = yaml.load(open(filename, 'r'), Loader=yaml.FullLoader)
        else:
            raise InvalidConfigFile('No config file in "%s"' % (filename))

        return Config.from_dict(raw, **kwargs)
