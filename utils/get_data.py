#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import pandas as pd
from utils import setting

def fruit_data():
    """我的水果店数据获取"""
    dir = os.listdir(setting.data + "/fruit")
    try:
        if dir:
            sheetName = '对照组'
            # sheetName = '实验1+实验2'
            a = pd.read_excel(setting.data + r"\fruit\test.xlsx", sheet_name=sheetName, columns=[], nrows=300, encoding_override="cp1252")
            min_data = list(a['波动-最小'])
            max_data = list(a['波动-最大'])
            nvs = zip(min_data, max_data)
            nvDict = list((name, value) for name, value in nvs)
            return nvDict
    except:
        return "数值表文件不存在"

def grill_data():
    """我的烧烤摊数据获取"""
    # sheetName = '对照组'
    sheetName = '实验1+实验2'
    a = pd.read_excel(setting.data + r"\1020-补贴实验配表.xlsx", sheet_name=sheetName, columns=[], nrows=300,
                      encoding_override="cp1252")
    min_data = list(a['波动-最小'])
    max_data = list(a['波动-最大'])
    nvs = zip(min_data, max_data)
    nvDict = list((name, value) for name, value in nvs)
    return nvDict

def richcity_data():
    """西瓜市首富数据获取"""
    sheetName = '闯关补贴'
    a = pd.read_excel(setting.data + r"\西瓜市首富补贴-升级.xlsx", sheet_name=sheetName, columns=[], nrows=300,
                      encoding_override="cp1252")
    min_data = list(a['波动最小'])
    max_data = list(a['波动最大'])
    nvs = zip(min_data, max_data)
    nvDict = list((name, value) for name, value in nvs)
    return nvDict

if __name__ == '__main__':
    # d = fruit_data()
    # d = grill_data()
    d = richcity_data()
    print(d)