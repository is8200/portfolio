package com.example.chapter5

import scala.collection.mutable.{HashMap, Map}
import java.io.{BufferedReader, InputStreamReader, Reader}
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.broadcast.Broadcast
import org.apache.spark.rdd.RDD

object BestSellerFinder {
  /**
   * 판매실적 데이터카 기록되어 있는 파일로부터
   * (상품ID, 판매개수)를 요소로 갖는 RDD를 생성하는 메소드
   */
  private def createSalesRDD(csvFile: String, sc: SparkContext) = {
    val logRDD = sc.textFile(csvFile)
    logRDD.map { record =>
      val splitRecord = record.split(",")
      val productId = splitRecord(2)
      val numOfSold = splitRecord(3).toInt
      (productId, numOfSold)
    }
  }

  /**
   * 각 달의 판매실적 데이터를 갖고 있는 RDD로부터
   * 50개이상 팔린 상품의 정보만을 갖는 RDD를 생성하는 메소드
   */
  private def createOver50SoldRDD(rdd: RDD[(String, Int)]) = {
    rdd.reduceByKey(_ + _).filter(_._2 >= 50)
  }

  /**
   * 상품의 마스터 데이터를 갖는 HashMap을 생성하는 메소드
   */
  private def loadCSVIntoMap(productsCSVFile: String) = {
    var productsCSVReader: Reader = null

    try {
      val productsMap = new HashMap[String, (String, Int)]
      val hadoopConf = new Configuration
      val fileSystem = FileSystem.get(hadoopConf)
      val inputStream = fileSystem.open(new Path(productsCSVFile))
      val productsCSVReader = new BufferedReader(new InputStreamReader(inputStream))
      var line = productsCSVReader.readLine

      while (line != null) {
        val splitLine = line.split(",")
        val productId = splitLine(0)
        val productName = splitLine(1)
        val unitPrice = splitLine(2).toInt
        productsMap(productId) = (productName, unitPrice)
        line = productsCSVReader.readLine
      }
      productsMap
    } finally {
      if (productsCSVReader != null) {
        productsCSVReader.close()
      }
    }
  }

  /**
   * 상품의 마스터 데이터와 결합해서
   * 두달 연속으로 50개 이상 판매된 상품정보를 갖는 RDD를 생성하는 메소드
   */
  private def createResultRDD(
      broadcastedMap: Broadcast[_ <: Map[String, (String, Int)]],
      rdd: RDD[(String, Int)]) = {
    rdd.map {
      case (productId, amount) =>
        val productsMap = broadcastedMap.value
        val (productName, unitPrice) = productsMap(productId)
        (productName, amount, amount * unitPrice)
    }
  }

  def main(args: Array[String]) {
    require(
      args.length >= 4,
      """
        |애플리케이션의 인자에
        |<첫번째 달의 판매데이터를 갖고 있는 파일의 경로>
        |<두번째 달의 판매데이터를 갖고 있는 파일의 경로>
        |<상품의 마스터 데이터 파일의 경로>
        |<출력하는 결과파일의 경로>를 지정해 주세요. """.stripMargin)

    val conf = new SparkConf
    val sc = new SparkContext(conf)

    try {
      // 드라이버 프로그램에 파라미터로 넘겨진 값을 일괄적으로 끄집어 낸다
      val Array(
        salesCSVFile1,
        salesCSVFile2,
        productsCSVFile,
        outputPath) = args.take(4)

      // 각 달의 판매실적이 기록된 CSV파일로부터
      // (상품ID, 판매개수) 형식의 튜플을 요소로 갖는 RDD를 생성한다
      val salesRDD1 = createSalesRDD(salesCSVFile1, sc)
      val salesRDD2 = createSalesRDD(salesCSVFile2, sc)

      // (상품ID, 판매개수) 형식의 튜플을 요소로 갖는 RDD로부터
      // (상품ID, 총판매개수) 형식의 튜플을 요소로 갖는 RDD를 생성한다
      val over50SoldRDD1 = createOver50SoldRDD(salesRDD1)
      val over50SoldRDD2 = createOver50SoldRDD(salesRDD2)

      // 두달 연속으로 50개 이상 판매된 상품에 대해서
      // (상품ID, 두달간의 총판매개수)형식의 튜플을 요소로 갖는 RDD를 생성한다
      val bothOver50SoldRDD = over50SoldRDD1.join(over50SoldRDD2)
      val over50SoldAndAmountRDD = bothOver50SoldRDD.map {
        case (productId, (amount1, amount2)) =>
          (productId, amount1 + amount2)
      }

      // 상품의 마스터 데이터를 HashMap에 로드하고
      // 브로드캐스트 변수로 이그제큐터에 배포한다
      val productsMap = loadCSVIntoMap(productsCSVFile)
      val broadcastedMap = sc.broadcast(productsMap)

      // 결과를 계산해 파일시스템이 출력한다
      val resultRDD = createResultRDD(broadcastedMap, over50SoldAndAmountRDD)
      resultRDD.saveAsTextFile(outputPath)
    } finally {
      sc.stop()
    }
  }
}
