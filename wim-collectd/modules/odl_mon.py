import collectd


def read_func():
    with open("/opt/collectd_plugins/example") as f:
        value = f.read().strip()

    value = int(value)
    val = collectd.Values(type="gauge")
    val.host = "odl-host"
    val.plugin = "odl_mon"
    val.plugin_instance = "test"
    val.type_instance = "test"
    val.dispatch(values=[value])


collectd.register_read(read_func)
