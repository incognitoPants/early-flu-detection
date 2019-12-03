# Libraries
import tweepy as tw
from twitter_key import twitter_keys


auth = tw.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tw.API(auth)
#for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
    #print(tweet.text)

# Search words filtering retweets
search_words = '#flu' + '-filter:retweets'
date_since = "2019-01-30"

# Collecting tweets
tweets = tw.Cursor(api.search, q=search_words, lang='en', since=date_since).items()

a = 0

# Print Tweets
for tweet in tweets:
    a = a+1