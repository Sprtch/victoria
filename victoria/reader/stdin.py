from victoria.reader.file import IoReader
from victoria.schema.message import VictoriaPrintMessage
import json
import io
import sys
import dataclasses


@dataclasses.dataclass
class Stdin(IoReader):
    """Yields lines from stdin as a continuous generator."""

    io: io.IOBase = sys.stdin

    def format(self, content) -> str:
        return json.dumps(VictoriaPrintMessage(
            device="victoria",
            origin="stdin",
            title="",
            barcode=content.strip(),
            number=1,
        ).asdict())
