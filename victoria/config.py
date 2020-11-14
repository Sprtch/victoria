from victoria.logger import logger
from victoria.printers import StaticAddressPrinter
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import os
import yaml

APPNAME = "victoria"

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)


class InvalidConfigFile(Exception):
    pass

class Config:
    REDIS_DEFAULT_CHAN = "victoria"

    def __init__(self, configpath):
        self.printers = []
        self.templates = {}
        if os.path.isfile(configpath):
            raw = yaml.load(open(configpath, 'r'), Loader=yaml.FullLoader)
        else:
            raise InvalidConfigFile('No config file in "%s"' % (configpath))

        if raw.get(APPNAME) is not None:
            config = raw[APPNAME]
        else:
            raise InvalidConfigFile("No '%s' field in the config file." % (APPNAME))
        
        redis_default = config.get('redis', Config.REDIS_DEFAULT_CHAN)

        
        for temp in config.get('templates', []): 
            try:
                self.templates[temp] = env.get_template(temp)
            except TemplateNotFound:
                logger.error("Template '%s' not found" % (template))
                raise TemplateNotFound

        for dev in config.get('printers', []):
            name, content = list(dev.items())[0]
            devicetype = content.get('type')
            if devicetype == 'static':
                self.printers.append(
                    StaticAddressPrinter(
                        name=name,
                        address=content.get('address'), 
                        port=content.get('port'),
                        redis=content.get('redis', redis_default),
                        template=self.templates[content.get('template')]
                    )
                )
            else:
                raise InvalidConfigFile("Type '%s' not supported" % (content.get('type')))
