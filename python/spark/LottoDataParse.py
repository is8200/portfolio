from bs4 import BeautifulSoup

f = open("e:/kiha/python/lotto/lotto.txt", "r", encoding='utf8')

soup = BeautifulSoup(f, 'lxml')

soup.find('div', {'id' : 'ex_id'})
f.close()
totalList = []
dataList = []
for idx in range(1, 844):
    print(idx)
    tr = soup.select('#contentRow' + str(idx))[0]
    tempData = []    
    tempCollection = {}

    tdCollection = tr.select('tr > td')
    tempCollection['no'] = tdCollection[1].text.replace('회', '').strip()
    tempData.append(tdCollection[1].text.replace('회', '').strip())
    tempCollection['date'] = tdCollection[2].text.strip()
    tempData.append(tdCollection[2].text.strip())

    luckyBalls = []
    bonusBall = 0
    for indx, img in enumerate(tr.select('img')):
        #print(img['src'])
        #no가 여러개 되게 처리 
        no = img['src'].replace('.gif', '').replace('/images/slotto_ball/', '')
        if indx == 6 :
            bonusBall = no    
        elif indx != 7:
            luckyBalls.append(no)
            
    tempCollection['luckyBalls'] = luckyBalls
    tempData.append('|'.join(luckyBalls))
    tempCollection['bonusBall'] = bonusBall
    tempData.append(bonusBall)
    tempCollection['firstWinnerPrice'] = tdCollection[5].text.replace('원', '').replace(',', '').strip()
    tempData.append(tdCollection[5].text.replace('원', '').replace(',', '').strip())

    firstWinnerNo = tdCollection[6].text.replace('명', '').strip()
    secondWinnerNo = tdCollection[7].text.replace('명', '').strip()
    
    tempCollection['firstWinnerNo'] = firstWinnerNo
    tempData.append(firstWinnerNo)
    tempCollection['secondWinnerNo'] = secondWinnerNo
    tempData.append(secondWinnerNo)

    totalList.append(tempCollection)
    
    dataRecord = ",".join(tempData)
    dataList.append(dataRecord)
    # 0번 없음. 1번 회차, 2번 날짜, 3번 > img 1등번호, 4 > img 보너스번호, 5 일등상금, 6 일등명수, 7. 2등명수, 
        



w = open("e:/kiha/python/lotto/lottoDatas.txt", "w", encoding='utf8')
w.write('\n'.join(dataList))
w.close()

print(totalList)