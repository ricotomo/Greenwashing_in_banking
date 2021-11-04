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
import time

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
#choose API version
vers=2

# set creds
if vers==1.1:
    result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds1.1.csv')
else:
    result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds.csv')
print(result)
CONSUMER_KEY=result.loc[0]['value']
CONSUMER_SECRET=result.loc[1]['value']
BEARER_TOKEN=result.loc[2]['value']
ACCESS_TOKEN=result.loc[3]['value']
ACCESS_TOKEN_SECRET=result.loc[4]['value']
# print(CONSUMER_KEY)
# print(CONSUMER_SECRET)
# print(ACCESS_TOKEN)
# print(ACCESS_TOKEN_SECRET)


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
    print("Authentication successfull")
    print(api.verify_credentials().name)
    # client = tweepy.Client(BEARER_TOKEN, wait_on_rate_limit=True)
except:
    print("Error: Authentication Failed")
    

#Get data
tweets_array = []
keyword = "Tweepy"
noOfTweets = int(5)
date_since="2021-10-20"


# #attempt with tweepy 4.3.0
for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(noOfTweets):
    tweets_array.append(tweet.text)

for tweet in tweets_array:
 print(tweet)



 # creating object of TwitterClient Class
    # api = TwitterClient()
    # # calling function to get tweets
    # tweets = api.get_tweets(query = 'Donald Trump', count = 200)

# call twitter api to fetch tweets
# fetched_tweets = self.api.search(q = query, count = count)


# for status in tweepy.Cursor(api.search_tweets, q=keyword,
#                             count=100).items(10):
#     print(status.text)

# for page in tweepy.Cursor(api.get_followers, screen_name="TwitterDev",
#                           count=200).pages(5):
#     print(len(page))

#attempt with old tweepy 3.10.0
# tweets = tweepy.Cursor(api.search, q=keyword, lang="en",
#                            tweet_mode='extended').items(noOfTweets)

#tweets = list(tweepy.Cursor(api.search_tweets(q=keyword)).items(noOfTweets))


# for response in tweepy.Paginator(client.search_all_tweets, 
#                                  query = 'COVID hoax -is:retweet lang:en',
#                                  user_fields = ['username', 'public_metrics', 'description', 'location'],
#                                  tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
#                                  expansions = 'author_id',
#                                  start_time = '2021-01-20T00:00:00Z',
#                                  end_time = '2021-01-21T00:00:00Z',
#                               max_results=5):
#     time.sleep(1)
#     tweets.append(response)

# print(tweets)
# print(tweets_array)