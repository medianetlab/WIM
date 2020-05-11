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

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    def commit_add_node(self, node):
        with self._driver.session() as session:
            resutl = session.write_transaction(self._add_node, node)
            logger.debug(resutl)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run(
            "CREATE (a:Greeting) "
            "SET a.message = $message "
            "RETURN a.message + ', from node ' + id(a)",
            message=message,
        )
        return result.single()[0]

    @staticmethod
    def _add_node(tx, node):
        query = (
            f"CREATE ({node['_id']}:node "
            + "{type: "
            + node["type"]
            + ", location: "
            + node["location"]
            + "})"
        )
        logger.debug(query)
        tx.run(
            "CREATE (a:node {id: $nid, type: $type, location: $location})",
            nid=node["_id"],
            type=node["type"],
            location=node["location"],
        )
