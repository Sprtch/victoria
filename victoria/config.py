from victoria.logger import logger
from victoria.printers import StaticAddressPrinter, StdoutPrinter
from victoria.template import Template
import os
import yaml

class InvalidConfigFile(Exception):
    pass

class Config:
    APPNAME = "victoria"
    REDIS_DEFAULT_CHAN = "victoria"

    def __init__(self):
        self.printers = []

    def parse(self, content):
        if content.get(Config.APPNAME) is not None:
            config = content[Config.APPNAME]
        else:
            raise InvalidConfigFile("No '%s' field in the config file." % (Config.APPNAME))
        
        redis_default = config.get('redis', Config.REDIS_DEFAULT_CHAN)

        for dev in config.get('printers', []):
            name, content = list(dev.items())[0]
            devicetype = content.get('type')
            if devicetype == 'static':
                dev = StaticAddressPrinter(
                    name=name,
                    address=content.get('address'), 
                    port=content.get('port'),
                    redis=content.get('redis', redis_default),
                    template=Template(
                        width=content.get('width', 50),
                        height=content.get('height', 70),
                        dialect=content.get('dialect', 'zpl'),
                    )
                )
            elif devicetype == 'stdout':
                dev = StdoutPrinter(
                    name=name,
                    redis=content.get('redis', redis_default),
                    template=Template(
                        width=content.get('width', 50),
                        height=content.get('height', 70),
                        dialect=content.get('dialect', 'zpl'),
                    )
                )
            else:
                raise InvalidConfigFile("Type '%s' not supported" % (content.get('type')))

            self.printers.append(dev)

        return self

    def from_yaml_file(self, filename):
        if os.path.isfile(filename):
            raw = yaml.load(open(filename, 'r'), Loader=yaml.FullLoader)
        else:
            raise InvalidConfigFile('No config file in "%s"' % (filename))

        return self.parse(raw)
