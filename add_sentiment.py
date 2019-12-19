from textblob import TextBlob
import pandas as pd
import re

file = "tweets_ns.csv" # replace with the CSV you want to add sentiment
df = pd.read_csv(file)
snt_list = []
for tweet in df["text"]:
    tweet = ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    s = TextBlob(tweet)
    if s.sentiment.polarity > 0:
        snt = 'positive'
        print(snt)
    elif s.sentiment.polarity == 0:
        snt = 'neutral'
        print(snt)
    else:
        snt = 'negative'
        print(snt)

    snt_list.append(snt)
df["sentiment"] = snt_list

# headers will not be included since the CSV's already have them.
df.to_csv("tweets_added_sentiment.csv", mode='w', index=False)