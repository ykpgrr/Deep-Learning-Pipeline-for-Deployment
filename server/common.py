from enum import Enum
from typing import Any


class JobStatus(Enum):
    # TODO Add extra status
    Accepted = 0
    InProgress = 1
    Done = 2
    Failed = 3


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x
