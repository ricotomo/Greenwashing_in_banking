import numpy as np
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def getPolarity(text):
   return sid.polarity_scores(text)

def getAnalysis(score):
  if score <= -0.05:
    return 'Negative'
  elif score >= 0.05:
    return 'Positive'
  else:
    return 'Neutral'

def getSentiment(tweet):
    compound = getPolarity(tweet)['compound']
    return getAnalysis(compound)