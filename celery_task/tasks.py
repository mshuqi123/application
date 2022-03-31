#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from flask import current_app
from models.basics_model import UserInfo
from celery_once import QueueOnce
from tools.send_email_fun import Email
from . import celery_app
from tools import send_email_tool
os.environ.setdefault("FLASK_SETTINGS_MODULE", "application.settings")

# 异步任务
@celery_app.task()
def send_email1():
    # kwargs = {'html_message': "<a href='http://10.0.26.106:8000/active_user/?id=%s'>点击激活gogogo</a>" % to}
    # try:
    #     message = Message(subject='测试', recipients=[to], body=kwargs)
    #     mail.send(message)
    # except Exception as e:
    #     print(e)
    #     raise
    to = '1170460010@qq.com'
    # app = current_app._get_current_object()
    sub = 'hello flask-mail'
    try:
        # with app.app_context():
        Email.send_email(sub, to, 'flask-mail测试代码')
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'
    # return "send email successfully!"

# 异步任务
@celery_app.task()
def send_email3():
    to = '1170460010@qq.com'
    try:
        kwargs = "<a href='http://10.0.26.106:8000/active_user/?id=%s'>djgogogo</a>" % to
        send_email_tool.send_mail(kwargs, to)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'

# 异步任务
@celery_app.task()
def send_email2(name):
    user_obj = UserInfo.objects.filter(name=name).first()
    email = user_obj.email
    try:
        kwargs = "<a href='http://10.0.26.106:8000/active_user/?id=%s'>djgogogo</a>" % name
        send_email_tool.send_mail(kwargs, email)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'

@celery_app.task()
def is_active(name):
    user_obj = UserInfo.objects.filter(name=name).first()
    if user_obj.is_active == False:
        user_obj.is_active = True
        user_obj.save()
        return '激活成功'
    else:
        return '已激活，可正常使用'

















