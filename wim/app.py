from flask import Flask

# APIs
from wim.api.sbi import SdnView
from wim.api.nbi import SmView
from wim.api.nbi import TestView

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

    # Config files
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    # Register the api calls
    SdnView.register(app, trailing_slash=False)
    SmView.register(app, trailing_slash=False)
    TestView.register(app, trailing_slash=False)

    # Initiate the db
    # Switch db 
    # mongoUtils.col_insert('switch_col', switches)
    # print (mongoUtils.create_index('switch_col',['dpname', 'dpid']), flush=True)
    # result = mongoUtils.index_col('switch_col')
    # for i in result:
    #     print (i, flush = True)

    return app