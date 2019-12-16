import logging
from abc import ABC, abstractmethod
from typing import Tuple

from .extractors import Extractor, ImageFolderExtractor, VideoExtractor, S3VideoExtractor
from .resource import Resource, VideoFileResource, ImageFolderResource, S3VideoResource

logger = logging.getLogger(__name__)


class ResourceFactory(ABC):
    """
    The ExtractorFactory class declares the factory method that is supposed to return an
    object of a Extractor class. The ExtractorFactory's subclasses usually provide the
    implementation of this create_extractor method.
    """

    @abstractmethod
    def _create_extractor(self, resource_type: str, path: str, time_interval):
        pass

    def create_extractor(self, resource_type: str, path, time_interval=None) -> Tuple[Extractor, Resource]:
        return self._create_extractor(resource_type, path, time_interval)


class ImageResourceFactory(ResourceFactory):
    def _create_extractor(self, resource_type: str, path: str, time_interval) -> Tuple[Extractor, Resource]:
        if resource_type == "Local":
            return ImageFolderExtractor(), ImageFolderResource(path)
        else:
            logger.error(f"There is no Extractor type like : {resource_type} in ImageExtractorFactory")
            ValueError(resource_type)


class VideoResourceFactory(ResourceFactory):
    def _create_extractor(self, resource_type: str, path: str, time_interval) -> Tuple[Extractor, Resource]:
        if resource_type == "Local":
            return VideoExtractor(), VideoFileResource(path, time_interval)
        elif resource_type == "S3":
            return S3VideoExtractor(), S3VideoResource(path, time_interval)
        else:
            logger.error(f"There is no Extractor type like : {resource_type} in VideoExtractorFactory")
            ValueError(resource_type)
