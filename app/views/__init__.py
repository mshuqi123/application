#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, functools
from flask import request
from utils.response_json import AppResponse
from utils.params_tools import ParamsParseInit


def parse_params(view):
    """
    参数解析
    :return:
    """
    @functools.wraps(view)
    def _wrapped(*args, **kwargs):
        try:
            if "l_params" in kwargs:
                l_params = kwargs["l_params"]
            else:
                kwargs["l_params"] = l_params = ParamsParseInit(request)
            start_time = time.time()
            f = view(*args, **kwargs)
            used_time = time.time() - start_time
            if used_time >= 0.1:
                # logger.sls_log(event_name="view_used_time", device_id=l_params.device_id, uid=l_params.user_id,view=view.__name__,
                #                used_time=used_time)
                pass
            return f
        except Exception as e:
            # logger.exception(e)
            return AppResponse.response(code=-100, funname=view.__name__)

    return _wrapped