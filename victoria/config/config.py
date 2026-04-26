from victoria.printers import StaticAddressPrinter, StdoutPrinter, PrinterTest
from victoria.template import Template
from victoria.logger import init_log
from despinassy.Printer import PrinterDialectEnum
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
    """
    """

    APPNAME = "victoria"
    """Familiar name of the program currently in use."""

    redis: str = "victoria"
    """Default recipient channel to listen for incoming messages."""

    printers: list = dataclasses.field(default_factory=list)
    """List of the printers declared in the config file."""

    debug: bool = False
    """Debug add more debugging messages"""

    logfile: Optional[str] = None
    """Path of the file storing the log output"""

    pidfile: Optional[str] = None
    """PID file path"""

    nodaemon: bool = False
    """Don't detach the program as a daemon and keep it running on the terminal"""

    database: DbConfig = DbConfig()
    """Database configuration information"""

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
                                        width=content.get('width', 0),
                                        height=content.get('height', 0),
                                        dialect=content.get('dialect', 'json'),
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

        if self.debug and not len(
                list(
                    filter(lambda x: isinstance(x, StdoutPrinter),
                           self.printers))):
            printers.append(
                StdoutPrinter(name="STDOUT",
                              redis=self.redis,
                              template=Template(
                                  width=0,
                                  height=0,
                                  dialect=PrinterDialectEnum.TEST_JSON,
                              )))

        # replace the list of dict with the data with a dict of proper Printer
        self.printers = printers

    @staticmethod
    def from_dict(raw, **kwargs):
        """Return a :class`victoria.config.Config` instance from a dict.

        :param raw: Dict with the content of the 'yaml' config file.
        :param kwargs: Arguments used to overide the content of the config file.
        """
        config = {}
        victoria_args = {**kwargs, **raw[Config.APPNAME]}
        raw[Config.APPNAME] = victoria_args
        if raw.get(Config.APPNAME) is not None:
            config = raw[Config.APPNAME]
        else:
            raise InvalidConfigFile("No '%s' field in the config file." %
                                    (Config.APPNAME))

        if raw.get('despinassy') is not None:
            config['database'] = DbConfig(**raw['despinassy'])

        return Config(**config)

    @staticmethod
    def from_yaml_file(filename, **kwargs):
        """Read a yaml file and return a :class`victoria.config.Config` instance

        :param filename: String path of the config file in yaml format.
        :param kwargs: Arguments used to overide the content of the config file.
        """
        if os.path.isfile(filename):
            raw = yaml.load(open(filename, 'r'), Loader=yaml.FullLoader)
        else:
            raise InvalidConfigFile('No config file in "%s"' % (filename))

        return Config.from_dict(raw, **kwargs)
