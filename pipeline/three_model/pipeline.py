import threading
from queue import Queue
import time
from pipeline.pipeline import Pipeline
from models.deeplearning_models import Model1, Model2, Model3
from .mediator import PipelineModel3Mediator
from models.preprocess_models import Preprocess1, Preprocess2, Preprocess3


class Model3Pipeline(Pipeline):
    """Defines a pose estimation pipeline that extracts images from resources and gives pose estimation results
    pipeline consists of 3 major components:
    extractor that is an instance of Extractor class that can extract images or sequence of images from a Resource
    detector that detects the bounding boxes of humans
    pose estimator that extracts the human poses for given bounding boxes
    """

    def __init__(self):
        pass

    def prepare(self):
        self._create_queues()
        self._create_models()
        # self._prepare_deep_learning_models() # to initialize models on GPU

    def _create_queues(self):
        self.time_ref_queue = Queue()

        self.orig_input_queue_for_p1 = Queue()
        self.orig_input_queue_for_p2 = Queue()
        self.orig_input_queue_for_p3 = Queue()

        self.model1_input_queue = Queue()
        self.model2_input_queue = Queue()
        self.model3_input_queue = Queue()

        self.model1_output_queue = Queue()
        self.model2_output_queue = Queue()
        self.model3_output_queue = Queue()

        self.preprocess1_input_queue = self.orig_input_queue_for_p1
        self.preprocess2_input_queue = self.model1_output_queue
        self.preprocess3_input_queue = self.model2_output_queue

        self.preprocess1_output_queue = self.model1_input_queue
        self.preprocess2_output_queue = self.model2_input_queue
        self.preprocess3_output_queue = self.model3_input_queue

    def _create_models(self):
        self.preprocess1 = Preprocess1(self.preprocess1_input_queue, self.preprocess1_output_queue)
        self.preprocess2 = Preprocess2(self.orig_input_queue_for_p2, self.preprocess2_input_queue,
                                       self.preprocess2_output_queue)
        self.preprocess3 = Preprocess3(self.orig_input_queue_for_p3, self.preprocess3_input_queue,
                                       self.preprocess3_output_queue)

        self.model1 = Model1(self.model1_input_queue, self.model1_output_queue)
        self.model2 = Model2(self.model2_input_queue, self.model2_output_queue)
        self.model3 = Model3(self.model3_input_queue, self.model3_output_queue)

        self.pipeline_model3_mediator = PipelineModel3Mediator(self.model1, self.model2, self.model3, self.preprocess1,
                                                               self.preprocess2, self.preprocess3)

    def _preprocess_models_run(self):
        print("Preprocess models started to run")
        self.preprocess1.run()

    def _deeplearning_models_run(self):
        print("Deep Learning models started to run")
        self.model1.run()

    def _source_extractor_run(self, extractor, resource):
        print("prediction_generator_run")
        """returns a generator that contains prediction results"""
        for frame, time_ref in extractor.extract(resource):
            print("---adding frame ---")
            self.orig_input_queue_for_p1.put(frame)
            self.orig_input_queue_for_p2.put(frame)
            self.orig_input_queue_for_p3.put(frame)
            self.time_ref_queue.put(time_ref)

    def start(self, pipeline_input_queue, pipeline_output_queue):
        while True:
            print("*******pipeline Waiting an item to run*******")
            request = pipeline_input_queue.get()
            print("-------pipeline is running---------")
            generator_thread = threading.Thread(target=self._source_extractor_run,
                                                args=(request.extractor, request.resource,))
            generator_thread.start()

            time.sleep(1)
            preprocess_thread = threading.Thread(target=self._preprocess_models_run, args=())
            preprocess_thread.start()

            model_thread = threading.Thread(target=self._deeplearning_models_run)
            model_thread.start()

            model_thread.join()
            request.set_result_from_queue(self.time_ref_queue, self.model3_output_queue)
            response = request.generate_response()
            pipeline_output_queue.put(response)
