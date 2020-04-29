import os

from flask import Flask
from flask_cors import CORS

import logging

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    @app.route('/hello')
    def hello():
        return 'Hello world'

    from BigInters import MainApp
    app.register_blueprint(MainApp.bp)

    return app
