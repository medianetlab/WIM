# -*- coding: utf-8 -*-

"""
Module that defines the wim manager slice functions
"""

import logging

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
    # Get the slice Components
    components = [ins["vim"] for ins in slice_data.get("extra_ns", [])]
    for connection in slice_data["core_connections"]:
        core = connection["core"]
        core_vims = [ins["vim"] for ins in core.get("ns", [])]
        core_pnf = [ipnf["pnf-id"] for ipnf in core.get("pnf", [])]
        radio = connection["radio"]
        radio_vims = [ins["vim"] for ins in radio.get("ns", [])]
        radio_pnf = [ipnf["pnf-id"] for ipnf in radio.get("pnf", [])]
        components = set(core_vims + core_pnf + radio_vims + radio_pnf + components)

    logger.debug(f"Core: {components}")
    # Create the slice connections
    connections = []
    while True:
        try:
            base_comp = components.pop()
        except KeyError:
            break
        for i in components:
            connections.append((base_comp, i))

    logger.debug(connections)
