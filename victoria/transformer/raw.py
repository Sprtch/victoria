from victoria.transformer.base import MessageTransformer
from victoria.schema.message import VictoriaPrintMessage
import dataclasses


@dataclasses.dataclass
class RawTransformer(MessageTransformer):
    def transform(self, content: str) -> VictoriaPrintMessage:
        return VictoriaPrintMessage(
            device="",
            origin="",
            title="",
            barcode=content,
        )
