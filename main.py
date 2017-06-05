from urllib.request import urlopen
from bs4 import BeautifulSoup
import telepot
from pprint import pprint
import datetime
import pandas_datareader.data as web
import fix_yahoo_finance
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

#connecting to bot
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
#check for new msg  
    wholeresponses =  bot.getUpdates(offset=True)
    newresponse = bot.getUpdates(offset=True)[-1]
    get_upid = newresponse['update_id']    
#    pprint(newresponse)

#if new message is received, print"new msg" in console"
    if(get_upid != store_upid):
        print("new message")        
    else:
#        print("no new message")
        continue
    store_upid = get_upid       #store the ID

#check for normal chat/ group chat
    if 'message' in newresponse:    #normal chat?
        print("normal chat")
    #store the speaker's chat ID, name, message(stock code)
        p1.id = newresponse['message']['chat']['id']
        p1.firstname = newresponse['message']['chat']['first_name']
       

    #if this is new user's chat(/start), say hello!
        start_test = newresponse['message']['text']
        if(start_test=='/start'):
            send_start_msg(p1.id)
            continue 
    #store the msg  
        requestStock = newresponse['message']['text']
        plist.append(p1)
    else:                           #group chat?
        print("group chat")
    #store the speaker's chat ID, name, message(stock code)
        p1.id = newresponse['channel_post']['chat']['id']
        p1.firstname= newresponse['channel_post']['chat']['username']

    #if this is new user's chat(/start), say hello!
        start_test = newresponse['channel_post']['text']
        if(start_test=='/start'):
            send_start_msg(p1.id)
            continue 
    #store the msg  
        requestStock = newresponse['channel_post']['text']
        plist.append(p1)

#check for validity of stock code
    try: 
        result = web.get_data_yahoo(requestStock, start,)
    except:
        print("wrong input")    
        bot.sendMessage(p1.id, errorMsg)
        pass
        continue

#process the information of stock data
    resultshort = result.tail(1)  #store the most recent information of stock
    adjStock = resultshort['Adj Close'][0]   #select the Adjust Close price of stock
    Stock = str(adjStock)


#Crawling of Yahoo Finance website
    targetUrl = "http://finance.yahoo.com/quote/"+requestStock+"/?p="+requestStock
    html = urlopen(targetUrl).read()
    soup = BeautifulSoup(html,'html.parser')
    mktcapSoup = soup.findAll('td',attrs={'data-test':'MARKET_CAP-value'})
    perSoup = soup.findAll('td',attrs={'data-test':"PE_RATIO-value"})
    divsoup = soup.findAll('td',attrs={'data-test':"DIVIDEND_AND_YIELD-value"})
    #if speaker ask the index info(not stock info)
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

#Distribute the Stock info to user
    bot.sendMessage(p1.id, p1.firstname+', '
    + str(requestStock)+':  ' +'\n'+Stock+'\n'+'MarketCap: $'+mktcap+ ' / '
    + 'PER: '+ per + ' / ' + 'Dividend: '+ div )
#    print(plist[0].firstname)
#    except:
#        print("ERROR")
#        pass
