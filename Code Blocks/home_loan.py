from operator import index
import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import numpy_financial as npf
import requests


from newsapi import NewsApiClient
import requests
import datetime
from newsapi import NewsApiClient
import nltk as nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
<<<<<<< HEAD

=======
>>>>>>> da0cbb682e1bac4c7e1a931f7d94ac4a4191d2e8

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

# Start of Sams Code
st.sidebar.write("# Loan Calculator")

year_option = st.sidebar.selectbox('Term of Loan',('Select Loan Term','5', '10', '20', '30'))

Interest_rate = st.sidebar.write("Benchmark Interest Rate of 6%")
savings_aud = int(savings) * c.get_rate(currency_option, 'AUD')

int_rate = 0.06
pmts_year = 12

#End of Sams Code

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

    #Sam's Code:
    #loan_amount = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, (savings_aud) * -1)
    st.session_state['loan_amount'] = npf.pv(int_rate/pmts_year, int(year_option)*pmts_year, (savings_aud) * -1)
    st.write("With a payment of ${:,.0f} per month,".format(round(savings_aud)))
    #st.write("You can borrow up to ${:,.0f}".format(round(loan_amount)))
    #st.write(f"You can borrow up to ${st.session_state['loan_amount']}")
    st.write("You can borrow up to ${:,.0f}".format(round(st.session_state['loan_amount'])))

    tab1, tab2, tab3 = st.tabs(["Geolocation", "Dwellings Suggestions", "Housing Market Sentiments"])

    with tab1:
        st.header("Geolocation")

        df = fetch_geo_data()
        df = df[df.Price <= st.session_state['loan_amount']]

        #st.dataframe(select_df)

        # Show State by Lat and Lon
        st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
         latitude=-37.8136,
         longitude=144.946457,
         zoom=11,
         pitch=50,
        ),

        layers=[
        # Add in Layer 1
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[longitude, latitude]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),

         # Add in Layer 2
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[longitude, latitude]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
    ))
        my_expander = st.expander(label='Expand me')
        with my_expander:
            st.write("Raw Data For Additional Information")
            cm = sns.light_palette("green", as_cmap=True)
            st.dataframe(df.style.background_gradient(cmap=cm).set_precision(2))
        
    #End of Sams Code


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
        news_from_date = "2022-06-27"

        api_key='8e935984687a40f79f1adf1d3ebfd548'
        url = "https://newsapi.org/v2/everything?q=melbourne-house-prices&from="+news_from_date+"&apiKey="+api_key
        news = requests.get(url).json()

        news_article = list(range(0,10))

        news_raw = []
        a = news["articles"]

        for each_news in news_article:
            news_raw.append(a[each_news])

        title = []
        description = []
        date = []
        date_format=[]

        for i in news_article:
            title.append(news_raw[i]['title'])
            description.append(news_raw[i]['description'])
            date.append(news_raw[i]['publishedAt'])

        #change date format
        for j in range(0,len(date)):
            date_format.append(date[j][0:10])

        news = {"Published_Date": date_format,"News_Headline": title, "News_Content": description}

        news_df = pd.DataFrame(data=news)
        st.dataframe(news_df)
        
        # Instantiate the lemmatizer
        lemmatizer = WordNetLemmatizer()

        # Create a list of stopwords
        sw = set(stopwords.words('english'))

        def tokenizer(text):
            """Tokenizes text."""
        
            # Create a list of the words
            sw = set(stopwords.words('english'))
            # Convert the words to lowercase
            regex = re.compile("[^a-zA-Z ]")
            # Remove the punctuation
            re_clean = regex.sub('', text)
            # Remove the stop words
            words = word_tokenize(re_clean)
            # Lemmatize Words into root words
            lem = [lemmatizer.lemmatize(word) for word in words]
            tokens = [word.lower() for word in lem if word.lower() not in sw]
        
            #return non list tokens so word cloud would work
            return ' '.join([str(tokens) for element in tokens])
        
        news_df['headline_tokens'] = news_df['News_Headline'].apply(tokenizer)

        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        plt.style.use('seaborn-whitegrid')
        import matplotlib as mpl
        st.set_option('deprecation.showPyplotGlobalUse', False)
        
        mpl.rcParams['figure.figsize'] = [20.0, 10.0]

        news_text = ' '.join(news_df.headline_tokens)
        wc = WordCloud().generate(news_text)
        plt.imshow(wc)
        plt.show()
        st.pyplot()

# Vinay's code starts here for clearing the session state to enable fresh calculation    
for key in st.session_state.keys():
    del st.session_state[key]
# Vinay's code ends here
