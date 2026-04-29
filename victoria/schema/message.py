import dataclasses
from enum import IntEnum

class IpcMessageType(IntEnum):
    UNDEFINED = 0
    IS_ALIVE = 1
    DISCONNECT = 2
    PRINT = 3
    LOG = 4


@dataclasses.dataclass
class BaseIpcMessage:
    device: str
    """Device name that originate the message"""

    origin: str
    """Application that originated the message"""

    def asdict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class VictoriaPrintMessage(BaseIpcMessage):
    """IPC message received as input."""

    title: str
    """Print title."""

    barcode: str
    """Barcode content to print."""

    number: int  = 1
    """Number of copy to print."""

    type: IpcMessageType = IpcMessageType.PRINT


@dataclasses.dataclass
class VictoriaLogMessage(BaseIpcMessage):
    type: IpcMessageType = IpcMessageType.LOG


@dataclasses.dataclass
class VictoriaPrinterNotAvailableMessage(BaseIpcMessage):
    type: IpcMessageType = IpcMessageType.DISCONNECT


@dataclasses.dataclass
class VictoriaPrinterAvailableMessage(BaseIpcMessage):
    type: IpcMessageType = IpcMessageType.IS_ALIVE
