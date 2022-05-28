from curses import keyname
from email.mime import image
from tkinter import CENTER
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time


st.snow()


# image=Image.open('cryp.jpeg')
# st.image(image,caption='Image taken from google',width=200)  
st.header("""
Crypto live EDA app""")


st.markdown("""
Using Coinmarketcap.com retrieving stats of the desired top N Crypto currencies
""")
col1 = st.sidebar
col2=st.container()


col1.header('Filters/Options')


##Data loader and scraper using beautiful soup

def scrape_data():
    parser=requests.get('https://coinmarketcap.com')
    BeautifulSoup()
    bsoup=BeautifulSoup(parser.content,'html.parser')

    data=bsoup.find('script',id='__NEXT_DATA__',type='application/json')
    all_coins={}
    all_coins_data=data.contents[0]
    all_coins_data=json.loads(all_coins_data)
    all_listings = all_coins_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    # print('listing 0 is ',all_listings[0])
    # print('listing 1 is ',all_listings[1])
    keys=all_listings[0]
    values=all_listings[1:]
    # print(keys)
    getidx=keys['keysArr']
    for lst in values:
        all_coins[lst[getidx.index('id')]]=str(lst[getidx.index('symbol')])
    # print(all_coins)

    coin_name=[]
    coin_symbol=[]
    market_cap=[]
    percentage_change_1hr=[]
    percentage_change_24hr=[]
    percentage_change_7d=[]
    price=[]
    vol_24hr=[]

    for lst in values:
      coin_name.append(lst[getidx.index('slug')])
      coin_symbol.append(lst[getidx.index('symbol')])
      price.append(lst[getidx.index('quote.USD.price')])

    #   price.append(lst[getidx.index(fquote.currency_price_unit.price')])
      percentage_change_1hr.append(lst[getidx.index('quote.USD.percentChange1h')])
      percentage_change_24hr.append(lst[getidx.index('quote.USD.percentChange24h')])
      percentage_change_7d.append(lst[getidx.index('quote.USD.percentChange7d')])
      market_cap.append(lst[getidx.index('quote.USD.marketCap')])
      vol_24hr.append(lst[getidx.index('quote.USD.volume24h')])
    print(coin_name)

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percentage_change_1hr
    df['percent_change_24h'] = percentage_change_24hr
    df['percent_change_7d'] = percentage_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = vol_24hr
    return df


df = scrape_data()



## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)
# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df_selected_coin)

st.download_button(
    label="Download above data as CSV",
    data=csv,
    file_name='All_Data.csv',
    mime='text/csv',
)







# col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

#---------------------------------#
# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)





with st.container():

    st.subheader('Bar plot of % Price Change')

    if percent_timeframe == '7d':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_7d'])
        st.write('*7 days period*')
        plt.figure(figsize=(10,30))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
        st.pyplot(plt)
    elif percent_timeframe == '24h':
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_24h'])
        st.write('*24 hour period*')
        plt.figure(figsize=(10,30))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
        st.pyplot(plt)
    else:
        if sort_values == 'Yes':
            df_change = df_change.sort_values(by=['percent_change_1h'])
        st.write('*1 hour period*')
        plt.figure(figsize=(10,30))
        plt.subplots_adjust(top = 1, bottom = 0)
        df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
        st.pyplot(plt)
    






# def test():

#     from requests import Request, Session
#     from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
#     import json

#     url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     parameters = {
#     'start':'1',
#     'limit':'5000',
#     'convert':'USD'
#     }
#     headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
#     }

#     session = Session()
#     session.headers.update(headers)

#     try:
#         response = session.get(url, params=parameters)
#         data = json.loads(response.text)
#         print(data)
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)
# test()

##About section (how to add it anywhere??)
expander_bar = st.expander("About")
expander_bar.markdown("""
Scraping data from Coinmarketcap using beautiful soup and designed an alert system 
""")

expander_bar = st.expander("How to Use")
expander_bar.markdown("""
1)use slider on the sidebox(left side bar) to select no of coins to display\n
2)Use filters to select required coins\n
3)sort if required

""")

# import telegram_send
# # telegram_send.send(messages=[text])
# df.to_csv('temp.csv')
# text='test'
# telegram_send.send(messages=[text])
# # telegram_send.send(image)
# telegram_send.send(files=["temp.csv"])
