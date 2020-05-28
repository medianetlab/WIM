#!/bin/bash

# Configure sdn-io to enable connectivity between OpenStack mnlcloud and Minilab eNodeB via slow path

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

# Configure br0
# Pass anything from ports 1<->2
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-io-br0/data_port1.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/p1to2

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-io-br0/data_port2.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/p2to1

else

# Delete Openflow rules
curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/p1to2

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/p2to1

fi