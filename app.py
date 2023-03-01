import streamlit as st
import pandas as pd
import plotly_express as px

cars = pd.read_csv('vehicles_us.csv')

cars['manufacturer'] = cars['model'].apply(lambda x: x.split()[0])

color = cars.groupby(['paint_color']).median().drop(['model_year','cylinders','is_4wd'], axis='columns')
color = color.reset_index()

brand_price = cars.groupby('manufacturer').median().sort_values(by='price', ascending= False).drop({'model_year','cylinders','is_4wd','days_listed','odometer'}, axis='columns').reset_index()

st.header('Data Viewer')

st.dataframe(cars)

st.header('Vehicle Price by Manufacturer')

fig = px.histogram(brand_price, x='manufacturer', y = 'price')

st.write(fig)

st.header('Histogram of Paint Color vs Days Listed.')

fig = px.histogram(color, x='paint_color', y = 'days_listed', color_discrete_sequence =['green']*len(color),  labels={'x': 'Paint Color', 'y':'Selling Price'})
st.write(fig)

st.header('Histogram of Paint Color vs Price.')

fig = px.histogram(color, x='paint_color', y = 'price', color_discrete_sequence =['yellow']*len(color))
st.write(fig)

st.header('Compare price distribution of two manufacturers')

manufac_list = sorted(cars['manufacturer'].unique())

manufacturer_1 = st.selectbox(label='Select Manufacturer 1',
                                options= manufac_list,
                                index = manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox(label='Select Manufacturer 2',
                                options= manufac_list,
                                index = manufac_list.index('ford'))

#mask_filter = (cars['manufacturer'] == manufacturer_1) | (cars['manufacturer'] == manufacturer_2)
cars_filtered = cars[(cars['manufacturer'] == manufacturer_1) | (cars['manufacturer'] == manufacturer_2)]

normalize = st.checkbox(label='Normalize histogram', value = True)
if normalize:
    histnorm1 = 'percent'
else:
    histnorm1 = None

fig = px.histogram(cars_filtered, x='price', nbins = 30, color='manufacturer', histnorm = histnorm1, barmode = 'overlay')

st.write(fig)


