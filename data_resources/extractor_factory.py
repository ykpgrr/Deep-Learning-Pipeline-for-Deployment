import logging
from abc import ABC, abstractmethod

from .extractors import Extractor, ImageFolderExtractor, VideoFileExtractor, S3VideoExtractor

logger = logging.getLogger(__name__)


class ExtractorFactory(ABC):
    @abstractmethod
    def _createExtractor(self, extractorType: str) -> Extractor:
        pass

    def createExtractor(self, resource):
        """returns a generator for images"""
        # self.check_resource_type(resource)
        return self._createExtractor(resource)


class ImageExtractorFactory():
    def _createExtractor(self, extractorType: str) -> Extractor:
        if extractorType == "imagefolder":
            return ImageFolderExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractorType} in ImageExtractorFactory")


class VideoExtractorFactory():
    def _createExtractor(self, extractorType: str) -> Extractor:
        if extractorType == "videofile":
            return VideoFileExtractor()
        elif extractorType == "s3video":
            return S3VideoExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractorType} in VideoExtractorFactory")
