# Import Libraries

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
import sentiment_analyzer

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

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
reset=True
load_or_query="query"

# # Searching for Tweets from the last 7 days 
# #client.search_recent_tweets

most_recent_date = None
if load_or_query=="load":
    tweets_df = pd.read_csv("result.csv", encoding='utf-8', index_col=0)
else:
    try:
        if reset:
            tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
        else:
            tweets_df = pd.read_csv("result.csv", encoding='utf-8', index_col=0) 
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

#get rid of duplicate tweets, get rid of NaNs, and reset index of dataframe
tweets_df = tweets_df.drop_duplicates('id', keep='last')
tweets_df = tweets_df.drop_duplicates('text', keep='last')
tweets_df = tweets_df[tweets_df['text'].notna()]
# get names of indexes for which
# column Age has value 21
# index_names = tweets_df[ tweets_df['text'] != 'en' ].index
# tweets_df.drop(index_names, inplace = True)
tweets_df = tweets_df.reset_index(drop = True)


#write dataframe to csv
tweets_df.to_csv("result.csv")

##tweet cleaning steps
# print(tweets_df.dtypes)
#make sure all tweet texts are of type string so we can work with them
# tweets_df['text'] = tweets_df['text'].astype(str)
# pd.set_option("display.max_rows", None, "display.max_columns", None) 
#tweets_df['text'].str.decode("utf-8")
#tweets_df['text'].str.decode('utf-8').fillna(tweets_df['text'])
# tweets_df['text'].apply(lambda x: bytes(x, 'utf-8').decode("utf-8"))
#results have strange bytes-like encoding with correct b'..' but also "b" these need to be corrected to encode and decode bytes
# tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.byte_to_string(x))
# print(tweets_df.head(5))
#remove usernames
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_usernames(x))
#demojize
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.demojize(x))
#remove punctuation
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_punct(x))
#remove links
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_links(x))
#tokenize
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.tokenization(x.lower()))
#remove stopwords
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_stopwords(x))
# #stemming
# tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.stemming(x))
#lemmantization
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.lemmatizer(x))
#untokenize after processing so we can calculate sentiment
tweets_df['text'] = tweets_df['text'].map(lambda x: TreebankWordDetokenizer().detokenize(x))

#print(tweets_df.head(5))

#sentiment analysis with textblob
tweets_df['textblob_polarity'] = np.nan
tweets_df['textblob_sentiment'] = np.nan
tweets_df['textblob_polarity'] = tweets_df['text'].map(lambda x: sentiment_analyzer.getPolarity(x))
tweets_df['textblob_sentiment'] = tweets_df['text'].map(lambda x: sentiment_analyzer.getSentiment(x))
tweets_df.to_csv("sentiment_textblob.csv")

#Number of Tweets (Total, Positive, Negative, Neutral)
print('positive number: ', tweets_df['textblob_sentiment'].value_counts()["Positive"])
print('negative number: ', tweets_df['textblob_sentiment'].value_counts()["Negative"])
print('neutral number: ', tweets_df['textblob_sentiment'].value_counts()["Neutral"])

#inform user code is done executing
print("The code has finished executing ")
