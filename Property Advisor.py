import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title('Property Investment/Buying Advisor')
st.markdown('The dashboard will advise areas and properties based on the affordability')
st.markdown('Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.’. This app gives you the real-time impact analysis of Confirmed, Deaths, active, and recovered cases of COVID-19')
st.sidebar.title('Visualization Selector')
st.sidebar.markdown('Select the Charts/Plots accordingly:')

DATA_URL=('E:\Data science Projects\NIELIT project\covid_19_world.csv')
@st.cache(persist=True) #( If you have a different use case where the data does not change so very often, you can simply use this)

def load_data():
    data=pd.read_csv(DATA_URL)
    return data

covid_data=load_data()