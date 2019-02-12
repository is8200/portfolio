package com.example.chapter5

import org.apache.spark.{Accumulator, SparkConf, SparkContext}
import org.apache.spark.rdd.RDD

object QuestionnaireSummarization {

  /**
   * 모든 앙케이트의 평가 평균값을 계산하는 메소드
   */ 
  private def computeAllAvg(rdd: RDD[(Int, String, Int)]) = {
    val (totalPoint, count) =
      rdd.map(record => (record._3, 1)).reduce {
        case ((intermedPoint, intermedCount), (point, one)) =>
          (intermedPoint + point, intermedCount + one)
      }
    totalPoint / count.toDouble
  }

  /**
   * 연령대별 평강의 평균값을 계산하는 메소드
   */
  private def computeAgeRangeAvg(rdd: RDD[(Int, String, Int)]) = {
    rdd.map(record => (record._1, (record._3, 1))).reduceByKey {
      case ((intermedPoint, intermedCount), (point, one)) =>
        (intermedPoint + point, intermedCount + one)
    }.map {
      case (ageRange, (totalPoint, count)) =>
        (ageRange, totalPoint / count.toDouble)
    }.collect
  }

  /**
   * 남녀별 평가의 평균값을 계산하는 메소드
   */
  private def computeMorFAvg(
      rdd: RDD[(Int, String, Int)],
      numMAcc: Accumulator[Int],
      totalPointMAcc: Accumulator[Int],
      numFAcc: Accumulator[Int],
      totalPointFAcc: Accumulator[Int]) = {
    rdd.foreach {
      case (_, maleOrFemale, point) =>
        maleOrFemale match {
          case "M" =>
            numMAcc += 1
            totalPointMAcc += point
          case "F" =>
            numFAcc += 1
            totalPointFAcc += point
        }
    }
    Seq(("Male", totalPointMAcc.value / numMAcc.value.toDouble),
      ("Female", totalPointFAcc.value / numFAcc.value.toDouble))
  }

  def main(args: Array[String]) {
    require(
      args.length >= 2,
      """
        |애플리케이션의 인자에
        |<앙케이트 CSV 파일의 경로>
        |<출력하는 결과파일의 경로>를 지정해 주세요. """.stripMargin)

    val conf = new SparkConf
    val sc = new SparkContext(conf)

    try {
      val filePath = args(0)

      // 앙케이트를 로드해 (연령대, 성별, 평가) 형식의
      // 튜플을 요소로 하는 RDD를 생성한다.
      val questionnaireRDD = sc.textFile(filePath).map { record =>
        val splitRecord = record.split(",")
        val ageRange = splitRecord(0).toInt / 10 * 10
        val maleOrFemale = splitRecord(1)
        val point = splitRecord(2).toInt
        (ageRange, maleOrFemale, point)
      }

      // questionnaireRDD는 각각의 집계처리에 이용되기 때문에 캐시에 보존한다
      questionnaireRDD.cache

      // 모든 평가의 평균치를 계산한다
      val avgAll = computeAllAvg(questionnaireRDD)
      // 연령대별 평균치를 계산한다
      val avgAgeRange = computeAgeRangeAvg(questionnaireRDD)

      // 성별이 M인 앙케이트의 건수를 세는 어큐뮬레이터
      val numMAcc = sc.accumulator(0, "Number of M")
      // 성별이 M인 앙케이트의 평가를 합계하는 어큐뮬레이터
      val totalPointMAcc = sc.accumulator(0, "Total Point of M")
      // 성별이 F인 앙케이트의 건수를 세는 어큐뮬레이터
      val numFAcc = sc.accumulator(0, "Number of F")
      // 성별이 F인 앙케이트의 평가를 합계하는 어큐뮬레이터
      val totalPointFAcc = sc.accumulator(0, "TotalPoint of F")

      // 남여별 평균치를 계산한다
      val avgMorF = computeMorFAvg(
        questionnaireRDD,
        numMAcc,
        totalPointMAcc,
        numFAcc,
        totalPointFAcc)

      println(s"AVG ALL: $avgAll")
      avgAgeRange.foreach {
        case (ageRange, avg) =>
          println(s"AVG Age Range($ageRange): $avg")
      }

      avgMorF.foreach {
        case (mOrF, avg) =>
          println(s"AVG $mOrF: $avg")
      }
    } finally {
      sc.stop()
    }
  }
}
