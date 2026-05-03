"""Message transformers for converting raw input into print messages.

Transformers parse raw strings from input sources (Redis, stdin, etc.) into
structured :class:`~victoria.schema.message.VictoriaPrintMessage` objects
that can be rendered by a template and sent to a printer.

Available transformers:

- :class:`MessageTransformer` -- abstract base class defining the interface.
- :class:`JsonTransformer` -- parses JSON input into a print message.
- :class:`RawTransformer` -- uses the raw input string as barcode content.
"""

from victoria.transformer.base import MessageTransformer
from victoria.transformer.json import JsonTransformer
from victoria.transformer.raw import RawTransformer
