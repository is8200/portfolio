#!/bin/bash

sudo sed -i 's/HADOOP_CONF_DIR/#HADOOP_CONF_DIR/g' /opt/spark/conf/spark-env.sh
