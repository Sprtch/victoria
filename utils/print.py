from despinassy.ipc import IpcPrintMessage, redis_subscribers_num
import argparse
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def main(channel, title, barcode, number):
    msg = IpcPrintMessage(
        barcode=barcode,
        name=title,
        number=number,
    )
    if redis_subscribers_num(r, channel):
        r.publish(channel, json.dumps(msg._asdict()))

    else:
        print("No recipient in channel '%s'" % (channel))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--title',
        dest='title',
        type=str,
        help='Barcode title',
        default=
        "Cadre Intermediaire 1200 mm Ht. 150 mm Goulotte 75mm x 200mm Inox 304"
    )
    parser.add_argument('--barcode',
                        dest='barcode',
                        type=str,
                        help='Barcode code',
                        default="05S200X100DBTPD-D-U-01")
    parser.add_argument('--redis',
                        dest='redis',
                        type=str,
                        help='The printer recipient redis channel',
                        default="victoria")
    parser.add_argument('--number',
                        dest='number',
                        type=int,
                        help='The number of prints',
                        default=1)

    args = parser.parse_args()

    main(args.redis, args.title, args.barcode, args.number)
