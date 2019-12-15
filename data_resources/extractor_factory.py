import logging
from abc import ABC, abstractmethod

from .extractors import Extractor, ImageFolderExtractor, VideoExtractor, S3VideoExtractor

logger = logging.getLogger(__name__)


class ExtractorFactory(ABC):
    @abstractmethod
    def _createExtractor(self, extractorType: str) -> Extractor:
        pass

    def createExtractor(self, extractorType: str):
        """returns a generator for images"""
        # self.check_resource_type(resource)
        return self._createExtractor(extractorType)


class ImageExtractorFactory(ExtractorFactory):
    def _createExtractor(self, extractorType: str) -> Extractor:
        if extractorType == "Local":
            return ImageFolderExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractorType} in ImageExtractorFactory")


class VideoExtractorFactory(ExtractorFactory):
    def _createExtractor(self, extractorType: str) -> Extractor:
        if extractorType == "Local":
            return VideoExtractor()
        elif extractorType == "S3":
            return S3VideoExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractorType} in VideoExtractorFactory")
