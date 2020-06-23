import threading
import logging
import requests

from prometheus_client import start_http_server, Gauge

# Create the logger
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
stream_handler.setFormatter(stream_formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class FlowThread(threading.Thread):
    """
    Class that creates an object thread for each flow that must be monitored
    """

    def __init__(
        self,
        switch_dpid,
        flow_id,
        table_id,
        sdn_controller,
        slice_id,
        user="admin",
        passwd="admin",
        name=None,
    ):
        super().__init__(name=name)
        self.switch_dpid = switch_dpid
        self.flow_id = flow_id
        self.table_id = table_id
        self.sdn_controller = sdn_controller
        self._stop = threading.Event()
        self.user = user
        self.passwd = passwd
        self.metric_bytes = Gauge(flow_id.replace("-", "_"), "Bytes for the flow id")
        self.metric_bytes.set(0)

    def run(self):
        """
        The function that will be used when the thread is running
        """
        while not self.stopped():
            url = (
                f"http://{self.sdn_controller}:8181/restconf/operational/opendaylight-inventory:"
                f"nodes/node/{self.switch_dpid}/table/{self.table_id}/flow/{self.flow_id}"
            )
            headers = {"Accept": "Application/json"}
            auth = (self.user, self.passwd)
            flow_req = requests.get(url=url, headers=headers, auth=auth)
            if flow_req.status_code == 200:
                cur_bytes = flow_req.json()["flow-node-inventory:flow"][0][
                    "opendaylight-flow-statistics:flow-statistics"
                ]["byte-count"]
                self.metric_bytes.set(cur_bytes)
            self._stop.wait(timeout=10)

    def stopped(self):
        """
        Check if the stop flag is set
        """
        return self._stop.is_set()

    def stop(self):
        """
        Sets the _stop flag to True and stops the thread
        """
        self._stop.set()

    @classmethod
    def start_prom_exporter_server(cls):
        """
        Function starts the prometheus exporter http server
        """
        start_http_server(8888)
