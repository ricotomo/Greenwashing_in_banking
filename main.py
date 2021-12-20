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
import csv 

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


# attempt with tweepy 4.3.0
for tweet in tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(noOfTweets):
    tweets_array.append(tweet.text)

for tweet in tweets_array:
 print(tweet)

## using Client object
## https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    print("client successfully created")
except:
    print("client connection failed")

# Searching for Tweets from the last 7 days 
#client.search_recent_tweets

query_client = 'covid'

tweets = client.search_recent_tweets(query=query_client, tweet_fields=['context_annotations', 'created_at'], max_results=10)

for tweet in tweets.data:
    print(tweet.text)
    if len(tweet.context_annotations) > 0:
        print(tweet.context_annotations)

#Searching for Tweets from the full-archive of public Tweets 
# Client.search_all_tweets(query, *, end_time, expansions, max_results, media_fields, next_token, place_fields, poll_fields, since_id, start_time, tweet_fields, until_id, user_fields)

# tweets = client.search_all_tweets(query=query_client, tweet_fields=['context_annotations', 'created_at'], max_results=10)

# for tweet in tweets.data:
#     print(tweet.text)
#     if len(tweet.context_annotations) > 0:
#         print(tweet.context_annotations)

#with timeframe

# # Replace with time period of your choice
# start_time = '2020-01-01T00:00:00Z'

# # Replace with time period of your choice
# end_time = '2020-08-01T00:00:00Z'

# tweets = client.search_all_tweets(query=query_client, tweet_fields=['context_annotations', 'created_at'],
#                                   start_time=start_time,
#                                   end_time=end_time, max_results=10)

# for tweet in tweets.data:
#     print(tweet.text)
#     print(tweet.created_at)

#Writing Tweets to a text file 

# Name and path of the file where you want the Tweets written to
file_name = 'tweets.txt'

with open(file_name, 'a+') as filehandle:
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query_client,
                                  tweet_fields=['text'], max_results=10).flatten(
            limit=100):
        filehandle.write('%s\n' % tweet.id)


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