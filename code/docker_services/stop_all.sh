#!/bin/bash

# stop the containers
cd agregation
docker-compose stop
cd ../controller
docker-compose stop
cd ../publisher
docker-compose stop
cd ../templates
docker-compose stop
cd ../users
docker-compose stop
cd ..

# remove the network
docker network rm bibliography-net