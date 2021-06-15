
import streamlit as st
import pandas as pd
import datetime
import requests

#url_correct = 'https://drive.google.com/uc?id=' + st.secrets['url'].split('/')[-2]
categories = ['Nocleg', 'Bilety', 'Transport', 'Rozrywka', 'Jedzenie']

def get_exchange(currency: str) -> float:
	response = requests.get(st.secrets['exchange_respone'])
	response = response.json()
	return response['rates'][currency]

ratePLN = get_exchange('PLN')


st.text('Holiday Tracker')

#data = pd.read_excel('st.secrets['drive_loc'])

data = pd.read_excel('holiday.xls')
#data = pd.read_excel(url_correct)
data = data[['Name', 'Category', 'Currency', 'Price']]
data['Price Conv'] = [x if y == 'PLN' else x * ratePLN for x,y in zip(data['Price'], data['Currency'])]

total = data['Price Conv'].sum()

data

st.text('Total Amount so far:')
total

cat_split = data.groupby(['Category'])['Price Conv'].sum()
st.bar_chart(cat_split, width = 800, use_container_width= False)

cost_name = st.text_input('Input next cost name')
cost_category = st.selectbox('Select Category', categories)
cost_currency = st.selectbox('Select Currency', ['PLN', 'EUR'])
cost_value = st.text_input('Input Cost')

if cost_category == 'EUR':
	cost_conv = cost_value * ratePLN
else:
	cost_conv = cost_value
if st.button('Confirm choice'):

	data = data.append({'Name' : cost_name, 'Category' : cost_category, 'Currency' : cost_currency, 'Price' : cost_value, 'Price Conv' : cost_conv}, ignore_index= True)
	#data.to_excel(st.secrets['drive_loc'])
	#data.to_excel(url_correct)
	data