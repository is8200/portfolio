#!/bin/bash
RUN mkdir /hadoop
RUN mkdir /hadoop/hdfs
RUN chown hdfs:hadoop /hadoop/hdfs
RUN chmod 775 /hadoop/hdfs
RUN mkdir /hadoop/yarn
RUN chown yarn:hadoop /hadoop/yarn
RUN chmod 775 /hadoop/yarn
RUN mkdir /hadoop/tmp
RUN chmod 777 /hadoop/tmp

