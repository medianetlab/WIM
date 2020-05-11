# -*- coding: utf-8 -*-

"""
Module that implements the resources /node and /nodes for the nbi
"""

from flask_restful import Resource, reqparse
from wim.models.models import NodeModel, NodeListModel
from wim.db import mongoUtils


class NodeApi(Resource):
    """
    The resource for the /node api
    """

    # Create the parser with all the required data
    parser = reqparse.RequestParser()
    parser.add_argument(
        "type",
        type=str,
        required=True,
        help="Define the type of the node (SDN, Traditional)",
        choices=("SDN", "Traditional"),
    )
    parser.add_argument("ports", type=dict, required=True, help="Define the links of the device")
    parser.add_argument("model", type=str, required=False, help="Define the model of the device")
    parser.add_argument(
        "location", type=str, required=False, help="Define the location of the device"
    )
    parser.add_argument(
        "description", type=str, required=False, help="Define the description of the device"
    )

    def get(self, _id):
        """
        Find the node from the database based on the id and return it
        If not found, return 404 error
        """
        node = NodeModel.find_from_id(_id)
        return (node.json(), 200) if node else (f"Node {_id} was not found", 404)

    def post(self, _id):
        """
        Create a new node and store it in the database
        """
        args = self.parser.parse_args()
        args["_id"] = _id
        new_node = NodeModel(**args)
        store = new_node.store_to_db()
        return (f"Created node {_id}", 201) if store else (f"Node {_id} already exists", 400)

    def put(self, _id):
        """
        Create or update an existing node
        """
        return f"Put /node/{_id}", 200

    def delete(self, _id):
        """
        Delete an existing node from the database
        If not found, return 404 error
        """
        return f"Delete /node/{_id}", 200


class NodeListApi(Resource):
    """
    The resource for the /nodes API
    """

    def get(self):
        """
        Return a list with all the switches
        """
        return f"All the switches"
