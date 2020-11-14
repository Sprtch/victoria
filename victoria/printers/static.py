from victoria.printers.printer import Printer
import socket

class StaticAddressPrinter(Printer):
    def __init__(self, name, redis, address, port, template):
        super().__init__(name, redis)
        self.address = address
        self.port = port
        self.template = template

    def available(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        ret = s.connect_ex((self.address, self.port))
        s.close()
        return (ret == 0)

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

    def render(self, content):
        return str(self.template.render(**content._asdict()))
