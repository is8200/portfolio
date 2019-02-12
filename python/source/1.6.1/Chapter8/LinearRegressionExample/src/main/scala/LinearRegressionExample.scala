import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.mllib.regression.{LabeledPoint,LinearRegressionWithSGD}
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.feature.StandardScaler
import org.apache.spark.mllib.evaluation.RegressionMetrics
import org.apache.spark.sql.functions.udf

case class Weather( date: String,
                    day_of_week: String,
                    avg_temp: Double,
                    max_temp: Double,
                    min_temp: Double,
                    rainfall: Double,
                    daylight_hours: Double,
                    max_depth_snowfall: Double,
                    total_snowfall: Double,
                    solar_radiation: Double,
                    mean_wind_speed: Double,
                    max_wind_speed: Double,
                    max_instantaneous_wind_speed: Double,
                    avg_humidity: Double,
                    avg_cloud_cover: Double)

case class Sales(date: String, sales: Double)

object LinearRegressionExample {

  def main(args: Array[String]) {

    val sparkConf = new SparkConf().setAppName("LinearRegressionExample")
    val sc = new SparkContext(sparkConf)
    val sqlContext = new org.apache.spark.sql.SQLContext(sc)
    import sqlContext.implicits._

    // 기상 데이터를 읽어 DataFrame으로 변환한다
    val weatherCSVRDD = sc.textFile("data/weather.csv")
    val headerOfWeatherCSVRDD = sc.parallelize(Array(weatherCSVRDD.first))
    val weatherCSVwithoutHeaderRDD = weatherCSVRDD.subtract(headerOfWeatherCSVRDD)
    val weatherDF = weatherCSVwithoutHeaderRDD.map(_.split(",")).
      map(p => Weather(p(0),
      p(1),
      p(2).trim.toDouble,
      p(3).trim.toDouble,
      p(4).trim.toDouble,
      p(5).trim.toDouble,
      p(6).trim.toDouble,
      p(7).trim.toDouble,
      p(8).trim.toDouble,
      p(9).trim.toDouble,
      p(10).trim.toDouble,
      p(11).trim.toDouble,
      p(12).trim.toDouble,
      p(13).trim.toDouble,
      p(14).trim.toDouble
    )).toDF()

    // 매출 데이터를 읽어 DataFrame으로 변환한다
    val salesCSVRDD = sc.textFile("data/sales.csv")
    val headerOfSalesCSVRDD = sc.parallelize(Array(salesCSVRDD.first))
    val salesCSVwithoutHeaderRDD = salesCSVRDD.subtract(headerOfSalesCSVRDD)
    val salesDF = salesCSVwithoutHeaderRDD.map(_.split(",")).map(p => Sales(p(0), p(1).trim.toDouble)).toDF()

    //println(weatherDF.printSchema)   // Spark-Shell을 이용하는 경우의 스키마를 확인하기위한 부분으로 
    //println(salesDF.printSchema)     // 주석처리

    // 데이터의 전처리
    val salesAndWeatherDF = salesDF.join(weatherDF, "date")
    val isWeekend = udf((t: String) => if(t.contains("일") || t.contains("토")) 1d else 0d)
    val replacedSalesAndWeatherDF = salesAndWeatherDF.withColumn("weekend", isWeekend(salesAndWeatherDF("day_of_week"))).drop("day_of_week")
    val selectedDataDF = replacedSalesAndWeatherDF.select("sales", "avg_temp", "rainfall", "weekend")
    val labeledPointsRDD = selectedDataDF.map(row => LabeledPoint(row.getDouble(0),
      Vectors.dense(
        row.getDouble(1),
        row.getDouble(2),
        row.getDouble(3)
      )))

    // 데이터의 표준화 (평균값을 조정하고 스케이링을 개별적으로 유효화 또는 무효화를 할 수 있다
    //val scaler = new StandardScaler(withMean = true, withStd = true).fit(labeledPointsRDD.map(x => x.features))
    val scaler = new StandardScaler().fit(labeledPointsRDD.map(x => x.features))
    val scaledLabledPointsRDD = labeledPointsRDD.map(x => LabeledPoint(x.label, scaler.transform(x.features)))

    // 선형회귀 모델을 작성한다
    val numIterations = 20
    scaledLabledPointsRDD.cache
    val linearRegressionModel = LinearRegressionWithSGD.train(scaledLabledPointsRDD, numIterations)

    println("weights :" + linearRegressionModel.weights)

    // 알고리즘에 미지의 데이터를 적용해 예측한다
    val targetDataVector1 = Vectors.dense(15.0,15.4,1)
    val targetDataVector2 = Vectors.dense(20.0,0,0)

    val targetScaledDataVector1 = scaler.transform(targetDataVector1)
    val targetScaledDataVector2 = scaler.transform(targetDataVector2)

    val result1 = linearRegressionModel.predict(targetScaledDataVector1)
    val result2 = linearRegressionModel.predict(targetScaledDataVector2)

    println("avg_tmp=15.0,rainfall=15.4,weekend=true : sales = " + result1)
    println("avg_tmp=20.0,rainfall=0,weekend=false : sales = " + result2)

    // 입력 데이터를 분할하고 평가한다
    val splitScaledLabeledPointsRDD = scaledLabledPointsRDD.randomSplit(Array(0.6, 0.4), seed = 11L)
    val trainingScaledLabeledPointsRDD = splitScaledLabeledPointsRDD(0).cache()
    val testScaledLabeledPointsRDD = splitScaledLabeledPointsRDD(1)
    val linearRegressionModel2 = LinearRegressionWithSGD.train(trainingScaledLabeledPointsRDD, numIterations)

    val scoreAndLabels = testScaledLabeledPointsRDD.map { point =>
      val score = linearRegressionModel2.predict(point.features)
      (score, point.label)
    }

    val metrics = new RegressionMetrics(scoreAndLabels)
    println("RMSE = "+ metrics.rootMeanSquaredError)

    // 작성한 모델을 보존한다
    //linearRegressionModel.save(sc,/path/to/modelDir)

  }
}
