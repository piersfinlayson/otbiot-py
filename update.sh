#!/usr/bin/bash
set -e

HOSTNAME=$1
REMOTE_DIR_DEFAULT="~/container-data/otbiot-py"
FILES_TO_COPY="*.sh *.py *.txt Dockerfile"

if [ -z $HOSTNAME ] || [ $HOSTNAME = '-h' ] || [ $HOSTNAME = '-?' ] || [ $HOSTNAME = '--help' ]; then
    echo "Usage: $0 <hostname> [remote-dir]"
    echo "       Copies otbiot-py files to [remote-dir] on <hostname>"
    echo "       If [remote-dir] is not specified] it defaults to $REMOTE_DIR"
    exit
fi
REMOTE_DIR=$2
if [ -z $REMOTE_DIR ]; then
    REMOTE_DIR=$REMOTE_DIR_DEFAULT
fi

echo "Copying $FILES_TO_COPY to $HOSTNAME:$REMOTE_DIR"
ssh $HOSTNAME "mkdir -p $REMOTE_DIR"
scp *.sh *.py *.txt Dockerfile $HOSTNAME:$REMOTE_DIR

if [ $HOSTNAME != "heating2" ]; then
    echo "Modifying user_config.py - replacing chip id d76a7d with $HOSTNAME"
    ssh $HOSTNAME sed -i -- 's/d76a7d/'"$HOSTNAME"'/g' /home/pdf/container-data/otbiot-py/user_config.py
fi
echo "Done"