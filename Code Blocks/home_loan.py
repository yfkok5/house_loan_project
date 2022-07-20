import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates

currency_dict = CurrencyRates()
c = CurrencyRates()

savings = st.sidebar.number_input("Excess Cashflow/Surplus Funds: ")

currency_option = st.sidebar.selectbox(
    'Which currency do you use?',
    ('EUR','JPY','BGN','CZK','DKK', 'GBP','HUF','PLN','RON','SEK','CHF','ISK','NOK','HRK','TRY','AUD','BRL','CAD','CNY',
    'HKD','IDR','INR','KRW','MXN','MYR','NZD','PHP','SGD','THB','ZAR'))

if st.sidebar.button("Display Savings"):
    st.sidebar.write(f"Current Savings Available: {currency_option} {savings}")

#converting savings from str to int
if st.sidebar.button("Convert Savings to AUD"):

    st.sidebar.write(f"Please wait while we convert {currency_option} to AUD...")
    savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')
    st.sidebar.write("Current Savings in AUD: ", round(savings_aud))


