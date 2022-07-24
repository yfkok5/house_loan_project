import streamlit as st
import pandas as pd
import numpy_financial as npf
from forex_python.converter import CurrencyRates

st.title('Property Investment Dashboard')
country_option = st.selectbox(
    'Which country are you from?',
    ("United States", "Europe","Japan","United Kingdown","Australia","Canada","Czech Republic","Bulgarian","Danmark","Hungary","China","Switzerland", "Sweden"))
st.write('You selected', country_option)

currency_dict = CurrencyRates()
c = CurrencyRates()

savings = st.number_input("Excess Cashflow/Surplus Funds: ")

currency_option = st.selectbox(
    'Which currency do you use?',
    ('EUR','JPY','BGN','CZK','DKK', 'GBP','HUF','PLN','RON','SEK','CHF','ISK','NOK','HRK','TRY','AUD','BRL','CAD','CNY',
    'HKD','IDR','INR','KRW','MXN','MYR','NZD','PHP','SGD','THB','ZAR'))

if st.button("Display Savings"):
    st.write(f"Current Savings Available: {currency_option} {savings}")

#converting savings from str to int
if st.button("Convert Savings to AUD"):

    st.write(f"Please wait while we convert {currency_option} to AUD...")
    savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')
    st.write(f"Current Savings Available: {round(savings_aud)} AUD")

st.write("Loan Calculator")

year_option = st.selectbox("Term of Loan", ('5', '10', '20', '30'))
interest_rate = st.write("Benchmark Interest Rate of 6%")
savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')

int_rate = 0.06
pmt_years = 12

if st.button("Determine Loan Amount"):
    st.write(f"Please wait while we calculate your maximum loan amount")
    loan_amount = npf.pv(int_rate/pmt_years, int(year_option) * pmts_year, (savings_aud)* -1)
    st.write("With a payment of: ${:,.0f".format(round(savings_aud)))
    st.write("You can borrow up to: ${:,.0f}".format(round(loan_amount)))



