from enum import IntEnum

class PrinterDialectEnum(IntEnum):
    """
    List the currently supported printer dialect for printer device to output.
    """

    UNDEFINED = 0
    """Not defined dialect"""
    ZEBRA_ZPL = 1
    """The Zebra ZPL printing language"""
    JSON = 2
    """Output as JSON object"""


class PrinterTypeEnum(IntEnum):
    """
    List the currently supported type of printer device.
    """

    UNDEFINED = 0
    """Not defined printer"""
    STDOUT = 1
    """Print to the terminal"""
    STATIC = 2
    """Network printer with a static IP address"""
