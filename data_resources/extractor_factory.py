import logging
from abc import ABC, abstractmethod

from .extractors import Extractor, ImageFolderExtractor, VideoExtractor, S3VideoExtractor

logger = logging.getLogger(__name__)


class ExtractorFactory(ABC):
    """
    The ExtractorFactory class declares the factory method that is supposed to return an
    object of a Extractor class. The ExtractorFactory's subclasses usually provide the
    implementation of this create_extractor method.
    """

    @abstractmethod
    def create_extractor(self, extractor_type: str):
        pass


class ImageExtractorFactory(ExtractorFactory):
    def create_extractor(self, extractor_type: str) -> Extractor:
        if extractor_type == "Local":
            return ImageFolderExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractor_type} in ImageExtractorFactory")


class VideoExtractorFactory(ExtractorFactory):
    def create_extractor(self, extractor_type: str) -> Extractor:
        if extractor_type == "Local":
            return VideoExtractor()
        elif extractor_type == "S3":
            return S3VideoExtractor()
        else:
            logger.error(f"There is no Extractor type like : {extractor_type} in VideoExtractorFactory")
