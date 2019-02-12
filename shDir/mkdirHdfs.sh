#!/bin/bash
sudo -u hdfs hdfs dfs -mkdir -p /hadoop/tmp
sudo -u hdfs hdfs dfs -chmod 777 /hadoop/tmp
sudo -u hdfs hdfs dfs -mkdir /tmp
sudo -u hdfs hdfs dfs -chmod 777 /tmp
sudo -u hdfs hdfs dfs -mkdir -p /hadoop/yarn/app-logs
sudo -u hdfs hdfs dfs -chmod 777 /hadoop/yarn/app-logs
sudo -u hdfs hdfs dfs -mkdir -p /user/is8200
sudo -u hdfs hdfs dfs -mkdir -p /user/is8200
sudo -u hdfs hdfs dfs -chown is8200:hadoop /user/is8200
