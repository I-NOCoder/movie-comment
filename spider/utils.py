# -*- coding: utf-8 -*-
import random

import requests
from lxml import etree
from fake_useragent import UserAgent

PROXIES = [] #应放配置文件中

TIMEOUT = 5


def choice_proxy():
    if PROXIES:
        return random.choice(PROXIES+[''])
    return ''


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, retry=0):
    s = requests.Session()
    proxies = {
        'http': choice_proxy()
    }
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': 'https://movie.douban.com/'})
    try:
        return s.get(url, timeout=TIMEOUT, proxies=proxies)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry+1)
        raise


def get_tree(url):
    r = fetch(url)
    return etree.HTML(r.text)


if __name__ == "__main__":
    print get_user_agent()
