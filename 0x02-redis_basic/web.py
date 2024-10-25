#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:).

The core of the function is very simple.
It uses the requests module to obtain the HTML content
of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was accessed
in the key "count:{url}" and cache the result with an expiration
time of 10 seconds
"""

import redis
import requests


def get_page(url: str) -> str:
    """Gets the HTML content of a particular URL

    Keyword arguments:
    url -- URL to get the content from
    Return: HTML content
    """

    r = redis.Redis()
    count_key = "count:{}".format(url)
    content_key = url

    r.incr(count_key)
    r.expire(count_key, 10)

    if not r.get(content_key):
        r.set(content_key, requests.get(url).text)

    return r.get(content_key).decode('utf-8')
