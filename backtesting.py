import pandas as pd 
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
import csv

#import my modules
import query_constucter
import twitter_client
import tweet_cleaner
import sentiment_analyzer
import vader_sentiment


def backtest(method):
    #perform backtesting with 100 tweets categorized manually on 01.01.2021
    bt_analysis_df = pd.read_csv("backtesting.csv", encoding='utf-8', index_col=0, sep=';,')
    #print("head of analysis df is: ........................")
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # pd.set_option('display.max_colwidth', None)
    #print(bt_analysis_df.head(5))

    bt_result_df = pd.DataFrame(columns=['id', 'text', 'predicted', 'actual'])

    ##tweet cleaning steps
    #remove usernames
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.remove_usernames(x))
    #demojize
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.demojize(x))
    #remove punctuation
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.remove_punct(x))
    #remove links
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.remove_links(x))
    #tokenize
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.tokenization(x.lower()))
    #remove stopwords
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.remove_stopwords(x))
    # #stemming
    # tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.stemming(x))
    #lemmantization
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: tweet_cleaner.lemmatizer(x))
    #untokenize after processing so we can calculate sentiment
    bt_analysis_df['text'] = bt_analysis_df['text'].map(lambda x: TreebankWordDetokenizer().detokenize(x))

    if method == "textblob":
        for index, x in bt_analysis_df.iterrows():
            #print("x is: ")
            #print(x)
            data = [{'id':x['id'], 'text':x['text'], 'predicted':x['sentiment_class'], 'actual': sentiment_analyzer.getSentiment(x['text'])}]
            returned_tweet = pd.DataFrame.from_dict(data, orient='columns')
            bt_result_df = bt_result_df.append(returned_tweet, ignore_index=True)
        bt_result_df.to_csv("textblob_backtesting.csv")
        print("The textblob sentiment analysis has an accuracy of: ")
    elif method == "vader":
            for index, x in bt_analysis_df.iterrows():
                data = [{'id':x['id'], 'text':x['text'], 'predicted':x['sentiment_class'], 'actual': vader_sentiment.getSentiment(x['text'])}]
                returned_tweet = pd.DataFrame.from_dict(data, orient='columns')
                bt_result_df = bt_result_df.append(returned_tweet, ignore_index=True)
            bt_result_df.to_csv("vader_backtesting.csv")
            print("The vader sentiment analysis has an accuracy of: ")
    
    #subsetDataFrame = bt_result_df[bt_result_df['predicted'] == bt_result_df['actual']]
    equality_counter=0
    for index, row in bt_result_df.iterrows():
        if row['predicted'] == row['actual']:
            equality_counter += 1
    print (equality_counter/len(bt_result_df.index)*100)
    return None