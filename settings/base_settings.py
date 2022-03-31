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

    MAIL_SERVER = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
    MAIL_PORT = 465
    MAIL_USERNAME = '1170460010@qq.com'  # 发送邮件的邮箱帐号
    MAIL_PASSWORD = 'bxbcqxnfhdbsigha'  # 授权码,各邮箱的设置中启用smtp服务时获取
    DEFAULT_FROM_EMAIL = MAIL_USERNAME
    MAIL_DEFAULT_SENDER = '1170460010@qq.com'
    # 这样收到的邮件，收件人处就会这样显示
    # DEFAULT_FROM_EMAIL = '2333<'1504703554@qq.com>'
    MAIL_USE_TLS = True  # 使用ssl

    # EMAIL_USE_TLS = False # 使用tls
    # EMAIL_USE_SSL 和 EMAIL_USE_TLS 是互斥的，即只能有一个为 True

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

