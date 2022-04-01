#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@file: wechet_models.py
@time: 2022-04-01
@name: msq
@desc: wechet库相关集合
"""

import random
import json
import time, datetime
from mongoengine import DynamicDocument, DoesNotExist
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import FloatField, IntField, ListField, StringField, SequenceField, DictField, BooleanField, DateTimeField


def uid_value_decorator(index):
    """
    uid生成函数
    :param index:
    :return:
    """
    value = ""
    for _ in range(3):
        value += str(random.randint(0, 9))
    index = 2 * index + random.randint(1017, 1018)
    filling_char = "1"
    return str(index) + value + filling_char  # 用户id是1结尾


class User(DynamicDocument):
    """
    用户信息表
    """

    uid = SequenceField(primary_key=True, value_decorator=uid_value_decorator)  # 用户id
    username = StringField(max_length=100, required=True)
    password_hash = StringField(max_length=200, required=True)
    phone = StringField(max_length=200, unique=True, required=True)
    create_time = DateTimeField(default=datetime.datetime.now)  # 记录的创建时间
    update_time = DateTimeField(default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 记录的最后更新时间

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    meta = {"collection": "user", "db_alias": "default", "shard_key": ("uid",)}

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @property
    def id(self):
        return self.uid












