#!/bin/bash

# docker build -t ffring .

docker build --tag ffring-docker .
docker run -d -p 8083:8083 ffring-docker

# docker build -t myuserapi .
# docker run -d -p 8083:5000 --restart always ffring

# docker build -t ffring .
# docker run -d -p 8083:5000 ffring
# docker run -p 8083:5000 --name ffring-container -d ffring
# docker run -p 8083:5000  -d ffring

# docker run -d -p 8082:8082 --restart always myuserapi
