from victoria.config.config import Config
from erie.reader.redis import RedisReader
from erie.reader.stdin import Stdin

from erie.publisher.redis import Redis
from erie.publisher.stdout import Stdout

from victoria.printer.stdout import StdoutPrinter
from victoria.printer.static import StaticAddressPrinter

from victoria.transformer import JsonTransformer, RawTransformer

from victoria.template import TemplateZpl, TemplateJson

from victoria.device import VictoriaDevice


def generate_devices_from_config(config: Config):
    """Return devices list from config object.

    >>> config = Config.from_json("/to/json/file.json")
    >>> generate_devices_from_config(config)
    """
    devices = []

    for dev in config.printers:
        if dev.printer.type == "stdout":
            printer = StdoutPrinter()
        elif dev.printer.type == "static":
            printer = StaticAddressPrinter(
                address=dev.printer.address,
                port=dev.printer.port,
            )
        else:
            raise ValueError(f"{dev.name}: unknown printer type '{dev.printer.type}'")


        if dev.reader.type == "redis":
            reader = RedisReader(
                channel=dev.reader.channel,
                host=dev.reader.host,
                port=dev.reader.port,
                db=dev.reader.db,
            )
            transformer = JsonTransformer()
        elif dev.reader.type == "stdin":
            reader = Stdin()
            transformer = RawTransformer()
        else:
            raise ValueError(f"{dev.name}: unknown reader type '{dev.reader.type}'")


        if dev.publisher.type == "redis":
            if not dev.publisher.channel:
                raise ValueError(f"{dev.name}: redis publisher requires 'channel'")
            publisher = Redis(
                host=dev.publisher.host,
                port=dev.publisher.port,
                channel=dev.publisher.channel
            )
        elif dev.publisher.type == "stdout":
            publisher = Stdout()
        else:
            raise ValueError(f"{dev.name}: unknown publisher type '{dev.publisher.type}'")

        if dev.template.dialect == "zpl":
            template = TemplateZpl(
                width=dev.template.width,
                height=dev.template.height,
            )
        elif dev.template.dialect == "json":
            template = TemplateJson(
                width=dev.template.width,
                height=dev.template.height,
            )
        else:
            raise ValueError(f"{dev.name}: unknown dialect type '{dev.reader.type}'")

        device = VictoriaDevice(
            name=dev.name,
            reader=reader,
            transformer=transformer,
            printer=printer,
            publisher=publisher,
            template=template,
        )

        devices.append(device)

    return devices
