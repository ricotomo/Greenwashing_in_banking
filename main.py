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

from wordcloud import WordCloud, STOPWORDS
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

# # Searching for Tweets from the last 7 days 
# #client.search_recent_tweets
tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
for query in queries:
    # print("this is the query")
    # print(query[1])
    data=twitter_client.get_data(client, query[1], query[0])
    #print("data from get data()")
    tweets_df = tweets_df.append(data)
    print(tweets_df)

tweets_df = tweets_df.drop_duplicates('id', keep='last')
tweets_df = tweets_df[tweets_df['text'].notna()]
tweets_df = tweets_df.reset_index(drop = True)

#write dataframe to csv
tweets_df.to_csv("results1.csv")

# #Open/create a file to append data to
# csvFile = open('result.csv', 'a')
# csvWriter = csv.writer(csvFile)
# for query_client in queries:
#     for tweet in tweepy.Paginator(client.search_recent_tweets, query=query_client, tweet_fields=['text', 'created_at', 'id'], max_results=100).flatten(limit=100):
#         print(tweet.text)
#         csvWriter.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8')])
# csvFile.close()
