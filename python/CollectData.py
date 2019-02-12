import requests
from bs4 import BeautifulSoup

#id="contentRow843"
#<img src="/images/slotto_ball/5.gif">

def spider() :
    
    url = 'http://www.lottorich.co.kr/lotto/analysis/jackpot_number.html'
    params = {'start' : '1', 'end' : '843', 'lsort' : 'seq', 'lsort_type' : 'desc', 'type' : '0' }
    source_code = requests.post(url, data = params)
    source_code.encoding = 'euc-kr'
    plain_text = source_code.text
    print(source_code.encoding)
    #plain_text = open("e:/kiha/shDir/python/lotto.txt", "r", encoding='utf8')
    #soup = BeautifulSoup(plain_text, 'lxml')
    
    f = open("e:/kiha/shDir/python/lotto.txt", "w", encoding='utf8')
    f.write(plain_text)
    f.close()


    #for link in soup.select('h2 > a') :
    #        href = 'http://' + link.get("href")
    #        title = link.string
    #        print(href)
    #        print(title)

    #page += 1

spider()