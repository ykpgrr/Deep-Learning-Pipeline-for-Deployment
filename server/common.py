from enum import Enum
from typing import Any


class JobStatus(Enum):
    # TODO Add extra status
    Accepted = 0
    InProgress = 1
    Done = 2
    Failed = 3


def create_resource(path, time_interval):
    if app_config.get('deployment').get('site') == "amazon":
        is_s3bucket = True
    elif app_config.get('deployment').get('site') == "local":
        is_s3bucket = False
    else:
        raise Exception(
            f"There is no deployment type like {app_config.get('deployment').get('site')}, please check the "
            "config file")

    if is_s3bucket:
        return S3VideoResource(
            video_path=path,
            time_interval=time_interval,
            clipping=clipping)
    else:
        return VideoFileResource(
            video_path=path,
            time_interval=time_interval,
            clipping=clipping)

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

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = to_float(self.start)
        result["end"] = to_float(self.end)
        return result

def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x
