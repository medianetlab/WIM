import collectd
import random


def read_func():
    value = random.randint(0, 1000)

    value = int(value)
    val = collectd.Values(type="gauge")
    val.host = "odl-host"
    val.plugin = "odl_mon"
    val.plugin_instance = "test"
    val.type_instance = "test"
    val.dispatch(values=[value])


collectd.register_read(read_func)
