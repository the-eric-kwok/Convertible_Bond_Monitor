#!/usr/bin/env python3
# encoding: utf-8

import wx_send
import requests
import re
import json
import time
import Bond

PAGE_URL = "http://data.eastmoney.com/kzz/default.html"
TARGET_URL = "http://datacenter-web.eastmoney.com/api/data/v1/get"
PARAMS = {
    'reportName': "RPT_BOND_CB_LIST",
    'columns': "ALL",
    'quoteColumns': "f229~10~SECURITY_CODE~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE,f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO,f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE,f23~01~CONVERT_STOCK_CODE~PBV_RATIO",
    'source': "WEB",
    'client': "WEB"
}


def log(string):
    for line in string.splitlines():
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        line = "[%s] %s" % (now, line)
        print(line)


def main():
    req = requests.get(TARGET_URL, params=PARAMS)
    js = json.loads(req.text)
    data = js["result"]["data"]
    today_bond = []
    shangshi_bond = []
    for item in data:
        if item['PUBLIC_START_DATE'] is not None:
            start_date = item['PUBLIC_START_DATE'].split(' ')[0].split('-')
            year = start_date[0]
            month = start_date[1]
            day = start_date[2]
            if int(year) == time.localtime().tm_year and int(month) == time.localtime().tm_mon and int(day) == time.localtime().tm_mday:
                today_bond.append(
                    Bond.Bond(item["SECURITY_NAME_ABBR"], item["SECURITY_CODE"], item["CONVERT_STOCK_PRICE"], item["TRANSFER_PRICE"]))
        if item['BOND_START_DATE'] is not None:
            list_date = item['BOND_START_DATE'].split(' ')[0].split('-')
            year = list_date[0]
            month = list_date[1]
            day = list_date[2]
            if int(year) == time.localtime().tm_year and int(month) == time.localtime().tm_mon and int(day) == time.localtime().tm_mday:
                shangshi_bond.append(
                    Bond.Bond(item["SECURITY_NAME_ABBR"], item["SECURITY_CODE"], item["CONVERT_STOCK_PRICE"], item["TRANSFER_PRICE"]))

    wx_msg = '\n'
    wx_msg += '今日发售：\n\n'

    if len(today_bond) > 0:
        for bond in today_bond:
            if bond.price != "-" and bond.price != "-":
                wx_msg += '- 债券代码：%s，债券简称：%s，正股价：%s，转股价：%s, 转股价值：%.2f' % (
                    bond.code, bond.name, bond.price, bond.swap_price, bond.swap_value)
                if bond.swap_value > 90:
                    wx_msg += '  推荐✅'
            else:
                wx_msg += '- 债券代码：%s，债券简称：%s，正股价：%s，转股价：%s, 转股价值：%s' % (
                    bond.code, bond.name, bond.price, bond.swap_price, bond.swap_value)
            wx_msg += '\n\n'
    else:
        wx_msg += '- 无\n\n'

    wx_msg += '今日上市：\n\n'
    if len(shangshi_bond) > 0:
        for bond in shangshi_bond:
            wx_msg += '- 债券代码：% s，债券简称：% s\n\n' % (bond.code, bond.name)
    else:
        wx_msg += '- 无\n\n'

    if '今日发售' in wx_msg or '今日上市' in wx_msg:
        wx_msg += '[点击详情查看一览表](%s)' % PAGE_URL
        log(wx_msg)
        wx_send.wx_send(title='每日可转债', content=wx_msg)
    else:
        log("今日无可转债发行或上市")


if __name__ == "__main__":
    main()
