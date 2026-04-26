from enum import IntEnum

class PrinterDialectEnum(IntEnum):
    """
    List the currently supported printer dialect for printer device to output.
    """

    UNDEFINED = 0
    """Not defined dialect"""
    ZEBRA_ZPL = 1
    """The Zebra ZPL printing language"""
    TEST_JSON = 2
    """Output as JSON object"""

    @staticmethod
    def from_extension(extension: str):
        """Return dialect from file extension.

        :param extension: String representing the extension of the dialect.
        """
        if extension == "zpl":
            return PrinterDialectEnum.ZEBRA_ZPL
        elif extension == "json":
            return PrinterDialectEnum.TEST_JSON
        else:
            return PrinterDialectEnum.UNDEFINED


class PrinterTypeEnum(IntEnum):
    """
    List the currently supported type of printer device.
    """

    UNDEFINED = 0
    """Not defined printer"""
    STDOUT = 1
    """Print to the terminal"""
    TEST = 2
    """Printer type used only on test case"""
    STATIC = 3
    """Network printer with a static IP address"""
