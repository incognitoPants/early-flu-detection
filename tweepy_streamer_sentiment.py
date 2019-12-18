#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 410, Fall 2019 Project
    - Aji Fatou Dibba
    - Kai Bogdanovich
    - Brian Maeng

Unmodified source code:
https://github.com/vprusso/youtube_tutorials/tree/master/twitter_python

Modified Code Purpose:
    To capture tweets live that fulfills the query terms provided. These can be done as bag-of-words search or by
    term or as hashtags. Queries for this project are primarily searching for hashtags. Regular word terms can be
    used for search, but would require topic modeling to ensure the tweets tabulated are relevant to the topic of
    influenza.

Implementation:
    The captured tweets are returned as a JSON, then flattened into a Pandas data frame.
    Data from of your four columns are extrapolated into a data frame:
        - created_at (when the tweet was created)
        - user.screen_name (twitter handle of the user posting the tweet)
        - lang (language of tweet)
        - text (actual tweet)

    The text of the tweet is stripped of any special characters and user mentions before analyzing its sentiment.
    We are ranking sentiment as follows:
        polarity > 0 is positive
        polarity == 0 is neutral
        polarity < 0 is negative

    The sentiment column is added to the data frame before appending it to a CSV to the local machine. If the CSV
    file does not exist, it will create it and add headers for the columns.

"""

# Libraries
import pandas
import twitter_credentials
import json
import re
from os import path
from pandas.io.json import json_normalize
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTNER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            # excluding retweets in tweet output
            decoded = json.loads(data)

            # RT indicates retweet, this section omits those tweets
            if not decoded['text'].startswith('RT'):
                print(data)  # printing complete tweets containing hash_tag_list in console for checking
                # columns to capture
                headers = ['created_at', 'user.screen_name', 'lang', 'text', 'sentiment']

                # No need to append to JSON - not really viable for appending
                # Convert captured data and append to CSV as needed

                decoded_res = json_normalize(decoded, max_level = 1)
                # remove mentions, special characters, and unwanted characters from tweet
                tweet = str(decoded_res['text'])
                tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
                #  Analyze the tweet's polarity
                s = TextBlob(tweet)
                if s.sentiment.polarity > 0:
                    snt = 'positive'
                elif s.sentiment.polarity == 0:
                    snt = 'neutral'
                else:
                    snt = 'negative'

                # add sentiment column to data frame
                decoded_res['sentiment'] = snt
                # output data frame values to CSV without headers
                # if it exists...
                try:
                    df = pandas.read_csv(output_file)
                    # print(decoded_res)
                    decoded_res.to_csv(output_file, mode='a', columns=headers, header=False, index=False)
                #if it doesn't...
                except FileNotFoundError:
                    decoded_res.to_csv(output_file, columns=headers, header=True, index=False)

            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)





if __name__ == "__main__":
    # hashtags need '#' added
    hash_tag_list = ["#flu", "#influenza", "#flushot", "#fluvaccine", "#sneeze"]
    fetched_tweets_filename = "tweets2.json"
    output_file = 'tweets.csv'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)