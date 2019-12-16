import logging

from .pipeline import Pipeline
from .three_model.pipeline import Model3Pipeline
from .two_model.pipeline import Model2Pipeline

logger = logging.getLogger(__name__)


class PipelineFactory:
    """
    The PipelineFactory class is designed as simple factory pattern that is supposed to return an
    object of a 'Pipeline' class.
    """

    def create_pipeline(self, pipeline_type: str, current_pipeline: Pipeline = None) -> Pipeline:
        """
        Creating a Pipeline object which consist of DL and Preprocess models and return it.
        :param pipeline_type: Which pipeline is wanted to be used
        :param current_pipeline: If there is a running pipeline, the requested pipeline and running pipeline may same,
        if it's same do not create new pipeline object
        :return: A 'Pipeline' object which consist of DL and Preprocess models.
        """
        if current_pipeline is not None and pipeline_type == current_pipeline.name:
            return current_pipeline
        elif pipeline_type == "three_model":
            return self._create_model3_pipeline()
        elif pipeline_type == "two_model":
            return self._create_model2_pipeline()
        else:
            raise ValueError(pipeline_type)

    def _create_model3_pipeline(self):
        pipeline = Model3Pipeline()
        pipeline.prepare()
        return pipeline

    def _create_model2_pipeline(self):
        pipeline = Model2Pipeline()
        pipeline.prepare()
        return pipeline
