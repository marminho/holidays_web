
import streamlit as st
import pandas as pd
import datetime
import requests



ratePLN = get_exchange('PLN')

categories = ['Nocleg', 'Bilety', 'Transport', 'Rozrywka', 'Jedzenie']

st.text('Holiday Tracker')


data = data[['Name', 'Category', 'Currency', 'Price']]
data['Price Conv'] = [x if y == 'PLN' else x * ratePLN for x,y in zip(data['Price'], data['Currency'])]

total = data['Price Conv'].sum()

data

st.text('Total Amount so far:')
total

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

	data