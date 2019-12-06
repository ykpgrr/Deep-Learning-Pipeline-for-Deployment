import threading

from pipeline.three_model.pipeline import Model3Pipeline

if __name__ == '__main__':
    p = Model3Pipeline()
    p.prepare()

    web_thread = threading.Thread(target=p._preprocess_models_run, args=())
    web_thread.start()

    response_thread = threading.Thread(target=p._source_extractor_run, args=())
    response_thread.start()

    model_thread = threading.Thread(target=p._deeplearning_models_run)
    model_thread.start()


