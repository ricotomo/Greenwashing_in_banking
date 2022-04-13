# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
import string
import re
import emoji
import demoji
from textblob import TextBlob
import iso8601
pd.set_option('display.max_colwidth', 100)

def remove_usernames(text):
    #print(text)
    try:
        str(text)
        text = re.sub('@[\w]+','',text)
    except:
        return text
    return text

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

def tokenization(text):
    text = re.split('\W+', text)
    return text

stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text

ps = nltk.PorterStemmer()

def stemming(text):
    text = [ps.stem(word) for word in text]
    return text

wn = nltk.WordNetLemmatizer()

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text

def demojize(text):
    # text.decode("unicode-escape")
    # text = emoji.demojize(text) 
    # text.encode('utf-8')
    text = demoji.replace_with_desc(text , " ")
    return text

def remove_links(text):
    text = re.sub(r"http\S+", "",text)
    return text

def byte_to_string(text):
    text = bytes(text, 'utf-8')
    return text

def spell_correct(text):
    text = TextBlob(text).correct()
    return text

def to_year(text):
    year = iso8601.parse_date(text).year
    return year

def standardize_names(text):
    dict={"Westpac": "Westpac Banking Corp", "Wells Fargo": "Wells Fargo & Co", "Standard Chartered":"Standard Chartered PLC","Schroders":"Schroders PLC",
    "National Australia Bank":"National Australia Bank Ltd","Lloyds Banking Group":"Lloyds Banking Group PLC","JP Morgan Chase":"JPMorgan Chase & Co","HSBC":"HSBC Holdings PLC",
        "HDFC Bank":"HDFC Bank Ltd","Goldman Sachs":"Goldman Sachs Group Inc","DBS Bank":"DBS Group Holdings LTD","Commonwealth Bank":"Commonwealth Bank of Australia",
        "Close Brothers":"Close Brothers Group PLC","Citigroup":"Citigroup Inc","Charles Schwab":"Charles Schwab Corp","Capital One":"Capital One Financial Corp",
        "Barclays":"Barclays PLC", "Scotiabank":"Bank of Nova Scotia", "Bank of America":"Bank of America Corp", "Santander":"Banco Santander SA "
        , "Australia and New Zealand Banking Group":"Australia and New Zealand Banking Group Ltd", "The Bank of New York Mellon":"Bank of New York Mellon Corp"}
    if text in dict:
        name = dict[text]
    else:
        name = text
    return name