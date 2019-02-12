#!/bin/bash

sudo docker run -d --privileged -e container=docker -v /sys/fs/cgroup:/sys/fs/cgroup:ro --add-host=client:10.0.120.5 --add-host=spark-master:10.0.120.6 --add-host=spark-worker00:10.0.120.7 --add-host=spark-worker01:10.0.120.8 --add-host=spark-worker02:10.0.120.9 --add-host=spark-worker03:10.0.120.10 --name spark-master --net spark-network --ip 10.0.120.6 spark-master

sudo docker exec -it spark-master ./start-hadoop.sh && /bin/bash

