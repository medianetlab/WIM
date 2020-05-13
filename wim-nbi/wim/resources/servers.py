# -*- coding: utf-8 -*-

"""
Module that implements the resources /server and /servers for the nbi
"""
import logging

from flask_restful import Resource, reqparse
from flask import g

# Mongo DB and models have been replaced by neo4j db
from wim.db import mongoUtils
from wim.models.servers import ServerModel
from wim.neo4j.servers import ServersNeo4j


# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


# Create the neo4j db connection
# username & password should be loaded from the env
def get_neo4j_db():
    if not hasattr(g, "neo4j_db"):
        g.neo4j_db = ServersNeo4j(uri="bolt://neo4j", user="neo4j", password="genesis")
    return g.neo4j_db


class ServerApi(Resource):
    """
    The resource for the /server api
    """

    # Create the parser with all the required data
    parser = reqparse.RequestParser()
    parser.add_argument(
        "type",
        type=str,
        required=False,
        help="Define the type of the Server (VIM, PNF)",
        choices=("VIM", "PNF"),
    )
    parser.add_argument("links", type=dict, required=True, help="Define the links of the device")
    parser.add_argument(
        "location", type=str, required=False, help="Define the location of the device"
    )
    parser.add_argument(
        "description", type=str, required=False, help="Define the description of the device"
    )

    def get(self, _id):
        """
        Find the server from the database based on the id and return it
        If not found, return 404 error
        """
        server = get_neo4j_db().get_server(_id)
        return (server, 200) if server else (f"Server {_id} was not found", 404)

    def post(self, _id):
        """
        Create a new server and store it in the database
        """
        args = self.parser.parse_args()
        args["_id"] = _id
        new_server = get_neo4j_db().add_server(args)
        return (
            (f"Created server {_id}", 201) if new_server else (f"Server {_id} already exists", 400)
        )

    def put(self, _id):
        """
        Create or update an existing server
        """
        args = self.parser.parse_args()
        if get_neo4j_db().update_server(_id, args):
            return (f"Updated server {_id}", 200)
        else:
            args["_id"] = _id
            get_neo4j_db().add_server(args)
            return (f"Created server {_id}", 201)

    def delete(self, _id):
        """
        Delete an existing server from the database
        If not found, return 404 error
        """
        if get_neo4j_db().delete_server(_id):
            return (f"Deleted server {_id}", 200)
        else:
            return (f"Server {_id} was not found", 404)


class ServerListApi(Resource):
    """
    The resource for the /servers API
    """

    def get(self):
        """
        Return a list with all the servers
        """
        return get_neo4j_db().get_all_servers(), 200
