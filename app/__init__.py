#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: __init__.py
@time: 2020/5/18
@name: app
@desc: flask view文件
"""

from flask import Flask
from flask_mongoengine import MongoEngine


def create_app(settings):
    """
    创建app
    :return:
    """
    app = Flask(import_name=__name__)
    # app.config.from_object('settings.AppDebugSettings')
    app.config.from_object(settings)
    app.debug = settings.is_debug
    # 将db注册到app中
    dbmongo = MongoEngine(app)

    from .views.user import user_view
    from .views.board import board_view

    app.register_blueprint(user_view)  # 用户模块
    app.register_blueprint(board_view)  # 留言模块

    return app
