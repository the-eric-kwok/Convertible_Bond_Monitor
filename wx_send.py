#!/usr/bin/env python3
# encoding: utf-8

import requests
import config

__SendKey = config.send_key


def wx_send(title='', content=''):
    requests.get(
        "https://sctapi.ftqq.com/"+__SendKey+".send",
        params={"title": title, 'desp': content})


if __name__ == '__main__':
    wx_send(title='你好👋', content='世界🌍')
