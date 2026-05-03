"""Victoria - Barcode printing daemon.

Victoria acts as a gateway between application processes and network-connected
label printers. It receives barcode print requests via Redis, transforms them
into printer-native output (e.g. Zebra ZPL), and sends the resulting data to
physical printers over TCP.
"""