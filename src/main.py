import os, sys
import random
from time import sleep
from ElyzaPencil import generate
import tweepy
from my_logging import get_my_logger, create_line
logger = get_my_logger(__name__)


class Twitter():
    def __init__(self):
        CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
        CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
        ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
        ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
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
    
    def tweet(self, text, tweet_id=None):
        return self.client_v2.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)


if __name__ == "__main__":
    create_line(logger, "START")
    twitter = Twitter()
    try:
        trend_words = twitter.get_trends()
        tweet_text = None
        create_line(logger, "GENERATED")
        for i in range(5):
            keywords = random.sample(trend_words, k=6)
            ep_res = generate(keywords)
            if 'error_code' in ep_res.keys():
                logger.error(ep_res)
                continue
            if not ep_res['status'] == 'success':
                logger.error(ep_res)
                continue
            if ep_res['status'] == 'success':
                logger.info(ep_res)
                tweet_text = ep_res['content']
                break
            sleep(5)
        if tweet_text is None:
            sys.exit()
        create_line(logger, "TWEETED")
        tweet_res = twitter.tweet(tweet_text)
        logger.info(tweet_res)
        reply_tweet_res = twitter.tweet("\n".join(ep_res['keywords']), tweet_res.data['id'])
        logger.info(reply_tweet_res)
    finally:
        create_line(logger, "END")