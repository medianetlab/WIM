#!/usr/bin/env python

import subprocess
import logging
import os
from sys import argv, exit

from wim.utils.neo4jUtils import Neo4j
from wim.utils import mongoUtils

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# The nodes that need to be modified
NODE_LIST = [
    {
        "switch-id": "sdn-lab1",
        "script": "sdn-lab1.sh",
        "tables": [{"table-id": "1", "flows": ["genesis-normal"]}],
    },
    {
        "switch-id": "sdn-lab2",
        "script": "sdn-lab2.sh",
        "tables": [{"table-id": "25", "flows": ["ip-slow2", "ip-slow3", "ip-slow4", "ip-slow5"]}],
    },
    {
        "switch-id": "sdn-io-br0",
        "script": "sdn-io-br0.sh",
        "tables": [{"table-id": "0", "flows": ["p1to2", "p2to1"]}],
    },
    {
        "switch-id": "sdn-io-br1",
        "script": "sdn-io-br1.sh",
        "tables": [{"table-id": "0", "flows": ["p9to10", "p10to9"]}],
    },
]

# Get neo4j credentials and create db instance
neo4j_auth = os.getenv("NEO4J_AUTH")
if not neo4j_auth:
    raise ValueError("NEO4J_AUTH variable is not defined")
username, password = neo4j_auth.split("/")
db = Neo4j(uri="bolt://neo4j", user=username, password=password)

# Get the action argument
action = argv[1]

# Get the slice id argument
slice_id = argv[2]

# Go to the rules directory
os.chdir("wim/rules/mnlcloud-amar_enb-slow-bins")

for node in NODE_LIST:
    # Find the switch from neo4j db
    target = db.get_node(node["switch-id"])
    if not target:
        logger.error(f"Could not find node {node['swich-id']}")
        exit(9999)
    try:
        ctl = target["sdn_controller"]
        dpid = target["dpid"]
    except KeyError:
        logger.error(f"SDN Controller and DPID were not defined for node {node['swich-id']}")
        exit(9999)
    node["switch-dpid"] = dpid
    node["sdn-ctl"] = ctl
    subprocess.run(["bash", node["script"], "-c", ctl, "-d", dpid, action])

# Update the slice information with the created SDN flows
slice_data = mongoUtils.get("slice", slice_id)
slice_flows = slice_data.get("slice_flows", [])
if action == "create":
    new_slice_flows = slice_flows + NODE_LIST
else:
    new_slice_flows = [node for node in slice_flows if node not in NODE_LIST]
slice_data["slice_flows"] = new_slice_flows
mongoUtils.update("slice", slice_id, slice_data)
