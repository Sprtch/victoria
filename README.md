# Victoria

Victoria is the barcode printing daemon handling the barcode generation
and the connection with the network connected printer.

It act as the gateway for the other process to physically print the barcodes
they send through _redis_.
Victoria also handle the data dispatching to printers and serve as
an abstraction for the different printers and the printing dialect.

## Usage

This package run as a daemon in the buildroot [firmware](https://github.com/Sprtch/buildroot)
with file logging and pid file.

During development process the script launch the program with the following
command to output the log in the console.

```txt
> source venv/bin/activate
> venv/bin/python victoria --no-daemon --debug
```

## Utils

A set of utility script are available in the `/utils` directory.

### `gen.py`

Generate a template with the title passed with `--title` argument, and
the barcode info with `--barcode` argument.

### `print.py`

Send a print request through redis to the running `victoria` script.

## Configure

The configuration serve to map the printers to a set of data.

* The communication medium to the printer
* The mandatory data to communicate with the printer depending on the medium
* The redis channel to listen to
* The available templates to print

This is an exemple configuration file loaded with the `-c <path>` arugment.

```yaml
victoria:
    redis: 'victoria' # Default redis channel to listen to
    templates:
        - "productbarcode70x50.zpl" # List the available priting format
    printers:
        - main: # Name of the printer
            type: "static" # The method of communication
            address: "192.168.8.8" # The 'static' method need an address
            port: 9100  # The 'static' method need a port
            template: "productbarcode70x50.zpl" # Refer to available templates
            redis: "victoria" # The redis channel this specific printer listen to
```

## Useful links

* [Zebra ZPL Manual](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf)
* [Label Viewer](http://labelary.com/viewer.html)
* [Z4M Printer Manual](https://www.servopack.de/support/zebra/Z4Mplus_Z6Mplus.pdf)
