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