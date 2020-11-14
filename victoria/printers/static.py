from victoria.printers.printer import Printer
import socket

class StaticAddressPrinter(Printer):
    def __init__(self, name, redis, address, port=9100):
        super().__init__(name, redis)
        self.address = address
        self.port = port

    def available(self):
        return True

    def print(self, content):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((self.address, self.port))
            s.sendall(bytes(content, "utf-8"))
            s.shutdown(socket.SHUT_WR)
            s.close()
        except OSError as e:
            self.error(e)
