from abc import ABC, abstractmethod
import dataclasses
import logging


@dataclasses.dataclass
class Publisher(ABC):
    """Abstraction publish generic data out.

    Publisher are used to log print, advertise internal state & errors.
    Its use is optional and they might be no recipient.
    """

    def __post_init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    @abstractmethod
    def available(self) -> bool:
        """Check the publishing medium is available to send message."""
        ...

    @abstractmethod
    def send(self, msg):
        """Publish payload content."""
        ...
