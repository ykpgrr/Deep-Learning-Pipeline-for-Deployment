import datetime


class FailedResponse:
    def __init__(self, response, retries_left=2, retry_interval_in_millis=60000):
        self.retries_left = retries_left
        self.response = response
        self.last_tried = datetime.datetime.now().timestamp()
        self.retry_interval_in_millis = retry_interval_in_millis

    def decrease_retry_count(self):
        self.last_tried = datetime.datetime.now().timestamp()
        self.retries_left -= 1

    def is_ok_to_retry(self):
        now = datetime.datetime.now().timestamp()
        time_passed = int((now - self.last_tried) * 1000.)
        return time_passed > self.retry_interval_in_millis
