from victoria.transformer.base import MessageTransformer
from victoria.schema.message import VictoriaPrintMessage
import json
import dataclasses


@dataclasses.dataclass
class JsonTransformer(MessageTransformer):
    def transform(self, content: str) -> VictoriaPrintMessage:
        return VictoriaPrintMessage(**json.loads(content))
