"""Device orchestration for the Victoria printing pipeline.

A :class:`VictoriaDevice` ties together a reader, transformer, template,
printer, and publisher into a single read-loop that processes incoming print
requests end-to-end.
"""

from victoria.device.device import VictoriaDevice
