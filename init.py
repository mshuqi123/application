#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: init.py
@time: 2020/2/16
@name: init
@desc: 初始化操作封装
"""
from models import CustomMongoConnect
from settings import Settings
import mongoengine


def init_tools():
    # 各项工具初始化
    # redis 首先初始化
    # RedisConnect.init_app(settings=Settings)
    # mongo connect初始化
    CustomMongoConnect.create_connections(Settings.MONGODB_SETTINGS)
    # 工具类初始化
    # Tools.init(settings=Settings, redis_connect=RedisConnect)
    pass