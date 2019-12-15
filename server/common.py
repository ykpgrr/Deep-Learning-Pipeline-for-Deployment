from enum import Enum
from typing import Any


class JobStatus(Enum):
    # TODO Add extra status
    Accepted = 0
    InProgress = 1
    Done = 2
    Failed = 3


class Interval:
    start: float  # Seconds
    end: float

    def __init__(self, start: float, end: float) -> None:
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(obj: Any) -> 'Interval':
        assert isinstance(obj, dict)
        start = from_float(obj.get("start"))
        if obj.get("end") is None:
            end = from_float(obj.get("start"))
        else:
            end = from_float(obj.get("end"))
        return Interval(start, end)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x
