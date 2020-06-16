#!/bin/bash

# Check for help option
if [[ " $@ " =~ " -h " ]] || [[ " $@ " =~ " --help " ]];
then
    printf "Usage:\n\tstart.sh [-p | --publish] [-h | --help]\nOptions:
    \t[-p | --publish] : Expose Kafka using WIM public IP
    \t[-h | --help] : Print this message and quit\n"
    exit 0
fi

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
*)
printf "Wrong option $key\n----------\n"
printf "Usage:\n\tstart.sh [-p | --publish] [-h | --help]\nOptions:
\t[-p | --publish] : Expose Kafka using WIM public IP
\t[-h | --help] : Print this message and quit\n"
exit 9999
;;
esac

done

# Check if .env file exists - If not create it
if [ ! -f .env ];
then
echo "NEO4J_AUTH=neo4j/neo4j" > .env
fi

docker-compose up --build -d

# Add the rules database
./rules_db.sh update
