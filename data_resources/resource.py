from abc import ABC


class Resource(ABC):
    """Abstract class for defining image/video sources"""

    def __init__(self, source_path=None):
        self.source_path = source_path


class VideoFileResource(Resource):
    def __init__(self, video_path, time_interval):
        super().__init__(source_path=video_path)
        self.time_interval = time_interval


class S3VideoResource(Resource):
    def __init__(self, video_path, time_interval):
        # video_path = os.path.join(app_config.get('s3bucket').get('mountDirPath'), video_path) #TODO
        super().__init__(source_path=video_path)
        self.time_interval = time_interval


class ImageFolderResource(Resource):
    def __init__(self, source_path):
        super().__init__(source_path=source_path)
