import logging

from pipeline.pipeline_factory import PipelineFactory

logger = logging.getLogger(__name__)


class PipelineManager:
    """Related DL pipeline runner from queues"""
    DEFAULT_PIPELINE = "three_model"

    def __init__(self):
        self.pipeline_factory = PipelineFactory()
        self._current_pipeline = self.pipeline_factory.create_pipeline(self.DEFAULT_PIPELINE)  # TODO

    @property
    def current_pipeline(self):
        return self._current_pipeline

    @current_pipeline.setter
    def current_pipeline(self, pipeline):
        self._current_pipeline = pipeline

    def run(self, pipeline_input_queue, pipeline_output_queue):
        while True:
            print("*******Pipeline Manager Waiting an item to run*******")
            request = pipeline_input_queue.get()
            print("-------Pipeline Manager is running---------")
            self.current_pipeline = self.pipeline_factory.create_pipeline(request.analyse_type, self._current_pipeline)
            self.current_pipeline.start(request)
            response = request.generate_response()
            pipeline_output_queue.put(response)
