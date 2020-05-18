#!/bin/bash

# Get the options
while [[ $# -gt 0 ]]
do
    key=$1

    case $key in
    -p | --publish)
        read -p "Expose Kafka Message Bus? (Y/n) " ans

        if [[ $ans != "n" ]];
        then
            read -p "WIM host public IP > " HOST_IP
            export "DOCKER_HOST_IP=${HOST_IP}"
        fi
        shift
    esac

done

docker-compose up --build -d