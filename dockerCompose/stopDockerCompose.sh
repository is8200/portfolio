#!/bin/bash

docker-compose -f docker-compose.manager.yml down
docker-compose -f docker-compose.node.yml down
