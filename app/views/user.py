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

@user_view.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.args.get('name')
        password = request.args.get('password')
        email = request.args.get('email')
        user_obj = UserInfo.objects.filter(name=name).first()
        if user_obj:
            return AppResponse.response(code=1, data='用户已存在')
        user_obj = UserInfo(name=name, password=password, email=email)
        user_obj.save()
        # 调用celery的发送邮件任务，将其加入消息队列，并将用户id传入
        result = send_email1.delay(name)
        print(check_result(result.id))
        # sub = 'hello flask-mail'
        # Email.send_email(sub, email, 'flask-mail测试代码')
        return AppResponse.response(code=1, data='注册成功，已向你发送一封激活邮件')
    return AppResponse.response(code=1, data='ok')

@user_view.route('/register2', methods=['POST'])
def register2():
    if request.method == 'POST':
        name = request.args.get('name')
        password = request.args.get('password')
        email = request.args.get('email')
        user_obj = UserInfo.objects.filter(name=name).first()
        if user_obj:
            # 调用celery的发送邮件任务，将其加入消息队列，并将用户id传入
            result = is_active.delay(name)
            print(check_result(result.id))
            return AppResponse.response(code=1, data='用户已存在,激活成功')
        user_obj = UserInfo(name=name, password=password, email=email)
        user_obj.save()
        return AppResponse.response(code=1, data='注册成功，请您继续请求后即可激活')
    return AppResponse.response(code=1, data='ok')

# def active_user(request):
#     uid = request.GET.get('id')
#     UserInfo.objects.filter(id=uid).update(is_active=True)
#     return redirect('/login/')


@user_view.route('/register3', methods=['POST'])
def register3():
    if request.method == 'POST':
        name = request.args.get('name')
        password = request.args.get('password')
        email = request.args.get('email')
        user_obj = UserInfo.objects.filter(name=name).first()
        if user_obj:
            return AppResponse.response(code=1, data='用户已存在')
        user_obj = UserInfo(name=name, password=password, email=email)
        user_obj.save()
        # 调用celery的发送邮件任务，将其加入消息队列，并将用户id传入
        result = send_email2.delay(name)
        print(check_result(result.id))
        return AppResponse.response(code=1, data='注册成功，已向你发送一封激活邮件')
    return AppResponse.response(code=1, data='ok')

def login(request):
    # 此处写登录的逻辑即可
    return AppResponse.response(code=1, data='ok')








