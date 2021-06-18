#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@file: params_tools.py
@time: 10/22/2020 10:30
@desc: 公共参数获取
"""


class ParamsParseInit(object):
    """
    封装request
    """

    def __init__(self, request):
        """
        初始化
        """
        self.__device_id = request.cookies.get("device_id", "")  # 设备号
        self.__version_name = request.args.get("version_name", "")  # 版本号
        self.__yid = request.cookies.get("yid", "")  # yid
        self.__user_id = request.args.get("user_id", "")  # user_id
        self.__channel_name = request.args.get("channel_name", "")  # 渠道号
        self.__remote_ip = request.headers.get("X-Real-IP") if request.headers.get(
            "X-Real-IP") else request.remote_addr  # 远端ip
        self.__box_pkg_name = request.args.get("box_pkg_name", "")
        self.__imei = request.cookies.get("imei", "")  # 手机IMEI码
        self.__android_id = request.cookies.get("android_id", "")  # android_id
        self.__mac_addr = request.cookies.get("mac_addr", "")  # 手机mac_addr码
        self.__wifi_mac_addr = request.cookies.get("wifi_mac_addr", "")  # wifi_mac_addr
        self.__oaid = request.args.get("oaid", "")  # 手机oaid
        self.__platform = request.args.get("platform", "android")  # 平台
        self.__sign = request.args.get("sign", "sign")  # sign码
        self.__os_version = request.args.get("os_version", "")  # 系统版本
        self.user = None  # Mongoengine UserInfo

    @property
    def user_id(self):
        return self.__user_id

    @property
    def android_id(self):
        return self.__android_id

    @property
    def oaid(self):
        return self.__oaid

    @property
    def mac_addr(self):
        return self.__mac_addr

    @property
    def device_id(self):
        return self.__device_id

    @property
    def version_name(self):
        return self.__version_name

    @property
    def yid(self):
        return self.__yid

    @property
    def channel_name(self):
        return self.__channel_name

    @property
    def box_pkg_name(self):
        return self.__box_pkg_name

    @property
    def remote_ip(self):
        return self.__remote_ip

    @property
    def imei(self):
        return self.__imei

    @property
    def os_version(self):
        return self.__os_version

    @property
    def sign(self):
        return self.__sign

    @property
    def wifi_mac_addr(self):
        return self.__wifi_mac_addr

    def to_json(self):
        return {
            "l_device_id": self.device_id, "l_version_name": self.version_name, "l_imei": self.imei, "l_yid": self.yid,
            "l_channel_name": self.channel_name, "l_remote_ip": self.remote_ip, "l_box_pkg_name": self.box_pkg_name,
            "user_id": self.user_id
        }

    def __str__(self):
        """
        打印class
        :return:
        """
        return f"device_id:{self.device_id} version_name:{self.version_name} imei:{self.imei} yid:{self.yid} " \
               f"channel_name:{self.channel_name} remote_ip:{self.remote_ip} box_pkg_name:{self.box_pkg_name} user_id:{self.user_id}"

    __repr__ = __str__
