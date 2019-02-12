#!/bin/bash

(docker-compose -f E:/kiha/composetest/docker-compose.node.yml up -d)  -and 
	(echo "1") -and 
  (docker exec -it sparknamenode sudo -u hdfs hdfs namenode -format) -and 
	(echo "2") -and 
	(docker exec -it sparkdatanode00 service hadoop-hdfs-datanode start) -and 
	(echo "3") -and 
	(docker exec -it sparknamenode service hadoop-hdfs-namenode start) -and 
	(echo "4") -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p hadoop/tmp) -and 
  (echo "5") -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 hadoop/tmp) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p tmp) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 tmp) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p hadoop/yarn/app-logs) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -chmod 777 hadoop/yarn/app-logs) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -mkdir -p user/is8200) -and 
	(docker exec -it sparkclient sudo -u hdfs hdfs dfs -chown is8200:hadoop user/is8200) -and 
  (docker-compose -f E:/kiha/composetest/docker-compose.manager.yml up -d) -and 
	(docker exec -it sparknodemanager00 service hadoop-yarn-nodemanager start) -and 
	(docker exec -it sparkresourcemanager service hadoop-yarn-resourcemanager start) -and 
	(docker exec -it sparkclient bash) 
	#echo "하둡 클러스터 구동 성공"
