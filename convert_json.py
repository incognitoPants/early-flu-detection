"""
**** Documentation ****
Running this will allow you to convert a lit of JSON files into a combined CSV file that includes a sentiment
column.

How to use:
    Add your JSON files to the /Input directory and edit input_files.txt to include the name of each file separated
    by a line break.

Result:
    An output file named as output_name.csv will be created in the /Output directory. If a file of that name already
    exists, it will append data to the existing file.

"""


from textblob import TextBlob
import re
import json
from pandas.io.json import json_normalize
import pandas as pd

addr = "Input/"
output_name = "tweets_json_converted.csv"

with open("Input/input_files.txt") as f_in:
    for line in f_in:
        input_file = addr + line.strip('\n')

        with open(input_file) as f:
            j_file = json.load(f)
            j_norm = json_normalize(j_file, max_level = 1)

        # remove tweets starting with "RT"
        j_norm = j_norm[~j_norm.text.str.startswith('RT ')]
        # remove tweets not lang = en
        j_norm = j_norm[j_norm.lang == 'en']


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
        output_file = "Output/" + output_name
        try:
            df = pd.read_csv(output_file)
            j_norm.to_csv(output_file, mode='a', columns=headers, header=False, index=False)
        # if it doesn't...
        except FileNotFoundError:
            j_norm.to_csv(output_file, mode='w', columns=headers, header=True, index=False)
