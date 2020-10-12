#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, time
from utils.response_json import AppResponse
from flask import Blueprint, request
from models.basics_model import Users
from app.extensions import cache
# from .. import dbmongo as db

user_view = Blueprint("user_view", __name__, url_prefix="/user")  # todo


@user_view.route('/login', methods=['POST'])
def login():
    """
    用户注册
    :return:
    """
    name_id = request.args.get('name_id')
    age = request.args.get('age')
    name = request.args.get('name')
    gender = request.args.get('gender')
    data = dict(name_id=name_id,
                age=age,
                name=name,
                gender=gender)
    Users(name_id=name_id, name=name, age=age, gender=gender).save()
    return AppResponse.response(code=1, data=data)


@user_view.route('/cache', methods=['GET'])
@cache.cached(key_prefix='cache')
def cache():
    time.sleep(2)
    return "马树起22222"










