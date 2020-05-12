# -*- coding: utf-8 -*-

"""
Module that creates and closes the connection to neo4j db
"""

import logging
from neo4j import GraphDatabase, basic_auth


# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class BaseNeo4j:
    """
    Class that models the neo4j functionalities
    """

    def __init__(self, uri, user, password):
        """
        Create the database driver connection
        """
        self._driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))

    def close(self):
        """
        Run the database driver connection
        """
        self._driver.close()
