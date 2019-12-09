import logging

from pipeline.pipeline import Pipeline
from pipeline.pipeline_factory import PipelineFactory

logger = logging.getLogger(__name__)


class PipelineManager:
    """Related DL pipeline runner from queues"""
    DEFAULT_PIPELINE_NAME = "three_model"

    def __init__(self):
        self.pipeline_factory = PipelineFactory()
        self._current_pipeline: Pipeline
        self.set_pipeline(self.pipeline_factory.create_pipeline(self.DEFAULT_PIPELINE_NAME))

    def set_pipeline(self, pipeline: Pipeline):
        self._current_pipeline = pipeline

    def run(self, pipeline_input_queue, pipeline_output_queue):
        while True:
            print("*******Pipeline Manager Waiting an item to run*******")
            request = pipeline_input_queue.get()
            print("-------Pipeline Manager is running---------")
            self._current_pipeline = self.pipeline_factory.create_pipeline(request.analyse_type, self._current_pipeline)
            self._current_pipeline.start(request)
            print("pipeline finished")
            response = request.generate_response()
            print("response  generated")
            pipeline_output_queue.put(response)
            print("queue putted")
