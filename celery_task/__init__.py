#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@file: __init__.py
@time: 2020/2/16
@name: zdl
@desc:
"""

import os
from models import CustomMongoConnect
from settings import Settings
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab


# 获取配置信息
redis_prefix = 'redis://101.43.185.228:6379'

celery_app = Celery('application', broker=redis_prefix, backend=redis_prefix)

celery_app.conf.BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3.1 * 24 * 60 * 60}
celery_app.conf.CELERY_TASK_RESULT_EXPIRES = 60
celery_app.conf.CELERY_REDIS_MAX_CONNECTIONS = 3  # redis最大链接数
celery_app.conf.CELERY_TASK_IGNORE_RESULT = True  # 忽略任务结果
# 时区
celery_app.conf.CELERY_TIMEZONE = 'Asia/Shanghai'
# 是否使用UTC
celery_app.conf.CELERY_TIMEZONE = False
celery_app.conf.CELERY_IMPORTS = (
    'celery_task.tasks'
)

# 防重复锁
celery_app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': redis_prefix + "/2",
        'default_timeout': 60
    }
}

celery_app.conf.CELERYBEAT_SCHEDULE  = {
    'add-every-30-seconds': {
         'task': 'celery_task.tasks.send_email3',
         'schedule': timedelta(seconds=60),      # 每 30 秒执行一次
#         'args': ()                             # 任务函数参数
    },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task.lession',
#         'schedule': crontab(hour=9, minute=50),  # 每天早上 9 点 50 分执行一次
# #       'args': ()                               # 任务函数参数
#     }
}

# mongo connect初始化
CustomMongoConnect.create_connections(Settings.MONGODB_SETTINGS)
