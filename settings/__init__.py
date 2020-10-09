#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file: __init__.py
@time: 2020/5/18
@name: application
@desc: 管理项目的基础配置信息
"""
import os

from dotenv import load_dotenv

from .app_settings import AppSettings, AppDebugSettings


# 加载配置文件
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".flask.env"))
# 获取环境部署信息
flask_config = os.getenv('FLASK_CONFIG')
Settings = {
    "App": AppSettings(),
    "AppDebug": AppDebugSettings()
}.get(flask_config)
