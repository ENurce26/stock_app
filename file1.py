import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import os




while (True):
    #find the content
    def web_content_div(web_content, class_path, value):
        web_content_div = web_content.find_all('div', {'class': class_path})
        try:
            if value != 'None':
                spans = web_content_div[0].find_all(value)
                texts = [span.get_text() for span in spans]
            else:
                texts = []
                '''
                text = web_content_div[0].get_text("|", strip=True)
                text= text.split("|")
                text=[-1]
                '''

        except IndexError:
            texts = []

        return texts
    
    #gather data from site using beautiful soup parser
    def real_time_price(stock_code):
        Error = 0
        url = 'https://finance.yahoo.com/quote/' + stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0'}
            r = requests.get(url, headers = headers) #(url,headers = headers)
            web_content = BeautifulSoup(r.text, 'lxml')
            texts = web_content_div(web_content, 'D(ib) Mend(20px)', 'fin-streamer')

            #Price and Price Change
            if texts != []:
                price, change = texts[0], texts[1] + '' + texts[2]
            else:
                price, change = [], []
                Error = 1

            #Volume
            if stock_code[-2:] == '=F':
                #search right hand side table, if a future
                texts = web_content_div(web_content,"D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)" 
                                        ,'fin-streamer')
            else: #search left hand side table, regular stock
                texts = web_content_div(web_content,'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)' 
                                        ,'fin-streamer')
            
            if texts != []:
                volume = texts[0]
            else:
                Error = 1
                volume = []
            
            #1y Target Est
            texts = web_content_div(web_content, "D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)"
                                    ,'None')
            
            if texts != []:
                if stock_code[-2:] == '=F':
                    one_year_target = [] #futures dont have a 1yr estimate
                else: #stocks do, so store texts
                    one_year_target = texts
            else:
                Error = 1
                one_year_target = []

            
        except(ConnectionError):
            price, change, volume, latest_pattern, one_year_target = [],[],[],[],[]
            Error = 1
            print('Connection Error')

        latest_pattern = []

        return price, change, volume, latest_pattern, one_year_target, Error
    
    Stock = ['ES=F', 'AAPL']



#RUN
    while(True):
        info = []
        for stock_code in Stock:
            stock_price, change, volume, latest_pattern, one_year_target, Error = real_time_price(stock_code)
            info.append(stock_price)
            info.append([change])
            info.append([volume])
            info.append([latest_pattern])
            info.append([one_year_target])
            print(info)
        if Error != 0:
            break
        
        '''
        time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        col = [time_stamp]
        col.extend(info)
        df = pd.DataFrame(col)
        df = df.T

        path = ?
        path += str(time_stamp[0:11] + "stock data.csv")

        df.to_csv(path, mode='a', header=False)
        '''
        
