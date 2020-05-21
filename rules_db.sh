#!/bin/bash

# Get the options
while [[ $# -gt 0 ]]
do

key=$1

case $key in
update)
echo "Updating Rules DB in WIM"
docker exec -it wim-mngr python -c "from wim.rules_db import update; update()"
shift
;;
index)
docker exec -it wim-mngr python -c "from wim.rules_db import index; print(index())" | python -m json.tool
shift
;;
*)
echo Wrong option $key
exit 9999
esac

done