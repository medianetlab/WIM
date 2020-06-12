#!/usr/bin/env python3

"""
Read the collected metrics and expose them to Prometheus
"""

import csv
import time
import logging

from prometheus_client import Gauge, start_http_server

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

# Create the metric
exam = Gauge("wim_example_value", "Example values from the collectd")


def set_value():
    with open("/opt/metrics/odl-host/odl_mon-test/gauge-test-2020-06-12", mode="r") as metric_file:
        metricreader = csv.reader(metric_file)
        while True:
            exam.set(list(metricreader)[-1][-1])
            time.sleep(5)


if __name__ == "__main__":
    start_http_server(8888)
    set_value()
