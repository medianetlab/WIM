# -*- coding: utf-8 -*-

"""
Module that implements the resources /node and /nodes for the nbi
"""

from flask_restful import Resource


class NodeApi(Resource):
    """
    The resource for the /node api
    """

    # Create the parser with all the required data

    def get(self, _id):
        """
        Find the node from the database based on the id and return it
        If not found, return 404 error
        """
        return f"Get /node/{_id}", 200

    def post(self, _id):
        """
        Create a new node and store it in the database
        """
        return f"Post /node/{_id}", 201

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
