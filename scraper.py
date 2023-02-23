import dotenv
import sys
import os

dotenv.load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

import tweepy

auth = tweepy.OAuth1UserHandler(
   CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

flox_tweets = api.search_tweets(q="@floxdevelopment", count=100)
nixos_tweets = api.search_tweets(q="nixos", count=100)
nixos_org_tweets = api.search_tweets(q="@nixos_org", count=100)

for tweet in flox_tweets:
    print(tweet.text)

for tweet in nixos_tweets:
    print(tweet.text)

for tweet in nixos_org_tweets:
    print(tweet.text)



