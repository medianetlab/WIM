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
-f | --flowid)
flowid=$2
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
printf "Wrong option %s \n%s < -d | --dpid SWITCH_DPID > < -c | --controller SDN_CONTROLLER_IP > < -f | --flowid FLOWID > < create/delete >\n" "$key" "$0"
exit 9999
;;
esac
done

if [ -z "${dpid}" ] || [ -z "${action}" ] || [ -z "${ctl_url}" ] || [ -z "${flowid}" ];
then
printf "Set SDN Controller URL, switch DPID and action \n%s < -d | --dpid SWITCH_DPID > < -c | --controller SDN_CONTROLLER_IP > < -f | --flowid FLOWID > < create/delete >\n" "$0"
exit 9999
fi


if [[ ${action} == "create" ]];
then

# Configure br1
# Pass anything from ports 9<->10

# Change the flow-id in the of-flow data files
sed -i "s/\"id\": \"FLOW-ID\"/\"id\": \"${flowid}-p9to10\"/g"  of-flows/sdn-io-br1/data_port9.json
sed -i "s/\"id\": \"FLOW-ID\"/\"id\": \"${flowid}-p10to9\"/g"  of-flows/sdn-io-br1/data_port10.json


curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-io-br1/data_port9.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/"${flowid}-p9to10"

sleep 3

curl -v -k -X PUT \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
-d @of-flows/sdn-io-br1/data_port10.json \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/"${flowid}-p10to9"

sed -i "s/\"id\": \"${flowid}-p9to10\"/\"id\": \"FLOW-ID\"/g"  of-flows/sdn-io-br1/data_port9.json
sed -i "s/\"id\": \"${flowid}-p10to9\"/\"id\": \"FLOW-ID\"/g"  of-flows/sdn-io-br1/data_port10.json

else

# DELETE ports 9<->10
curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/"${flowid}-p9to10"

sleep 3

curl -v -k -X DELETE \
--user "${ODL_AUTH}" \
-H "Accept:application/json" \
-H "Content-type: application/json" \
http://"${ctl_url}":8181/restconf/config/opendaylight-inventory:nodes/node/"${dpid}"/flow-node-inventory:table/0/flow/"${flowid}-p10to9"

fi