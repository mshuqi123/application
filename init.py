#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: init.py
@time: 2020/2/16
@name: init
@desc: 初始化操作封装
"""
from settings.app_settings import AppSettings, AppDebugSettings
import mongoengine


def init_tools():
    # 各项工具初始化
    # redis 首先初始化
    # RedisConnect.init_app(settings=Settings)
    # mongo connect初始化
    # CustomMongoConnect.create_connections(Settings.mongodb_settings)
    # 工具类初始化
    # Tools.init(settings=Settings, redis_connect=RedisConnect)
    pass