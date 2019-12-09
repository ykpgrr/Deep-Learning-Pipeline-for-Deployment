import threading
import time
from abc import abstractmethod
from queue import Queue

from models.deeplearning_models import Model1
from models.preprocess_models import Preprocess1
from pipeline.mediator import Mediator


class Pipeline():
    """Defines a analyse_type that extracts images from resources and gives DL Models results
    analyse_type consists of 3 major components:
    extractor that is an instance of Extractor class that can extract images or sequence of images from a Resource
    Models that DL model
    Preprocess that converting source appropriate form for DL Model
    """

    def start(self, request):
        """
        template method
        :param request: incoming request
        :return: None
        """
        print(f"|||{self.name} is running|||")  # Fixme
        generator_thread = threading.Thread(target=self._source_extractor_run,
                                            args=(request.extractor, request.resource,))
        generator_thread.start()
        time.sleep(1)

        preprocess_thread = threading.Thread(target=self._preprocess_models_run, args=())
        preprocess_thread.start()

        model_thread = threading.Thread(target=self._deeplearning_models_run)
        model_thread.start()

        model_thread.join()

        request.set_result_from_queue(self.time_ref_queue, self.pipeline_output_queue)

    def prepare(self):
        """
        template method
        :return: None
        """
        self._create_queues()
        self._create_models()
        self._prepare_deep_learning_models()  # to initialize models on GPU

    def _preprocess_models_run(self):
        print("Preprocess models started to run")
        self.preprocess1.run()

    def _deeplearning_models_run(self):
        print("Deep Learning models started to run")
        self.model1.run()

    def _create_queues(self):
        self.time_ref_queue = Queue()

        self.orig_input_queue_for_p1 = Queue()

        self.model1_input_queue = Queue()

        self.model1_output_queue = Queue()
        self.pipeline_output_queue = self.model1_output_queue

        self.preprocess1_input_queue = self.orig_input_queue_for_p1

        self.preprocess1_output_queue = self.model1_input_queue

    def _create_models(self):
        self.preprocess1 = Preprocess1(self.preprocess1_input_queue, self.preprocess1_output_queue)
        self.model1 = Model1(self.model1_input_queue, self.model1_output_queue)
        self.mediator: Mediator

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def _prepare_deep_learning_models(self):
        pass

    @abstractmethod
    def _source_extractor_run(self, extractor, resource):
        """
        Extract input step by step and put them queus
        :param extractor: Reading and extracting input source
        :param resource: Source of input
        :return:
        """
        pass
