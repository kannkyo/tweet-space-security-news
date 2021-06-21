import logging
import re
from datetime import datetime, timedelta

import feedparser
import pytz
from common import tag

logger = logging.getLogger()
THRESHOLD = 24


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
            messages.append(message)

    return messages


if __name__ == "__main__":
    keywords_en = r"security|vlus|military|AWS|Azure|Hack"
    keywords_jp = r"セキュリティ|脆弱性|軍事|クラウド|脅威|ハック"
    keywords_all = keywords_en + "|" + keywords_jp

    messages = []
    messages.extend(get_rss_news("https://spacenews.com/feed/", keywords_en))
    messages.extend(get_rss_news("https://sorabatake.jp/feed/", keywords_all))

    for message in messages:
        print(message)
