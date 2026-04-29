from typing import Optional
import dataclasses
import yaml


@dataclasses.dataclass
class ConfigPrinterReader:
    type: str
    """Device type ('evdev', 'serial', 'stdin')"""

    path: Optional[str] = None
    """Device 'path' for 'evdev' & 'serial' devices"""

    device_id: Optional[str] = None
    """Device 'id' for 'evdev' & 'serial' devices"""

    host: str = "localhost"
    """Host address for 'redis' publisher type"""

    port: int = 6379
    """Port for 'redis' publisher type"""

    channel: str = "victoria"
    """Communication channel for 'redis' publisher type"""

    db: int = 0
    """"""


@dataclasses.dataclass
class ConfigPrinterPublisher:
    """Publisher configuration."""

    type: str = "redis"
    """Publisher type ('redis', 'stdout')"""

    host: str = "localhost"
    """Host address for 'redis' publisher type"""

    port: int = 6379
    """Port for 'redis' publisher type"""

    channel: str = "victoria"
    """Communication channel for 'redis' publisher type"""

    db: int = 0
    """"""


@dataclasses.dataclass
class ConfigPrinterTemplate:
    dialect: str
    width: int
    height: int


@dataclasses.dataclass
class ConfigPrinter:
    type: str = "redis"
    """Publisher type ('static', 'stdout')"""

@dataclasses.dataclass
class ConfigDevice:
    """Device configuration."""

    name: str
    """Device name"""

    printer: ConfigPrinter
    """"""

    template: ConfigPrinterTemplate
    """"""

    publisher: ConfigPrinterPublisher
    """Publisher channel for the device"""

    reader: ConfigPrinterReader
    """"""

@dataclasses.dataclass
class Config:
    """
    """

    name: str = "victoria"
    """Familiar name of the program currently in use."""

    debug: bool = False
    """Use debugging logging level (default 'warn')"""

    nodaemon: bool = False
    """Do not run the application as a daemon"""

    logfile: Optional[str] = None
    """Log file location (default: stdout)"""

    pidfile: Optional[str] = None
    """Pid file location required for daemon mode (default: None)"""

    publisher: ConfigPrinterPublisher = dataclasses.field(default_factory=ConfigPrinterPublisher)
    """Default 'publisher' configuration. This publisher will be used if device doesn't define any publisher."""

    printers: list = dataclasses.field(default_factory=list)
    """List of the printers declared in the config file."""

    @staticmethod
    def from_dict(data: Dict[str, Any], **kwargs) -> "Config":
        data = data.get("victoria", {})  # Retrieve the app config
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        default_publisher = data.get("publisher", dataclasses.asdict(ConfigPrinterPublisher()))

        printers = []
        for d in data.get("printers", []):
            out_data = d.get("publisher", default_publisher)
            publisher = ConfigPrinterPublisher(
                **out_data,
            )

            template = ConfigPrinterTemplate(
                **d["template"]
            )

            reader = ConfigPrinterReader(
                **d["reader"]
            )

            printer = ConfigPrinter(
                **d["printer"]
            )

            printers.append(
                ConfigDevice(**{
                    **d,
                    "printer": printer,
                    "publisher": publisher,
                    "template": template,
                    "reader": reader,
                })
            )

        return Config(**{
            **data,
            "publisher": default_publisher,
            "printers": printers,
        })

 

    @staticmethod
    def from_yaml(path: str, **kwargs) -> "Config":
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return Config.from_dict(data, **kwargs)

    @staticmethod
    def from_json(path: str, **kwargs) -> "Config":
        with open(path) as f:
            data = json.load(f)
        return Config.from_dict(data, **kwargs)
