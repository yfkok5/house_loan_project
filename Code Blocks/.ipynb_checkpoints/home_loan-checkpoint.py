import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import numpy_financial as npf

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


int_rate = 0.06
pmts_year = 12



st.write("Loan Calculator")
year_option = st.selectbox('Term of Loan',('5', '10', '20', '30'))
Interest_rate = st.write("Benchmark Interest Rate of 6%")

if st.button("Determine Loan Amount"):

    st.write(f"Please wait while we calculate your maximum loan amount")
    loan_amount = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, savings_aud * -1)
    st.write("With a payment of ${0:,.2f}, you can borrow ${1:,.2f}.".format({savings_aud}, loan_amount))







