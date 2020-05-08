from flask import Flask

# APIs
from wim.api.nbi import SmView

# DB elements
from wim.db.my_db import switches
from wim.db import mongoUtils


def create_app():
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    """

    # Create the Flask Application that will be returned to the gunicorn
    app = Flask(__name__, instance_relative_config=True)

    # Register the api calls
    SmView.register(app, trailing_slash=False)

    # Initiate the db
    # Switch db
    # mongoUtils.col_insert("switch_col", switches)
    # mongoUtils.create_index('switch_col',['dpname', 'dpid'])

    return app
