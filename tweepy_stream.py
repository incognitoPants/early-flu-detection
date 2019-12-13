# Libraries
import tweepy as tw
from twitter_key import twitter_keys


auth = tw.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

token = rtweet::create_token(app_name,cons_key,cons_sec,acc_tok,acc_sec)
api = tw.API(auth)

# Search words filtering retweets
search_words = '#flu' + '-filter:retweets'
date_since = "2015-12-31"
date_until = "2016-12-31"

# Collecting tweets
tweets = tw.Cursor(api.search, q=search_words, lang='en', since=date_since, until=date_until).items()

a = 0

# Count Tweets
for tweet in tweets:
    a = a+1