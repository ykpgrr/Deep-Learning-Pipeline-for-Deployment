import logging
import time
from .basemodel import BaseModel

logger = logging.getLogger(__name__)
"""
Concrete Components implement various functionality. They don't depend on other
components. They also don't depend on any concrete mediator classes.
"""


class Model1(BaseModel):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Model 1 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and counter != 0:
                counter = 0
                print("model1complete")
                self.mediator.notify(self, "Model1Completed")
                break
            frame = self.input_queue.get()
            result = self.predict(frame)
            time.sleep(0.1)
            counter = counter + 1
            self.output_queue.put(result)

    def predict(self, frame):
        print("running model1")
        return "a"


class Model2(BaseModel):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Model 2 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and counter != 0:
                counter = 0
                print("model2complete")
                self.mediator.notify(self, "Model2Completed")
                break
            frame = self.input_queue.get()
            result = self.predict(frame)
            time.sleep(0.1)
            counter = counter + 1
            self.output_queue.put(result)

    def predict(self, frame):
        print("running model2")
        return "a"


class Model3(BaseModel):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Model 3 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and counter != 0:
                counter = 0
                print("model3complete")
                self.mediator.notify(self, "Model3Completed")
                break
            frame = self.input_queue.get()
            result = self.predict(frame)
            time.sleep(0.1)
            counter = counter + 1
            self.output_queue.put(result)

    def predict(self, frame):
        print("running model3")
        return "a"
