from victoria.reader.reader import Reader
from victoria.printer.printer import Printer
from victoria.template import Template
from victoria.publisher import Publisher
import dataclasses
import logging
import time

logger = logging.getLogger()


@dataclasses.dataclass
class Device:
    """Device definition built from the configuration.

    An input device is defined by multiple components:

    - Its name
    - The 'reader' or the input source.
    - The 'formatter' or the method that transform an input message into an
      'output' message.
    - The 'output' or the medium to push out the message.
    """

    name: str
    """Familiar name to give to a device."""

    reader: Reader
    """The input source."""

    printer: Printer
    """The printer source."""

    publisher: Publisher
    """The output source to communicate log and status."""

    template: Template
    """Processor to transform a raw input into a printable message."""

    def disconnect(self):
        # TODO send a message that notificate the disconnection.
        pass

    def read_loop(self, stop_event=None):
        logger.info(
            f"[{self.__class__.__name__}:{self.name}] Init `read_loop` function."
        )

        while stop_event is None or not stop_event.is_set():
            if not self.reader.present():
                # TODO
                logger.debug(
                    f"[{self.__class__.__name__}:{self.name}] Reader '{self.reader.type}' is not present"
                )
                time.sleep(5)
            else:
                # self.publisher.send(
                #     IpcIsAliveMessage(
                #         device=self.name,
                #     )
                # )
                logger.info(
                    f"[{self.__class__.__name__}:{self.name}] Reader '{self.reader.type}' connecting."
                )
                with self.reader as reader:
                    for content in reader.retrieve(stop_event):
                        template = self.template.render(content)
                        if self.printer.available():
                            ret = self.printer.print(template, number=content.number)
                            if ret is None:
                                pass # TODO self.publisher.send(PrinterError)
                            else:
                                pass # TODO self.publisher.send(PrinterLog)
                        else:
                            self.publisher.send(VictoriaPrinterNotAvailableMessage())
                logger.info(
                    f"[{self.__class__.__name__}:{self.name}] Reader '{self.reader.type}' Disconnected."
                )
        self.publisher.send(
            IpcDisconnectMessage(
                device=self.name,
            )
        )
