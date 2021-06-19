# see https://qiita.com/katafuchix/items/7fa1323265b6a448cdbc

import json
import os
import logging
import traceback
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta, timezone

import requests
from secret import get_secret
from twitter import tweet_text
from bs4 import BeautifulSoup

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


def scraping_space():
    load_url = "https://www8.cao.go.jp/space/index.html"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    topics = soup.find(attrs={"class": "topicsList"}).children
    print(topics)

    jst = timezone(timedelta(hours=9))

    today = datetime.now(jst).strftime('%Y年%-m月%-d日')
    today = "2021年6月1日"

    print(f"search {today} topics")

    messages = list()
    is_include_today_topics = False
    for topic in topics:
        if topic == "\n":
            continue
        if topic.name == "dt":
            if topic.text == today:
                print(f"find {today} topic")
                is_include_today_topics = True
            else:
                is_include_today_topics = False
        elif topic.name == "dd":
            if is_include_today_topics == True:
                text: str = topic.a.text
                if "宇宙安全保障部会" in text:
                    print(f"find 宇宙安全保障部会 in {topic.a}")
                    message = f"[宇宙政策委員会 宇宙安全保障部会]\n{topic.a.text}\nhttps://www8.cao.go.jp/space/{topic.a['href']}"
                    print(message)
                    messages.append(message)


def lambda_handler(event, context):
    logger.debug(event)

    try:
        scraping_space()
        secret = get_secret(
            region_name="ap-northeast-1",
            secret_name=os.environ.get('TWITTER_SECRET_NAME'))

        twitter = OAuth1Session(
            secret['api_key'],
            secret['api_secret_key'],
            secret['access_token'],
            secret['access_token_secret']
        )

        messages = scraping_space()
        for message in messages:
            res_text = tweet_text(
                twitter=twitter,
                message=message)

        return {
            'statusCode': res_text.status_code
        }

    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def main():
    lambda_handler(None, None)


if __name__ == "__main__":
    main()
