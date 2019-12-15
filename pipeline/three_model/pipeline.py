from queue import Queue

from models.deeplearning_models import Model2, Model3
from models.preprocess_models import Preprocess2, Preprocess3
from pipeline.pipeline import Pipeline
from .mediator import PipelineModel3Mediator


class Model3Pipeline(Pipeline):
    """Defines a analyse_type that extracts images from resources and gives DL Models results
    analyse_type consists of 3 major components:
    extractor that is an instance of Extractor class that can extract images or sequence of images from a Resource
    Models that DL model
    Preprocess that converting source appropriate form for DL Model
    """
    name = "three_model"

    def _create_queues(self):
        super()._create_queues()

        self.orig_input_queue_for_p2 = Queue()
        self.orig_input_queue_for_p3 = Queue()

        self.model2_input_queue = Queue()
        self.model3_input_queue = Queue()

        self.model2_output_queue = Queue()
        self.model3_output_queue = Queue()
        self.pipeline_output_queue = self.model3_output_queue

        self.preprocess2_input_queue = self.model1_output_queue
        self.preprocess3_input_queue = self.model2_output_queue

        self.preprocess2_output_queue = self.model2_input_queue
        self.preprocess3_output_queue = self.model3_input_queue

    def _create_models(self):
        super()._create_models()
        self.preprocess2 = Preprocess2(self.orig_input_queue_for_p2, self.preprocess2_input_queue,
                                       self.preprocess2_output_queue)
        self.preprocess3 = Preprocess3(self.orig_input_queue_for_p3, self.preprocess3_input_queue,
                                       self.preprocess3_output_queue)

        self.model2 = Model2(self.model2_input_queue, self.model2_output_queue)
        self.model3 = Model3(self.model3_input_queue, self.model3_output_queue)

        self.mediator = PipelineModel3Mediator(self.model1, self.model2, self.model3, self.preprocess1,
                                               self.preprocess2, self.preprocess3)

    def _prepare_deep_learning_models(self):
        """
        Model's weights loading on GPU
        :return: None
        """  # TODO
        pass

    def _source_extractor_run(self, extractor, resource):
        """
        Extract input step by step and put them queus
        :param extractor: Reading and extracting input source
        :param resource: Source of input
        :return:
        """
        print("source_generator_run")
        """returns a generator that contains prediction results"""
        for frame, time_ref in extractor.extract(resource):
            print("---adding frame ---")
            self.orig_input_queue_for_p1.put(frame)
            self.orig_input_queue_for_p2.put(frame)
            self.orig_input_queue_for_p3.put(frame)
            self.time_ref_queue.put(time_ref)
