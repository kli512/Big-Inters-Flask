import os

from flask import Flask

import logging

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/hello')
    def hello():
        return 'Hello world'

    from BigInters import MainApp
    app.register_blueprint(MainApp.bp)

    return app
