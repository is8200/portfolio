#!/bin/bash

docker-compose -f docker-compose.node.yml up -d  && \
	echo "1" && \
  docker exec -it sparknamenode sudo -u hdfs hdfs namenode -format && \
	echo "2" && \
	docker exec -it sparkdatanode00 service hadoop-hdfs-datanode start && \
	echo "3" && \
	docker exec -it sparknamenode service hadoop-hdfs-namenode start && \
	echo "4" && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p /hadoop/tmp && \
  echo "5"&& \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 /hadoop/tmp && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p /tmp && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 /tmp && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p /hadoop/yarn/app-logs && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 /hadoop/yarn/app-logs && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p /user/is8200 && \
	docker exec -it sparkclient sudo -u hdfs hdfs dfs -chown is8200:hadoop /user/is8200 && \
  docker-compose -f docker-compose.manager.yml up -d && \
	docker exec -it sparknodemanager00 service hadoop-yarn-nodemanager start && \
	docker exec -it sparkresourcemanager service hadoop-yarn-resourcemanager start && \
	docker exec -it sparkclient bash 
	#echo "하둡 클러스터 구동 성공"
