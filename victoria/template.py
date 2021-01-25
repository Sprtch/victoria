from despinassy.ipc import IpcPrintMessage
from despinassy.Printer import PrinterDialectEnum
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import logging
import dataclasses

# Jinja2 Init
env = Environment(loader=PackageLoader('victoria', 'templates'))

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Template:
    width: int = 0
    height: int = 0
    rotate: bool = False
    dialect: PrinterDialectEnum = PrinterDialectEnum.ZEBRA_ZPL

    def __post_init__(self):
        if isinstance(self.dialect, str):
            self.dialect = PrinterDialectEnum.from_extension(self.dialect)
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if hasattr(field.type, "__args__") and len(
                    field.type.__args__
            ) == 2 and field.type.__args__[-1] is type(None):
                if value is not None and not isinstance(
                        value, field.type.__args__[0]):
                    raise ValueError(
                        f'Expected {field.name} to be either {field.type.__args__[0]} or None'
                    )
            elif not isinstance(value, field.type):
                raise ValueError(f'Expected {field.name} to be {field.type}, '
                                 f'got {repr(value)}')

    def size(self, width, height):
        self.width = width
        self.height = height

    def set_rotation(self, value):
        self.rotate = value

    def _get_barcode_filename(self):
        if self.dialect == PrinterDialectEnum.ZEBRA_ZPL:
            return "barcode.zpl"
        if self.dialect == PrinterDialectEnum.TEST_JSON:
            return "barcode.json"
        else:
            logger.error("The dialect '%s' is not supported" %
                         (str(self.dialect)))

    def render_barcode(self, msg: IpcPrintMessage):
        try:
            filename = self._get_barcode_filename()
            templates = env.get_template(filename)
            if self.rotate:
                width = self.height
                height = self.width
            else:
                width = self.width
                height = self.height
            return str(
                templates.render(**msg._asdict(),
                                 width=width,
                                 height=height,
                                 rotation=self.rotate))
        except TemplateNotFound:
            logger.error("Template '%s' not found" % (filename))
            raise TemplateNotFound
