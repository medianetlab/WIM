from flask import Flask
from flask_restful import Api

from wim.resources.nodes import NodeApi, NodeListApi


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    # Create the Flask Application that will be returned to the gunicorn
    app = Flask(__name__, instance_relative_config=True)

    # Register the api calls
    api = Api(app=app, prefix="/api")
    api.add_resource(NodeApi, "/node/<string:_id>")
    api.add_resource(NodeListApi, "/nodes")

    return app
