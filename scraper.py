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
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

neon_eng = create_engine(NEON_CONNSTRG)

neon_conn = neon_eng.connect()

import tweepy

auth = tweepy.OAuth1UserHandler(
   TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

from pyairtable import Table
table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)

table_pull = table.all(fields=["TweetID"])

def track_tweets(keyword:str, count:int):

    tweets = api.search_tweets(q=keyword, result_type="recent", count=count)

    for tweet in tweets:
        tweet_id = str(tweet.id)
        tweet_text = tweet.text
        user_url = "https://twitter.com/"+tweet.user.screen_name
        nix_tweets_uuid = uuid.uuid4()
            
        # test = neon_conn.execute(text("SELECT * FROM nix_tweets WHERE tweetid=:tweetid"), [{"tweetid": int(tweet_id)}]).mappings()

        table.create(
            {
                "TweetID": tweet_id,
                "TweetText": tweet_text,
                "UserURL": user_url,
                                }
            )                
        
        neon_conn.execute(
                text(
                "INSERT INTO nix_tweets_two (id, tweetid, tweettext, userurl) VALUES (:id, :tweetid, :tweettext, :userurl) ON CONFLICT (tweetid) DO NOTHING"
                ),
                [{"id":nix_tweets_uuid, "tweetid": int(tweet_id), "tweettext": tweet_text, "userurl": user_url}]
                )
        neon_conn.commit()

track_tweets("@floxdevelopment", 10)

print("Done!")