import dotenv
import sys
import os
import uuid

dotenv.load_dotenv()

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")
NEON_CONNSTRG = os.getenv("NEON_CONNSTRG")

# use sqlalchemy to connect with neon and push tweets there too
from sqlalchemy import create_engine
from sqlalchemy import text

neon_conn = create_engine(NEON_CONNSTRG)

test = neon_conn.connect()

import tweepy

auth = tweepy.OAuth1UserHandler(
   TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

from pyairtable import Table
table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)

flox_tweets = api.search_tweets(q="@floxdevelopment", result_type="recent", count=5)

table_pull = table.all(fields=["TweetID"])

tweet_id_list = []

def track_tweets(keyword:str, count:int):

    tweets = api.search_tweets(q=keyword, result_type="recent", count=count)

    for id in table_pull:
        tweet_id_list.append(id["fields"]["TweetID"])

    for tweet in tweets:
        tweet_id = str(tweet.id)
        tweet_text = tweet.text
        user_url = "https://twitter.com/"+tweet.user.screen_name
        nix_tweets_uuid = uuid.uuid4()

        table.create(
            {
                "TweetID": tweet_id,
                "TweetText": tweet_text,
                "UserURL": user_url,
                                }
            )

        # need to insert uuid here

        test.execute(
            text("INSERT INTO nix_tweets (id, tweetid, tweettext, userurl) VALUES (:id, :tweetid, :tweettext, :userurl)"),
            [{"id":nix_tweets_uuid, "tweetid": int(tweet_id), "tweettext": tweet_text, "userurl": user_url}]
            )
        test.commit()

track_tweets("@floxdevelopment", 5)

print("Done!")