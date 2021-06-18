#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
from utils.response_json import AppResponse
from flask import request
from models.source_models import UserDayStat, UserInfo, Relationship


def tourists_register_submit(request_data):
    """
    游客注册提交
    :param request_data:公共参数
    :return:
    """
    try:
        if Relationship.device_uid_exists(device_id=request_data.device_id):
            return AppResponse.response(code=-8888, message="此设备非新设备")
        user = UserInfo(status="active", devices=[request_data.device_id], gold_coin_balance=0,
                        cash_balance=0.0, box_pkg_name=request_data.box_pkg_name,
                        create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        last_login_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                        register_method="tourists", is_tourists=True, register_type="tourists")

        user.generate_yid()
        if request_data.channel_name:
            user.channel_name = request_data.channel_name
        if request_data.version_name:
            user.version_name = request_data.version_name
        user.nick_name = f"游客{user.uid}"
        user.tongdun_decision = "Accept"

        # logger.info("code: %d, device_id number: %s, message: %s" % (1, request_data.device_id, "游客注册成功"))
        msg = "注册成功"

        relation_ship = Relationship.get_by_id(request_data.device_id, user.uid)
        if not relation_ship:
            relation_ship = Relationship.create(channel_name=request_data.channel_name,
                                                device_id=request_data.device_id, mac_addr=request_data.mac_addr,
                                                android_id=request_data.android_id, imei=request_data.imei,
                                                first_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                                                version_name=request_data.version_name, user_id=user.uid,
                                                last_update_time=int(time.time()),
                                                box_pkg_name=request_data.box_pkg_name,
                                                is_tourists=True)
        else:
            relation_ship.update_attr(channel_name=request_data.channel_name, device_id=request_data.device_id,
                                      mac_addr=request_data.mac_addr,
                                      android_id=request_data.android_id, imei=request_data.imei,
                                      last_update_time=int(time.time()),
                                      version_name=request_data.version_name,
                                      user_id=user.uid)
        relation_ship.save()
        user.save()

        return AppResponse.response(code=1, message=msg,
                                    data={
                                        "yid": user.yid,
                                        "user_id": user.uid,
                                        "user_name": user.nick_name
                                    })
    except Exception as e:
        # logger.exception(e)
        return AppResponse.response(code=-1000)

























