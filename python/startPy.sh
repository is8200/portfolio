#!/bin/bash

sudo -u hdfs hdfs dfs -put lottoDatas.txt /hadoop
$SPARK_HOME/bin/spark-submit --master yarn-client lottoDataAnal.py /hadoop/lottoDatas.txt
