from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.rdd import RDD
from pyspark.sql import Row
from pyspark.sql import SQLContext
from matplotlib import pyplot
import numpy as np
import sys
import re
import os
import json

class LottoDataAnal :
    def __init__(self, *args, **kwargs):

        #return super().__init__(*args, **kwargs)
        isContainSecond = kwargs.get("isContainSecond")
        if  isContainSecond == None:
            self.isContainSecond = False    
        else :
            self.isContainSecond = isContainSecond
        
        startDate = kwargs.get("startDate")
        if  startDate == None:
            self.startDate = '0000-01-01'    
        else :
            self.startDate = startDate
        
        endDate = kwargs.get("endDate")
        if  endDate == None:
            self.endDate = '9999-12-31'    
        else :
            self.endDate = endDate

    def getEvenRatio(self, lottoNumbers) :
        evenNo = 0
        totalNo = len(lottoNumbers)
        for idx, value in enumerate(lottoNumbers) :
            if value % 2 == 0 :
                evenNo += 1
        return evenNo/totalNo

    def getMedium(self, lottoNumbers) :
        return float(np.median(lottoNumbers))
    
    def getAvgerage(self, lottoNumbers) :
        return float(np.mean(lottoNumbers))

    def getMax(self, lottoNumbers) :
        return np.max(lottoNumbers)

    def getMin(self, lottoNumbers) :
        return np.min(lottoNumbers)
    
    def getDeviation(self, lottoNumbers) :
        return float(np.std(lottoNumbers))
    
    def dataParse(self, datas) :
        splitData = datas.split(',')
        lottoNo = int(splitData[0])
        date = splitData[1]
        winnerBalls = (splitData[2].split('|'))
        luckyBalls = list(map(lambda ball : int(ball), winnerBalls))
        bonusBall = int(splitData[3])
        firstWinnerPrice = int(splitData[4])
        
        firstWinnerNo = 0
        secondWinnerNo = 0

        tempFirstNo = re.findall('\d+', splitData[5])
        if len(tempFirstNo) > 0 :
            firstWinnerNo = int(tempFirstNo[0])
        
        tempSecondNo = re.findall('\d+', splitData[6])
        if len(tempSecondNo) > 0 :
            secondWinnerNo = int(tempSecondNo[0])
        
        return (lottoNo, date, luckyBalls, bonusBall, firstWinnerPrice, firstWinnerNo, secondWinnerNo)

    def dataToDetail(self, rdd) :
        isContainSecond = self.isContainSecond
        startDate = self.startDate
        endDate = self.endDate

        getMin = self.getMin
        getMax = self.getMax
        getMedium = self.getMedium
        getAvgerage = self.getAvgerage
        getDeviation = self.getDeviation

        #print()
        if isContainSecond :
            tempRDD = rdd.map(lambda data : (data[0], data[1], data[2] + [data[3]], data[5] + data[6]))
        else :
            tempRDD = rdd.map(lambda data : (data[0], data[1], data[2], data[5]))
        #print("midi2")
        #print(tempRDD.collect())
        
        applyRDD = tempRDD.map(lambda data : data + (getMin(data[2]), getMax(data[2]), getMedium(data[2]), getAvgerage(data[2]), getDeviation(data[2]))) \
            .filter(lambda data : startDate <= data[1] and endDate >= data[1])
        
        return applyRDD

    def dataToDetailFunction(self, datas) :
        isContainSecond = self.isContainSecond
    
        getMin = self.getMin
        getMax = self.getMax
        getMedium = self.getMedium
        getAvgerage = self.getAvgerage
        getDeviation = self.getDeviation

        #print()
        if isContainSecond :
            newDatas = (datas[0], datas[1], datas[2] + [datas[3]], datas[5] + datas[6])
        else :
            newDatas = (datas[0], datas[1], datas[2], datas[5])
        applyRDD = newDatas + (getMin(newDatas[2]), getMax(newDatas[2]), getMedium(newDatas[2]), getAvgerage(newDatas[2]), getDeviation(newDatas[2]))

        return applyRDD

    def checkValue(self, datas) :
        print('asd')
        print(datas)

    def connection(self) :
        params = sys.argv 
        #print(params)
        filePath = params[1]

        conf = SparkConf()
        sc = SparkContext(conf = conf)
        lawDataRDD = sc.textFile(filePath)

        startDate = self.startDate
        endDate = self.endDate
        dataParse = self.dataParse

        lottoBasicDatasRDD = lawDataRDD.map(dataParse)
        dataToDetailFunction = self.dataToDetailFunction
       
        #dataToDetail = self.dataToDetail
        #lottoRDD = dataToDetail(lottoBasicDatasRDD)
        lottoRDD = lottoBasicDatasRDD.map(dataToDetailFunction) \
            .filter(lambda date : startDate <= date[1] and endDate >= date[1]) 
           #.partitionBy(4) \
           # .cache()
           
        abc = lottoRDD.collect()
        print(abc)
        jsonList = json.dumps(abc)
        #dfRDD = lottoRDD.map(lambda data : Row(name='xxx', no=data[2]))
        #sqlCtx = SQLContext(sc)
        #df = sqlCtx.createDataFrame(dfRDD)
        
       
   
#lottoDataAnalysys = LottoDataAnal(startDate='2018-11-20')
#lottoDataAnalysys.connection()