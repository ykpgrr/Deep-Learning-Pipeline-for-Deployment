from abc import ABC, abstractmethod

from server.common import JobStatus


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
