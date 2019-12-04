import datetime

from data_resources.extractor_factory import ImageExtractorFactory, VideoExtractorFactory
from data_resources.resource import VideoFileResource, ImageFolderResource, S3VideoResource
from server.common import from_int, from_str, Interval
from .request import *


class Cs550Request(RequestBase):
    """ analysis for Cs550 example use case"""

    def __init__(self, request_id, user_id, time_stamp, extractor, resource):
        super().__init__(request_id, time_stamp, extractor, resource)
        self.user_id = user_id

    @staticmethod
    def from_dict(obj: dict) -> 'Cs550Request':
        assert isinstance(obj, dict)
        request_id = from_int(obj.get("requestId"))
        user_id = str(obj.get("userId"))
        time_stamp = from_int(obj.get("ts"))
        time_interval = Interval.from_dict(obj.get("interval"))
        source = from_str(obj.get("source"))
        path = from_str(obj.get("path"))

        factory_type, resource_type = source.split('/')
        if factory_type == "Video":
            if resource_type == "Local":
                extractor = VideoExtractorFactory().createExtractor(resource_type)
                resource = VideoFileResource(path, time_interval)
            elif resource_type == "S3":
                extractor = VideoExtractorFactory().createExtractor(resource_type)
                resource = S3VideoResource(path, time_interval)
            else:
                raise NotImplementedError
        elif factory_type == "Image":
            if resource_type == "Local":
                extractor = ImageExtractorFactory().createExtractor(resource_type)
                resource = ImageFolderResource(path)
            else:
                raise NotImplementedError

        return Cs550Request(
            request_id=request_id,
            user_id=user_id,
            time_stamp=time_stamp,
            extractor=extractor,
            resource=resource
        )

    def _convert_result(self, time_ref_queue, result_queue):
        result_dict = dict()
        while not time_ref_queue.empty():
            time_ref = time_ref_queue.get()
            result = result_queue.get()
            result_dict[time_ref] = result
        return result_dict

    def set_result_from_queue(self, time_ref_queue, result_queue):
        """Sets the result and updates the status"""
        self.result = self._convert_result(time_ref_queue, result_queue)
        self.set_status(JobStatus.Done)

    def set_status(self, obj: JobStatus):
        self.status = obj

    def generate_response(self):
        response = {
            "requestId": self.request_id,
            "userId": self.user_id,
            "timestamp": datetime.datetime.now().timestamp(),
            "status": self.status.name,
            "cs550Result": self.result
        }
        return response
