#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@file: custom_logger.py
@time: 2020/2/5
@desc:
"""

try:
    import simplejson as json
except ImportError:
    import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler, WatchedFileHandler

from utils.os_tools import OSTools


class Logger(object):
    """
    新盒子日志，解决是否投递问题
    """
    # 初始化 streamHandler

    FATAL = CRITICAL = logging.FATAL
    ERROR = logging.ERROR
    WARN = WARNING = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    __stream_handler = logging.StreamHandler()
    __stream_handler.setLevel(DEBUG)
    __stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(process)d - %(levelname)s - %(message)s"))
    __logger = logging.getLogger("app_base")  # 正常日志
    __logger.propagate = False
    __logger.setLevel(DEBUG)
    __logger.addHandler(__stream_handler)

    __sls_stream_handler = logging.StreamHandler()
    __sls_stream_handler.setLevel(INFO)
    __sls_stream_handler.setFormatter(logging.Formatter("%(asctime)s ~ %(message)s"))
    __sls_logger = logging.getLogger("box_base_sls")  # 投递日志
    __sls_logger.propagate = False
    __sls_logger.setLevel(INFO)
    __sls_logger.addHandler(__sls_stream_handler)

    __sls_logger_flag = False  # 投递日志，区分线上及测试

    __sls_init = False  # 是否初始化

    @classmethod
    def set_logger(cls, logfile="log", level=logging.DEBUG, interval=0, backup_count=20, log_put_file=None,
                   sls_logger_flag=False):
        if cls.__sls_init:
            return
            # 正常日志部分
        for handler in list(cls.__logger.handlers):
            cls.__logger.removeHandler(handler)
        file_name = logfile + ".log"
        abs_path = os.path.dirname(file_name)
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)
        if interval != 0:
            file_handler = TimedRotatingFileHandler(filename=file_name, interval=interval, backupCount=backup_count)
        else:
            file_handler = WatchedFileHandler(filename=file_name)
        file_handler.setLevel(level=level)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(process)d - %(levelname)s - %(message)s"))
        cls.__logger.addHandler(file_handler)
        # 投递日志部分
        for handler in list(cls.__sls_logger.handlers):
            cls.__sls_logger.removeHandler(handler)
        if log_put_file is None:
            log_put_file = logfile + "_put.log"
        sls_file_handler = WatchedFileHandler(filename=log_put_file)
        sls_file_handler.setLevel(logging.INFO)
        sls_file_handler.setFormatter(logging.Formatter("%(asctime)s ~ %(message)s"))
        cls.__sls_logger.addHandler(sls_file_handler)
        cls.__sls_logger_flag = sls_logger_flag

        cls.__sls_init = True

    @classmethod
    def info(cls, msg, *args, **kwargs):
        filename, funname, lineno = OSTools.get_stack_info(2)
        msg = "%s - %s - %s - %s" % (filename, funname, lineno, msg)
        cls.__logger.info(msg=msg, *args, **kwargs)

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        filename, funname, lineno = OSTools.get_stack_info(2)
        msg = "%s - %s - %s - %s" % (filename, funname, lineno, msg)
        cls.__logger.debug(msg=msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        filename, funname, lineno = OSTools.get_stack_info(2)
        msg = "%s - %s - %s - %s" % (filename, funname, lineno, msg)
        cls.__logger.warning(msg=msg, *args, **kwargs)

    @classmethod
    def warn(cls, msg, *args, **kwargs):
        filename, funname, lineno = OSTools.get_stack_info(2)
        msg = "%s - %s - %s - %s" % (filename, funname, lineno, msg)
        cls.__logger.warning(msg=msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        filename, funname, lineno = OSTools.get_stack_info(2)
        msg = "%s - %s - %s - %s" % (filename, funname, lineno, msg)
        cls.__logger.error(msg=msg, *args, **kwargs)

    @classmethod
    def exception(cls, msg, *args, **kwargs):
        cls.__logger.exception(msg=msg, *args, **kwargs)

    @classmethod
    def sls_log(cls, event_name, device_id=None, uid=None, stack_level=2, **kwargs):
        filename, funcname, lineno = OSTools.get_stack_info(stack_level)
        kwargs["funcname"] = funcname
        log_msg = f'{event_name} ~ {lineno} ~ {device_id} ~ {uid} ~ ' \
                  f'{cls.__sls_logger_flag} ~ {json.dumps(kwargs, ensure_ascii=False)}'
        cls.__sls_logger.info(msg=log_msg)
        # cls.info(log_msg)
