from bs4 import BeautifulSoup

import io
import logging
import math
import os
import requests
import sys
import traceback

BASE_URL = "https://ingatlan.com"
PAGE_SIZE = 20

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def __crawl(url):
    divs = BeautifulSoup(__get(url).content, "html.parser").find_all(
        "div", attrs={"data-id": True}
    )
    if len(divs) > 0:
        return __parse(divs)
    return []


def __get(url, stream=False):
    res = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"
        },
        stream=stream,
    )
    if res.ok:
        return res
    else:
        log.error(res.status_code)
        sys.exit(res.status_code)


def __get_last_page(url):
    return int(
        BeautifulSoup(__get(url).content, "html.parser")
        .find("div", {"class": "pagination__page-number"})
        .text.split()[2]
    )


def __parse(divs):
    properties = []
    for div in divs:
        properties.append(
            {
                "id": div["data-id"],
                "address": div.find("div", {"class": "listing__address"}).text,
                "balcony": div.find(
                    "div", {"class": "listing__data--balcony-size"}
                ).text[:-10]
                if div.find("div", {"class": "listing__data--balcony-size"})
                else None,
                "image": div.find("img", {"class": "listing__image"})["src"]
                if div.find("img", {"class": "listing__image"})
                else None,
                "price": div.find("div", {"class": "price"}).text[:-5],
                "size": div.find("div", {"class": "listing__data--area-size"}).text[
                    :-11
                ],
                "rooms": div.find("div", {"class": "listing__data--room-count"}).text[
                    :-6
                ],
                "url": div.find("a", {"class": "listing__link"})["href"],
            }
        )
    return properties


def main():
    curr = 0
    properties = []
    last = 1
    while curr < last:
        url = "{}/lista/70-m2-felett+elado+xiii-ker+lakas+50-60-mFt?page={}".format(
            BASE_URL, curr + 1
        )
        print(url)
        if curr == 0:
            last = __get_last_page(url)
        properties += __crawl(url)
        curr += 1
    log.info(properties)


if __name__ == "__main__":
    main()
