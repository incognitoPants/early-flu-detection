#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is python code for tweepy streamer without using Cursor. This code is generated by Vinnie who runs 
LucidProgramming in Youtube.
"""

# Libraries

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from operator import itemgetter
import json
import csv

import twitter_credentials


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
            if not decoded['text'].startswith('RT'):
                print(data)                # printing complete tweets containing hash_tag_list in console for checking
                header = ['created_at', 'text', 'user']
                required_cols = itemgetter(*header)
                
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(data)
                    
                with open(self.fetched_tweets_filename) as f_input, open(output_file, 'w') as f_output:
                    csv_output = csv.writer(f_output)
                    csv_output.writerow(header)
                    
                    for row in f_input:
                        if row.strip():
                            csv_output.writerow(required_cols(json.loads(row)))
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
    
    hash_tag_list =["flu"]
    fetched_tweets_filename = "tweets2.json"
    output_file = 'tweets.csv'
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
    
    
    
