
import http.client
import json
import logging
import urllib.parse
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta

from common import tag

logger = logging.getLogger()


def get_items(query: str, item_num: int = 5, page: str = "1", par_page: str = "100"):

    conn = http.client.HTTPSConnection("qiita.com", 443)

    url = f"/api/v2/items?page={page}&per_page={par_page}&query={urllib.parse.quote(query)}"
    logger.info(f"request to {url}")

    conn.request("GET", url)
    res = conn.getresponse()
    logger.info(f"response status={res.status} reason={res.reason}")

    data = res.read().decode("utf-8")
    jsonstr = json.loads(data)

    jst = timezone(timedelta(hours=9))
    yesterday = (datetime.now(jst) - relativedelta(days=1)).date()
    logger.info(f"search {yesterday} items")

    messages = list()
    for num in range(item_num):
        created_at = datetime.fromisoformat(jsonstr[num]['created_at']).date()
        title = jsonstr[num]['title']
        url = jsonstr[num]['url']

        logger.info(f"find {str(num)} {created_at} {title} {url}")

        if created_at == yesterday:
            message = f"{title} {tag} {url}"
            logger.info(f"add message={message}")
            messages.append(message)

    conn.close()

    return messages


if __name__ == "__main__":
    get_items("人工衛星+セキュリティ")
