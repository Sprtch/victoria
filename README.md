# Victoria

The barcode printing daemon handling the barcode generation and the connection
with the network connected printer. The barcode query are received with redis.

## Usage

This package is made to be ran as a daemon in the buildroot [firmware](https://github.com/Sprtch/buildroot)
with file logging and pid file.

During development process the script can be launched with the following
command to log in the console.

```txt
> source venv/bin/activate
> venv/bin/python victoria --no-daemon
```

## Utils

* `gen.py` Generate a template with the title passed with `--title` argument, and
  the barcode info with `--barcode` argument.
* `print.py` Send a print request through redis to the running `victoria`
  script.


# Useful links

* [Zebra ZPL Manual](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf)
* [Label Viewer](http://labelary.com/viewer.html)
* [Z4M Printer Manual](https://www.servopack.de/support/zebra/Z4Mplus_Z6Mplus.pdf)
