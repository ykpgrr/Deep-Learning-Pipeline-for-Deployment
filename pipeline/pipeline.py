from abc import ABC, abstractmethod

class Pipeline(ABC):
    """ Request base class"""

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self, pipeline_input_queue, pipeline_output_queue):
        pass
