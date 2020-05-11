# -*- coding: utf-8 -*-

"""
Module that implements the resources /node and /nodes for the nbi
"""

from wim.db import mongoUtils


class NodeModel:
    """
    Modeling the node elements as they enter the database
    """

    def __init__(self, _id, type, ports, model=None, location=None, description=None):
        self._id = _id
        self.ports = ports
        self._type = type
        self.model = model
        self.location = location
        self.description = description

    def store_to_db(self):
        """
        Store an Nodes object in the database
        """
        try:
            store = mongoUtils.add("nodes", self.json())
        except mongoUtils.dub_error:
            return None
        else:
            return store

    def json(self):
        """
        Return a JSON object of the Node
        """
        return {
            "_id": self._id,
            "type": self._type,
            "ports": self.ports,
            "model": self.model,
            "location": self.location,
            "description": self.description,
        }

    def __str__(self) -> str:
        """
        Return a print string
        """
        return str(self.json())

    @classmethod
    def find_from_id(cls, _id):
        """
        Find the Node with the given id from the DB and return the object
        If not found return None
        """
        node_data = mongoUtils.get("nodes", _id)
        return cls(**node_data) if node_data else None


class NodeListModel:
    """
    Modeling the list of node elements
    """

    @staticmethod
    def get_list():
        """
        Get the list of Node elements from the database and return it
        """
        pass
