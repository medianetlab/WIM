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
* __-m | --monitoring__ : Start prometheus exporter module for collecting traffic metrics per flow

## Environmenta Varibles

Before you start the wim, make sure to create a .env file containing a variable with the credentials for:

* The Neo4j database, in the form `NEO4J_AUTH=username/password`. If no such file is created, the default username/passwords will be used (neo4j/neo4j)
* OpenDayLight, in the form `ODL_AUTH=admin:admin`. If no such file is created, the default username/passwords will be used (admin/admin)
