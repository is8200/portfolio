#!/bin/bash

sudo docker run -d --cpuset-cpus=0 -m=1024m --memory-swap=2048m --privileged -e container=docker -v /sys/fs/cgroup:/sys/fs/cgroup:ro --add-host=client:10.0.120.5 --add-host=spark-master:10.0.120.6 --add-host=spark-worker00:10.0.120.7 --add-host=spark-worker01:10.0.120.8 --add-host=spark-worker02:10.0.120.9 --add-host=spark-worker03:10.0.120.10 --name spark-worker00 --net spark-network --ip 10.0.120.7 spark-worker

