
import streamlit as st
import pandas as pd
import datetime
import requests
import dropbox
import io
categories = ['Nocleg', 'Bilety', 'Transport', 'Rozrywka', 'Jedzenie']
dbx = dropbox.Dropbox(st.secrets['dropbox_token'])
file = '/holiday.xls'


def get_exchange(currency: str) -> float:
	response = requests.get(st.secrets['exchange_respone'])
	response = response.json()
	return response['rates'][currency]

def read_dropbox(dbx, file):
    _, f = dbx.files_download(file)
    with io.BytesIO(f.content) as stream:
           df = pd.read_excel(stream, index_col=0)
    return df

def upload_dropbox(dbx, df):
	with io.BytesIO() as stream:
		with pd.ExcelWriter(stream) as writer:
			df.to_excel(writer)
			writer.save()
		stream.seek(0)
		dbx.files_upload(stream.getvalue(), '/holiday.xls', mode= dropbox.files.WriteMode.overwrite)

ratePLN = get_exchange('PLN')

data = read_dropbox(dbx, file)
data = data[['Name', 'Category', 'Currency', 'Price']]
data['Price Conv'] = [x if y == 'PLN' else x * ratePLN for x,y in zip(data['Price'], data['Currency'])]
total = data['Price Conv'].sum()
cat_split = data.groupby(['Category'])['Price Conv'].sum()

st.text('Holiday Tracker')
data
st.text('Total Amount so far:')
total
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
	#dbx.files_upload(data.to_excel('holiday.xls'), '/holiday,xls', mode = dropbox.files.WriteMode.overwrite)
	upload_dropbox(dbx, data)
	data