import pandas as pd
import numpy as np
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db
from pykrx import stock

# Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('./mykey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kis-project-29909-default-rtdb.firebaseio.com/'
})

def get_tickers(idx):
  for ticker in stock.get_market_ticker_list(market="ALL"):
    name = stock.get_market_ticker_name(ticker).replace(".", "")
    ref = db.reference('tickers/' + str(idx))  # db 위치 지정, 기본 가장 상단을 가르킴
    ref.update({'label': name, 'subLabel': ticker, 'id': ticker})
    idx += 1
  for ticker in stock.get_etf_ticker_list():
    name = stock.get_etf_ticker_name(ticker).replace(".", "")
    ref = db.reference('tickers/' + str(idx))  # db 위치 지정, 기본 가장 상단을 가르킴
    ref.update({'label': name, 'subLabel': ticker, 'id': ticker})
    idx += 1
  print('finish')

def get_stock_data():
  for ticker in stock.get_market_ticker_list(market="ALL")[2445:]:
    stock_name = stock.get_market_ticker_name(ticker).replace(".", "")
    df = stock.get_market_ohlcv("20200101", "20230714", ticker)[['시가', '고가', '저가', '종가', '거래량']]
    df.drop(df[(df['거래량'] == 0)].index, inplace=True)
    df.reset_index(inplace=True)

    df_date = []
    for d in df['날짜']:
        df_date.append(pd.to_datetime(d).value)
    del df['날짜']
    df.insert(0, '날짜', df_date)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    js = df.to_dict(orient='index')
    ref = db.reference('data/' + ticker)
    ref.update({'id': ticker})
    ref.update({'name': stock_name})
    for i in range(len(js)):
        ref.update({i: js[i]})
    print(ticker, ' ', stock_name)

def get_etf_data():
  for ticker in stock.get_etf_ticker_list():
    stock_name = stock.get_etf_ticker_name(ticker).replace(".", "")
    df = stock.get_etf_ohlcv_by_date("20200101", "20230712", ticker)[['시가', '고가', '저가', '종가', '거래량']]
    df.drop(df[(df['거래량'] == 0)].index, inplace=True)
    df.reset_index(inplace=True)

    df_date = []
    for d in df['날짜']:
        df_date.append(pd.to_datetime(d).value)
    del df['날짜']
    df.insert(0, '날짜', df_date)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    js = df.to_dict(orient='index')
    ref = db.reference('data/' + ticker)
    ref.update({'id': ticker})
    ref.update({'name': stock_name})
    for i in range(len(js)):
        ref.update({i: js[i]})
    print(ticker, ' ', stock_name)

# idx = 0
# get_tickers(idx)
get_stock_data()
# get_etf_data()