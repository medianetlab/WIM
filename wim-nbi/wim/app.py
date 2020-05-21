from flask import Flask, g
from flask_restful import Api

from wim.resources.nodes import NodeApi, NodeListApi
from wim.resources.servers import ServerApi, ServerListApi
from wim.resources.slices import SliceApi, SliceListApi


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
    api.add_resource(ServerApi, "/server/<string:_id>")
    api.add_resource(ServerListApi, "/servers")
    api.add_resource(SliceApi, "/slice/<string:_id>")
    api.add_resource(SliceListApi, "/slices")

    # Close the neo4j db connection
    @app.teardown_appcontext
    def close_neo4j(error):
        if hasattr(g, "neo4j_db"):
            g.neo4j_db.close()

    return app
