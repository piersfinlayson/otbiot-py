#!/usr/bin/bash
set -e

docker run --rm -ti --name otbiot-temp --privileged -v .:/usr/src/app/ otbiot-py