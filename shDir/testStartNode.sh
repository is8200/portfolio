#!/bin/sh


#sudo docker run -d --cpuset-cpus=1 -m=1024m --memory-swap=2048m --privileged -e container=docker -v /sys/fs/cgroup:/sys/fs/cgroup:ro --add-host=client:10.0.120.5 --add-host=spark-master:10.0.120.6 --add-host=spark-worker00:10.0.120.7 --add-host=spark-worker01:10.0.120.8 --add-host=spark-worker02:10.0.120.9 --add-host=spark-worker03:10.0.120.10 --name spark-master-namenode --net spark-network --ip 10.0.120.6 spark-master-namenode

sudo -u hdfs hdfs namenode -format

#sudo docker exec -it spark-worker00 sudo -u hdfs hdfs namenode -format
sudo docker exec -it spark-datanode00 service hadoop-hdfs-datanode start

#sudo docker exec -it spark-master sudo -u hdfs hdfs namenode -format
sudo docker exec -it spark-master service hadoop-hdfs-namenode start

#hdfs mkdir
sudo -u hdfs hdfs dfs -mkdir -p /hadoop/tmp
sudo -u hdfs hdfs dfs -chmod 777 /hadoop/tmp
sudo -u hdfs hdfs dfs -mkdir /tmp
sudo -u hdfs hdfs dfs -chmod 777 /tmp
sudo -u hdfs hdfs dfs -mkdir -p /hadoop/yarn/app-logs
sudo -u hdfs hdfs dfs -chmod 777 /hadoop/yarn/app-logs
sudo -u hdfs hdfs dfs -mkdir -p /user/is8200
#sudo -u hdfs hdfs dfs -mkdir -p /user/is8200
sudo -u hdfs hdfs dfs -chown is8200:hadoop /user/is8200
#sudo -u hdfs hdfs dfs -chown is8200:hadoop /user/is8200

#after node operation
sudo docker exec -it spark-nodemanager sudo service hadoop-yarn-nodemanager start
#sudo docker exec -it spark-worker01 sudo service hadoop-yarn-nodemanager start
#sudo docker exec -it spark-worker02 sudo service hadoop-yarn-nodemanager start
#sudo docker exec -it spark-worker03 sudo service hadoop-yarn-nodemanager start
sudo docker exec -it spark-resourcemanager sudo service hadoop-yarn-resourcemanager start
