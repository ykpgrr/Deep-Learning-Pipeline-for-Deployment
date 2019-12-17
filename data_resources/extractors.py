import glob
import logging
import os
from abc import ABC, abstractmethod

import cv2

from .resource import ImageFolderResource, VideoFileResource, S3VideoResource

logger = logging.getLogger(__name__)


class Extractor(ABC):
    """
    Abstract extractor class for extractors that can extract the related images from resources and
    return related time(sec) and frame
    """

    def __init__(self):
        self.resource_class = None

    @abstractmethod
    def _extract(self, resource):
        pass

    def extract(self, resource):
        """returns a generator for images"""
        # self.check_resource_type(resource)
        return self._extract(resource)


class ImageFolderExtractor(Extractor):
    """ Image file Extractor with support regex from file system, returns 'image' and 'time reference'(as always 0)"""

    def __init__(self):
        super().__init__()
        self.resource_class = ImageFolderResource

    def _extract(self, resource):
        for file in glob.glob(os.path.join(resource.source_path, "*")):
            yield cv2.imread(file), 0


class VideoExtractor(Extractor):
    """
    Video file extractor from file system, returns related frame and time reference corresponding to given time interval
    """

    def __init__(self):
        super().__init__()
        self.resource_class = VideoFileResource

    def _extract(self, resource):
        capture = cv2.VideoCapture(resource.source_path)
        if capture.isOpened():
            if resource.time_interval:
                # jump to relevant "start msec"
                capture.set(cv2.CAP_PROP_POS_MSEC, resource.time_interval.start * 1000)
                # check single frame or not
                if resource.time_interval.start == resource.time_interval.end:
                    current_msec = capture.get(cv2.CAP_PROP_POS_MSEC)
                    is_read, frame = capture.read()
                    yield frame, format(current_msec / 1000, '.3f')
                    return
        else:
            logger.info(f"Video Path Not Found: {resource.source_path}")
            return

        frame_number = 1
        curr_frame = 1
        is_read = True
        while is_read:
            current_msec = capture.get(cv2.CAP_PROP_POS_MSEC)
            is_read, frame = capture.read()

            if is_read:
                curr_frame += 1
                frame_number += 1
                yield frame, format(current_msec / 1000, '.3f')
            else:
                break

            if resource.time_interval:
                if capture.get(cv2.CAP_PROP_POS_MSEC) > resource.time_interval.end * 1000:
                    break


class S3VideoExtractor(VideoExtractor):
    """ S3 Video file download and Process"""

    def __init__(self):
        super().__init__()
        self.resource_class = S3VideoResource

    def _extract(self, resource):
        return super()._extract(resource)
