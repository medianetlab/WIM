#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Module that the base WIM manager process. It creates a KAFKA consumer
"""

import logging

from wim.utils.kafkaUtils import create_consumer, create_topic
from wim.utils.sliceUtils import create_slice

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def start_manager():
    """
    Creates and starts the KAFKA consumer
    """
    # Create the topic
    create_topic("slice")

    # Create the consumer
    consumer = create_consumer("slice")

    # Wait for messages
    for message in consumer:
        if message.value["action"] == "Create":
            create_slice()


if __name__ == "__main__":
    start_manager()
