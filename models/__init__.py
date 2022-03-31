#!/usr/bin/python
# -*- coding: UTF-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@file: __init__.py
@time: 2020/5/18
@name: zdl
@desc: 数据库 mongodb  models配置
"""
import json
import mongoengine


def replace_id_models(data):
    """
    将models格式化输出
    :param data:
    :return:
    """
    format_json = json.loads(data.to_json())
    format_json["id"] = format_json["_id"]
    format_json.pop("_id")
    return format_json


class CustomMongoConnect(object):
    """
    初始化链接
    """
    connections = {}

    @classmethod
    def create_connections(cls, conn_settings):
        """
        创建链接
        :param config:
        :return:
        """
        if cls.connections:  # 初始化一次
            return
        # If conn_settings is a list, set up each item as a separate connection
        # and return a dict of connection aliases and their connections.

        if isinstance(conn_settings, list):
            connections = {}
            for each in conn_settings:
                alias = each['alias']
                cls.connections[alias] = cls._connect(each)

    @staticmethod
    def _connect(conn_settings):
        """Given a dict of connection settings, create a connection to
        MongoDB by calling mongoengine.connect and return its result.
        """
        # db_name = conn_settings.pop('name')
        return mongoengine.connect(**conn_settings)