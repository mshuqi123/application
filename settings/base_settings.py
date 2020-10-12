#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: base_settings.py
@time: 2020/5/18
@name: application
@desc: 基础配置
"""


class BaseSettings(object):
    """
    基础配置信息
    """
    debug = False
    SECRET_KEY = 'dev key'
    CACHE_TYPE = 'simple'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    @staticmethod
    def init_app(app):
        """
        扩展类需要的话，可自行扩充
        :param app:
        :return:
        """
        pass

    @property
    def is_debug(self):
        return self.debug

