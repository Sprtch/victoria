"""Printer abstractions for sending rendered output to physical devices.

Printers receive rendered content (e.g. ZPL commands) and deliver it to the
target output device, whether that is a network printer over TCP or stdout for
debugging purposes.

Available printers:

- :class:`~victoria.printer.base.Printer` -- abstract base class.
- :class:`~victoria.printer.static.StaticAddressPrinter` -- network printer
  at a fixed IP address and port.
- :class:`~victoria.printer.stdout.StdoutPrinter` -- prints to stdout.
"""