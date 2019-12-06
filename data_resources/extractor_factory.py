import logging
from abc import ABC, abstractmethod

from .extractors import Extractor, ImageFolderExtractor, VideoExtractor, S3VideoExtractor

logger = logging.getLogger(__name__)


class ExtractorFactory(ABC):
    @abstractmethod
    def _create_extractor(self, extractor_type: str) -> Extractor:
        pass

    def create_extractor(self, extractor_type: str):
        """returns a generator for images"""
        # self.check_resource_type(resource)
        return self._create_extractor(extractor_type)


class ImageExtractorFactory(ExtractorFactory):
    def _create_extractor(self, extractor_type: str) -> Extractor:
        if extractor_type == "Local":
            return ImageFolderExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractor_type} in ImageExtractorFactory")


class VideoExtractorFactory(ExtractorFactory):
    def _create_extractor(self, extractor_type: str) -> Extractor:
        if extractor_type == "Local":
            return VideoExtractor()
        elif extractor_type == "S3":
            return S3VideoExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractor_type} in VideoExtractorFactory")
