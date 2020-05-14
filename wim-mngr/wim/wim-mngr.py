#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
Module that the base WIM manager process. It creates a KAFKA consumer
"""

import logging
import time

from kafka import KafkaConsumer


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
    logger.debug("WIM MANAGER HERE")
    time.sleep(360)


if __name__ == "__main__":
    start_manager()
