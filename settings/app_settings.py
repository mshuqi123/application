#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: app_settings.py
@time: 2020/5/18
@name: application
@desc: 应用基础相关配置
"""
from .base_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    应用相关配置
    """
    app_name = "测试应用"
    # mongo 数据库配置
    MONGODB_SETTINGS = [{
        "db": "app",
        "host": "101.43.185.228",
        "port": 20017,
        "alias": "default",
        "maxPoolSize": 10,
        "maxIdleTimeMS": 30000
    }]


class AppDebugSettings(BaseSettings):
    """
    应用测试服相关配置
    """
    debug = True
    # mongo 数据库配置
    MONGODB_SETTINGS = [{
        "db": "app_test",
        "host": "101.43.185.228",
        "port": 20017,
        "alias": "default",
        "maxPoolSize": 10,
        "maxIdleTimeMS": 30000
    }]

    #  celery 配置连接redis
    CELERY_BROKER_URL = 'redis://101.43.185.228:6379'
    CELERY_RESULT_BACKEND = 'redis://101.43.185.228:6379'

    @property
    def is_debug(self):
        return self.debug














