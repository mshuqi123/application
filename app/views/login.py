#!/usr/bin/python
# -*- coding: UTF-8 -*-

from utils.response_json import AppResponse
from flask import Blueprint, request
from models.source_models import UserDayStat, UserInfo
from app.views import parse_params
from commons.login_fun import tourists_register_submit

login_view = Blueprint("login_view", __name__, url_prefix="/login")  # todo


@login_view.route('/tourists_submit', methods=["POST"])
@parse_params
def tourists_submit(l_params):
    """
    游客登录
    :return:
    """
    try:
        return tourists_register_submit(l_params)

    except Exception as e:
        return AppResponse.response(code=-1000, device_id=l_params.device_id)


