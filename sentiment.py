from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import API
import twitter_keys
import time

from textblob import TextBlob
import pandas as pd
import numpy as np
import re


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

# Authenicates


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_keys.consumer_key, twitter_keys.consumer_secret)
        auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
        return auth


# Twitter Streamer
class TwitterStreamer():
    """
    class for streming and processing live tweets
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, pull_tweets_file, hash_tag_list):
        # handles twitter authentication and connection to the twitter streaming API
        listener = TwitterListener(pull_tweets_file)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # Filters Tweitter stream to with the keywords listed in hash_tag_list
        stream.filter(track=hash_tag_list)


# Twitter Stream Listener
class TwitterListener(StreamListener):
    """
    Its a basic listener class that receives and prints tweets. Takes the data from streamListener
    """
    "Create a constructors to store the tweets"

    def __init__(self, pull_tweets_file):
        self.pull_tweets_file = pull_tweets_file

    def on_data(self, data):
        try:
            print(data)
            with open(self.pull_tweets_file, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            # returns false on_data method in case rate limit is reached on twitter
            return False
        print("status:", status)


class TweetAnalyzer():
    """"
    Analyzes and categorizes tweets
    """

    def tidy_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    # uses the in-built sentiment analysis tool to analyze tweets
    def sentiment_analyzer(self, tweet):
        # analysis = TextBlob(self.clean_tweet(tweet))
        analysis = TextBlob(self.tidy_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    # creates a dataframe for the extracted tweets
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=["tweets"])

        df["retweets"] = np.array([tweet.retweet_count for tweet in tweets])
        df["len"] = np.array([len(tweet.text) for tweet in tweets])
        df["likes"] = np.array([tweet.favorite_count for tweet in tweets])

        return df


if __name__ == "__main__":

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="CDCgov", count=20)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.sentiment_analyzer(tweet) for tweet in df["tweets"]])

    print(df.head(10))

    # hash_tag_list = ["flu", "influenza", "sick", "sneeze"]
    # pull_tweets_file = "tweets._json"
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(pull_tweets_file, hash_tag_list)
