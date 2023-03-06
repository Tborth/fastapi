#!/bin/bash
xhost +local:root
ENV_FILE=src/config/.env

echo "Stopping configAPIs ..."
docker-compose down
docker-compose up -d --build # --env-file $ENV_FILE
# docker-compose up
