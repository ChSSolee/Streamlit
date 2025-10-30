#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import FinanceDataReader as fdr
import matplotlib.pyplot as plt 
import koreanize_matplotlib
import datetime 
import numpy as np
import pandas as pd
import plotly.graph_objects as go




st.set_page_config(
    page_title = '주식 차트 대시보드',
    page_icon = '📈',
)

# 제목
st.title("📈 주식 차트 대시보드")


# 주식 시장 종목 선택 

market = st.sidebar.selectbox("주식시장을 선택하세요", ["KRX", "KOSPI", "KOSDAQ", "KONEX"])
df_market = fdr.StockListing(market)


# 주식 시장의 상위 10개의 종목 시가 총액 그래프 생성 
fig = go.Figure(data=go.Bar(x=(df_market['Marcap'][:10])[::-1],
                        y=(df_market['Name'][:10])[::-1],
                        orientation='h',
                        text=(df_market['Marcap'][:10])[::-1] / 1e12,
                        texttemplate='%{text:.0f} 조',
                        ))

# 레이아웃 설정
fig.update_layout(
    title=market + '시가 총액 TOP10',
    xaxis=dict(title='시가 총액 (조)'),
    yaxis=dict(title='종목명'),
    bargap=0.1)

st.plotly_chart(fig)


# 종목 선택 생성 
list_kospi = fdr.StockListing('KOSPI')
stocks = list_kospi['Name'].loc[:9].tolist()
stock = st.sidebar.multiselect('종목을 선택해주세요.', stocks) 

list_stock = [
    list_kospi['Code'][list_kospi['Name'] == s].values[0]
    for s in stock
]
list_stock = [s for s in list_stock if s and s.strip()]

# 시작일과 종료일 생성 
col1, col2 = st.columns(2)
with col1:
    start_date = st.sidebar.date_input('시작 날짜', datetime.date(2022,1,1))
with col2:
    end_date = st.sidebar.date_input('종료 날짜', datetime.datetime.now()-datetime.timedelta(days=1))

# 날짜를 문자열로 변환
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

if not list_stock:
    st.warning("📌 종목을 하나 이상 선택해주세요.")
    st.stop()  # 여기서 Streamlit 실행 중단
    
# 매트릭 생성 
for i in range(len(list_stock)):
    df_price = fdr.DataReader(list_stock[i], start_date_str, end_date_str)
    stock_value1 = df_price["Close"].iloc[-1]
    stock_value2 = df_price["Close"].iloc[-2]
    st.metric(label=f'{stock[i]}', value=f'{stock_value1}원', delta=f'{stock_value1 - stock_value2}원')


# Tab 생성 + 그래프 생성 
tab1, tab2 = st.tabs(['라인 그래프', '캔들스틱 그래프'])
with tab1:
    if len(list_stock) == 1:
        df = fdr.DataReader(list_stock[0], start_date_str, end_date_str)
        st.line_chart(df['Close'])
    else:
        df = fdr.DataReader('KRX:' + ','.join(list_stock), start_date_str, end_date_str)
        df.columns = stock
        st.line_chart(df)

with tab2:
    for i in range(len(list_stock)):
        df = fdr.DataReader(list_stock[i], start_date_str, end_date_str)
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                )
            ]
        )
        fig.update_layout(title_text=f'{stock[i]}', height=400)
        st.plotly_chart(fig, config={"displayModeBar": False})

                         
                         
                         
                         
