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

# set creds
result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds.csv')
print(result)
CONSUMER_KEY=result.loc[0]['value']
CONSUMER_SECRET=result.loc[1]['value']
Bearer_Token=result.loc[2]['value']
ACCESS_TOKEN=result.loc[3]['value']
ACCESS_TOKEN_SECRET=result.loc[4]['value']
print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_TOKEN)
print(ACCESS_TOKEN_SECRET)


# Utility function to clean tweet text by removing links, special characters
# using simple regex statements.
def clean_tweet(self, tweet):       
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

# Authenticate to Twitter
try:
    # create OAuthHandler object
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    # set access token and secret
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    # Create API object
    api = tweepy.API(auth)
    print(api.verify_credentials().name)
except:
    print("Error: Authentication Failed")
    

#Get data
keyword = "lockdown2london"
noOfTweets = int(5)
tweets = tweepy.Cursor(api.search_tweets(q=keyword, count=noOfTweets))

for tweet in tweets:
 print(tweet.text)


 # creating object of TwitterClient Class
    # api = TwitterClient()
    # # calling function to get tweets
    # tweets = api.get_tweets(query = 'Donald Trump', count = 200)

# call twitter api to fetch tweets
# fetched_tweets = self.api.search(q = query, count = count)