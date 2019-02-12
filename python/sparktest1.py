from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.rdd import RDD
import sys

class sparktest1:

    def __init__(self):
        self.dd = ''

    def computeAllAvg(self, rdd):
        (totalPoint, count) = rdd.map(lambda record : (record[2], 1)) \
            .reduce(lambda sumRecord, record : (int(sumRecord[0]) + int(record[0]), int(sumRecord[1]) + int(record[1])))
        return totalPoint / float(count)

    def computeAgeRangeAvg(self, rdd):
        return rdd.map(lambda record : (record[0], (record[2], 1))) \
            .reduceByKey(lambda sumRecord, record : (int(sumRecord[0]) + int(record[0]), int(sumRecord[1]) + int(record[1]))) \
            .map(lambda record : (record[0], record[1][0] / float(record[1][1]))) \
            .collect()
        
    def computeMorFAvg(self, rdd, numMAcc, totalPointMAcc, numFAcc, totalPointFAcc):
        dictTotal = rdd.map(lambda record : (record[1], (record[2], 1))) \
            .reduceByKey(lambda sumRecord, record : (int(sumRecord[0]) + int(record[0]), int(sumRecord[1]) + int(record[1]))) \
            .collectAsMap() 

        print(dictTotal) 
        print(type(totalPointMAcc.value))   
        print(type(numMAcc.value))
        arrTotal =[("Male", (dictTotal["M"][0] + totalPointMAcc.value) / (dictTotal["M"][1] + numMAcc.value)), \
            ("FeMale", (dictTotal["F"][0] + totalPointFAcc.value) / (dictTotal["F"][1] + numFAcc.value))]
        return arrTotal

    def recordToTuple(self, record):
        splitRecord = record.split(",")
        ageRange = int(splitRecord[0]) // 10 * 10
        maleOrFemale = splitRecord[1]
        point = int(splitRecord[2])
        print("asd")
        return (ageRange, maleOrFemale, point)

    def printCheck(param, *args):
        print("check00")
        print(param)

    def connenctSpark(self):
        params = sys.argv
        print(params)
        filePath = params[1]

        conf = SparkConf()
        sc = SparkContext(conf = conf)
        temp = sc.textFile(filePath)
        print(temp.collect())
        recordToTuple = self.recordToTuple
        questionaireRDD = temp.map(recordToTuple)
        print(questionaireRDD.collect())
        questionaireRDD.cache()

        computeAllAvg = self.computeAllAvg
        computeAgeRangeAvg = self.computeAgeRangeAvg
        computeMorFAvg = self.computeMorFAvg

        avgAll = computeAllAvg(questionaireRDD)
        aveAgeRange = computeAgeRangeAvg(questionaireRDD)
        numMAcc = sc.accumulator(0, 'Number of M')
        totalPointMAcc = sc.accumulator(0, 'Total point of M')
        numFAcc = sc.accumulator(0, 'Number of F')
        totalPointFAcc = sc.accumulator(0, 'Total point of F')
        
        avgMorF = computeMorFAvg(questionaireRDD, numMAcc, totalPointMAcc, numFAcc, totalPointFAcc)
        print(avgMorF)
        #aveAgeRange.foreach(self.printCheck)

        #avgMorF.foreach(self.printCheck)

ad = sparktest1()
ad.connenctSpark()