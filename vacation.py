import streamlit as st
import pandas as pd
import datetime
import requests
import dropbox
import io
import openpyxl

categories = ['Nocleg', 'Bilety', 'Transport', 'Rozrywka', 'Jedzenie']
dbx = dropbox.Dropbox(st.secrets['dropbox_token'])
file = '/holiday.xls'
columns = ['Name', 'Category', 'Currency', 'Paid?', 'Price']
def get_exchange(currency: str) -> float:
	response = requests.get(st.secrets['exchange_respone'])
	response = response.json()
	return response['rates'][currency]

def read_dropbox(dbx, file):
    _, f = dbx.files_download(file)
    with io.BytesIO(f.content) as stream:
           df = pd.read_excel(stream, index_col=0)
    return df

def upload_dropbox(dbx, df, file):
	with io.BytesIO() as stream:
		with pd.ExcelWriter(stream) as writer:
			df.to_excel(writer)
			writer.save()
		stream.seek(0)
		dbx.files_upload(stream.getvalue(), file, mode= dropbox.files.WriteMode.overwrite)

#ratePLN = get_exchange('PLN')
ratePLN = 4.55
data = read_dropbox(dbx, file)

data = data[columns]
data['Price Conv'] = [x if y == 'PLN' else x * ratePLN for x,y in zip(data['Price'], data['Currency'])]
total = data['Price Conv'].sum()
cat_split = data.groupby(['Category'])['Price Conv'].sum()
total_paid = data[data['Paid?'] == 'Yes']
total_paid = total_paid['Price Conv'].sum()

total_unpaid = data[data['Paid?'] == 'No']
total_unpaid = total_unpaid['Price Conv'].sum()

st.text('Holiday Tracker')
st.button('Refresh')
data
st.text('Total Amount so far:')
total
st.text('Total Paid Amount so far:')
total_paid
st.text('Total Unpaid Amount so far:')
total_unpaid
st.bar_chart(cat_split, width = 800, use_container_width= False)

with st.form('Inputs'):

	cost_name = st.text_input('Input next cost name')
	cost_category = st.selectbox('Select Category', categories)
	cost_currency = st.selectbox('Select Currency', ['PLN', 'EUR'])
	cost_value = st.text_input('Input Cost')
	cost_paid = st.selectbox('Is it paid already?', ['Yes', 'No'])

	if cost_category == 'EUR':
		cost_conv = cost_value * ratePLN
	else:
		cost_conv = cost_value

	if st.form_submit_button('Confirm choice'):
		if cost_name in list(data['Name'].values):
			data = data.drop(index = data.index[data['Name'] == cost_name])
		data = data.append({'Name' : cost_name, 'Category' : cost_category, 'Currency' : cost_currency, 'Paid?' : cost_paid, 'Price' : cost_value, 'Price Conv' : cost_conv}, ignore_index= True)
		upload_dropbox(dbx, data, file)
		data
