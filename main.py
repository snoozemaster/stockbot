from urllib.request import urlopen
from bs4 import BeautifulSoup
import telepot
from pprint import pprint
import datetime
import pandas_datareader.data as web
import time

class Person:
    firstname = 'default'
    lastname = 'default'
    id = 'default'
    msg = 'default'
    def __init__(self):
        self.firstname = 'first'
        self.lastname = 'last'
        self.id = 0
        self.msg = 'stock'

def send_start_msg(_chat_id):
    bot.sendMessage(_chat_id, "Welcome to Soojin Stock")
    bot.sendMessage(_chat_id, "Please search the stock by its code (should be same as yahoo finance)")
    bot.sendMessage(_chat_id, "EX:Samsung Electronics: 005930.ks, Apple: aapl")

#봇 불러오기
bot = telepot.Bot('351258906:AAGdjeEa817a6AJAyAMok1FfYuO-htbtvxw')
bot.getMe()

start = datetime.datetime(2017,1,1)
store_upid = 1
get_upid = 0
errorMsg = 'Try other stocks'

chat_id = None
chatter_name = 'default name'

plist = []
p1 = Person()
plist.append(p1)

while(True):
#    try:
    time.sleep(1) 
#봇이 새로운 메세지 있는지 검사    
    wholeresponses =  bot.getUpdates(offset=True)
    newresponse = bot.getUpdates(offset=True)[-1]
    get_upid = newresponse['update_id']    
#    pprint(newresponse)

#새로운 메세지인지 검사하고, 새로운 메세지일 경우만 아래코드들 시행
    if(get_upid != store_upid):
        print("new message")        
    else:
#        print("no new message")
        continue
    store_upid = get_upid       #방금 방은ID store.

#일반챗과 단채쳇은 구조가 달라서 검사하고 진행
    if 'message' in newresponse:    #일반챗임?
        print("일반챗")
    #말건사람 챗아이디, 이름, stock 저장하기
        p1.id = newresponse['message']['chat']['id']
        p1.firstname = newresponse['message']['chat']['first_name']
       

    #새로운 사용자인지 검사, 인사하기
        start_test = newresponse['message']['text']
        if(start_test=='/start'):
            send_start_msg(p1.id)
            continue 
    #정보요청한 stock 저장하기    
        requestStock = newresponse['message']['text']
        plist.append(p1)
    else:                           #단체챗임?
        print("단체챗")
    #말건사람 챗아이디, 이름 저장하기
        p1.id = newresponse['channel_post']['chat']['id']
        p1.firstname= newresponse['channel_post']['chat']['username']

    #새로운 사용자인지 검사, 인사하기
        start_test = newresponse['channel_post']['text']
        if(start_test=='/start'):
            send_start_msg(p1.id)
            continue 
    #정보요청한 stock 저장하기    
        requestStock = newresponse['channel_post']['text']
        plist.append(p1)

#사용자가보낸 stock이 실제 있는지 검사, valid한 경우에만 아래코드 시행
    try: 
        result = web.DataReader(requestStock,'yahoo', start,)
    except:
        print("사용자가 잘못 입력함")    
        bot.sendMessage(p1.id, errorMsg)
        pass
        continue

#야후파이낸스에서 받아온 데이터 가공
    resultshort = result.tail(1)  #데이터리더에서 가장 최근일 stock정보만 불러오기
    adjStock = resultshort['Adj Close'][0]   #여기에 [0]이거 안붙이면 날짜랑 타입정보가 같이 들어가버림
    Stock = str(adjStock)


#야후파이낸스에서 시총 스크랩핑하기
    targetUrl = "http://finance.yahoo.com/quote/"+requestStock+"/?p="+requestStock
    html = urlopen(targetUrl).read()
    soup = BeautifulSoup(html,'html.parser')
    mktcapSoup = soup.findAll('td',attrs={'data-test':'MARKET_CAP-value'})
    perSoup = soup.findAll('td',attrs={'data-test':"PE_RATIO-value"})
    divsoup = soup.findAll('td',attrs={'data-test':"DIVIDEND_AND_YIELD-value"})
    #지수검색했을경우는 시총이 안뜸으로 예외처리 해줘야함
    try:
        mktcap = mktcapSoup[0].text
    except:
        print("No market cap data")
        mktcap = 'No market cap data'
        pass
    try:
        per = perSoup[0].text
    except:
        print("No PER data")
        per = 'No PER data'
        pass    
    try:
        div = divsoup[0].text
    except:
        print("No Div data")
        div = 'No Div data'
        pass

#완성된 데이타를 봇이 사용자에게 뿌림
    bot.sendMessage(p1.id, p1.firstname+', '
    + str(requestStock)+':  ' +'\n'+Stock+'\n'+'MarketCap: $'+mktcap+ ' / '
    + 'PER: '+ per + ' / ' + 'Dividend: '+ div )
#    print(plist[0].firstname)
#    except:
#        print("뭔가 에러남")
#        pass
