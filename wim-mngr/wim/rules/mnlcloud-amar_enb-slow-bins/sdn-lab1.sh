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


if [[ $action == "create" ]];
then
# Create the Normal flow for all the ports that are part of the OF-Instance
curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept: application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-lab1/genesis-normal.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/1/flow/genesis-normal

else
# DELETE the Normal flow for all the ports that are part of the OF-Instance
curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept: application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/1/flow/genesis-normal

fi