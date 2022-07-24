import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import numpy_financial as npf

st.sidebar.write("Savings Details")

currency_dict = CurrencyRates()
c = CurrencyRates()

savings = st.sidebar.number_input(
    label="Excess Cashflow/Surplus Funds: ",
    min_value =500, 
    step=100,
    value=500,
)

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

    if savings_aud < 1000:
        st.sidebar.write(f"Current Savings Available: {round(savings_aud)} AUD, you do not have enough excess cashflow!")
    else:
        st.sidebar.write(f"Current Savings Available: {round(savings_aud)} AUD")


st.sidebar.write("Loan Calculator")

year_option = st.sidebar.selectbox('Term of Loan',('Select Loan Term','5', '10', '20', '30'))

Interest_rate = st.sidebar.write("Benchmark Interest Rate of 6%")
savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')

int_rate = 0.06
pmts_year = 12

if st.sidebar.button("Determine Loan Amount"):
    st.sidebar.write(f"Please wait while we calculate your maximum loan amount")
    loan_amount = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, (savings_aud) * -1)
    st.write("With a payment of ${:,.0f} per month,".format(round(savings_aud)))
    st.write("You can borrow up to ${:,.0f}".format(round(loan_amount)))

tab1, tab2, tab3 = st.tabs(["Geolocation", "Dwellings Suggestions", "Housing Market Sentiments"])

with tab1:
    st.header("Geolocation")
    st.write("LINK GEOLOCATION WITH MEDIAN HOUSE PRICE & POST CODE")

with tab2:
    st.header("Dwellings Suggestions")
    st.write("Suggestions for best postcode to invest in")

with tab3:
    st.header("Housing Market Sentiments")
    st.write("Housing NEWS")
