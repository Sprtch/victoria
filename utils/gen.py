from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import argparse

# Jinja2 Init
env = Environment(
    loader=PackageLoader('victoria','templates')
)

def main(title, barcode, size):
    try:
        template = env.get_template("productbarcode%s.zpl" % size)
    except TemplateNotFound:
        print("Template not found")
        return

    print(str(template.render(name=title, number=barcode)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--title', dest='title', type=str, help='Barcode title', default="Cadre Intermediaire 1200 mm Ht. 150 mm Goulotte 75mm x 200mm Inox 304")
    parser.add_argument('--barcode', dest='barcode', type=str, help='Barcode code', default="05S200X100DBTPD-D-U-01")
    parser.add_argument('--size', dest='size', type=str, help='Barcode size', default="70x50")

    args = parser.parse_args()

    main(args.title, args.barcode, args.size)
