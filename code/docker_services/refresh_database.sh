#!/bin/bash

cd refresh_db
docker build -t refresh_db .
docker run --net bibliography-net refresh_db
cd ..