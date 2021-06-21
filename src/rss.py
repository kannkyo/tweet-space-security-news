import logging
import re
from datetime import datetime, timedelta

import feedparser
import pytz
from common import tag

logger = logging.getLogger()
THRESHOLD = 240


def get_rss_news(url: str, exp: str = r""):
    feed = feedparser.parse(url)
    messages = []

    p = re.compile(exp)

    for entry in feed.entries:
        tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tz)
        entry_date = datetime(
            *entry.published_parsed[:6], tzinfo=pytz.utc).astimezone(tz)
        threshold = now - timedelta(hours=THRESHOLD)

        if threshold <= entry_date < now and p.findall(f"{entry.title} {entry.content}"):
            message = f"{entry.title} {tag} {entry.link}"
            logger.info(f"add date={entry_date}  message={message}")
            print(message)
            messages.append(message)

    return messages
