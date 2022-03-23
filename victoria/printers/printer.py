from victoria.template import Template
from victoria.db import db
from despinassy.ipc import IpcPrintMessage, ipc_create_print_message
from despinassy import Printer as PrinterTable
import logging
import dataclasses
import json

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Printer():
    """
    The `Printer` base class abstracting a device outputting parts.

    This base class is made to be inherited by a different class specializing
    the inner working of the ouput printer.
    """

    name: str
    """Familiar name of the printer to identify it."""

    redis: str
    """Redis channel to listen to."""

    template: Template
    """
    :class:`victoria.template` of the printer output containing size and
    output format (dialect).
    """
    def initialize(self):
        self._reader = self.set_reader()
        self.retrieve_printer()
        self.info("Initialzed printer: '%s' on channel: '%s'" % (self.name, self.redis))

    def save_printer(self):
        """Save the printer to the database on class initialization.

        The current printer will be saved to the database if it's not
        already present in the database on the class initialization.
        If the printer is already on the database it will unset
        the `hidden` flag to mark the printer as visible for the other app.
        """
        q = PrinterTable.query.filter(PrinterTable.name == self.name)
        if q.count():
            q.first().hidden = False
        else:
            self._entry = PrinterTable(type=self.get_type(),
                                       width=self.template.width,
                                       height=self.template.height,
                                       dialect=self.template.dialect,
                                       name=self.name,
                                       redis=self.redis,
                                       settings=self.export_config())
            db.session.add(self._entry)
        db.session.commit()

    def retrieve_printer(self):
        """Retrive matching printer in the database of the printer class.

        Check the database and find the printer in the database by 
        looking for its name. This function is used to have a direct pointer
        to the database entry for this printer. This pointer is used
        if any modification to the entry need to be done.

        If the printer is not in the database the function will create
        a new entry. It should only happen the first time the program is
        ran.
        Return the database entry found.
        """
        q = PrinterTable.query.filter(PrinterTable.name == self.name)
        if q.count():
            self._entry = q.first()
        else:
            self.error("Printer was not found in the database: creating a new entry")
            self.save_printer()

    def warning(self, msg):
        logger.warning("[warn:%s] %s" % (self.name, msg))

    def error(self, msg):
        logger.error("[err:%s] %s" % (self.name, msg))

    def info(self, msg):
        logger.info("[info:%s] %s" % (self.name, msg))

    def debug(self, msg):
        logger.debug("[dbg:%s] %s" % (self.name, msg))

    def get_type(self):
        return self.PRINTER_TYPE

    def set_reader(self):
        """Set the reader for the current printer.

        The readers are class that implement how to read the stream of
        incoming message. The reader can be different depending on the type
        of printer.
        This function needs to be implemented in the specialized class.

        :ref :class`victoria.reader.MsgReader`
        """
        raise NotImplementedError

    def get_reader(self):
        """Get the reader for the current printer class.
        """
        return self._reader

    def export_config(self) -> str:
        """Return a string in JSON format of the configuration specificity of the current printer type.

        This function needs to be implemented in the specialized class.
        """
        raise NotImplementedError

    def available(self) -> bool:
        """Return if the printer is currently available for print.

        This function needs to be implemented in the specialized class.
        """
        raise NotImplementedError

    def check_availability(self) -> bool:
        """Return if the printer is currently available for print.

        Check the availabilty of the printer and also change the status
        of the printer in the database.
        """
        ret = self.available()
        self._entry.available = ret
        db.session.commit()
        return ret

    def print(self, content: str):
        """Launch a print of the `content` to the printer device.

        This function needs to be implemented in the specialized class.

        :param content: String intrepretable by the printer including the
            content received by this process.
        """
        raise NotImplementedError

    def render(self, message: IpcPrintMessage) -> str:
        """Return a string in the format accepted by the printer device.

        :param message: Content in :class`IpcPrintMessage` structure
            to render
        """
        return self.template.render_barcode(message)

    def print_filename(self, filename):
        """Launch a print from a file.

        :param filename: File with content to print.
        """
        with open(filename, "rb") as fn:
            self.print(fn.read())

    def launch_print(self, content: str, number=1):
        """Start printing a rendered content for the printer.

        :param content: Rendered string interpretable by the printer.
        :param number: Number of print to execute.
        """
        for _ in range(number):
            self.print(content)

    def log_printer_transaction(self, msg: IpcPrintMessage):
        """Save the print executed in this printer to the database.

        :param msg: The content of the message to print.
        """
        db.session.add(self._entry.add_transaction(**msg._asdict()))
        db.session.commit()

    def handle_print_msg(self, printmsg: IpcPrintMessage):
        """Interpret a received message that will execute a print.

        Print messages are special type of message that will trigger
        the execution of a printing on the current printer device.

        :param printmsg: Content to print.
        """
        self.info("Launching the print of the barcode :%s" %
                  (printmsg._asdict()))
        if self.check_availability():
            self.log_printer_transaction(printmsg)
            rendered_print = self.render(printmsg)
            self.launch_print(rendered_print, printmsg.number)
        else:
            rendered_print = self.render(printmsg)
            self.debug("\n" + rendered_print)

    def handle_msg_reception(self, content: str):
        """Interpret the raw string stream incoming to the printer.

        This function will parse the incoming message received by the
        :class`MsgReader` associated to this class. The message should
        be in a JSON format and contain information on its function
        and content.

        :param content: Json formated string.
        """
        try:
            info = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            self.error("Failed to decode json data from redis: %s" % e)
            return

        try:
            self.handle_print_msg(ipc_create_print_message(info))
        except TypeError as e:
            self.error("Invalid message format: %s" % e)

    def listen(self):
        """Infinite loop connecting to the stream of message.
        """

        # TODO Receive msg to stop the loop correctly
        with self.get_reader() as r:
            for msg in r.read_loop():
                self.handle_msg_reception(msg)
