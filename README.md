# UIUC CS 410, Fall 2019 Project
## Early Influenza Detection
## Members:
* Aji Fatou Dibba (adibba2)
* Kai Bogdanovich (erikabb2)
* Brian Maeng (jooyolm2)

## Project Purpose:

[Github Project Link](https://github.com/incognitoPants/early-flu-detection)

This project is meant to help someone build and create a stream in order to see if
tweets from Twitter can be used as a signal for an early or late Influenza season.

By capturing tweets over time and comparing both volume and tabulating sentiment, we
hope it will act as a useful signal to determine if the Flu / Influenza season is
starting sooner or later than expected. 

For our purpose, we visualized the results of our findings using Tableau. This can be
used to find anomalies and trends in recent tweets and compare them to historical
data.

[Tableau Visualization of Results]
One will need a Tableau Public account to view Dashboard
(https://public.tableau.com/views/SentimentAnalysisViz_15768034428880/SentimentAnalysisontwitterstreams?:display_count=y&:origin=viz_share_link)  
***

## Features:
* [Live Tweet Capture](#live-tweet-capture)
* [Adding Sentiment Analysis to Existing CSV](#adding-sentiment-to-existing-csv)
* [Capture Historical Data as JSON](#capture-historical-data-as-json)
* [Convert Twitter JSON to CSV](#convert-twitter-json-to-csv)  

***

## Requirements:
### Environment:
This project was created using Python 3.7. Using a different version of Python does guarantee
compatibility with existing code or libraries.

### Required Libraries:
Please see ```requirements.txt``` for all required libraries. The most important libraries
to install are the following:  

**TextBlob**  
```pip3 install textblob```

**Pandas**  
```pip3 install pandas```

**Tweepy**  
```pip3 install tweepy```

**Search Tweets**  
```pip3 install searchtweets```

### Twitter Developer Account
In order to use the streaming functionality, you will need a twitter developer account
and have your own unique Consumer Key and Consumer Secret. It will also be useful to
obtain a bearer token. [See Twitter's documentation on how to generate a bearer token](https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0/bearer-tokens)

***

## Project Breakdown:
* Twitter Developer Access - Kai & Aji
* Coding Tweet Capture - Brian & Kai
* Capturing Live Tweets Over Recent Days - Kai
* Adding Sentiment Analysis - Aji & Kai
* Compiling Historical Data - Brian
* Converting Historical Data - Kai
* Visualization on Tableau - Aji
* Documentation - Kai


***

## Feature Details:

### **Live Tweet Capture**  
*tweepy_streamer_sentiment.py*  
Capture tweets live as they come in, analyze their polarity, and assigned either positive, 
neutral, or negative sentiment. It also captures the degree of polarity for more granular
comparisons.

By default it only includes four data points from the twitter data.
This can be changed by editing the contents of the ```header``` variable.  
created_at
: Date and time a tweet was created  
user.screen_name
: Twitter username who posted the tweet  
lang
: Language of the tweet  
text
: Contents of a tweet  


### **Adding Sentiment to Existing CSV**  
*add_sentiment.py*  
If you already have a CSV of twitter data containing tweet texts, this can be ran to
add sentiment and polarity columns to the file.  

In order to protect the integrity of the original file, it creates a new output file 
with the additional columns. 

The user can indicate where they want the output saved. By default the output file
will be created in the `Output` directory. This can be modified in the the code.


### **Capture Historical Data as JSON**  
*tweets_historical.py*  
Depending on your Twitter developer account type, you can make specific API requests
that can go back to 2006. This is made to be flexible, but will require the user to
create a `~./twitter_keys.yaml` file. The file should look as follows:  

**Version 1: Using Bearer Token**
```yaml
search_tweets_api:
  account_type: premium
  endpoint: 'https://api.twitter.com/1.1/tweets/search/30day/dev_environment_name.json'
  bearer_token: '<BEARER_TOKEN>'
```  
**Version 2: Using Consumer Key and Consumer Secret**
```yaml
search_tweets_api:
  account_type: premium
  endpoint: 'https://api.twitter.com/1.1/tweets/search/30day/dev_environment_name.json'
  consumer_key: '<CONSUMER_KEY>'
  consumer_secret: '<CONSUMER_SECRET>'
```  

You can read more about endpoint URLs for Twitter [here.](https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search)

### **Convert Twitter JSON to CSV**  
*convert_json.py*
Once you capture your historical data, you can convert the JSON output to CSV and 
append the `sentiment` and `polarity` columns.

Since JSON files from historical data tend to be multiple files, we have automated 
this by adding a file in `Input/input_files.txt`.  

1. Add all the files you would ike to convert in the `Input` directory.
2. Modify `input_files.txt` to list all the files you will be converting.
3. Run the file. 
4. The converted JSON files will be merged into one file in the `Ouput` directory.  
*Note: You can change the variable `output_name` to customize the output filename*

## Sources:
Much of our code was built on concepts and ideas from the following projects:
* [Twitter Python - By LucidProgramming](https://github.com/vprusso/youtube_tutorials/tree/master/twitter_python
)
* [Python Twitter Search API](https://github.com/twitterdev/search-tweets-python)
