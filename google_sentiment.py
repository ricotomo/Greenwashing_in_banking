import os
from google.cloud import language_v1

credential_path="C:\\Users\\morit\\Downloads\\custom-defender-346909-bacf56b8acd1.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def getPolarity(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return sentiment.score

def getAnalysis(score):
  if score <= -0.5:
    return 'Negative'
  elif score >= 0.5:
    return 'Positive'
  else:
    return 'Neutral'

def getSentiment(tweet):
    polarity = getPolarity(tweet)
    return getAnalysis(polarity)

def sentiment_from_polarity(polarity):
  return getAnalysis(polarity)