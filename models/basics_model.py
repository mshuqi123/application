#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from mongoengine import Document
from mongoengine import connect, DynamicDocument, SequenceField, StringField, ListField, IntField, FloatField, \
    DoesNotExist, DictField,DateTimeField,EmailField,BooleanField


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


class Info(Document):
    name_id = StringField(max_length=20, unique=True, required=True)
    age = IntField(required=True)
    name = StringField(max_length=60, required=True)
    gender = StringField(max_length=60, required=True)

class UserInfo(Document):
    meta = {"collection": "user_info", "db_alias": "default"}
    name = StringField(max_length=32, required=True)
    password = StringField(max_length=32, required=True)
    email = EmailField(required=True)
    # 记录激活状态
    is_active = BooleanField(default=False)



