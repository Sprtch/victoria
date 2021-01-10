from victoria.printers.printer import Printer
from victoria.reader import MsgReader
from despinassy.Printer import PrinterTypeEnum
import dataclasses
import socket
import json


@dataclasses.dataclass
class StaticAddressPrinter(Printer):
    address: str
    port: int
    PRINTER_TYPE: PrinterTypeEnum = PrinterTypeEnum.STATIC

    def set_reader(self):
        return MsgReader(self.redis)

    def export_config(self):
        return json.dumps({
            "address": self.address,
            "port": self.port,
        })

    def available(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        ret = s.connect_ex((self.address, self.port))
        s.close()
        return (ret == 0)

    def print(self, content: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.address, self.port))
            s.sendall(bytes(content, "utf-8"))
            s.shutdown(socket.SHUT_WR)
            s.close()
        except OSError as e:
            self.error(e)
