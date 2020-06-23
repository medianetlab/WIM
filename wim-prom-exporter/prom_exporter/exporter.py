#!/usr/bin/env python3

"""
Read the collected metrics and expose them to Prometheus
"""

import logging
import threading
import uuid

from prom_exporter.utils.kafkaUtils import create_consumer, create_topic
from prom_exporter.utils import mongoUtils
from prom_exporter.utils import threadingUtils
from prom_exporter.utils.threadingUtils import FlowThread

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def start_monitor(slice_data, thread_dict):
    """
    Starts monitoring the defined flows in slice_data. Creates a thread for each flow.
    """
    slice_flows = slice_data["slice_flows"]
    for node in slice_flows:
        for table in node["tables"]:
            for flow in table["flows"]:
                thread_id = str(uuid.uuid4())
                new_thread = threadingUtils.FlowThread(
                    switch_dpid=node["switch-dpid"],
                    flow_id=flow,
                    table_id=table["table-id"],
                    sdn_controller=node["sdn-ctl"],
                    name=thread_id,
                    slice_id=slice_data["_id"],
                )
                new_thread.start()
                new_thread_data = {
                    "_id": thread_id,
                    "switch_dpid": node["switch-dpid"],
                    "flow_id": flow,
                    "table_id": table["table-id"],
                    "sdn_controller": node["sdn-ctl"],
                }
                mongoUtils.add("flows", new_thread_data)
                thread_dict[thread_id] = new_thread


def stop_monitor(slice_data, thread_dict):
    """
    Stops monitoring the defined flows in slice_data. Terminates the thread for each flow.
    """
    slice_flows = slice_data["slice_flows"]
    for node in slice_flows:
        for table in node["tables"]:
            for flow in table["flows"]:
                data = {
                    "switch_dpid": node["switch-dpid"],
                    "flow_id": flow,
                    "table_id": table["table-id"],
                }
                thread = mongoUtils.find("flows", data=data)
                mongoUtils.delete("flows", thread["_id"])
                term_thread = thread_dict[thread["_id"]]
                term_thread.stop()
    thread_list = threading.enumerate()


def start_manager():
    """
    Creates and starts the KAFKA consumer
    """

    # Create the thread dictionary
    thread_dict = {}

    # Create the topic
    create_topic("wan-slice")

    # Create the consumer
    consumer = create_consumer("wan-monitoring")

    # Wait for messages
    for message in consumer:
        slice_data = message.value["slice_data"]
        if message.value["action"] == "create":
            logger.info(f"Monitoring slice: {slice_data['_id']}")
            start_monitor(slice_data, thread_dict)
        elif message.value["action"] == "terminate":
            logger.info(f"Deleted slice {slice_data['_id']}")
            stop_monitor(slice_data, thread_dict)


if __name__ == "__main__":
    FlowThread.start_prom_exporter_server()
    start_manager()
