import os
from abc import ABC

from config import Config


class Resource(ABC):
    """Abstract class for defining image/video sources"""

    def __init__(self, source_path=None):
        self.source_path = source_path


class VideoFileResource(Resource):
    """Video Sources which consist of video file path and time interval"""

    def __init__(self, video_path, time_interval):
        super().__init__(source_path=video_path)
        self.time_interval = time_interval


class S3VideoResource(Resource):
    """
    S3Video Sources which consist of video file path from S3 and time interval.
    S3Bucket can be mounted on local disk file as a normal disk or can be streamed with using boto3 library.
    This implementation accept that S3bucket mounted as an external disk on file system.
    """

    def __init__(self, video_path, time_interval):
        s3_mount_dir = Config().get_app_config().get('s3bucket').get('mountDirPath')
        video_path = os.path.join(s3_mount_dir, video_path)  # TODO
        super().__init__(source_path=video_path)
        self.time_interval = time_interval


class ImageFolderResource(Resource):
    """Image Folder Resource which consist of image Folder path and read images in this folder"""

    def __init__(self, source_path):
        super().__init__(source_path=source_path)
