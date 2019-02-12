from matplotlib import pyplot
import numpy as np
from pandas import DataFrame
import sys
import re
import os

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
        #print("acdacd")
        ##print(lottoNumbers)
        #print(np.median(lottoNumbers))
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

    def reduceDataFunction(self, datas, std, val) :
        return list(map(lambda data : [data[std], data[val]], datas))
    
    def reduceDataAllFunction(self, datas) :
        return list(map(lambda data : [data[3], data[4], data[5], data[6], data[7], data[8]], datas))

    def connection(self) :
        params = sys.argv 
        #print(params)
        filePath = params[1]
                
        fileOpen = open(filePath, 'r', encoding='utf8')
        lottoDatas = fileOpen.readlines()
        startDate = self.startDate
        endDate = self.endDate
        dataParse = self.dataParse
        reduceDataFunction = self.reduceDataFunction
        lottoBasicDatas = list(map(dataParse, lottoDatas))
        dataToDetailFunction = self.dataToDetailFunction
        reduceDataAllFunction = self.reduceDataAllFunction
       
        lottoApplyData = list(filter(lambda date : startDate <= date[1] and endDate >= date[1], list(map(dataToDetailFunction, lottoBasicDatas)))) 
        #0 회차 1 날짜 2 번호 3 당첨자수 4 최소값 5 최대값 6 중간값 7 평균 8 편차 
        reduceLottoData = reduceDataAllFunction(lottoApplyData)
        #reduceLottoDataOne = reduceDataFunction(lottoApplyData, 6, 3)
        #reduceLottoDataTwo = reduceDataFunction(lottoApplyData, 7, 3)
        #reduceLottoDataThree = reduceDataFunction(lottoApplyData, 8, 3)
        #reduceLottoDataFour = reduceDataFunction(lottoApplyData, 4, 3)
        #reduceLottoDataFive = reduceDataFunction(lottoApplyData, 5, 3)
        #print(lottoApplyData)
        sortedLottoData = sorted(reduceLottoData , key=lambda data: data[1])
        lottoDF = DataFrame(sortedLottoData, columns=['no', 'min', 'max', 'mid', 'avg', 'div'])
        ax1 = lottoDF.plot(x='min', y='no', kind='scatter', color='C1')
        ax2 = lottoDF.plot(x='max', y='no', kind='scatter', color='C2', ax = ax1)
        ax3 = lottoDF.plot(x='mid', y='no', kind='scatter', color='C3', ax = ax1)
        ax4 = lottoDF.plot(x='avg', y='no', kind='scatter', color='C4', ax = ax1)
        ax5 = lottoDF.plot(x='div', y='no', kind='scatter', color='C5', ax = ax1)

        #lottoOneDF = DataFrame(reduceLottoDataOne, columns=['a', 'b'])
        #lottoTwoDF = DataFrame(reduceLottoDataTwo, columns=['c', 'b'])
        #lottoThreeDF = DataFrame(reduceLottoDataThree, columns=['d', 'b'])
        #lottoFourDF = DataFrame(reduceLottoDataFour, columns=['e', 'b'])
        #lottoFiveDF = DataFrame(reduceLottoDataFive, columns=['f', 'b'])
        #ax1 = lottoOneDF.plot(x='a', y='b', kind='scatter', color='C1')
        #ax2 = lottoTwoDF.plot(x='c', y='b', kind='scatter', color='C2', ax = ax1)
        #ax3 = lottoThreeDF.plot(x='d', y='b', kind='scatter', color='C3', ax = ax1)
        #ax4 = lottoFourDF.plot(x='e', y='b', kind='scatter', color='C4', ax = ax1)
        #ax5 = lottoFiveDF.plot(x='f', y='b', kind='scatter', color='C5', ax = ax1)
        #lottoDF.plot(x=0, y=1, kind='scatter', color='C3')
        #pyplot.scatter(x='a', y='b')
        #pyplot.plot(lottoDF)
        
        pyplot.show()
        #lottoDF.plot(kind='line')
        #lottoDF.plot(kind='barh',x='name',y='id',colormap='winter_r')
        #lottoDF.show()
        #pdf = lottoDF.
        
        #pdf.plot(kind='barh',x='name',y='id',colormap='winter_r')

        fileOpen.close()
       

        #print(lottoRDD.collect())
            
lottoDataAnalysys = LottoDataAnal(startDate='2017-11-20')
#lottoDataAnalysys = LottoDataAnal()
lottoDataAnalysys.connection()