import logging

from models.deeplearning_models import Model1, Model2, Model3
from models.preprocess_models import Preprocess1, Preprocess2, Preprocess3
from pipeline.mediator import Mediator

logger = logging.getLogger(__name__)


class PipelineModel3Mediator(Mediator):
    def __init__(self, model1: Model1, model2: Model2, model3: Model3,
                 preprocess1: Preprocess1, preprocess2: Preprocess2, preprocess3: Preprocess3) -> None:
        self._model1 = model1
        self._model1.mediator = self
        self._model2 = model2
        self._model2.mediator = self
        self._model3 = model3
        self._model3.mediator = self

        self._preprocess1 = preprocess1
        self._preprocess1.mediator = self
        self._preprocess2 = preprocess2
        self._preprocess2.mediator = self
        self._preprocess3 = preprocess3
        self._preprocess3.mediator = self

    def notify(self, sender: object, event: str) -> None:
        if event == "Model1Completed":
            logger.info("PipelineMediator reacts 'Model1Completed' and triggers the Model2")
            self._model2.run()
        elif event == "Model2Completed":
            logger.info("PipelineMediator reacts 'Model2Completed' and triggers the Model3")
            self._model3.run()
        elif event == "Model3Completed":
            logger.info("PipelineMediator reacts 'Model3Completed' and triggers the responseServer")
        elif event == "Preprocess1Completed":
            logger.info("PipelineMediator reacts 'Preprocess1Completed' and triggers the Model2")
            self._preprocess2.run()
        elif event == "Preprocess2Completed":
            logger.info("PipelineMediator reacts 'Preprocess2Completed' and triggers the Model3")
            self._preprocess3.run()
        elif event == "Preprocess3Completed":
            logger.info("PipelineMediator reacts 'Preprocess3Completed' and triggers the responseServer")
