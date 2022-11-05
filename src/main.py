import os, sys
import random
from ElyzaPencil import generate
import tweepy
from my_logging import get_my_logger
logger = get_my_logger(__name__)


class Twitter():
    def __init__(self):
        CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
        CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
        ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
        ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
        ACCESS_TOKEN_PKCE = os.environ.get('TWITTER_ACCESS_TOKEN_PKCE')
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api_v1 = tweepy.API(auth)
        self.client_v2 = tweepy.Client(
            consumer_key = CONSUMER_KEY,
            consumer_secret = CONSUMER_SECRET,
            access_token = ACCESS_TOKEN,
            access_token_secret = ACCESS_SECRET
        )


    def get_trends(self):
        woeid = {'東京': 1118370}
        res = self.api_v1.get_place_trends(woeid['東京'])
        trend_words = []
        for trend in res[0]["trends"]:
            trend_words.append(trend['name'])
        return trend_words
    
    def tweet(self, text):
        return self.client_v2.create_tweet(text=text)

if __name__ == "__main__":
    twitter = Twitter()
    trend_words = twitter.get_trends()
    keywords = random.sample(trend_words, k=6)
    ep_res = generate(keywords)
    if 'error_code' in ep_res.keys():
        logger.error(ep_res)
        sys.exit()
    if not ep_res['status'] == 'success':
        logger.error(ep_res)
        sys.exit()
    logger.info(ep_res)
    tweet_res = twitter.tweet(ep_res['content'])
    logger.info(tweet_res)