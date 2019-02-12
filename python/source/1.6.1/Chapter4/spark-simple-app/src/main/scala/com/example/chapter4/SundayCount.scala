package com.example.chapter4
import org.joda.time.{DateTime, DateTimeConstants}
import org.joda.time.format.DateTimeFormat
import org.apache.spark.{SparkConf, SparkContext}

object SundayCount {
  def main(args: Array[String]) {
    if (args.length < 1) {
      throw new IllegalArgumentException("커맨드 인자에 날짜가 기록된 파일의 경로를 지정해 주세요.")
    }
    val filePath = args(0)
    val conf = new SparkConf
    val sc = new SparkContext(conf)
    try {
      // 텍스트파일을 로드한다
      val textRDD = sc.textFile(filePath)

      // 문자열로 표현된 날짜로부터 DateTime형식의 인스턴스를 생성한다
      val dateTimeRDD = textRDD.map { dateStr =>
        val pattern =
          DateTimeFormat.forPattern("yyyyMMdd")
        DateTime.parse(dateStr, pattern)
      }

      // 일요일만을 추출한다
      val sundayRDD = dateTimeRDD.filter { dateTime =>
        dateTime.getDayOfWeek == DateTimeConstants.SUNDAY
      }

      // sundayRDD에 들어 있는 일요일의 개수를 센다
      val numOfSunday = sundayRDD.count
      println(s"주어진 데이터에는 일요일이 ${numOfSunday}개 들어 있습니다.")
    } catch {
      case e : Throwable => e.printStackTrace()
    } finally {
      sc.stop()
    }
  }
}
