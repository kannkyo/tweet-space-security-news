
import logging
import os
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta
from common import tag

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


def scraping_space():
    load_url = "https://www8.cao.go.jp/space/index.html"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")
    topics = soup.find(attrs={"class": "topicsList"}).children
    logger.debug(topics)

    jst = timezone(timedelta(hours=9))
    yesterday = (datetime.now(jst) - relativedelta(days=1)
                 ).strftime('%Y年%-m月%-d日')
    logger.info(f"search {yesterday} topics")

    messages = list()
    is_include_yesterday_topics = False
    for topic in topics:
        if topic == "\n":
            continue
        if topic.name == "dt":
            if topic.text == yesterday:
                logger.info(f"find {yesterday} topic")
                is_include_yesterday_topics = True
            else:
                is_include_yesterday_topics = False
        elif topic.name == "dd":
            if is_include_yesterday_topics == True:
                message = f"[宇宙政策委員会]\n{topic.a.text}\nhttps://www8.cao.go.jp/space/{topic.a['href']}"
                logger.info(message)
                messages.append(message)

    return messages
