from abc import ABC, abstractmethod


class Pipeline(ABC):
    """ Request base class"""

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def start(self, request):
        pass
