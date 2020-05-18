#!/bin/bash


while [[ $# -gt 0 ]]
do
    key=$1
    case $key in
        -c | --clear)
            options="$options -v"
            shift
    esac
done

docker-compose down $options