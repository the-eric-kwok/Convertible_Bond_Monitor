#!/usr/bin/env python3
# encoding: utf-8

class Bond:
    _name = ""
    _code = ""
    _price = 0.0
    _swap_price = 0.0

    def __init__(self, name, code, price, swap_price):
        self._name = name
        self._code = code
        self._price = price
        self._swap_price = swap_price
        

    """
    转股价值
    """
    @property
    def swap_value(self):
        if self._swap_price > 0 and self._price > 0:
            return self._price / self._swap_price * 100
        return "-"

    """
    正股价
    """
    @property
    def price(self):
        if self._price > 0:
            return self._price
        return "-"

    """
    转股价
    """
    @property
    def swap_price(self):
        if self._swap_price > 0:
            return self._swap_price
        return "-"

    """
    债券代码
    """
    @property
    def code(self):
        return self._code

    """
    债券简称
    """
    @property
    def name(self):
        return self._name