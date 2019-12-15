import logging
import os
import threading
from logging.handlers import TimedRotatingFileHandler
from queue import Queue

from pyhocon import ConfigFactory

from pipeline.three_model.pipeline import Model3Pipeline
from manager.response_manager import ResponseManager
from server.request_server import RequestServer

APP_CONFIG_PATH = os.getenv('APP_CONFIG_PATH', 'app.conf')
app_config = ConfigFactory.parse_file(APP_CONFIG_PATH)
response_server_config = app_config['response_server']

# Set the Log Directory
DEFAULT_LOG_DIR_PATH = 'logs'
if not os.path.exists(DEFAULT_LOG_DIR_PATH):
    os.makedirs(DEFAULT_LOG_DIR_PATH)
filename = os.path.join(DEFAULT_LOG_DIR_PATH, 'log')

# Set the logger configurations
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
file_handler = TimedRotatingFileHandler(filename=filename, when='MIDNIGHT', backupCount=10)
file_handler.setFormatter(FORMATTER)

# Set the logger configuration on the root module (make default configuration)
logger = logging.getLogger()
logger.addHandler(file_handler)

# Set Logger Level
logger.setLevel(logging.DEBUG)


def start_request_server(request_queue):
    flask_server = RequestServer(request_queue)
    flask_server.run_server()


def start_pipeline(pipeline_input_queue, pipeline_output_queue):
    pipeline = Model3Pipeline()
    pipeline.prepare()
    pipeline.start(pipeline_input_queue, pipeline_output_queue)


def start_response_server(response_queue):
    response_server = ResponseManager(url_cs550_post=response_server_config["urlComparison"],
                                      secret_key=response_server_config["SECRET_KEY"],
                                      secret_key_key=response_server_config["SECRET_KEY_KEY"],
                                      interval=response_server_config.get_int('messageInterval'),
                                      timeout=response_server_config.get_int('httpTimeOut'),
                                      max_http_retries=response_server_config.get_int('httpRetry')
                                      )
    response_server.run(response_queue)


if __name__ == '__main__':
    request_queue = Queue()
    response_queue = Queue()

    request_thread = threading.Thread(target=start_request_server, args=(request_queue,))
    request_thread.start()

    pipeline_thread = threading.Thread(target=start_pipeline, args=(request_queue, response_queue,))
    pipeline_thread.start()

    response_thread = threading.Thread(target=start_response_server, args=(response_queue,))
    response_thread.start()
