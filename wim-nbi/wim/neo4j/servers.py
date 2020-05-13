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
            tx = session.begin_transaction()
            if tx.run("MATCH (s:servers {id: $sid}) RETURN s", sid=server["_id"]).single():
                tx.commit()
                return 0
            else:
                self._add_server(tx, server)
                for dest, link in server["links"].items():
                    if self._check_if_node_exists(tx, dest):
                        # Add the link to the existing node
                        self._add_link(tx, server["_id"], dest, link)
                tx.commit()
                return 201

    def get_server(self, server_id):
        """
        Gets a server and all the connections
        """
        with self._driver.session() as session:
            tx = session.begin_transaction()
            server = tx.run("MATCH (s:servers {id: $sid}) RETURN s", sid=server_id).single()
            if not server:
                tx.commit()
                return None
            else:
                result = dict(server.value())
                logger.debug(result)
                result["links"] = self._get_server_link(tx, server_id)
                return result

    def get_all_servers(self):
        """
        Return a list with all the servers
        """
        with self._driver.session() as session:
            tx = session.begin_transaction()
            server_list = list(tx.run("MATCH (s:servers) RETURN s"))
            return [self.get_server(node.value()["id"]) for node in server_list]

    def update_server(self, server_id, server):
        """
        Update a server
        """
        with self._driver.session() as session:
            tx = session.begin_transaction()
            if not self._update_server_params(tx, server_id, server):
                tx.commit()
                return None
            else:
                # Update the links
                # Delete the links
                tx.run("MATCH (s:servers {id: $sid}) -[c]- (n:nodes) DELETE c", sid=server_id)
                for dest, link in server["links"].items():
                    if self._check_if_node_exists(tx, dest):
                        # Add the link to the existing node
                        self._add_link(tx, server_id, dest, link)
                tx.commit()
                return 200

    def delete_server(self, server_id):
        """
        Delete a server
        """
        with self._driver.session() as session:
            tx = session.begin_transaction()
            result = tx.run(
                "MATCH (s:servers {id: $sid}) DETACH DELETE s RETURN s", sid=server_id
            ).single()
            tx.commit()
            return result

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
    def _add_link(tx, src_id, dst_id, link):
        tx.run(
            "MATCH (a:servers), (b:nodes) WHERE a.id = $src_id AND b.id = $dst_id"
            " CREATE (a)-[c:connected {src_port: $src_port, dst_port: $dst_port}]->(b)",
            src_id=src_id,
            dst_id=dst_id,
            src_port=link["src_port"],
            dst_port=link["dst_port"],
        )

    @staticmethod
    def _get_server_link(tx, sid):
        link_list = list(
            tx.run("MATCH (s:servers {id: $sid}) -[c]- (d:nodes) RETURN d, c", sid=sid)
        )
        return {dest["id"]: dict(link) for dest, link in [tuple(c) for c in link_list]}

    @staticmethod
    def _update_server_params(tx, sid, server):
        return tx.run(
            "MATCH (s:servers {id: $sid}) SET s = {id: $sid, type: $type, location: $location} "
            "RETURN s",
            sid=sid,
            type=server["type"],
            location=server["location"],
        ).single()
