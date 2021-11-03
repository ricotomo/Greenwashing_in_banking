# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

# Twitter authentication
result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds.csv')
print(result)
API_key=result.loc[0]['value']
API_Key_Secret=result.loc[1]['value']
Bearer_Token=result.loc[2]['value']

# consumerKey = “Type your consumer key here”
# consumerSecret = “Type your consumer secret here”
# accessToken = “Type your accedd token here”
# accessTokenSecret = “Type your access token secret here”auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
# auth.set_access_token(accessToken, accessTokenSecret)
# api = tweepy.API(auth)