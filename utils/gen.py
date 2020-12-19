from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
from victoria.config import Config
from despinassy.ipc import IpcPrintMessage
import argparse

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)

config = {
    "victoria": {
        "redis": 'victoria',
        "printers": [
            { "main": {
                "type": "stdout",
                "width": 70,
                "height": 50,
                "dialect": "zpl",
                "redis": "victoria"
            }}
        ]
    }
}

def main(printer, title, barcode, size):
    if len(size.split('x')) == 2:
        width, height = size.split('x')
        printer.template.size(int(width), int(height))
    else:
        return
    msg = IpcPrintMessage(barcode=barcode, name=title)
    printer.handle_print_msg(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--title', dest='title', type=str, help='Barcode title', default="Cadre Intermediaire 1200 mm Ht. 150 mm Goulotte 75mm x 200mm Inox 304")
    parser.add_argument('--barcode', dest='barcode', type=str, help='Barcode code', default="05S200X100DBTPD-D-U-01")
    parser.add_argument('--size', dest='size', type=str, help='Barcode size', default="70x50")
    args = parser.parse_args()
    conf = Config().parse(config)
    if len(conf.printers) == 1:
        main(conf.printers[0], args.title, args.barcode, args.size)
