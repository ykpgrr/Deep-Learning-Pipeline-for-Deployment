from abc import ABC, abstractmethod
from enum import Enum


class JobStatus(Enum):
# TODO Add extra status
    Accepted = 0
    InProgress = 1
    Done = 2
    Failed = 3


class RequestBase(ABC):
    """ Request base class"""

    def __init__(self, request_id, resource):
        self.request_id = request_id
        self.resource = resource
        self.status = JobStatus.Accepted
        self.result = None

    @abstractmethod
    def from_dict(obj: dict):
        pass

    @abstractmethod
    def set_result(self, result):
        pass

    @abstractmethod
    def set_status(self, obj: JobStatus):
        pass

    @abstractmethod
    def generate_responses(self):
        pass
