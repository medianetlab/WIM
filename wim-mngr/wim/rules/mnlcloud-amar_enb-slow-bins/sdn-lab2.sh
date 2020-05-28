#!/bin/bash

# Configure sdn-lab2 to enable connectivity between OpenStack mnlcloud and Minilab eNodeB

# Get SDN Controller URL and Switch DPID from the options

while [[ $# -gt 0 ]]
do
key=$1
case $key in
-c | --controller)
ctl_url=$2
shift
shift
;;
-d | --dpid)
dpid=$2
shift
shift
;;
create)
action="create"
shift
;;
delete)
action="delete"
shift
;;
*)
printf "Wrong option %s \n%s < -d | --dpid SWITCH_DPID > < -c | --controller SDN_CONTROLLER_IP > < create/delete >\n" "$key" "$0"
exit 9999
;;
esac
done

if [ -z "${dpid}" ] || [ -z "${action}" ] || [ -z "${ctl_url}" ];
then
printf "Set SDN Controller URL, switch DPID and action \n%s < -d | --dpid SWITCH_DPID > < -c | --controller SDN_CONTROLLER_IP > < create/delete >\n" "$0"
exit 9999
fi

if [[ ${action} == "create" ]];
then

# Create the Normal flow for the management port (This might not be necessary if it has been installed earlier)
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept: application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/mgmt_port-normal.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/mgmt

sleep 3

# Drop traffic from ports 2-5 with priority = 1
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/drop_port2.json  \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/drop2

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/drop_port3.json  \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/drop3

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/drop_port4.json  \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/drop4

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/drop_port5.json  \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/drop5

sleep 3

# Handle ARP Messages from port 2->3 and port 3->2 (ARP will follow the fast path)
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/arp2.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/arp2

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/arp3.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/arp3

sleep 3

# Handle IP packets: ports 2<->4 and 5<->3 - Priority = 50 (lower than fast path in case of overwrite)
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/ip-slow2.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow2

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/ip-slow3.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow3

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/ip-slow4.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow4

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab2/ip-slow5.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow5

else

# DELETE ARP rules
curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/arp2

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/arp3

sleep 3

# DELETE IP packets rules
curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow2

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow3

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow4

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/60/flow/ip-slow5

fi
