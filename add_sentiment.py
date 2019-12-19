"""
**** Documentation ****
Use this to convert an existing CSV file containing tweets. Please note that this assumes the column names from
the twitter data were not modified.

How to use:
    Assign the address of your CSV to variable input_file. We recommend keeping files in the Input directory.

Result:
    An output file named as output_file.csv will be created in the /Output directory.

"""
from textblob import TextBlob
import pandas as pd
import re

input_file = 'Input/tweets_ns2.csv' # replace with the CSV you want to add sentiment
output_name = 'tweets_added_sentiment1.csv'
output_file = 'Output/' + output_name
lang_filter = 'en'
df = pd.read_csv(input_file)

# Only keep tweets that are in English
df = df[df.lang == 'en']

snt_list = []
for tweet in df['text']:
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    s = TextBlob(tweet)
    if s.sentiment.polarity > 0:
        snt = 'positive'
    elif s.sentiment.polarity == 0:
        snt = 'neutral'
    else:
        snt = 'negative'

    snt_list.append(snt)
df["sentiment"] = snt_list

# headers will not be included since the CSV's already have them.
df.to_csv(output_file, mode='w', index=False)