from victoria.schema.message import VictoriaPrintMessage
from victoria.schema.type import PrinterDialectEnum
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import logging
import dataclasses
from abc import ABC, abstractmethod

# Jinja2 Init
env = Environment(loader=PackageLoader('victoria', 'templates'))

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Template(ABC):
    """
    The `Template` class is made to output text from `IPCPrintMessages`.

    The `Template` class is made to abstract the handling of jinja2 files
    without having to handle the filesystem or the project structure.
    This class is also made to store the different information about the printer
    output that don't need to be known from the user of the printer (format, etc ...).
    This class is also made to output text that can be interpreted by
    supported printers when receiving `IPCPrintMessages`.
    So far only the Zebra ZPL printing language and JSON debug output is supported.
    """

    width: int = 0
    height: int = 0
    rotate: bool = False

    @property
    @abstractmethod
    def dialect(self):
        ...

    def render(self, msg: VictoriaPrintMessage) -> str:
        ...

class TemplateJinja(Template):
    @property
    @abstractmethod
    def filename(self):
        ...

    def render(self, msg):
        try:
            templates = env.get_template(self.filename)
            # TODO use something like "__file__" ?
            return str(
                templates.render(
                    **msg._asdict(),
                    width=self.width,
                    height=self.height,
                    rotation=self.rotate
                )
            )
        except TemplateNotFound:
            logger.error("Template '%s' not found" % (self.filename))
            raise TemplateNotFound


class TemplateZpl(TemplateJinja):
    @property
    def dialect(self):
        return PrinterDialectEnum.ZEBRA_ZPL

    @property
    def filename(self):
        return "barcode.zpl"

class TemplateJson(TemplateJinja):
    @property
    def dialect(self):
        return PrinterDialectEnum.JSON

    @property
    def filename(self):
        return "barcode.json"
