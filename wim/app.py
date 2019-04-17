from flask import Flask
from wim.api.sbi import SdnView
from wim.api.nbi import SmView

def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    SdnView.register(app, trailing_slash=False)
    SmView.register(app, trailing_slash=False)

    return app