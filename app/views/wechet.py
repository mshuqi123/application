#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json, time
from utils.response_json import AppResponse
from flask import Blueprint, request, g, jsonify, abort
from models.wechet_model import User, Content
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

@wechet_view.route('/write', methods=['POST'])
def write():
    """
    新增日记
    :return:
    """
    phone = request.form.get('phone')
    user = User.objects.filter(phone=phone).first()
    if user:
        uid = user.uid
        username = user.username
    else:
        return AppResponse.response(code=-1, data={"title": "用户不存在"})
    title = request.form.get('title')
    data = request.form.get('data')
    text = request.form.get('text')
    status = request.form.get('status')
    if phone is None or title is None or data is None or text is None or status is None:
        return AppResponse.response(code=-1, data={"title": "内容均不可为空；请重新输入"})
    content = Content(phone=phone, uid=uid, username=username, title=title, data=data, text=text, status=status)
    content.save()
    return AppResponse.response(code=1, data={"title": "日记发布成功"})

@wechet_view.route('/get_data', methods=['POST'])
def get_data():
    """
    获取全部日记
    :return:
    """
    phone = request.form.get('phone')
    if phone is None:
        return AppResponse.response(code=-1, data={"title": "手机号不可为空；请重新输入"})
    content = Content.objects.filter(phone=phone).all()
    data = []
    for con in content:
        cont = dict(cid=con.cid,
                    title=con.title,
                     data=con.data,
                     username=con.username,
                     text=con.text,
                     status=con.status
             )
        data.append(cont)
    print(data)
    return AppResponse.response(code=1, data=data)

@wechet_view.route('/get_diary', methods=['GET'])
def get_diary():
    """
    获取日记详情
    :return:
    """
    cid = request.args.get('cid')
    if cid is None:
        return AppResponse.response(code=-1, data={"title": "该文章不存在"})
    con = Content.objects.filter(_id=cid).first()
    cont = dict(cid=con.cid,
                title=con.title,
                 data=con.data,
                 username=con.username,
                 text=con.text,
                 status=con.status
         )
    return AppResponse.response(code=1, data=cont)