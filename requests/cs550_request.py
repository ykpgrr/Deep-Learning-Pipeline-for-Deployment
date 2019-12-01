from .common import from_int, from_str
from .request import *


class Cs550Request(RequestBase):
    """ analysis for Cs550 example use case"""

    def __init__(self, request_id, userId, resource):
        super().__init__(request_id, resource)
        self.user_id = userId

    @staticmethod
    def from_dict(obj: dict) -> 'VideoRequest':
        assert isinstance(obj, dict)
        request_id = from_int(obj.get("requestId"))
        user_id = str(obj.get("userId"))
        path = from_str(obj.get("videoSource"))
        time_stamp = from_int(obj.get("ts"))

        return Cs550Request(
            request_id=request_id,
            userId=user_id,
            #resource=create_resource(path=path), # TODO
            time_stamp=time_stamp, status=None
        )

    def _convert_result(self, result):
        # TODO
        return result

    def set_result(self, result):
        """Sets the result and updates the status"""
        result_json = self._convert_result(result)
        self.result = result_json
        # self.set_status(JobStatus.Done)

    def set_status(self, obj: JobStatus):
        self.status = obj

    def generate_responses(self):
        response = {
            "requestId": self.request_id,
            "userId": self.user_id,
            "status": self.status,
            "videoId": self.resource.resource_id,
            "analyticsResults": self.result
        }
        return response
