from victoria.printer.stdout import StdoutPrinter
from victoria.printer.static import StaticAddressPrinter
from victoria.printer.base import Printer
from victoria.schema.type import PrinterTypeEnum
from unittest.mock import patch, MagicMock
import pytest


class TestStdoutPrinter:
    def test_is_printer(self):
        p = StdoutPrinter()
        assert isinstance(p, Printer)

    def test_type(self):
        p = StdoutPrinter()
        assert p.type == PrinterTypeEnum.STDOUT

    def test_available(self):
        p = StdoutPrinter()
        assert p.available() is True

    def test_print_single(self, capsys):
        p = StdoutPrinter()
        p.print("hello")
        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_print_multiple(self, capsys):
        p = StdoutPrinter()
        p.print("line", number=3)
        captured = capsys.readouterr()
        assert captured.out.count("line") == 3

    def test_print_default_number(self, capsys):
        p = StdoutPrinter()
        p.print("single")
        captured = capsys.readouterr()
        assert captured.out.count("single") == 1

    def test_context_manager(self):
        p = StdoutPrinter()
        with p as ctx:
            assert ctx is p


class TestStaticAddressPrinter:
    def test_is_printer(self):
        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        assert isinstance(p, Printer)

    def test_type(self):
        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        assert p.type == PrinterTypeEnum.STATIC

    def test_stores_address_and_port(self):
        p = StaticAddressPrinter(address="10.0.0.1", port=8080)
        assert p.address == "10.0.0.1"
        assert p.port == 8080

    @patch("victoria.printer.static.socket.socket")
    def test_available_true(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket_cls.return_value = mock_sock

        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        assert p.available() is True
        mock_sock.connect_ex.assert_called_once_with(("192.168.1.1", 9100))
        mock_sock.close.assert_called_once()

    @patch("victoria.printer.static.socket.socket")
    def test_available_false(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 1
        mock_socket_cls.return_value = mock_sock

        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        assert p.available() is False

    @patch("victoria.printer.static.socket.socket")
    def test_print_sends_content(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        p.print("test-data")

        mock_sock.connect.assert_called_once_with(("192.168.1.1", 9100))
        mock_sock.sendall.assert_called_once_with(b"test-data")
        mock_sock.shutdown.assert_called_once()
        mock_sock.close.assert_called_once()

    @patch("victoria.printer.static.socket.socket")
    def test_print_multiple(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_socket_cls.return_value = mock_sock

        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        p.print("data", number=3)

        assert mock_sock.connect.call_count == 3
        assert mock_sock.sendall.call_count == 3

    @patch("victoria.printer.static.socket.socket")
    def test_print_handles_oserror(self, mock_socket_cls):
        mock_sock = MagicMock()
        mock_sock.connect.side_effect = OSError("connection refused")
        mock_socket_cls.return_value = mock_sock

        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        p.print("data")

    def test_context_manager(self):
        p = StaticAddressPrinter(address="192.168.1.1", port=9100)
        with p as ctx:
            assert ctx is p
