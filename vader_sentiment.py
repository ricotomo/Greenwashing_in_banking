import numpy as np
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def getPolarity(text):
   return sid.polarity_scores(text)['compound']

def getAnalysis(score):
  if score <= -0.5:
    return 'Negative'
  elif score >= 0.5:
    return 'Positive'
  else:
    return 'Neutral'

def getSentiment(tweet):
    compound = getPolarity(tweet)
    return getAnalysis(compound)