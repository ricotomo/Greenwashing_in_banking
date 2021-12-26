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

    
#Build query from company accounts and ESG keywords
queries=query_constucter.build_query()
queries=query_constucter.split_query(queries)


# #Get data
client = twitter_client.connect_client()

# # Searching for Tweets from the last 7 days 
# #client.search_recent_tweets

#Open/create a file to append data to
csvFile = open('result.csv', 'a')
csvWriter = csv.writer(csvFile)
for query_client in queries:
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query_client, tweet_fields=['text', 'created_at', 'id'], max_results=100).flatten(limit=100):
        print(tweet.text)
        csvWriter.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8')])
csvFile.close()
