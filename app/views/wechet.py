#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, time
from utils.response_json import AppResponse
from flask import Blueprint, request, g, jsonify, abort
from models.wechet_model import User
from commons import wechet_fun

wechet_view = Blueprint("wechet_view", __name__, url_prefix="/wechet")  # todo


@wechet_view.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')
    re_password = request.form.get('re_password')
    if username is None or password is None or phone is None:
        return AppResponse.response(code=-1, data={"title": "用户名及密码、手机号均不可为空；请重新输入"})
    if User.objects.filter(phone=phone).first():
        return AppResponse.response(code=-1, data={"title": "用户已存在请直接登录"})
    if password == re_password:
        user = User(username=username, phone=phone)
        user.hash_password(password)
        user.save()
        return AppResponse.response(code=1, data={"title": "注册成功"})
    else:
        return AppResponse.response(code=-1, data={"title": "密码输入不一致请重新输入"})
#
#
# @app.route('/api/users/<int:id>')
# def get_user(id):
#     user = User.query.get(id)
#     if not user:
#         abort(400)
#     return jsonify({'username': user.username})
#
#
# @app.route('/api/token')
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token(600)
#     return jsonify({'token': token.decode('ascii'), 'duration': 600})


# @app.route('/api/resource')
# @auth.login_required
# def get_resource():
#     return jsonify({'data': 'Hello, %s!' % g.user.username})

# @wechet_view.route('/register', methods=['POST'])
# def register():
#     """
#     用户注册
#     :return:
#     """
#     # name_id = request.args.get('name_id')
#     # age = request.args.get('age')
#     # name = request.args.get('name')
#     # gender = request.args.get('gender')
#     # data = dict(name_id=name_id,
#     #             age=age,
#     #             name=name,
#     #             gender=gender)
#     # Users(name_id=name_id, name=name, age=age, gender=gender).save()
#     return AppResponse.response(code=1, data={})

@wechet_view.route('/login', methods=['POST'])
def login():
    """
    用户登陆
    :return:
    """
    username = request.form.get('username')
    password = request.form.get('password')
    phone = request.form.get('phone')
    if username is None or password is None or phone is None:
        return AppResponse.response(code=-1, data={"title": "用户名及密码、手机号均不可为空；请重新输入"})
    user = User.objects.filter(phone=phone).first()
    if user:
        if user.verify_password(password):
            token = wechet_fun.generate_token(phone)
            data = dict(username=username,
                        phone=phone,
                        token=token,
                        title="登陆成功")
            return AppResponse.response(code=1, data=data)
        else:
            return AppResponse.response(code=-1, data={"title": "密码错误"})
    else:
        return AppResponse.response(code=-1, data={"title": "没有该用户请先注册后再登录"})

@wechet_view.route('/auto_login', methods=['POST'])
def auto_login():
    """
    用户登陆
    :return:
    """
    phone = request.form.get('phone')
    token = request.form.get('token')
    cer = wechet_fun.certify_token(phone, token)
    if cer:
        user = User.objects.filter(phone=phone).first()
        data = dict(username=user.username,
                    phone=phone,
                    token=token,
                    title="自动登陆成功")
        return AppResponse.response(code=1, data=data)
    else:
        return AppResponse.response(code=-1, data={"title": "登陆已过期请重新登录"})