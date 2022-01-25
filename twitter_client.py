import tweepy
import pandas as pd
import numpy as np
import datetime
from datetime import timezone
import traceback

#choose API version
vers="academic"

# set creds
if vers==1.1:
    result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds1.1.csv')
elif vers==2:
    result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/creds.csv')
else:
    result = pd.read_csv('C:/Users/morit/Documents/School/MSc - Research Project (Semester 3)/credsacademic.csv')
#print(result)
CONSUMER_KEY=result.loc[0]['value']
CONSUMER_SECRET=result.loc[1]['value']
BEARER_TOKEN=result.loc[2]['value']
ACCESS_TOKEN=result.loc[3]['value']
ACCESS_TOKEN_SECRET=result.loc[4]['value']
# print(CONSUMER_KEY)
# print(CONSUMER_SECRET)
# print(ACCESS_TOKEN)
# print(ACCESS_TOKEN_SECRET)

def connect_api(verbose):
    # Authenticate to Twitter
    try:
        # create OAuthHandler object
        auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        # set access token and secret
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        # Create API object
        api = tweepy.API(auth)
        if verbose: 
            print("Authentication successfull")
        print(api.verify_credentials().name)
        # client = tweepy.Client(BEARER_TOKEN, wait_on_rate_limit=True)
    except:
        print("Error: Authentication Failed")
        return None
        

## using Client object Twitter API v2
## https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
def connect_client(verbose):
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
        if verbose: 
            print("client successfully created")
        return client
    except Exception:
        traceback.print_exc()
        print("Error: client connection failed")
        return None

def get_data(client, query_client, FI, date=None, reset=False, verbose=False):
    #the max time in the past the twitter API gives acess too
    start="2006-03-27T00:00:00+00:00"
    #uses current time in UTC minus thirty seconds
    end=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=30))
    #data = np.array([['test'], ['test']])
    data = pd.DataFrame(columns=['id', 'text', 'created_at', 'company'])
    pd.set_option("display.max_rows", None, "display.max_columns", None) 
    query_client = query_client.replace("'" ,'"') 
    if query_client.find("(") != 0:
            if verbose:
                print(" entered twitter client finder")
            query_client = "(" + query_client
    if verbose:
        print("query is : ")
        print(query_client)
    
    # Use the start_time parameter to only get data past most recent pull
    if (date != None and reset==False):
        start=date
    
    for tweet in tweepy.Paginator(client.search_all_tweets, query=query_client, tweet_fields=['text', 'created_at', 'id'], start_time=start, end_time=end, max_results=500).flatten(limit=20000):
    #The below line is for elevated API acces rather than academic (search recent tweets vs search all)
        data1 = [{'id':tweet.id, 'text':tweet.text.replace('\n', ' '), 'created_at':tweet.created_at, 'company':str(FI)}]
        returned_tweet = pd.DataFrame.from_dict(data1, orient='columns')
        data = data.append(returned_tweet, ignore_index=True)
        if verbose:
            print("...............................................")
            print(returned_tweet)
            print("the data dataframe with tweets in get_data() of twitter client is: ")
            print(returned_tweet)
    if verbose:
        print("twitter client complete data is")
        print(data)
    return data