#!/usr/bin/bash

IMAGE_NAME="otbiot-py"
CONT_NAME="otbiot-py"

# Build the container, with the newest version of the app
docker build . -t $IMAGE_NAME

# Delete an old version of the container, if present
docker rm -f $CONT_NAME

# Run the container - privileged required for GPIO access
docker run -d --restart=always --privileged --name $CONT_NAME $IMAGE_NAME

# Tail the logs if requested
if [ ! -z $1 ] && [ $1 = 'logs' ]; then
    docker logs -f $CONT_NAME
fi
