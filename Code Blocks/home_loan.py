from operator import index
import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import numpy_financial as npf

#Vinay added for geo location calculation using post code. So before running the code pip install pgeocode in dev environment.
import pgeocode
import time
import seaborn as sns
import pydeck as pdk

# Vinay's Code starts here
# This is for reading the CSV file that only has sold data plus append latitude and longitude data for each postcode, for dwelling calculation.   
@st.cache(allow_output_mutation=True)
def fetch_geo_data():
    housesold_df = pd.read_csv("../Code Blocks/Datasets/MELBOURNE_HOUSE_PRICES_SOLD.csv")
    nomi = pgeocode.Nominatim('au')
    housesold_df[['latitude', 'longitude']] = housesold_df.apply(lambda row: nomi.query_postal_code(row['Postcode'])[['latitude', 'longitude']], axis=1, result_type='expand')
    housesold_df = housesold_df.drop(columns= ['Unnamed: 0','Method','Date'])
    return housesold_df

# Vinay added the code to include session state for loan_amount, to be used in tabs for dwellings calculation
if 'loan_amount' not in st.session_state:
    st.session_state['loan_amount'] = 0
# Vinay's code ends here

st.set_page_config(layout="wide", page_title="Property Zone")

st.write("# Welcome to the Property Zone! 👋")

st.markdown(
    """
    Property Zone is an portal built specifically for
    people who want to get a view of properties meeting their budget.
    **👈 Enter the savings details** to get a view of what Property Zone can do!
"""
)

st.sidebar.write("Savings Details")

currency_dict = CurrencyRates()
c = CurrencyRates()

savings = st.sidebar.number_input(
    label="Enter the excess cashflow/surplus funds: ",
    min_value =500, 
    step=100,
    value=500,
)

currency_option = st.sidebar.selectbox(
    'Which currency do you use?',
    ('EUR','JPY','BGN','CZK','DKK', 'GBP','HUF','PLN','RON','SEK','CHF','ISK','NOK','HRK','TRY','AUD','BRL','CAD','CNY',
    'HKD','IDR','INR','KRW','MXN','MYR','NZD','PHP','SGD','THB','ZAR'),index=15)

#if st.sidebar.button("Display Savings"):
#    st.sidebar.write(f"Current Savings Available: {currency_option} {savings}")

#converting savings from str to int
if currency_option != 'AUD':

    if st.sidebar.button("Convert Savings to AUD"):

        st.sidebar.write(f"Please wait while we convert {currency_option} to AUD...")
        savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')

        if savings_aud < 1000:
            st.sidebar.write(f"Current Savings Available: {round(savings_aud)} AUD, you do not have enough excess cashflow!")
        else:
            st.sidebar.write(f"Current Savings Available: {round(savings_aud)} AUD")


st.sidebar.write("# Loan Calculator")

year_option = st.sidebar.selectbox('Term of Loan',('Select Loan Term','5', '10', '20', '30'))

Interest_rate = st.sidebar.write("Benchmark Interest Rate of 6%")
savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')

int_rate = 0.06
pmts_year = 12

if st.sidebar.button("Determine Loan Amount"):
    # Vinay's code starts here
    placeholder = st.empty()
    placeholder.text("Please wait while we calculate your maximum loan amount")
       
    my_bar = st.progress(0)
    for percent_complete in range(100):        
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    my_bar.empty()
    
    placeholder.text("Done!")    

    # Vinay's code ends here

    #loan_amount = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, (savings_aud) * -1)
    st.session_state['loan_amount'] = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, (savings_aud) * -1)
    st.write("With a payment of ${:,.0f} per month,".format(round(savings_aud)))
    #st.write("You can borrow up to ${:,.0f}".format(round(loan_amount)))
    #st.write(f"You can borrow up to ${st.session_state['loan_amount']}")
    st.write("You can borrow up to ${:,.0f}".format(round(st.session_state['loan_amount'])))

    tab1, tab2, tab3 = st.tabs(["Geolocation", "Dwellings Suggestions", "Housing Market Sentiments"])

    with tab1:
        st.header("Geolocation")
        st.write("LINK GEOLOCATION WITH MEDIAN HOUSE PRICE & POST CODE")
    
    with tab2:
        tab2.header("Dwellings Suggestions")
        tab2.write("Suggestions for best postcode to invest in")
        # Vinay's code starts here
        select_df = fetch_geo_data()
        select_df = select_df[select_df.Price <= st.session_state['loan_amount']]

        st.map(select_df)
        #st.dataframe(select_df)
        
        postcode_df = select_df.drop(columns= ['Propertycount','Distance','SellerG','latitude','longitude'])
        my_expander = st.expander(label='Expand me')
        with my_expander:
            st.write("Raw Data For Additional Information")
            cm = sns.light_palette("green", as_cmap=True)
            st.dataframe(postcode_df.style.background_gradient(cmap=cm).set_precision(2))
        
        # Vinay's code ends here

    with tab3:
        st.header("Housing Market Sentiments")
        st.write("Housing NEWS")

# Vinay's code starts here for clearing the session state to enable fresh calculation    
for key in st.session_state.keys():
    del st.session_state[key]
# Vinay's code ends here