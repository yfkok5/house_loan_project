import streamlit as st
import pandas as pd
from forex_python.converter import CurrencyRates
import numpy_financial as npf
from newsapi import NewsApiClient
import requests
from datetime import datetime
from newsapi import NewsApiClient
import os
import nltk as nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import pandas as pd

from PIL import Image
image = Image.open('house.jpg')

st.image(image, caption='Time to Invest!')

st.header("Housing Market Sentiments")

st.write("Input Date for News Data, note that we could only fetch 1 month worth of news :)")

#creates an input for user

city = st.selectbox(
    'Housing News from which City?',
    ('Melbourne','Sydney', 'Brisbane', 'Darwin', 'Adelaide'))

st.write('You have selected housing market news for ',city)

news_from_date = st.date_input("Enter your date")

st.write('Sentiments/news from: ', news_from_date)

#converts datetime format to str
date_convert= news_from_date.strftime("%Y/%m/%d")

api_key='8e935984687a40f79f1adf1d3ebfd548'
url = "https://newsapi.org/v2/everything?q=" + city + "-house-prices&from=" + date_convert + "&apiKey=" + api_key
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

def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(news_df)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='house_price_news.csv',
     mime='text/csv',
 )