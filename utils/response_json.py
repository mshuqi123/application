#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@file: response_json.py
@time: 2020-08-18
@desc: 返回消息组装
"""

from flask import jsonify


class AppResponse(object):
    """
    json response类
    """
    code_dict = {
        1: [200, "测试成功"],
        -1000: [200, "系统内部错误"],
        -1001: [200, "手机号已被注册"],
        -1002: [200, "验证码已发"],
        -1003: [200, "短信平台校验错误"],
        -1004: [200, "未输入验证码"],
        -1005: [200, "未输入手机号"],
        -1007: [200, "验证码不正确"],
        -1008: [200, "手机号尚未注册"],
        -1010: [200, "yid错误或不存在"],
    }

    @classmethod
    def response(cls, code=1, message='', data=None, **kwargs):
        j = dict()
        j["code"] = code
        http_status = cls.code_dict.get(code, [200, ""])[0]
        if message:
            j["message"] = message
        else:
            j["message"] = cls.code_dict.get(code, [200, ""])[1]
        if data or data == []:
            j["data"] = data
        else:
            j["data"] = {}

        # 打印相关日志
        # if code < 0:
        #     logger.sls_log(event_name="response", stack_level=3, message=message, data=data, **kwargs)
        return jsonify(j), http_status
