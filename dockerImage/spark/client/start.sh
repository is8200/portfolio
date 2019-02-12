#!/bin/bash
docker run -d --privileged -e container=docker -v e:/kiha/sharedDir/cgroup:/sys/fs/cgroup:ro -v e:/kiha/sharedDir/hadoop:/hadoop -v e:/kiha/sharedDir/hadoopConf:/etc/hadoop/conf --name spark-client is8200/sparkclient:0.1
