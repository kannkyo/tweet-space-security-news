import logging
from datetime import datetime, timedelta

import feedparser
import pytz
from common import tag
# import re

logger = logging.getLogger()
THRESHOLD = 240


def get_news_from_rss(url: str, exp: str = ""):
    feed = feedparser.parse(url)
    messages = []

    for entry in feed.entries:
        tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz)
        entry_date = datetime(
            *entry.published_parsed[:6], tzinfo=pytz.utc).astimezone(tz)
        threshold = now - timedelta(hours=THRESHOLD)

        if threshold <= entry_date < now:
            # matched = re.search(exp, entry.title)

            message = f"{entry_date} {entry.title} {tag} {entry.link}"
            logger.info(f"add message={message}")
            print(message)
            messages.append(message)

    return messages


get_news_from_rss("https://sorabatake.jp/feed/")
