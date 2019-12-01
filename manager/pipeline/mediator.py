import logging
from abc import ABC

logger = logging.getLogger(__name__)


class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def notify(self, sender: object, event: str) -> None:
        pass


class Pipeline3ModelMediator(Mediator):
    def __init__(self, model1: Model1, model2: Model2, model3: Model3) -> None:
        self._model1 = model1
        self._model1.mediator = self
        self._model2 = model2
        self._model2.mediator = self
        self._model3 = model3
        self._model3.mediator = self

    def notify(self, sender: object, event: str) -> None:
        if event == "Model1Completed":
            logger.info("PipelineMediator reacts 'Model1Completed' and triggers the Model2")
            self._model2.run()
        elif event == "Model2Completed":
            logger.info("PipelineMediator reacts 'Model2Completed' and triggers the Model3")
            self._model3.run()
        elif event == "Model3Completed":
            logger.info("PipelineMediator reacts 'Model3Completed' and triggers the responseServer")
            self._model3.run()


class BaseModel:
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


"""
Concrete Components implement various functionality. They don't depend on other
components. They also don't depend on any concrete mediator classes.
"""


class Model1(BaseModel):
    def run(self, model1_input_queue, model1_output_queue) -> None:
        logger.info("Model 1 is running")
        counter = 0
        while True:
            if model1_input_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Model1Completed")
                break
            frame = model1_input_queue.get()
            result = self.predict(frame)
            counter = counter + 1
            model1_output_queue.put(result)


class Model2(BaseModel):
    def run(self, model2_input_queue, model2_output_queue) -> None:
        logger.info("Model 2 is running")
        counter = 0
        while True:
            if model2_input_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Model2Completed")
                break
            frame = model2_input_queue.get()
            result = self.predict(frame)
            model2_output_queue.put(result)


class Model3(BaseModel):
    def run(self, model3_input_queue, model3_output_queue) -> None:
        logger.info("Model 3 is running")
        counter = 0
        while True:
            if model3_input_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Model3Completed")
                break
            frame = model3_input_queue.get()
            result = self.predict(frame)
            model3_output_queue.put(result)
