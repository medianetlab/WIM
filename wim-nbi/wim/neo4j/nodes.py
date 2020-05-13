# -*- coding: utf-8 -*-

"""
Module that implements the functions for the interaction with the neo4j db from the /node API
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


class NodesNeo4j(BaseNeo4j):
    """
    Class that models the neo4j functionalities
    """

    def add_node(self, node):
        """
        Creates the connection and adds the Node to the graph db if it doesn't exists
        """
        with self._driver.session() as session:
            # Create the session
            tx = session.begin_transaction()
            # Check if the Node exists. If it doesn't, add it
            if not self._check_if_node_exists(tx, node["_id"]):
                self._add_node(tx, node)
                for dest, link in node["links"].items():
                    # Add the link to the existing node
                    self._add_link(tx, node["_id"], dest, link)
            tx.commit()

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
                result["links"] = self._get_node_links(tx, node_id)
                tx.commit()
                return result

    def get_all_nodes(self):
        """
        Return a list with all the nodes
        """
        with self._driver.session() as session:
            node_list = session.run("MATCH (n:nodes) RETURN n")
            return [self.get_node(node.value()["id"]) for node in node_list]

    def update_node(self, node_id, node):
        """
        Updates an existing Node
        """
        pass

    @staticmethod
    def _add_node(tx, node):
        tx.run(
            "CREATE (a:nodes {id: $nid, type: $type, location: $loc, description: $des})",
            nid=node["_id"],
            type=node["type"],
            loc=node["location"],
            des=node["description"],
        )

    @staticmethod
    def _check_if_node_exists(tx, node_id):
        return tx.run("MATCH (n:nodes) WHERE n.id = $nid RETURN n", nid=node_id).single()

    @staticmethod
    def _add_link(tx, src_id, dst_id, link):
        tx.run(
            "MATCH (a:nodes), (b:nodes) WHERE a.id = $src_id AND b.id = $dst_id"
            " CREATE (a)-[c:connected {weight: $weight,"
            " src_port: $src_port, dst_port: $dst_port}]->(b)",
            src_id=src_id,
            dst_id=dst_id,
            weight=link["weight"],
            src_port=link["src_port"],
            dst_port=link["dst_port"],
        )

    @staticmethod
    def _get_node_links(tx, node_id):
        link_list = list(
            tx.run("MATCH (a:nodes {id: $node_id}) -[c]- (d:nodes) RETURN d, c", node_id=node_id)
        )
        return {dest["id"]: dict(link) for (dest, link) in [tuple(r) for r in link_list]}
