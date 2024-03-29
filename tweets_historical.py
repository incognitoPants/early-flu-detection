#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS 410, Fall 2019 Project
    - Aji Fatou Dibba
    - Kai Bogdanovich
    - Brian Maeng

Original source code can be found at: https://github.com/twitterdev/search-tweets-python

Modified Code Purpose:
    Run to look up old tweets based on specific search queries.
    Thie data would be used a baseline to determine if there is an increase in the population talking about
    the flu / influenza more so than typically seen in the previous years.

For future users:
    A yaml file needs to be created that contains the following information. Note that you can use either the consumer
    key and secret or a bearer token. It will automatically request for a bearer token if none is provided.

    search_tweets_api:
      account_type: premium
      endpoint: <END POINT URL>
      #consumer_key: <CONSUMER KEY>
      #consumer_secret: <CONSUMER SECRET>
      bearer_token: <BEARER TOKEN>


"""

# Libraries
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results
import json

file_name='data.json'
FROM_DATE='2019-11-18 00:00' 
TO_DATE='2019-12-18 00:00'

premium_search_args = load_credentials("twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

rule = gen_rule_payload("#flu", 
                        from_date=FROM_DATE,
                        to_date=TO_DATE,
                        results_per_call=100)  # change the query (first param) as needed

tweets = collect_results(rule,
                         max_results=100,
                         result_stream_args=premium_search_args)  # change this if you need to

with open(file_name, 'w') as f:
    json.dump(tweets, f, indent=4)
