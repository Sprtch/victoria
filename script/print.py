from victoria.schema.message import VictoriaPrintMessage, IpcMessageType
import argparse
import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def main(channel, title, barcode, number, device, origin):
    msg = VictoriaPrintMessage(
        device=device,
        origin=origin,
        title=title,
        barcode=barcode,
        number=number,
        type=IpcMessageType.PRINT,
    )
    r.publish(channel, json.dumps(msg.asdict()))


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
    parser.add_argument('--device',
                        dest='device',
                        type=str,
                        help='Device name',
                        default='victoria')
    parser.add_argument('--origin',
                        dest='origin',
                        type=str,
                        help='Origin application',
                        default='victoria')

    args = parser.parse_args()

    main(args.redis, args.title, args.barcode, args.number, args.device, args.origin)
