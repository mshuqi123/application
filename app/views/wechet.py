#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, time
from utils.response_json import AppResponse
from flask import Blueprint, request
from models.basics_model import Users, UserInfo
from app.extensions import cache
from tools.send_email_fun import Email
from celery_task.tasks import send_email1, is_active, send_email2
from check_result import check_result


wechet_view = Blueprint("wechet_view", __name__, url_prefix="/wechet")  # todo

@wechet_view.route('/login', methods=['POST'])
def login():
    """
    用户注册
    :return:
    """
    # name_id = request.args.get('name_id')
    # age = request.args.get('age')
    # name = request.args.get('name')
    # gender = request.args.get('gender')
    # data = dict(name_id=name_id,
    #             age=age,
    #             name=name,
    #             gender=gender)
    # Users(name_id=name_id, name=name, age=age, gender=gender).save()
    return AppResponse.response(code=1, data={})
