from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound
import argparse
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def main(title, barcode, size):
    r.publish('printer', '{"name": "%s", "barcode": "%s"}' % (title, barcode))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--title', dest='title', type=str, help='Barcode title', default="Cadre Intermediaire 1200 mm Ht. 150 mm Goulotte 75mm x 200mm Inox 304")
    parser.add_argument('--barcode', dest='barcode', type=str, help='Barcode code', default="05S200X100DBTPD-D-U-01")
    parser.add_argument('--size', dest='size', type=str, help='Barcode size', default="40x100")

    args = parser.parse_args()

    main(args.title, args.barcode, args.size)
