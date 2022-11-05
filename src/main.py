from pip import main
from ElyzaPencil import generate
import tweepy
import os
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
        self.client_v2 = tweepy.Client(ACCESS_TOKEN_PKCE)

    def get_trends(self):
        woeid = {'東京': 1118370}
        res = self.api_v1.get_place_trends(woeid['東京'])
        trend_words = []
        for trend in res[0]["trends"]:
            trend_words.append(trend['name'])
        return trend_words
    
    def tweet(self, text):
        return 0



if __name__ == "__main__":
    twitter = Twitter()
    trend_words = twitter.get_trends()

    keywords = trend_words[:5]
    res = generate(keywords)
    print(res)
    {'draft_id': '15718759913312897990', 'keywords': ['いい感じ', '天気が悪い'], 'kind': 'news', 'status': 'success', 'title': '天気の悪い日はいい感じに距離が縮まる!?男子が思う「いい感じの彼女」の特徴4つ', 'content': '天気の悪い日に「いいな」と思う女性の特徴を22〜39歳の社会人男性に聞いた。気遣いができる、雰囲気がいい、笑顔がかわいい。服装がオシャレである、いい感じの関係が続いている。'}