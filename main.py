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

#import my modules
import query_constucter
import twitter_client
import tweet_cleaner

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

#print results?
verbose=False
    
#Build query from company accounts and ESG keywords
queries_by_FI=query_constucter.build_query(verbose)
queries=[]
for index, query in enumerate(queries_by_FI):
    for query2 in (query_constucter.split_query(query[1], verbose)):
            queries.append([query[0], query2])
#print(queries)

# #Get data
client = twitter_client.connect_client(verbose)

#if we want to erase the csv data and start from scratch set to true
reset=False


# # Searching for Tweets from the last 7 days 
# #client.search_recent_tweets

most_recent_date = None

try:
    if reset:
        tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
    else:
        tweets_df = pd.read_csv("results1.csv", index_col=0) 
        tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'])
        most_recent_date = tweets_df['created_at'].max()

    for query in queries:
        data=twitter_client.get_data(client, query[1], query[0], most_recent_date, reset)
        tweets_df = tweets_df.append(data)
        #print(tweets_df)
except:
    tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
    for query in queries:
        data=twitter_client.get_data(client, query[1], query[0], most_recent_date, reset)
        tweets_df = tweets_df.append(data)
        #print(tweets_df)

#get rid of duplicate tweets, get rid of NaNs and reset index of dataframe
tweets_df = tweets_df.drop_duplicates('id', keep='last')
tweets_df = tweets_df[tweets_df['text'].notna()]
tweets_df = tweets_df.reset_index(drop = True)


#write dataframe to csv
tweets_df.to_csv("results1.csv")

##tweet cleaning steps

#make sure all tweet texts are of type string so we can work with them
tweets_df['text'] = tweets_df['text'].astype(str)
#remove usernames
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_usernames(x))
#remove punctuation
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_punct(x))
#tokenize
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.tokenization(x.lower()))
#remove stopwords
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_stopwords(x))
print(tweets_df.head(10))
#stemming
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.stemming(x))
#lemmantization
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.lemmatizer(x))

#inform user code is done executing
print("The code has finished executing ")

