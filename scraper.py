import dotenv
import sys
import os

dotenv.load_dotenv()

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_ID = os.getenv("AIRTABLE_TABLE_ID")

import tweepy

auth = tweepy.OAuth1UserHandler(
   TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

from pyairtable import Table
table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)

flox_tweets = api.search_tweets(q="@floxdevelopment", result_type="recent", count=5)
# nixos_tweets = api.search_tweets(q="nixos", result_type="recent", count=100)
# nixos_org_tweets = api.search_tweets(q="@nixos_org", result_type="recent", count=100)


# COME BACK
# table_pull = table.all(fields=["TweetID"])
# tweet_ids = table_pull[0]["fields"]["TweetID"]

for tweet in flox_tweets:
    tweet_id = tweet.id
    tweet_text = tweet.text
    user_url = "https://twitter.com/"+tweet.user.screen_name
    print(tweet_id)

    table.create(
        {
            "TweetID": tweet_id,
            "TweetText": tweet_text,
            "UserURL": user_url,
                            }
    )

    # From the above, we can see that we can get nix-related tweets from the API, but we need to do some more work to get the data we want. We can see that the tweets are returned as a list of objects, and we can see that each object has an id attribute. We can use this to check if we have already seen the tweet before, and if not, we can add it to our database.

    # for id in table_pull:
    #     print(id["fields"])
    #     # if id["fields"]["TweetID"] == tweet_id:
    #         # print("Tweet already in database")
    #         # sys.exit()


    





