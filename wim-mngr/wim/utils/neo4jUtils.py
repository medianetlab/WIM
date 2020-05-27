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


class Neo4j:
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

    def get_node(self, node_id):
        """
        Get a node and all the connections
        """
        with self._driver.session() as session:
            tx = session.begin_transaction()
            node = self._check_if_node_exists(tx, node_id)
            if not node:
                tx.commit()
                return None
            else:
                result = dict(node.value())
                tx.commit()
                return result

    @staticmethod
    def _check_if_node_exists(tx, node_id):
        return tx.run("MATCH (n:nodes) WHERE n.id = $nid RETURN n", nid=node_id).single()
