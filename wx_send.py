#!/usr/bin/env python3
# encoding: utf-8

import requests
import config

__SendKey = config.send_key


def wx_send(title=' ', content=' ', uid=''):
    requests.get(
        "https://sctapi.ftqq.com/"+__SendKey+".send",
        params={"title": title, 'desp': content, 'openid': uid})



if __name__ == '__main__':
    wx_send(title='测试消息',
            content='\n我们对消息模板进行了升级，接下来将推送新版可转债信息，如果你有任何意见，欢迎反馈！')
