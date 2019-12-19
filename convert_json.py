from textblob import TextBlob
import re
import json
from pandas.io.json import json_normalize
import pandas as pd

# Change this as needed!
input_file = "/Users/idris/Downloads/data1.json"

with open(input_file) as f:
    j_file = json.load(f)
    j_norm = json_normalize(j_file, max_level = 1)

# remove tweets starting with "RT"
j_norm = j_norm[~j_norm.text.str.startswith('RT ')]


headers = ['created_at', 'user.screen_name', 'lang', 'text', 'sentiment']
snt_list = []
for tweet in j_norm['text']:
    if not tweet.startswith('RT'):
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        #  Analyze the tweet's polarity
        s = TextBlob(tweet)
        if s.sentiment.polarity > 0:
            snt = 'positive'
        elif s.sentiment.polarity == 0:
            snt = 'neutral'
        else:
            snt = 'negative'
        snt_list.append(snt)

j_norm["sentiment"] = snt_list
output_file = "Output/tweets_json.csv"
try:
    df = pd.read_csv(output_file)
    j_norm.to_csv(output_file, mode='a', columns=headers, header=False, index=False)
# if it doesn't...
except FileNotFoundError:
    j_norm.to_csv(output_file, mode='w', columns=headers, header=True, index=False)
