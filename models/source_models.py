#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: source_models.py
@time: 2020-10-22
@name: msq
@desc: source库相关集合
"""

import random
import json
import time, datetime
from mongoengine import DynamicDocument, DoesNotExist
from mongoengine.queryset.visitor import Q
from mongoengine import FloatField, IntField, ListField, StringField, SequenceField, DictField, BooleanField


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

    GENDER_TYPE = (("secret", "保密"), ("male", "男"), ("female", "女"))

    uid = SequenceField(primary_key=True, value_decorator=uid_value_decorator)  # 用户id
    phone_number = StringField(max_length=200)  # 手机号码
    yid = StringField(max_length=200)  # 与客户验证的ID
    create_time = StringField(max_length=100, required=True)  # 账号创建时间
    last_login_time = StringField(max_length=100, required=True, default=time.strftime("%Y-%m-%d %H:%M:%S"))  # 最后登录时间
    status = StringField(max_length=20, required=True)  # 账号状态
    devices = ListField(required=True)  # 设备id

    gender = StringField(max_length=30, default="secret", choices=GENDER_TYPE)  # 性别
    birth_day = StringField(max_length=200)  # 出生日期
    avatar_image = StringField(max_length=200)  # 头像
    nick_name = StringField(max_length=100)  # 昵称
    tongdun_decision = StringField(max_length=100, default="Accept")
    is_cancel = BooleanField(default=False)
    current_version_name = StringField(default="", max_length=100)      # 用户当前版本号
    next_retain = FloatField(default=0) # 徒弟次日留存
    avg_dur = FloatField(default=0) # 徒弟当日平均时长
    last_update_time = IntField(default=int(time.time()))  # 最近更新时间戳

    # 收入相关
    cash_balance = FloatField(default=0)  # 现金余额
    gold_coin_balance = FloatField(default=0)  # 金币余额
    cash_coupon_balance = FloatField(default=0)  # 提现券余额
    total_extract_cash = FloatField(default=0) # 用户历史提现总额

    meta = {"collection": "userInfo", "db_alias": "default", "shard_key": ("uid",)}

    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__(*args, **kwargs)

    @property
    def id(self):
        return self.uid

    @classmethod
    def wechat_open_id_attr(cls, box_name=None):
        """
        根据不同的包名，返回不同的openid字段，兼容不同渠道的openid，uniconid一致
        :param box_name: ios跟android复用该字段
        :return:
        """
        if box_name == "c.l.b":
            return "clbw_open_id"
        elif box_name == "h5":
            return "h5_wechat_open_id"
        else:
            return "wechat_open_id"

    @classmethod
    def id_card_exists(cls, id_card):
        """
        身份证号是否已经认证
        :param id_card: 身份证号
        :return:
        """
        rs = cls.objects(id_card=id_card)
        return True if rs else False

    @classmethod
    def id_card_exists_new(cls, id_card, user_id):
        """
        身份证号是否已经认证(兼容大小写)
        :param id_card: 身份证号
        :return:
        """
        count = cls.objects(_id__ne=user_id).filter(Q(id_card=id_card.upper()) | Q(id_card=id_card.lower())).count()
        return True if count > 0 else False

    @property
    def day_age(self):
        """
        获取用户age
        :return:
        """
        try:
            return datetime.datetime.now().toordinal() - datetime.datetime.strptime(self.create_time,
                                                                                    '%Y-%m-%d %H:%M:%S').toordinal()
        except:
            return 0

    def generate_yid(self):
        """
        生成yid
        :return:
        """
        suffix = ""
        for _ in range(10):
            suffix += str(random.randint(0, 9))
        self.yid = "%s_%s" % (self.uid, suffix)

    @classmethod
    def is_login_new(cls, yid):
        """
        判断用户是否登录
        :param yid:
        :return:
        """
        uid = cls.get_uid_from_yid(yid)
        user = cls.get_by_id(uid)
        if not user:
            return None
        if user.yid != yid:
            return None
        return user

    @classmethod
    def get_by_alipay(cls, alipay_account):
        """
        获取支付宝用户
        :param alipay_account:
        :return:
        """
        rs = cls.objects(alipay_account=alipay_account)
        if not rs:
            return False
        return cls.get_by_id(rs.first().uid)

    @classmethod
    def wechat_open_id_exists(cls, wechat_open_id, box_name=None):
        """
        微信账号是否存在
        :param wechat_open_id:
        :return:
        """
        rs = cls.objects(wechat_open_id=wechat_open_id)
        return True if rs else False

    def to_format_son(self):
        """
        生成格式化的item dict
        :return:
        """
        dic = self.to_mongo()
        if "devices" in dic:
            dic.pop("devices")
        if "tongdun_decision" in dic:
            dic.pop("tongdun_decision")
        if "cash_balance" in dic:
            dic["cash_balance"] = round(dic["cash_balance"], 2)
            if dic["cash_balance"] <= 0.0:
                dic["cash_balance"] = 0.0
        if dic.get('nick_name', None):
            dic["user_name"] = dic.get('nick_name', None)
        elif dic.get("wechat_nickname", None):
            dic["user_name"] = dic.get("wechat_nickname", None)
        else:
            dic["user_name"] = dic.get('phone_number', None)
        check_values = dic.get("check_values") or {}
        dic.update(check_values)
        if "day_age" not in dic:
            dic["day_age"] = self.day_age
        return dic

    @classmethod
    def get_by_id(cls, _id):
        """
        :param _id:
        :return:
        """
        if not _id:
            return None
        return super(UserInfo, cls).get_by_id(_id)

    @classmethod
    def get_by_phone_number(cls, phone_number):
        if not phone_number:
            return None
        rs = cls.objects(phone_number=phone_number)
        if not rs:
            return None
        return cls.get_by_id(rs.first().uid)

    @classmethod
    def get_by_open_id(cls, open_id, box_pkg_name=None):
        if not open_id:
            return None
        if box_pkg_name == "c.l.b":  # 普通版
            rs = cls.objects(clbw_open_id=open_id)
        else:
            rs = cls.objects(wechat_open_id=open_id)
        if not rs:
            return None
        return cls.get_by_id(rs.first().uid)

    @classmethod
    def get_by_union_id(cls, union_id):
        if not union_id:
            return None
        rs = cls.objects(wechat_unionid=union_id)
        if not rs:
            return None
        return cls.get_by_id(rs.first().uid)

    @classmethod
    def wechat_union_id_exists(cls, union_id):
        """
        支付宝账号是否存在
        :param alipay_account:
        :return:
        """
        rs = cls.objects(wechat_unionid=union_id)
        return True if rs else False

    @classmethod
    def get_uid_from_yid(cls, yid):
        """
        从yid获取uid，默认返回""
        :param yid:
        :return:
        """
        try:
            if yid and not yid.startswith("yid"):
                return yid.split("_")[0]
            return ""
        except Exception as e:
            return ""

    @classmethod
    def get_by_yid(cls, yid):
        """
        根据yid来获取用户，并不判断用户yid是否一致
        :param yid:
        :return:
        """
        uid = cls.get_uid_from_yid(yid)
        return cls.get_by_id(uid)

    @classmethod
    def get_by_device_id(cls, device_id):
        try:
            user = cls.objects.get(device_id=device_id)
        except DoesNotExist:
            return None
        return user

    @classmethod
    def get_by_id_card(cls, id_card):
        """
        获取身份证认证用户
        :param id_card:
        :return:
        """
        rs = cls.objects(id_card=id_card)
        if not rs:
            return False
        return cls.get_by_id(rs.first().uid)

    def is_login(self, yid):
        """
        判断用户是否登录
        :param yid:
        :return: Boolean
        """
        return self.yid == yid

    @classmethod
    def get_by_yid_login(cls, yid):
        """
        判断用户是否登录
        :param yid:
        :return:
        """
        user = cls.get_by_yid(yid)
        if not user:
            return None
        if user.is_login(yid):
            return user
        return None

    def get_extract_cash_mutable(self):
        # 根据用户提现等级返回可修改的字段
        mutable_fields = []
        # 如果用户身份证号是否存在
        user_real_name = getattr(self, "real_name", None)
        user_id_card = getattr(self, "id_card", None)
        user_alipay_account = getattr(self, "alipay_account", None)
        check_values = getattr(self, "check_values", {})
        if "real_name" not in check_values.keys():
            if not (user_real_name and user_id_card):
                mutable_fields.append("real_name")
        if "id_card" not in check_values.keys():
            if not (user_real_name and user_id_card):
                mutable_fields.append("id_card")
        if "alipay_account" not in check_values.keys():
            if not user_alipay_account:
                mutable_fields.append("alipay_account")
        return mutable_fields

    def check_user_field_mutable(self, key):
        """
        检查用户real_name, id_card是否可修改，如果认证通过不能修改
        :param user:
        :param key:
        :return:
        """
        check_values = getattr(self, "check_values", {})
        value = getattr(self, key, None)
        if key in check_values.keys():
            check_value = check_values[key]
            if check_value == value:
                return False
        return True

    def update_attr(self, **kwargs):
        """
        更新相关字段信息
        :param kwargs:
        :return:
        """
        for key in kwargs:
            if hasattr(self, key) and getattr(self, key, None) not in ["", "null", None]:
                continue
            setattr(self, key, kwargs[key])
        self.last_update_time = int(time.time())


class Relationship(DynamicDocument):
    """
    设备表
    """
    _id = StringField(max_length=200, primary_key=True)  # 主键
    user_id = StringField(max_length=200)  # 用户id
    device_id = StringField(max_length=200)  # 设备ID
    android_device = StringField(max_length=200)  # 基于安卓ID的设备ID
    first_time = StringField(max_length=200, required=True,
                             default=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))  # 基于安卓ID的设备ID
    last_update_time = IntField(default=int(time.time()))  # 最近更新时间戳
    check_code_status = StringField(max_length=300, default='') # json格式，存放验证码历史状态
    check_code_pass = IntField(default=0) # 当前验证码状态，0:默认 1:后续不再验证，且给出一次弹窗提示，补贴极度衰减 2:连续三次验证通过，且超过三天可以继续弹出一次 3:连续三次验证通过，处在三天不可弹验证码期间 4:连续四次通过，永远不需弹
    check_code_record = ListField()  # 验证码历次记录
    last_check_time = IntField(default=int(time.time()))  # 最近验证码时间戳
    meta = {"collection": "relationship", "db_alias": "default", "shard_key": ("_id",)}

    def __init__(self, *args, **kwargs):
        super(Relationship, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, device_id, user_id="", *args, **kwargs):
        """
        封装主键的生成
        :param device_id:
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        return cls(device_id=device_id, user_id=user_id, _id="%s@%s" % (device_id, user_id), *args, **kwargs)

    @classmethod
    def get_by_id(cls, device_id, user_id=""):
        """
        :param device_id:
        :param user_id:
        :return:
        """
        try:
            return cls.objects.get(_id="%s@%s" % (device_id, user_id))
        except DoesNotExist:
            return None

    @classmethod
    def delete_by_id(cls, device_id, user_id=""):
        try:
            cls.objects.filter(_id="%s@%s" % (device_id, user_id)).delete()
        except Exception as e:
            # logger.exception(e)
            pass

    def update_attr(self, **kwargs):
        """
        更新相关字段信息
        :param kwargs:
        :return:
        """
        for key in kwargs:
            if hasattr(self, key) and getattr(self, key, None) not in ["", "null", None]:
                continue
            setattr(self, key, kwargs[key])
        self.last_update_time = int(time.time())

    def update_special_attr(self, special_attr):
        """
        投放相关字段专用 字段不存在或者为False情况下，更新该字段为True，且更新last_update_time
        :param special_attr: 特殊字段名
        :return:
        """
        if not getattr(self, special_attr, False):
            setattr(self, special_attr, True)
            self.last_update_time = int(time.time())
            self.save()

    @property
    def day_age(self):
        """
        获取用户age
        :return:
        """
        try:
            return datetime.datetime.now().toordinal() - datetime.datetime.strptime(self.first_time,
                                                                                    '%Y-%m-%d %H:%M:%S').toordinal()
        except:
            return 0

    @classmethod
    def device_uid_exists(cls, device_id):
        """
        获取用户age
        :return:
        """
        count = cls.objects(device_id=device_id, user_id__ne="").count()
        return True if count > 0 else False

    @classmethod
    def get_device_from_user_id(cls, user_id):
        """
        :param user_id:
        :return:
        """
        try:
            rs = cls.objects(user_id=user_id)
            if not rs:
                return None
            return cls.get_by_id(rs.first().device_id)
        except DoesNotExist:
            return None




















