import logging

from .three_model.pipeline import Model3Pipeline
from .two_model.pipeline import Model2Pipeline

logger = logging.getLogger(__name__)


class PipelineFactory:

    def create_pipeline(self, pipeline_type: str, current_pipeline=None):
        if current_pipeline is not None and pipeline_type == current_pipeline.name:
            return current_pipeline
        elif pipeline_type == "three_model":
            pipeline = Model3Pipeline()
            pipeline.prepare()
            return pipeline
        elif pipeline_type == "two_model":
            pipeline = Model2Pipeline()
            pipeline.prepare()
            return pipeline
        else:
            raise NotImplementedError
