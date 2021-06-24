#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from mongoengine import Document
from mongoengine import connect, DynamicDocument, SequenceField, StringField, ListField, IntField, FloatField, \
    DoesNotExist, DictField,DateTimeField

# 用户升级消耗数值表
class Data2(Document):
    fac_id = IntField(unique=True, required=True)
    data = ListField()

    @classmethod
    def get_data(cls, id):
        """
        :param 工厂ID:
        :return:
        """
        try:
            d = cls.objects.get(fac_id=id)
            data = d.data
            return data
        except DoesNotExist:
            return None



