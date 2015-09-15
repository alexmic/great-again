# -*- coding: utf-8 -*-

from flask import Flask
from ga.views import blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('ga.settings')
    app.register_blueprint(blueprint)
    return app
