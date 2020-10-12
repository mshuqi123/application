#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import json
import time, datetime
from mongoengine import DynamicDocument, DoesNotExist
from mongoengine import FloatField, IntField, ListField, StringField, SequenceField, DictField


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


class UserDayStat(DynamicDocument):
    """
    用户日统计表 (游戏人天表)
    """
    _id = StringField(max_length=200, primary_key=True)  # 主键
    user_id = StringField(max_length=100)  # 用户id
    device_id = StringField(max_length=200)  # 设备id
    date = StringField(max_length=100)  # 日期
    game_count = IntField(default=0)  # 当日比赛次数
    win_game_count = IntField(default=0)  # 当天通关次数

    def __init__(self, *args, **kwargs):
        super(UserDayStat, self).__init__(*args, **kwargs)
        self._id = "%s@%s" % (self.user_id, self.date)

    @property
    def uid(self):
        return self.user_id


class UserInfo(DynamicDocument):
    """
    用户信息表
    """
    uid = SequenceField(primary_key=True, value_decorator=uid_value_decorator)  # 用户id
    phone_number = StringField(max_length=200)  # 手机号码



