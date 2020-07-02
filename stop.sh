#!/bin/bash

# Check for help option
if [[ " $@ " =~ " -h " ]] || [[ " $@ " =~ " --help " ]];
then
    printf "Usage:\n\tstart.sh [-c | --clear] [-h | --help]\nOptions:
    \t[-c | --clear] : Remove the container volumes
    \t[-h | --help] : Print this message and quit\n"
    exit 0
fi

while [[ $# -gt 0 ]]
do
key=$1
case $key in
-c | --clear)
options="$options -v"
shift
;;
*)
printf "Wrong option $key\n----------\n"
printf "Usage:\n\tstart.sh [-c | --clear] [-h | --help]\nOptions:
\t[-c | --clear] : Remove the container volumes
\t[-h | --help] : Print this message and quit\n"
exit 9999
esac
done

# Remove the monitoring variable
sed -i 's/WIM_MONITORING=.*/WIM_MONITORING=/' .env

docker-compose down $options
