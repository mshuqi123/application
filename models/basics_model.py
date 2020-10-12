#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from mongoengine import Document
from mongoengine import connect, DynamicDocument, SequenceField, StringField, ListField, IntField, FloatField, \
    DoesNotExist, DictField,DateTimeField


class Users(Document):
    """
    用户
    """
    name_id = StringField(max_length=20, unique=True, required=True)    #学号
    name = StringField(max_length=60, required=True, unique=True)
    age = IntField(unique=True, required=True)
    gender = StringField(max_length=60, required=True)
    create_time = DateTimeField(default=datetime.datetime.now)  # 记录的创建时间
    update_time = DateTimeField(default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 记录的最后更新时间

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

class Board(Document):
    """
    留言板数据表
    """
    messager_name = StringField(max_length=20, required=True)  # 留言人
    content = StringField(max_length=500, required=True)     #内容
    messager_age = IntField(required=True)   #留言人年龄
    messager_sex = StringField(max_length=10, required=True)   #留言人性别
    receiver = StringField(max_length=20, required=True)  # 收信人姓名
    create_time = DateTimeField(default=datetime.datetime.now)  # 记录的创建时间
    update_time = DateTimeField(default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 记录的最后更新时间

    def __unicode__(self):
        return self.messager_name

    def __repr__(self):
        return self.messager_name






