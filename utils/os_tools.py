#!/usr/bin/env python
# -*- coding:utf-8 _*-
"""
@file: os_tools.py
@time: 2019-06-03
@desc: 常用工具集合
"""
import glob
import gzip
import os
import platform

import shutil
import sys
import time
from urllib.parse import urljoin, urlencode, urlsplit


class OSTools(object):
    """
    系统处理相关类
    """

    @classmethod
    def get_host_name(cls):
        """
        获取当前ecs hostname
        :return:
        """
        try:
            return platform.node()
        except Exception as e:
            return ""

    @classmethod
    def get_file_name(cls, filename):
        """
        根据__file__来获取文件名，出错情况下返回bin
        :return:
        """
        try:
            import os
            return os.path.split(filename)[-1].split('.')[0]
        except Exception as e:
            return "bin"

    @classmethod
    def get_stack_info(cls, level=2):
        """
        获取调用栈相关信息
        :return: filename, lineno, name
        """
        try:
            current_frame = sys._getframe(level)
            return os.path.basename(
                current_frame.f_code.co_filename), current_frame.f_code.co_name, current_frame.f_lineno
        except Exception:
            return "(unknown file)", 0, "(unknown function)"

    @classmethod
    def join_url(cls, host, path, version_name, yid="", uid="", cache_time=18000, back_page=1, platform="android",
                 sdhzinfo='{"downloadTag": -1, "schemeSupport": true}', **kwargs):
        """
        根据host拼接字符串
        :param host: 静态资源所在域名 例如http://www.baidu.com  or  https://www.baidu.com
        :param path: 具体地址
        :param version_name: 版本号
        :param yid:
        :param uid:
        :param cache_time: 缓存时间，秒数，必须为10的整数倍
        :param back_page: 1 是否允许H5返回上一级
        :param sdhzinfo: 客户端参数，是否允许下载
        :param 其他扩展参数
        :return:
        """
        # 对params进行分装
        cache_time = 18000 if cache_time == 0 else cache_time  # 不可为零
        cache_time = int(cache_time // 10)  # 必须为10的整数倍
        params = {
            "sdhzinfo": sdhzinfo,
            "back_page": back_page,
            "version_name": version_name,
            "platform": platform,
            "yid": yid,
            "uid": uid,
            "timestamp": int(time.time() // (cache_time * 10))
        }
        for key, value in kwargs.items():
            if isinstance(value, bool):
                params[key] = "true" if value else "false"
            else:
                params[key] = value

        return urljoin(base=host, url=path) + "?" + urlencode(params)

    @classmethod
    def get_netloc_from_url(cls, url):
        """
        根据url获取host
        :param url:
        :return:
        """
        split_result = urlsplit(url)
        if split_result:
            return split_result.netloc
        return ""

    @classmethod
    def delete_file(cls, file):
        """
        删除相关文件
        :param file:
        :return:
        """
        if os.path.exists(file):
            os.remove(file)

    @classmethod
    def rotate_to_gz(cls, source, limit=0):
        """
        针对日志进行打包
        :param source:
        :param limit:
        :return:
        """
        if os.path.exists(source):
            target = "%s.%s.gz" % (source, time.strftime("%Y-%m-%d_%H-%M-%S"))
            with open(source, "rb") as fin, gzip.open(target, "wb") as fout:
                shutil.copyfileobj(fin, fout)

            with open(source, "w"):
                pass
            # 文件个数
            if limit > 0:
                rm_files = sorted(glob.glob(
                    '%s.[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]' % source + '_[0-9][0-9]-[0-9][0-9]-[0-9][0-9].gz'))[
                           :-limit]
                for f in rm_files:
                    cls.delete_file(f)
