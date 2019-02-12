#!/bin/bash

${SPARK_HOME}/bin/spark-submit --master local --class com.example.chapter4.SundayCount --name SundayCount ~/spark-simple-app/target/scala-2.10/spark-simple-app-assembly-0.1.jar /home/is8200/path/to/date.txt 



