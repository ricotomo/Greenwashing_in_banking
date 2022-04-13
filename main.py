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
from datetime import datetime
from os.path import exists


#import my modules
import query_constucter
import twitter_client
import tweet_cleaner
import sentiment_analyzer
import vader_sentiment
import google_sentiment
import backtesting

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

#set to true to show print statements to help with debugging
verbose=True  

#Get data
client = twitter_client.connect_client(verbose)

#if we want to erase the csv data and start from scratch set to true
reset=False
load_or_query="load"


#Build query from company accounts and ESG keywords for getting tweets @ company
# rules=") -'credit score' -'credit rating' -'covid' -'omnicron' -RT lang:en -is:retweet"
# if load_or_query != "load":
#     queries_by_FI=query_constucter.build_query(verbose)
#     queries=[]
#     for index, query in enumerate(queries_by_FI):
#         for query2 in (query_constucter.split_query(query[1], rules, verbose)):
#                 queries.append([query[0], query2])
#     #fix error were the double quote is being saved as a single quote. Twitter API only recognizes double qoutes
#     for query in queries:
#         query[1] = query[1].replace("'" ,'"') 
#     df = pd.DataFrame(queries)
#     df.replace({'\'': '"'}, regex=True, inplace=True)
#     df.replace({'""': '"'}, regex=True, inplace=True)
#     pd.set_option('display.max_colwidth', None)
#     #print(df.head(10))
#     df.to_csv("queries.csv")


    #print(queries)

most_recent_date = None
if load_or_query=="load":
    tweets_df = pd.read_csv("result.csv", encoding='utf-8', index_col=0)
    if verbose:
        print("You have loaded the twitter query results. The first results look like:")
        pd.set_option('display.max_colwidth', None)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(tweets_df.head(5))
else:
    try:
        if reset:
            tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
            if verbose:
                print("You have chosen to reset the twitter query results")
                pd.set_option('display.max_colwidth', None)
                pd.set_option("display.max_rows", None, "display.max_columns", None)
                print(tweets_df.head(5))
        else:
            tweets_df = pd.read_csv("result.csv", encoding='utf-8', index_col=0) 
            tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'])
            most_recent_date = tweets_df['created_at'].max()
            print("getting data from: ")
            print(most_recent_date)
        for query in queries:
            data=twitter_client.get_data(client, query[1], query[0], most_recent_date, reset, verbose)
            tweets_df = tweets_df.append(data)
            #print(tweets_df)
    except:
        tweets_df = pd.DataFrame(columns=['id', 'created_at', 'text', 'company'])
        for query in queries:
            data=twitter_client.get_data(client, query[1], query[0], most_recent_date, reset, verbose)
            tweets_df = tweets_df.append(data)
            #print(tweets_df)

#######################DATA CLEANING#######################################
if verbose:
    print ("starting data cleaning")
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
# tweets_df.to_csv("result.csv")

#tweet cleaning steps
print(tweets_df.dtypes)
#make sure all tweet texts are of type string so we can work with them
tweets_df['text'] = tweets_df['text'].astype(str)
pd.set_option("display.max_rows", None, "display.max_columns", None) 
tweets_df['text'].str.decode("utf-8")
tweets_df['text'].str.decode('utf-8').fillna(tweets_df['text'])
tweets_df['text'].apply(lambda x: bytes(x, 'utf-8').decode("utf-8"))
#results have strange bytes-like encoding with correct b'..' but also "b" these need to be corrected to encode and decode bytes
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.byte_to_string(x))
p<#rint(tweets_df.head(5))
#remove usernames
if verbose:
    print("[INFO]: starting removal of usernames")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_usernames(x))
if verbose:
    print("[INFO]: finished removal of usernames")
#demojize
if verbose:
    print("[INFO]: starting demojize")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.demojize(x))
if verbose:
    print("[INFO]: finished demojize")
#remove punctuation
if verbose:
    print("[INFO]: starting removal of punctuation")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_punct(x))
if verbose:
    print("[INFO]: finished removal of usernames")
#remove links
if verbose:
    print("[INFO]: starting removal of links")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_links(x))
if verbose:
    print("[INFO]: finished removal of usernames")
#tokenize
if verbose:
    print("[INFO]: starting tokenization")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.tokenization(x.lower()))
if verbose:
    print("[INFO]: finished tokenization")
#remove stopwords
if verbose:
    print("[INFO]: starting removal of stopwords")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.remove_stopwords(x))
if verbose:
    print("[INFO]: finished removal of stopwords")
# #stemming
# tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.stemming(x))
#lemmatization
if verbose:
    print("[INFO]: starting lemmatization")
tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.lemmatizer(x))
if verbose:
    print("[INFO]: finished lemmatization")
#untokenize after processing so we can calculate sentiment
if verbose:
    print("[INFO]: started untokenizeing text")
tweets_df['text'] = tweets_df['text'].map(lambda x: TreebankWordDetokenizer().detokenize(x))
if verbose:
    print("[INFO]: finished untokenizing text")

#print(tweets_df.head(5))
if verbose:
    "tweet cleaning done"

#######################SENTIMENT ANALYSIS#######################################


# #sentiment analysis with textblob
# tweets_df['textblob_polarity'] = np.nan
# tweets_df['textblob_sentiment'] = np.nan
# tweets_df['textblob_polarity'] = tweets_df['text'].map(lambda x: sentiment_analyzer.getPolarity(x))
# tweets_df['textblob_sentiment'] = tweets_df['text'].map(lambda x: sentiment_analyzer.getSentiment(x))
# tweets_df.to_csv("sentiment_textblob.csv")

# #Number of Tweets (Total, Positive, Negative, Neutral)
# print("Using Textblob sentiment analysis tweets are classified as:")
# print('positive number: ', tweets_df['textblob_sentiment'].value_counts()["Positive"])
# print('negative number: ', tweets_df['textblob_sentiment'].value_counts()["Negative"])
# print('neutral number: ', tweets_df['textblob_sentiment'].value_counts()["Neutral"])
# if verbose:
#     "Textblob sentiment analysis done"

# #perform backtesting 
# backtesting.backtest("textblob")

# #sentiment analysis with VADER
# tweets_df['vader_polarity'] = np.nan
# tweets_df['vader_sentiment'] = np.nan
# #convert dates to just years for comparability with greenwashing scores
# tweets_df['created_at'] = tweets_df['created_at'].map(lambda x: tweet_cleaner.to_year(x))
# #standardize names so they match Bloomber and Thompson Reuters
# tweets_df['company'] = tweets_df['company'].map(lambda x: tweet_cleaner.standardize_names(x))
# tweets_df['vader_polarity'] = tweets_df['text'].map(lambda x: vader_sentiment.getPolarity(x))
# tweets_df['vader_sentiment'] = tweets_df['text'].map(lambda x: vader_sentiment.getSentiment(x))
# tweets_df.to_csv("sentiment_vader.csv")

# print("Using Vader sentiment analysis tweets are classified as:")
# print('positive number: ', tweets_df['vader_sentiment'].value_counts()["Positive"])
# print('negative number: ', tweets_df['vader_sentiment'].value_counts()["Negative"])
# print('neutral number: ', tweets_df['vader_sentiment'].value_counts()["Neutral"])
# if verbose:
# print("Vader sentiment analysis done")

#sentiment analysis with Google Cloud NLP

csv_counter=0

def fun1(x):
    polarity = google_sentiment.getPolarity(x)
    print(x)
    print(polarity)
    return polarity


def csv_writer_helper(x):
    polarity = fun1(x)
    global csv_counter
    csv_counter += 1
    print(csv_counter)
    if csv_counter % 1000 == 0:
        tweets_df.to_csv("sentiment_google.csv")
    return polarity



# tweets_df['google_polarity'] = np.nan
# tweets_df['google_sentiment'] = np.nan
# #convert dates to just years for comparability with greenwashing scores
# tweets_df['created_at'] = tweets_df['created_at'].map(lambda x: tweet_cleaner.to_year(x))
# #standardize names so they match Bloomber and Thompson Reuters
# tweets_df['company'] = tweets_df['company'].map(lambda x: tweet_cleaner.standardize_names(x))
# tweets_df['google_polarity'] = tweets_df['text'].map(lambda x: csv_writer_helper(x))
# tweets_df['google_sentiment'] = tweets_df['google_polarity'].map(lambda x: google_sentiment.sentiment_from_polarity(x))
# tweets_df.to_csv("sentiment_google.csv")


start_position= 0
reset_google=False

if exists("sentiment_google.csv") and reset_google:
    f = open("sentiment_google.csv", "w",newline='', encoding='UTF8')
    f.truncate()
    header = ['index', 'id', 'created_at', 'text', 'company', 'polarity', 'sentiment']
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()
    if verbose:
        print("[WARN]: The results of previous Google sentiment analysis was reset.")


if exists("sentiment_google.csv") and reset_google==False:
    with open('sentiment_google.csv', 'r', encoding='utf-8') as f:
        last_line = f.readlines()[-1]
        if verbose:
            print("[INFO] the last line previously written to the Google sentiment analysis csv file is: " + str(last_line))
    start_position = int(last_line.split(",")[0]) + 1
    if verbose:
        print("[INFO] the Twitter sentiment analysis is starting with the tweet with index: " + str(start_position))


data = []
interval=5

for index, row in tweets_df.iloc[start_position:].iterrows():
    polarity = google_sentiment.getPolarity(row['text'])
    sentiment = google_sentiment.sentiment_from_polarity(polarity)
    data.append([str(index), row['id'], row['created_at'], row['text'],row['company'],polarity,sentiment])
    
    if verbose:
        print("[INFO]: Tweet with index " + str(index) + " is being sent to the Google API for sentiment analysis.")
   
    if index % interval == 0 and index != 0:
        if verbose:
            print("[INFO] Entered Google Sentiment Analyis csv writer block. After sending text to the Google API this code will write the results after every " + str(interval) + " tweets.")
        df = pd.DataFrame(data, columns=['index', 'id', 'created_at', 'text', 'company', 'polarity', 'sentiment'])
        # df = df.set_index('index')
        df.to_csv('sentiment_google.csv', mode='a', index=False, header=False)
        data=[]
    
df = pd.DataFrame(data, columns=["index", 'id', 'created_at', 'text', 'company', 'polarity', 'sentiment'])
df.to_csv('sentiment_google.csv', mode='a', index=False, header=False)

# #Number of Tweets (Total, Positive, Negative, Neutral)
if verbose:
    print("[INFO]: Using Google sentiment analysis tweets are classified as:")
    print('positive number: ', df['sentiment'].value_counts()["Positive"])
    print('negative number: ', df['sentiment'].value_counts()["Negative"])
    print('neutral number: ', df['sentiment'].value_counts()["Neutral"])
    print("Google Cloud NLP sentiment analysis done")

# backtesting.backtest("vader")

# #sentiment analysis with Google Cloud NLP

# backtesting.backtest("google")


# #######################GREENWASHING SCORE#######################################

# #######################QUERY BUILDER#######################################


# #Build query from company accounts and ESG keywords for getting tweets from company
# # rules=""
# # if load_or_query != "load":
# #     queries_from_FI=query_constucter.build_query_from(verbose)
# #     queries=[]
# #     for index, query in enumerate(queries_by_FI):
# #         for query2 in (query_constucter.split_query(query[1], rules, verbose)):
# #                 queries.append([query[0], query2])
# #     #fix error were the double quote is being saved as a single quote. Twitter API only recognizes double qoutes
# #     for query in queries:
# #         query[1] = query[1].replace("'" ,'"') 
# #     df = pd.DataFrame(queries)
# #     df.replace({'\'': '"'}, regex=True, inplace=True)
# #     df.replace({'""': '"'}, regex=True, inplace=True)
# #     pd.set_option('display.max_colwidth', None)
# #     #print(df.head(10))
# #     df.to_csv("queries.csv")

#inform user code is done executing
print("[INFO]: The code has finished executing")
