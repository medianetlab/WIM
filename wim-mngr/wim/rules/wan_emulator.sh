#!/bin/bash

# IMPORTANT NOTE!!!
# WIM must have passwordless ssh access to the WAN emulator using ssh keys

# Get the action
ACTION=$1

if [[ $ACTION == "create" ]]; then
	wan_emu_command='cd /home/localadmin/sdn-mininet; sudo python3.7 /home/localadmin/sdn-mininet/sdn_topology_service.py --ryu -b 200 -d 5 -l 2'
else
	wan_emu_command='sudo mn -c'
fi

# TODO: Get the WAN Emulator information from the database
ssh -o StrictHostKeyChecking=no -i /wim-mngr/ssh-keys/id_rsa.key localadmin@10.143.143.80 $wan_emu_command
