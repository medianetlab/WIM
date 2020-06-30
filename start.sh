#!/bin/bash

# Check for help option
if [[ " $@ " =~ " -h " ]] || [[ " $@ " =~ " --help " ]];
then
    printf "Usage:\n\tstart.sh [-p | --publish] [-m | --monitoring] [-h | --help]\nOptions:
    \t[-p | --publish] : Expose Kafka using WIM public IP
    \t[-m | --monitoring] : Start prometheus exporter module
    \t[-h | --help] : Print this message and quit\n"
    exit 0
fi

containers="zookeeper kafka neo4j wim-nbi wim-mngr wim-cli mongo"

# Get the options
while [[ $# -gt 0 ]]
do
key=$1

case $key in
-p | --publish)
read -p "Expose Kafka Message Bus? (Y/n) " ans

if [[ $ans != "n" ]];
then
    ip_list=$(hostname -I 2> /dev/null)
    read -p "WIM host public IP (Available: $ip_list) >> " HOST_IP
    export "DOCKER_HOST_IP=${HOST_IP}"
fi
shift
;;
-m | --monitoring)
containers=""
shift
;;
*)
printf "Wrong option $key\n----------\n"
printf "Usage:\n\tstart.sh [-p | --publish] [-m | --monitoring] [-h | --help]\nOptions:
\t[-p | --publish] : Expose Kafka using WIM public IP
\t[-m | --monitoring] : Start prometheus exporter module
\t[-h | --help] : Print this message and quit\n"
exit 9999
;;
esac

done

# Check if .env file exists - If not create it
if [ ! -f .env ];
then
echo "NEO4J_AUTH=neo4j/neo4j" > .env
echo "ODL_AUTH=admin:admin" >> .env
fi

docker-compose up --build -d ${containers}

# Add the rules database
./rules_db.sh update
