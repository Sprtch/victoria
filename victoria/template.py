import dataclasses
from enum import Enum
from despinassy.ipc import IpcPrintMessage
from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)

class DialectEnum(Enum):
    ZEBRA_ZPL = "zpl"

@dataclasses.dataclass
class Template:
    width: int = 0
    height: int = 0
    dialect: DialectEnum = DialectEnum.ZEBRA_ZPL

    def __post_init__(self):
        self.dialect = DialectEnum(self.dialect)
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if hasattr(field.type, "__args__") and len(field.type.__args__) == 2 and field.type.__args__[-1] is type(None):
                if value is not None and not isinstance(value, field.type.__args__[0]):
                    raise ValueError(f'Expected {field.name} to be either {field.type.__args__[0]} or None')
            elif not isinstance(value, field.type):
                raise ValueError(f'Expected {field.name} to be {field.type}, '
                                f'got {repr(value)}')

    def size(width, height):
        self.width = width
        self.height = height

    def _get_barcode_filename(self):
        if self.dialect == DialectEnum.ZEBRA_ZPL:
            return "barcode.zpl"
        else:
            print("Not Supported")

    def render_barcode(self, msg: IpcPrintMessage):
        try:
            templates = env.get_template(self._get_barcode_filename())
            return str(templates.render(**msg._asdict(), width=self.width, height=self.height))
        except TemplateNotFound:
            logger.error("Template '%s' not found" % (temp))
            raise TemplateNotFound
