from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.rdd import RDD
import sys
import re
import numpy as np

def dataParse(datas) :
    splitData = datas.split(',')
    #splitData = re.split(',(?=([^\"]*\"[^\"]*\")*[^\"]*$)', datas)
    
    lottoNo = int(splitData[0])
    date = splitData[1]
    winnerBalls = (splitData[2].split('|'))
    luckyBalls = set(map(lambda ball : int(ball), winnerBalls))
    #print("ceh")
    #print(luckyBalls)
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
    
    print((lottoNo, date, luckyBalls, bonusBall, firstWinnerPrice, firstWinnerNo, secondWinnerNo))
    return (lottoNo, date, luckyBalls, bonusBall, firstWinnerPrice, firstWinnerNo, secondWinnerNo)


w = open("e:/kiha/shDir/python/lottoDatas.txt", "r", encoding='utf8')
datas = w.readlines()
asd = np.median([1,4,8])
print([map(lambda a : a*2, [1,4,5])])
#print(type(asd))
#print(asd)
for idx, data in enumerate(datas):
    if idx > 0 :
        break
    dataParse(data)
w.close()

