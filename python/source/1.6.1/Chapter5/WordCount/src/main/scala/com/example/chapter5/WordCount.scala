package com.example.chapter5

import org.apache.spark.{SparkConf, SparkContext}

object WordCount {

  def main(args: Array[String]) {
    require (args.length >= 1,
      "드라이버 프로그램의 인자에 단어를 세고자 하는 " +
      "파일의 경로를 지정해 주세요 ")

    val conf = new SparkConf
    val sc = new SparkContext(conf)

    try {
      // 모든 단어에 대해 (단어, 등장횟수)형식의 튜플을 만든다
      val filePath = args(0)
      val wordAndCountRDD = sc.textFile(filePath)
                              .flatMap(_.split("[ ,.]"))
                              .filter(_.matches("""\p{Alnum}+"""))
                              .map((_, 1))
                              .reduceByKey(_ + _)
      

      // 모든 단어의 등장횟수를 출력한다
      wordAndCountRDD.collect.foreach(println)
    } finally {
      sc.stop()
    }
  }
}
    
