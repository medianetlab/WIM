# -*- coding: utf-8 -*-

"""
Module that implements the models for servers resources
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


class ServerModel:
    """
    Modeling the server elements as they enter the database
    """

    def __init__(self, _id, links, type=None, location=None, description=None):
        self._id = _id
        self.links = links
        self._type = type
        self.location = location
        self.description = description

    def store_to_db(self):
        """
        Store a server object in the database
        """
        try:
            store = mongoUtils.add("servers", self.json())
        except mongoUtils.dub_error:
            return None
        else:
            return store

    def json(self):
        """
        Return a JSON object of the server
        """
        return {
            "_id": self._id,
            "type": self._type,
            "links": self.links,
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
        Find the server with the given id from the DB and return the object
        If not found return None
        """
        server_data = mongoUtils.get("servers", _id)
        return cls(**server_data) if server_data else None
