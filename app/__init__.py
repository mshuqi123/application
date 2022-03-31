#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: __init__.py
@time: 2020/5/18
@name: app
@desc: flask view文件
"""

from flask import Flask
from app.extensions import cache, mongo, celery, cors, mail


def create_app(settings):
    """
    创建app
    :return:
    """
    app = Flask(import_name=__name__)
    app.config.from_object(settings)
    app.debug = settings.is_debug

    register_extensions(app)     #将第三方插件整体注册到app中
    register_blueprints(app)     #将蓝图注册到app中

    return app


def register_blueprints(app):
    """蓝图集装箱"""
    from .views.user import user_view
    from .views.board import board_view
    from .views.game import game_view
    from .views.login import login_view
    from .views.Legend_town import Legend_town_view
    from .views.data_processing import data_processing_view
    from .views.wechet import wechet_view

    app.register_blueprint(user_view)  # 用户模块
    app.register_blueprint(board_view)  # 留言模块
    app.register_blueprint(game_view)  # 人天表模块
    app.register_blueprint(login_view)  # 登陆注册模块
    app.register_blueprint(Legend_town_view)  # 小镇传奇数值测试模块
    app.register_blueprint(data_processing_view)  # 测试组数值测试模块
    app.register_blueprint(wechet_view)  # 微信小程序模块


def register_extensions(app):
    """第三方插件集装箱"""
    cache.init_app(app)
    # mongo.init_app(app)    #将mongodb注册到app中
    celery.init_app(app)
    cors.init_app(app, supports_credentials=True)     # 配置全局跨域路由
    mail.init_app(app)





