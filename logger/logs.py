#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import logging.config
from utils import setting

class Log:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(setting.BASE_DIR + "/logger/log.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        self.logger.addHandler(handler)
        self.logger.addHandler(console)

if __name__ == '__main__':
    logger = Log(__name__).logger
    logger.info("aasf")