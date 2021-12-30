import tweet_cleaner

s = b'@HSBC_UK Wow, coal use (in terms of TWh) has increased by nearly 30% in the last ~ 20 years so how much will it increase by in the next ~ 20 years \xf0\x9f\xa4\x94 \xf0\x9f\x98\x8c @ajlabs #green #ClimateCrisis #renewableenergy #greed https://t.co/xvNta7Adis'

x= s.decode('utf-8')

s2 = str(s)
#s2 = bytes(s2, 'utf-8')
s2 = s2.encode("utf-8")
s2.decode('utf-8')

#remove usernames
x= tweet_cleaner.remove_usernames(x)
#print(x)

# #demojize
x= tweet_cleaner.demojize(x)
#print(x)

# #remove punctuation
x= tweet_cleaner.remove_punct(x)
#print(x)
# #remove links
x= tweet_cleaner.remove_links(x)
print(x)
#spell check
x= tweet_cleaner.spell_correct(x)
print(x)
# #tokenize
# x= tweet_cleaner.tokenization(x.lower())
# print(x)
# #remove stopwords
# x= tweet_cleaner.remove_stopwords(x)
# print(x)
# # #stemming
# # tweets_df['text'] = tweets_df['text'].map(lambda x: tweet_cleaner.stemming(x))
# print(x)
# #lemmantization
# x= tweet_cleaner.lemmatizer(x)
# print(x)
# #untokenize after processing so we can calculate sentiment
# x= TreebankWordDetokenizer().detokenize(x)
# print(x)