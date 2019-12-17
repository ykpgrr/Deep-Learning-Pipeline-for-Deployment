import logging
import os

from flask import Flask, jsonify, abort, request
from gevent.pywsgi import WSGIServer

from server.common import JobStatus
from server.request.cs550_request import Cs550Request

logger = logging.getLogger(__name__)
FLASK_CONFIG_PATH = os.getenv('FLASK_CONFIG_PATH', '../flask.cfg')


class RequestServer:
    def __init__(self, request_queue):
        self.app = Flask(__name__)
        self.app.config.from_pyfile(FLASK_CONFIG_PATH)
        self.SECRET_KEY = self.app.config['SECRET_KEY']
        self.SECRET_KEY_KEY = self.app.config['SECRET_KEY_KEY']
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/cs550_request',
                              'cs550_request',
                              self.cs550_request,
                              methods=['POST'])
        self.__request_queue = request_queue

    def _secret_key_check(self, req):
        return
        """
        if not (self.SECRET_KEY_KEY in req.headers) or req.headers.get(self.SECRET_KEY_KEY) != self.SECRET_KEY:
            logger.error(f"The request doesn't have correct SECRET_KEY. requestId:{req.json['requestId']}")
            abort(401, {"requestId": req.json["requestId"], "message": 'authentication failed'})
        """

    def index(self):
        return jsonify({
            'status': 'active',
            'DL': 'Example Deeplearning Service'
        })

    def cs550_request(self):
        """From Backend to deeplearning service"""

        if not request.json or 'requestId' not in request.json:
            logger.error("The request is not correct or there is no requestId in request at 'cs550_request'.")
            abort(400, {
                "requestId": None,
                "message": "Bad Request"
            })

        self._secret_key_check(request)

        try:
            cs550_request = Cs550Request.from_dict(request.json)
            self.__request_queue.put(cs550_request)
            response = {"requestId": request.json["requestId"],
                        "message": "successful",
                        "jobStatus": cs550_request.status.name}
        except:
            logger.exception(
                f"The request is not correct in cs550_post_request. requestId:{request.json['requestId']}")
            abort(400, {"requestId": request.json["requestId"],
                        "message": "Bad Request",
                        "jobStatus": JobStatus.Failed.name})

        return jsonify(response), 201

    def run(self):
        # self.app.run(host=self.app.config['HOST'], port=self.app.config['PORT'])
        # Serve the app with gevent
        http_server = WSGIServer((self.app.config['HOST'], self.app.config['PORT']), self.app)
        http_server.serve_forever()
