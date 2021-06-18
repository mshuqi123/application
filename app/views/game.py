#!/usr/bin/python
# -*- coding: UTF-8 -*-

from utils.response_json import AppResponse
from flask import Blueprint, request
from flask import current_app
from models.source_models import UserDayStat, UserInfo
from app.views import parse_params

game_view = Blueprint("game_view", __name__, url_prefix="/game")  # todo


@game_view.route('/get_data', methods=['POST'])
def get_data():
    """
    获取人天表信息
    :return:
    """
    _id = request.args.get('_id')
    user_id = request.args.get('user_id')
    device_id = request.args.get('device_id')
    date = request.args.get('date')
    game_count = request.args.get('game_count')
    u = UserDayStat(
                user_id=user_id,
                device_id=device_id,
                date=date,
                game_count=game_count)
    u.win_game_count = 500
    u.save()
    uid = u.uid
    data = dict(
        user_id=uid,
        device_id=device_id,
        date=date,
        game_count=game_count)
    # current_app.logger.info(data)
    return AppResponse.response(code=1, data=data)


@game_view.route('/login', methods=['POST'])
def login():
    """
    游客注册
    :return:
    """
    phone_number = request.args.get('phone_number')
    channel_name = request.args.get('channel_name')
    u = UserInfo(
                phone_number=phone_number,
                channel_name=channel_name)
    u.save()
    uid = u.uid
    data = dict(
        uid=uid,
        phone_number=phone_number,
        channel_name=channel_name)
    return AppResponse.response(code=1, data=data)


@game_view.route('/get_login', methods=['POST'])
@parse_params
def get_login(l_params):
    """
    游客登陆
    :return:
    """
    phone_number = request.args.get('phone_number')
    channel_name = l_params.channel_name
    try:
        u = UserInfo.objects(phone_number=phone_number)[0]
        data = dict(
            uid=u["uid"],
            phone_number=u['phone_number'],
            channel_name=channel_name)
        return AppResponse.response(code=1, data=data)
    except:
        return AppResponse.response(code=-1008)


