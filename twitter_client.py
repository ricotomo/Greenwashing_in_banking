import tweepy
import pandas as pd

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

def connect_api():
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
        return None
        

## using Client object
## https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9
def connect_client():
    try:
        client = tweepy.Client(bearer_token=BEARER_TOKEN)
        print("client successfully created")
        return client
    except:
        print("client connection failed")
        return None