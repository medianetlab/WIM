import os
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


class NodesNeo4j:
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
                for link in node["links"].values():
                    if self._check_if_node_exists(tx, link["dest"]):
                        # Add the link to the existing node
                        self._add_link(tx, node["_id"], link["dest"], link["weight"])
            tx.commit()

    @staticmethod
    def _add_node(tx, node):
        tx.run(
            "CREATE (a:nodes {id: $nid, type: $type, location: $location})",
            nid=node["_id"],
            type=node["type"],
            location=node["location"],
        )

    @staticmethod
    def _check_if_node_exists(tx, node_id):
        return tx.run("MATCH (n:nodes) WHERE n.id = $nid RETURN n", nid=node_id).single()

    @staticmethod
    def _add_link(tx, src_id, dst_id, weight):
        tx.run(
            "MATCH (a:nodes), (b:nodes) WHERE a.id = $src_id AND b.id = $dst_id"
            " CREATE (a)-[c:connected {weight: $weight}]->(b)",
            src_id=src_id,
            dst_id=dst_id,
            weight=weight,
        )
