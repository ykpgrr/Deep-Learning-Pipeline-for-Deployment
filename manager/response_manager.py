import json
import logging
import time
from queue import Queue

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

from server.response.failed_response import FailedResponse

logger = logging.getLogger(__name__)


class ResponseManager:
    """Related ML result runner from queues"""

    def __init__(self, url_cs550_post,
                 secret_key,
                 secret_key_key,
                 interval=2,
                 timeout=3,
                 max_http_retries=3):
        self.__url_cs550_post = url_cs550_post
        self.__secret_key = secret_key
        self.__secret_key_key = secret_key_key
        self.interval = interval
        self.timeout = timeout
        self.headers = {'SECRET_KEY': secret_key, 'SECRET_KEY_KEY': secret_key_key}
        self.session = requests.Session()
        self.adapter = HTTPAdapter(max_retries=max_http_retries)
        self.session.mount(self.__url_cs550_post, self.adapter)
        self.error_queue = Queue()

    def cs550_post(self, response):
        failed_response = None
        try:
            if isinstance(response, FailedResponse):
                failed_response = response
                response = response.response
            request = self.session.post(self.__url_cs550_post,
                                        data=json.dumps(response),
                                        timeout=self.timeout,
                                        headers=self.headers)
            if int(request.status_code) // 200 == 1:
                logger.info(f"cs550 post is posted. requestId: {response['requestId']} ")
            elif int(request.status_code) // 500 == 1:
                logger.info(
                    f"cs550 post is not posted. Server returned 500, requestId: {response['requestId']} ")
            else:
                logger.info(f"cs550 post is not posted. requestId: {response['requestId']} ")
                self._put_response_in_error_queue(response, failed_response)
        except Timeout:
            logger.exception(f"The Analytics Request is timed out: {response['requestId']} ")
            self._put_response_in_error_queue(response, failed_response)
        except ConnectionError as ce:
            logger.info(f"Connection error: {ce} ")
            self._put_response_in_error_queue(response, failed_response)
        except Exception as error:
            logger.info(f"Undefined error in cs550_post: {error} ")

    def run(self, queue: Queue):

        while True:
            # Consume result queue
            if not queue.empty():
                try:
                    response = queue.get()
                    self.cs550_post(response)
                except Exception as exp:
                    logger.exception("There is an error when running to ResponseManager.{0}".format(str(exp)))
            self._consume_error_queue()

    def _put_response_in_error_queue(self, response, failed_response: FailedResponse = None):
        if failed_response is None:
            self.error_queue.put(FailedResponse(response))
        else:
            failed_response.decrease_retry_count()
            if failed_response.retries_left > 0:
                self.error_queue.put(failed_response)

    def _consume_error_queue(self):
        if not self.error_queue.empty():
            failed_response: FailedResponse = self.error_queue.get()
            try:
                # If enough time has been passed for a retry, try to send the message
                if failed_response.is_ok_to_retry():
                    self.cs550_post(failed_response)
                # If not, put it back to end
                else:
                    self.error_queue.put(failed_response)
                    time.sleep(0.1)
            except Exception as exp:
                logger.exception(
                    "Tried to resend a previously failed message and failed again.{0}".format(str(exp)))
                failed_response.decrease_retry_count()
                if failed_response.retries_left > 0:
                    self.error_queue.put(failed_response)
        else:
            time.sleep(self.interval)
