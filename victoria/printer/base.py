from abc import ABC, abstractmethod
import logging
import dataclasses

logger = logging.getLogger()


@dataclasses.dataclass
class Printer(ABC):
    """
    The `Printer` base class abstracting a device outputting parts.

    This base class is made to be inherited by a different class specializing
    the inner working of the ouput printer.
    """

    def connect(self):
        pass

    def disconnect(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return self

    @property
    @abstractmethod
    def type(self):
        ...

    @abstractmethod
    def available(self) -> bool:
        """Return if the printer is currently available for print.

        This function needs to be implemented in the specialized class.
        """
        ...

    @abstractmethod
    def print(self, content: str, number=1) -> int | None:
        """Launch a print of the `content` to the printer device.

        This function needs to be implemented in the specialized class.

        :param content: String intrepretable by the printer including the
            content received by this process.
        """
        ...
