# -*- coding: utf-8 -*-

"""
Module that defines the wim manager slice functions
"""

import logging
import subprocess

from wim.utils import mongoUtils

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def create_slice(slice_data):
    """
    Creates the WAN Slice between the endpoints
    """
    logger.info("Creating WAN Slice")
    # Add the slice to the database
    mongoUtils.add("slice", slice_data)
    logger.info(slice_data)
    # Get the slices SLAs
    sla = slice_data["slice_sla"]
    # Get the probes
    probes = slice_data.get("probes", [])
    # Get the slice Components
    components = [ins["vim"] for ins in slice_data.get("extra_ns", [])] + probes
    for connection in slice_data["core_connections"]:
        core = connection["core"]
        core_vims = [ins["vim"] for ins in core.get("ns", [])]
        core_pnf = [ipnf["pnf-id"] for ipnf in core.get("pnf", [])]
        radio = connection["radio"]
        radio_vims = [ins["vim"] for ins in radio.get("ns", [])]
        radio_pnf = [ipnf["pnf-id"] for ipnf in radio.get("pnf", [])]
        components = set(core_vims + core_pnf + radio_vims + radio_pnf + components)

    # Create the slice connections
    connections = []
    while True:
        try:
            base_comp = components.pop()
        except KeyError:
            break
        for i in components:
            connections.append({"endpoints": (base_comp, i)})

    # TODO: Calculate the qos level based on SLA

    # Find the rules to be created
    rules_list = []
    for conn in connections:
        endpoints = conn["endpoints"]
        rule = mongoUtils.find("rules", {"source": endpoints[0], "dest": endpoints[1]})
        if not rule:
            logger.warning(f"Didn't find connection rule from {endpoints[0]} to {endpoints[1]}")
            continue
        rule_file1 = rule["rule"]
        # Other way
        rule = mongoUtils.find("rules", {"source": endpoints[1], "dest": endpoints[0]})
        if not rule:
            logger.warning(f"Didn't find connection rule from {endpoints[1]} to {endpoints[0]}")
            continue
        rule_file2 = rule["rule"]
        logger.debug(f"Creating connection from {endpoints[0]} to {endpoints[1]}")
        subprocess.run(["bash", f"wim/rules/{rule_file1}", "create"])
        logger.debug(f"Creating rule from {endpoints[1]} to {endpoints[0]}")
        subprocess.run(["bash", f"wim/rules/{rule_file2}", "create"])
        rules_list += [rule_file1, rule_file2]
        conn["rules"] = (rule_file1, rule_file2)
    slice_data["connections"] = connections
    mongoUtils.update("slice", slice_data["_id"], slice_data)


def delete_slice(slice_id):
    """
    Deletes the WAN Slice between the endpoints
    """
    logger.debug(f"Terminating WAN Slice {slice_id}")
    slice_data = mongoUtils.get("slice", slice_id)
    for conn in slice_data["connections"]:
        try:
            rules = conn["rules"]
        except KeyError:
            logger.debug(f"Skipping {conn}")
            continue
        subprocess.run(["bash", f"wim/rules/{rules[0]}", "delete"])
        subprocess.run(["bash", f"wim/rules/{rules[1]}", "delete"])

    mongoUtils.delete("slice", slice_id)
