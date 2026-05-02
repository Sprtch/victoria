from abc import ABC, abstractmethod
from victoria.schema.message import VictoriaPrintMessage
import dataclasses


@dataclasses.dataclass
class MessageTransformer(ABC):
    """
    """

    @abstractmethod
    def transform(self, content: str) -> VictoriaPrintMessage:
        """Transform text input into `VictoriaPrintMessage`."""
        ...
