from victoria.printers.printer import Printer
import logging
import dataclasses
import socket

logger = logging.getLogger()

@dataclasses.dataclass
class StaticAddressPrinter(Printer):
    address: str
    port: int

    @property
    def type(self):
        return PrinterTypeEnum.STATIC

    def available(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        ret = s.connect_ex((self.address, self.port))
        s.close()
        return (ret == 0)

    def print(self, content: str, number=1):
        def _print():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect((self.address, self.port))
                s.sendall(bytes(content, "utf-8"))
                s.shutdown(socket.SHUT_WR)
                s.close()
            except OSError as e:
                logger.error(e)

        for _ in range(number):
            _print()
