import threading

from manager.pipeline.pipeline import Model3Pipeline

if __name__ == '__main__':
    p = Model3Pipeline("asd")

    web_thread = threading.Thread(target=p.preprocess1_run, args=())
    web_thread.start()

    response_thread = threading.Thread(target=p.prediction_generator, args=())
    response_thread.start()

    model_thread = threading.Thread(target=p.model1_run)
    model_thread.start()

