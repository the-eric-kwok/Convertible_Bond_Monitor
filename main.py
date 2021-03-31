#!/usr/bin/env python3
# encoding: utf-8

import wx_send
import requests
import re
import json
import time
import Bond

TARGET_URL = "http://data.eastmoney.com/kzz/default.html"


def log(string):
    for line in string.splitlines():
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        line = "[%s] %s" % (now, line)
        print(line)


def main():
    req = requests.get(TARGET_URL)
    match = re.search('defjson:\{pages:.*?,data:(\[.*?\])', req.text).group(1)
    js = json.loads(match)
    today_bond = []
    shangshi_bond = []
    for item in js:
        if item['STARTDATE'] != '-':
            start_date = item['STARTDATE'].split('T')[0].split('-')
            year = start_date[0]
            month = start_date[1]
            day = start_date[2]
            if int(year) == time.localtime().tm_year and int(month) == time.localtime().tm_mon and int(day) == time.localtime().tm_mday:
                today_bond.append(
                    Bond.Bond(item["SNAME"], item["BONDCODE"], item["ZGJ"], item["SWAPPRICE"]))
        if item['LISTDATE'] != '-':
            list_date = item['LISTDATE'].split('T')[0].split('-')
            year = list_date[0]
            month = list_date[1]
            day = list_date[2]
            if int(year) == time.localtime().tm_year and int(month) == time.localtime().tm_mon and int(day) == time.localtime().tm_mday:
                shangshi_bond.append(
                    Bond.Bond(item["SNAME"], item["BONDCODE"], item["ZGJ"], item["SWAPPRICE"]))

    wx_msg = '\n'
    wx_msg += '今日发售债券：\n\n'

    if len(today_bond) > 0:
        for bond in today_bond:
            if bond.price != "-" and bond.price != "-":
                wx_msg += '- 债券代码：%s，债券简称：%s，正股价：%s，转股价：%s, 转股价值：%.2f' % (
                    bond.code, bond.name, bond.price, bond.swap_price, bond.swap_value)
                if bond.swap_value > 90:
                    wx_msg += ' **推荐申购✅**'
            else:
                wx_msg += '- 债券代码：%s，债券简称：%s，正股价：%s，转股价：%s, 转股价值：%s' % (
                    bond.code, bond.name, bond.price, bond.swap_price, bond.swap_value)
            wx_msg += '\n\n'
    else:
        wx_msg += '- 无\n\n'

    wx_msg += '今日上市债券：\n\n'
    if len(shangshi_bond) > 0:
        for bond in shangshi_bond:
            wx_msg += '- 债券代码：% s，债券简称：% s\n\n' % (bond.code, bond.name)
    else:
        wx_msg += '- 无\n\n'

    if '今日发售债券' in wx_msg or '今日上市债券' in wx_msg:
        wx_msg += '<a href="%s">点这里查看可转债一览表</a>' % TARGET_URL
        log(wx_msg)
        wx_send.wx_send(title='每日可转债推送', content=wx_msg)
    else:
        log("今日无可转债发行或上市")


if __name__ == "__main__":
    main()
