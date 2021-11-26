#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from utils.response_json import AppResponse
from flask import Blueprint, request
from logger import logs
from commons.test_reward_fruit import ContentTest
from utils import setting

data_processing_view = Blueprint("data_processing_view", __name__, url_prefix="/data_processing")  # todo
log = logs.Log(__name__).logger

@data_processing_view.route('/fruit_reward', methods=['POST'])
def fruit_reward():
    """我的水果店数值测试接口
    param id: 该参数为工厂id
    param grade: 该参数为工厂当前等级
    param mgrade: 该参数为工厂当前目标要升级到的等级
    """
    yid = request.args.get('yid')
    game_count = request.args.get('game_count')
    is_test = request.args.get('is_test')
    open_verification = request.args.get('open_verification')
    version_name = request.args.get('version_name')
    channel_name = request.args.get('channel_name')
    game_version = request.args.get('game_version')
    device_id = request.args.get('device_id')
    file_obj = request.files.get('file')
    if file_obj:
        f = open(setting.data + '\\fruit\\test.xlsx', 'wb')
        data = file_obj.read()
        f.write(data)
        f.close()

    dir = os.listdir(setting.data)
    for i in dir:
        if f'{yid}.txt' == i:
            path = setting.data + f'\\{yid}.txt'
            try:
                os.remove(path)    # 删除文件
                # os.rmdir(path)    # 删除文件夹
            except:
                pass
    test = ContentTest(yid=yid,
                       game_count=int(game_count),
                       is_test=int(is_test),
                       channel_name=channel_name,
                       version_name=version_name,
                       device_id=device_id,
                       game_version=game_version,
                       open_verification=int(open_verification))
    test.start_test()
    with open(setting.data + f'\\{yid}.txt', 'r', encoding='utf-8') as f:
        re = f.readlines()
    data = dict(
        log=re)
    return AppResponse.response(code=1, data=data)















