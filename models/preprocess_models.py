import logging

from models.basemodel import BaseModel

logger = logging.getLogger(__name__)
"""
Concrete Components implement various functionality. They don't depend on other
components. They also don't depend on any concrete mediator classes.
"""


class Preprocess1(BaseModel):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Preprocess1 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Preprocess1Completed")
                break
            print(f"running preprocess1 counter: {counter}")
            frame = self.input_queue.get()
            result = self.preprocess(frame)
            counter = counter + 1
            self.output_queue.put(result)

    def preprocess(self, frame):
        return "Preprocess1Result"


class Preprocess2(BaseModel):
    def __init__(self, orig_queue, input_queue, output_queue):
        super().__init__()
        self.orig_queue = orig_queue
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Preprocess2 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and self.orig_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Preprocess2Completed")
                break
            print(f"running preprocess2 counter: {counter}")
            frame = self.orig_queue.get()
            frame = self.input_queue.get()
            counter = counter + 1
            result = self.preprocess(frame)
            self.output_queue.put(result)

    def preprocess(self, frame):
        return "Preprocess2Result"


class Preprocess3(BaseModel):
    def __init__(self, orig_queue, input_queue, output_queue):
        super().__init__()
        self.orig_queue = orig_queue
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self) -> None:
        logger.info("Preprocess3 is running")
        counter = 0
        while True:
            if self.input_queue.empty() and self.orig_queue.empty() and counter != 0:
                counter = 0
                self.mediator.notify(self, "Preprocess3Completed")
                break
            print(f"running preprocess3 counter: {counter}")
            frame = self.orig_queue.get()
            frame = self.input_queue.get()
            counter = counter + 1
            result = self.preprocess(frame)
            self.output_queue.put(result)

    def preprocess(self, frame):
        return "Preproces3Result"
