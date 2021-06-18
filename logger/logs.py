#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os
from utils import setting
import logging.config
import sys

class Log:
    __obj = False
    def __new__(cls, *args, **kwargs):
        if not cls.__obj:
            cls.__obj = super().__new__(cls, *args, **kwargs)
        return cls.__obj

    def __init__(self):
        CONF_LOG = setting.BASE_DIR + "/logger/config.ini"
        logging.config.fileConfig(CONF_LOG)  # 采用配置文件
        self.logger = logging.getLogger('application')

if __name__ == '__main__':
    logger = Log().logger
    logger.info("aasf")