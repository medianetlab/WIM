# -*- coding: utf-8 -*-

"""
Module that implements the functions for the interaction with the neo4j db from the /server API
"""

import logging
from wim.neo4j.base import BaseNeo4j


# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class ServersNeo4j(BaseNeo4j):
    """
    Class that models the neo4j functionalities
    """

    def add_server(self, server):
        """
        Creates the connection and adds the server to the graph db if it doesn't exists
        """
        with self._driver.session() as session:
            # Create the session
            tx = session.begin_transaction()
            # Create the server
            self._add_server(tx, server)
            for link in server["links"].values():
                if self._check_if_node_exists(tx, link["dest"]):
                    # Add the link to the existing node
                    self._add_link(tx, server["_id"], link["dest"])
            tx.commit()

    @staticmethod
    def _add_server(tx, server):
        tx.run(
            "CREATE (a:servers {id: $nid, type: $type, location: $location})",
            nid=server["_id"],
            type=server["type"],
            location=server["location"],
        )

    @staticmethod
    def _check_if_node_exists(tx, node_id):
        return tx.run("MATCH (n:nodes) WHERE n.id = $nid RETURN n", nid=node_id).single()

    @staticmethod
    def _add_link(tx, src_id, dst_id):
        tx.run(
            "MATCH (a:servers), (b:nodes) WHERE a.id = $src_id AND b.id = $dst_id"
            " CREATE (a)-[c:connected]->(b)",
            src_id=src_id,
            dst_id=dst_id,
        )
