from typing import TypeVar, Type, Callable, Iterable
import logging
import dataclasses

T = TypeVar("T")
logger = logging.getLogger(__name__)


def attempt(action: Callable[[], T], label: str) -> T | None:
    """Run a side-effecting call, log and swallow any exception."""
    try:
        return action()
    except Exception:
        logger.exception("Error in: %s", label)
        return None


def attempt_all(actions: Iterable[Callable[[], None]]) -> None:
    """Run every action, never let one failure abort the rest."""
    for action in actions:
        attempt(action, label=action.__qualname__)


def narrow(data: dict, target: Type[T]) -> dict:
    """Extract only the fields from data that exist in target dataclass.

    >>> @dataclasses.dataclass
        class Foo:
            foo: int
            bar: int
    >>> narrow({ "foo": 1, "bar": 2, "baz": 3}, Foo)
    { "foo": 1, "bar": 2 }
    """
    valid_keys = {f.name for f in dataclasses.fields(target)}
    return {k: v for k, v in data.items() if k in valid_keys}
