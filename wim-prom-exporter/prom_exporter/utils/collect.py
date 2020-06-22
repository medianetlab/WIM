import logging

from prometheus_client import start_http_server, Gauge

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


traffic_bytes = {}


def collect(flow_id, _bytes):
    """
    Function that collects the traffic metrics
    """
    global traffic_bytes

    traffic_bytes_metric = traffic_bytes.get(
        flow_id, Gauge(flow_id.replace("-", "_"), "Bytes for the flow id")
    )
    traffic_bytes_metric.set(_bytes)
    traffic_bytes[flow_id] = traffic_bytes_metric
    logger.debug(_bytes)


def start_prom_exporter_server():
    """
    Function that starts the creates the prometheus exporter metrics and starts the http server
    """
    start_http_server(8888)
