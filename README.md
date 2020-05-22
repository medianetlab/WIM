# WAN Infrastructure Manager - WIM

WIM is used as the WAN Infrastructure Manager for SDN Networks, interacting with ODL Controller (Oxygen and Fluorine releases currently supported)

## Features

* Configure end-to-end Network Slices over SDN Networks
* QoS parametes per slice
* Graphical Database [neo4j](https://neo4j.com/)
* Graphical topology representation

## Install and Run

```bash
./start.sh [-p | --publish]
```

* __-p | --publish__ : Expose Kafka Message Bus to external components
