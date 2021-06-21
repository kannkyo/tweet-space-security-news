import logging
import os
import traceback

from requests.models import Response

from cao import scraping_space
from qiita import get_items
from requests_oauthlib import OAuth1Session
from rss import get_news_from_rss
from secret import get_secret
from twitter import tweet_text

level = os.environ.get('LOG_LEVEL', 'DEBUG')


def logger_level():
    print(f"set log level = {level}")
    if level == 'CRITICAL':
        return 50
    elif level == 'ERROR':
        return 40
    elif level == 'WARNING':
        return 30
    elif level == 'INFO':
        return 20
    elif level == 'DEBUG':
        return 10
    else:
        return 0


logger = logging.getLogger()
logger.setLevel(logger_level())


def tweet(twitter: OAuth1Session):
    messages = []
    messages.extend(get_items("人工衛星+セキュリティ"))
    # messages.extend(get_news_from_rss("https://sorabatake.jp/feed/"))
    messages.extend(scraping_space())

    res_text = None
    for message in messages:
        res_text = tweet_text(
            twitter=twitter,
            message=message)

    if res_text == None:
        res_text = {'status_code': '200', 'reason': ''}

    return res_text


def lambda_handler(event, context):
    logger.debug(event)

    try:
        secret = get_secret(
            region_name="ap-northeast-1",
            secret_name=os.environ.get('TWITTER_SECRET_NAME'))

        twitter = OAuth1Session(
            secret['api_key'],
            secret['api_secret_key'],
            secret['access_token'],
            secret['access_token_secret']
        )

        response = tweet(twitter=twitter)

        return {
            'status_code': response['status_code'],
            'reason': response['reason']
        }

    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


if __name__ == "__main__":
    lambda_handler(None, None)
