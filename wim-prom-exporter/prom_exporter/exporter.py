#!/usr/bin/env python3

"""
Read the collected metrics and expose them to Prometheus
"""

import logging

from prom_exporter.utils.kafkaUtils import create_consumer, create_topic
from prometheus_client import Gauge, start_http_server

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
    create_topic("wan-slice")

    # Create the consumer
    consumer = create_consumer("wan-monitoring")

    # Wait for messages
    for message in consumer:
        slice_data = message.value["slice_data"]
        if message.value["action"] == "create":
            logger.debug(f"New slice {slice_data}")
        elif message.value["action"] == "terminate":
            logger.debug(f"Del slice {slice_data}")


if __name__ == "__main__":
    start_manager()
