# -*- coding: utf-8 -*-
"""
Created January 2021
@author: Sirlene Andreis
"""
import streamlit as st 
import numpy as np
import pandas as pd 
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode,iplot, plot
import os


st.cache(persist=True)
st.title('💉😷 Track COVID-19 numbers Worldwide!')

   
def load_data():
    covid19 = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv',encoding='UTF-8', engine='python')
    covid19['date'] = pd.to_datetime(covid19['date'],format = '%Y-%m-%d')
    return covid19
covid19 = load_data()


###################################################################################

covid19['new_tests'] = covid19['new_tests'].replace(np.nan, '')
covid19['new_cases'] = covid19['new_cases'].replace(np.nan, '')
covid19['new_deaths'] = covid19['new_deaths'].replace(np.nan, '')
covid19['new_vaccinations'] = covid19['new_vaccinations'].replace(np.nan, '')
covid19['total_cases'] = covid19['total_cases'].replace(np.nan, '')
covid19['total_vaccinations'] = covid19['total_vaccinations'].replace(np.nan, '')
covid19['people_fully_vaccinated'] = covid19['people_fully_vaccinated'].replace(np.nan, '')
covid19['total_deaths'] = covid19['total_deaths'].replace(np.nan, '')

#######################################################################################


st.write('**Choose a country to Visualize COVID-19 numbers :**')

country = st.selectbox("Choose a country",covid19["location"].unique())

st.header(f"Select the data of your interesse to visualize for {country}")
daily = st.selectbox("Select the option",('Daily New Cases','Daily New Vaccinations', 'Daily New Deaths', 'Daily New Tests', 
'Total Cases', 'Total Deaths', 'Total Vaccinations'))
typ = st.radio("Select the type of Chart",("Line Chart","Scatter Chart"))


vaccine = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date", y="new_vaccinations", tooltip=["date:T","location:N","new_vaccinations:Q"]).interactive()

new_cases = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="new_cases",tooltip=["date:T","location:N","new_cases:Q"]).interactive()

new_tests = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="new_tests",tooltip=["date:T","location:N","new_tests:Q"]).interactive()

new_deaths = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="new_deaths",tooltip=["date:T","location:N","new_deaths:Q"]).interactive()

t_cases = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="total_cases",tooltip=["date:T","location:N","total_cases:Q"]).interactive()

t_deaths = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="total_deaths",tooltip=["date:T","location:N","total_deaths:Q"]).interactive()

t_vaccinations = alt.Chart(covid19[covid19["location"]==country]).encode(
    x="date",y="total_vaccinations",tooltip=["date:T","location:N","total_vaccinations:Q"]).interactive()

cases= alt.Chart(covid19[covid19["location"]==country],title="Scatter Chart",width=500,height=400).mark_circle(color='green').encode( 
    x ="date",
    y ="total_cases",
    size ="total_deaths",
    color ="total_vaccinations",
    tooltip=["date:T","location:N", "total_cases:Q","total_deaths:Q","total_vaccinations:Q"]
    ).interactive()



if daily =='Daily New Cases':
    if typ == 'Line Chart':
        st.altair_chart(new_cases.mark_line(color='firebrick'))
    else:
        st.altair_chart(new_cases.mark_circle(color='firebrick'))
elif daily =='Total Vaccinations':
    if typ == 'Line Chart':
        st.altair_chart(t_vaccinations.mark_line(color='green'))
    else:
        st.altair_chart(t_vaccinations.mark_circle(color='green'))
elif daily =='Daily New Deaths':
    if typ == 'Line Chart':
        st.altair_chart(new_deaths.mark_line(color='purple'))
    else:
        st.altair_chart(new_deaths.mark_circle(color='purple'))
elif daily =='Total Deaths':
    if typ == 'Line Chart':
        st.altair_chart(t_deaths.mark_line(color='yellow'))
    else:
        st.altair_chart(t_deaths.mark_circle(color='yellow'))
elif daily =='Total Cases':
    if typ == 'Line Chart':
        st.altair_chart(t_cases.mark_line(color='orange'))
    else:
        st.altair_chart(t_cases.mark_circle(color='orange'))
elif daily =='New Tests':
    if typ == 'Line Chart':
        st.altair_chart(new_tests.mark_line(color='red'))
    else:
        st.altair_chart(new_tests.mark_circle(color='red'))


'Visualizing Total Cases, Total Deaths and Total Vaccinations in a Single Chart'
'In Scatter Chart, **Circle** represent Daily New Cases, size of the circle shows the daily New Deaths and the color variation shows the Total Vaccinations'
st.altair_chart(cases)

#################################################################################################



###########################################################################################################################
st.sidebar.markdown('**COVID-19 Dashboard**')
st.sidebar.markdown('''
🗂️ Data on COVID-19 vaccination, cases, deaths, tests and vaccinations.

• Updated daily by Our World in Data www.ourworldindata.org/coronavirus.

• All the charts are interactive you can select the different options to vary the Visualization.

• Scroll the mouse over the charts to see the different interactions available.

**Stable URLs**

The `/public` path of this repository is hosted at `https://covid.ourworldindata.org/`.

This data has been collected, aggregated, and documented by Cameron Appel, Diana Beltekian, Daniel Gavrilov, 
Charlie Giattino, Joe Hasell, Bobbie Macdonald, Edouard Mathieu, Esteban Ortiz-Ospina, Hannah Ritchie, Max Roser.''')


#############################################################################################################################
trace1 = go.Scatter(
    x=covid19.groupby(['date'])['date'].apply(lambda x: np.unique(x)[0]),
    y=covid19.groupby(['date'])['new_tests_smoothed'].sum().astype(int),
        xaxis='x2',
    yaxis='y2',
    name = "new tests smoothed")
    
trace2 = go.Scatter(
    x=covid19.groupby(['date'])['date'].apply(lambda x: np.unique(x)[0]),
    y=covid19.groupby(['date'])['new_deaths_smoothed'].sum().astype(int),
    name = "new deaths smoothed")

trace3 = go.Scatter(
    x=covid19.groupby(['date'])['date'].apply(lambda x: np.unique(x)[0]),
    y=(covid19.groupby(['date'])['positive_rate'].mean() * 100).round(3),
    xaxis='x3',
    yaxis='y3',
    name = "test positive rate %")

trace4 = go.Scatter(
    x=covid19.groupby(['date'])['date'].apply(lambda x: np.unique(x)[0]),
    y=covid19.groupby(['date'])['new_cases_smoothed'].sum().astype(int),
    xaxis='x4',
    yaxis='y4',
    name = "new cases smoothed")

data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    xaxis=dict(domain=[0, 0.45]),
    yaxis=dict(domain=[0, 0.45]),
    xaxis2=dict(domain=[0.55, 1]),
    xaxis3=dict(domain=[0, 0.45],
        anchor='y3'),
    xaxis4=dict(domain=[0.55, 1],
        anchor='y4'),
    yaxis2=dict(domain=[0, 0.45],
        anchor='x2'),
    yaxis3=dict(domain=[0.55, 1]),
    yaxis4=dict(domain=[0.55, 1],
        anchor='x4'),
   
    title = 'New tests, deaths, cases and test positive rate',
    width = 1000,
    height = 800)
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

######################################################################################


st.header(f"View the Dataset by Month")

if st.checkbox("Click to View the Dataset",False):
    "Select the Month from Slider"
    nc = st.slider("Month",1,12)
    covid19 = covid19[covid19["date"].dt.month ==nc]
    "data", covid19