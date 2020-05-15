# -*- coding: utf-8 -*-

"""
Module that defines the wim manager slice functions
"""

import logging

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def create_slice():
    """
    Creates the WAN Slice between the endpoints
    """
    logger.debug("Creating WAN Slice")
