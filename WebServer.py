import logging
import os

from flask import Flask, jsonify
from gevent.pywsgi import WSGIServer

logger = logging.getLogger(__name__)
FLASK_CONFIG_PATH = os.getenv('FLASK_CONFIG_PATH', 'flask.cfg')


class WebServer:
    def __init__(self, queue, result_queue):
        self.app = Flask(__name__)
        self.app.config.from_pyfile(FLASK_CONFIG_PATH)
        self.SECRET_KEY = self.app.config['SECRET_KEY']
        self.SECRET_KEY_KEY = self.app.config['SECRET_KEY_KEY']
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/cs550_request',
                              'cs550_request',
                              self.cs550_request,
                              methods=['POST'])

    def index(self):
        return jsonify({
            'status': 'active',
            'DL': 'Example Deeplearning Service'
        })

    # TODO
    def cs550_request(self):
        """From Backend to deeplearning service"""
        pass

    def run_server(self):
        # self.app.run(host=self.app.config['HOST'], port=self.app.config['PORT'])
        # Serve the app with gevent
        http_server = WSGIServer((self.app.config['HOST'], self.app.config['PORT']), self.app)
        http_server.serve_forever()
