from abc import ABC, abstractmethod

from server.common import JobStatus


class RequestBase(ABC):
    """ Request base class"""

    def __init__(self, request_id, time_stamp, extractor, resource):
        self.request_id = request_id
        self.time_stamp = time_stamp
        self.extractor = extractor
        self.resource = resource
        self.status = JobStatus.Accepted
        self.result = None

    @abstractmethod
    def from_dict(obj: dict):
        pass

    @abstractmethod
    def set_result_from_queue(self, time_ref_queue, result_queue):
        pass

    @abstractmethod
    def set_status(self, obj: JobStatus):
        pass

    @abstractmethod
    def generate_response(self):
        pass
