# -*- coding: utf-8 -*-

"""
Module that implements the resources /node and /nodes for the nbi
"""

import logging

from wim.db import mongoUtils


# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


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
