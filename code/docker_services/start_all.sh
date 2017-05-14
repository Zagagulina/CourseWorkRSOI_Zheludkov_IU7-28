#!/bin/bash

# create the network
docker network create bibliography-net

# build the containers
cd agregation
docker-compose build
cd ../controller
docker-compose build
cd ../publisher
docker-compose build
cd ../templates
docker-compose build
cd ../users
docker-compose build
cd ..

# start the containers
cd agregation
docker-compose up -d
cd ../controller
docker-compose up -d
cd ../publisher
docker-compose up -d
cd ../templates
docker-compose up -d
cd ../users
docker-compose up -d