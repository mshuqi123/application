#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import traceback
import base64
import hashlib
import calendar
import datetime
import uuid
import time, json
from utils import rsa_tools
from utils import setting
from utils import get_data
from logger import logs
private_path = setting.conf + '/rsa-private.pem'
pubkey_path = setting.conf + '/rsa-public.pem'
log = logs.Log(__name__).logger

TEST_HOST = "http://backend-debug1.huixuanjiasu.com/fruit"
ONLINE_HOST = "http://fruit.yuanlijuzhen.com"
pkg_name = "com.sellfruit.ljjz"


class ContentTest:

    def __init__(self, yid, version_name, channel_name, game_version, device_id, is_test, game_count, open_verification):
        self.yid = yid
        assert "_" in yid
        self.user_id = yid.split("_")[0]
        self.version_name = version_name
        self.channel_name = channel_name
        self.device_id = device_id
        self.game_version = game_version
        self.is_test = is_test
        self.guest_total = 0
        self.data_fw = get_data.fruit_data()
        self.open_verification = open_verification
        if self.is_test:
            self.host = TEST_HOST
        else:
            self.host = ONLINE_HOST
        self.count = game_count
        self.rsa = rsa_tools.RSATool(private_path, pubkey_path)

    def get_reward(self):
        url = f"{self.host}/behaviors/get_pick_up_reward"
        params = dict(
            version_name=self.version_name,
            game_version=self.game_version,
            channel_name=self.channel_name,
            user_id=self.user_id,
            device_id=self.device_id,
            oaid='47FC4B40F5254F1C97A77E48E1A1DAB84f28677e544ce5bfc0553cc41e29dab6',
            ii='ODYyNTY2MDQ1ODc0NTMx',
            box_pkg_name=pkg_name
        )
        cookies = dict(
            yid=self.yid,
            device_id=self.device_id,
            android_id=self.device_id
        )
        body = dict(
            yid=self.yid,
            device_id=self.device_id,
            business_data='{"food_info":[{"pos_id":1,"food_data":[{"food_id":1,"status":0}]}]}'
        )
        sign_data = self.get_sign(channel_name=self.channel_name,
                                  version_name=self.version_name,
                                  uri='/behaviors/get_pick_up_reward',
                                  device_id=self.device_id)
        params.update(sign_data)
        try:
            resp = requests.request(method="POST", url=url, params=params, data=body, cookies=cookies)
            resp = resp.json()
            if resp.get("encrypt"):   # 解密
                resp = self.rsa.rsa_decrypt(resp["data"])
            data = resp["data"]['reward'][0]
            cash_balance = data['cash_balance']
            if len(str(int(cash_balance))) >= 1:
                cash_balance = cash_balance / 10000
                cash_balance = f"{cash_balance} 元 "
            game_balance = data['game_balance']
            with open(setting.data + f'\\{self.yid}.txt', 'a+', encoding='utf-8') as f:
                f.write(f"本次揽客获得红包 {cash_balance}, 金币 {game_balance}\n")
                if self.open_verification:
                    pass
                else:
                    data_fw = self.data_fw[self.guest_total - 1]
                    f.write(f"本关卡的奖励波动范围为 {data_fw}\n")
                    if data_fw[0] <= float(cash_balance.split(' ')[0]) <= data_fw[1]:
                        f.write("奖励符合预期\n--------------------------------------------------\n")
                    else:
                        f.write("奖励与预期不符请注意核对\n--------------------------------------------------\n")
        except Exception:
            traceback.print_exc()

    def sync_quest(self):
        url = f"{self.host}/game/sync_guest"
        params = dict(
            version_name=self.version_name,
            game_version=self.game_version,
            channel_name=self.channel_name,
            user_id=self.user_id,
            device_id=self.device_id,
            oaid='47FC4B40F5254F1C97A77E48E1A1DAB84f28677e544ce5bfc0553cc41e29dab6',
            ii='/game/sync_guest',
            box_pkg_name=pkg_name
        )
        cookies = dict(
            yid=self.yid,
            device_id=self.device_id,
            android_id=self.device_id
        )
        body = dict(
            yid=self.yid,
            device_id=self.device_id,
            business_data='{"desk_pos_id":1,"game_time":6,"guest_channel":1,"local_used_time":"32","agreement_time":"0"}'
        )
        sign_data = self.get_sign(channel_name=self.channel_name,
                                  version_name=self.version_name,
                                  uri='/game/sync_guest',
                                  device_id=self.device_id)
        params.update(sign_data)
        try:
            resp = requests.request(method="POST", url=url, params=params, data=body, cookies=cookies)
            resp = resp.json()
            if resp.get("encrypt"):  # 解密
                resp = self.rsa.rsa_decrypt(resp["data"])
            data = resp["data"]
            guest_total = data['guest_total']
            level = data['level']
            self.guest_total = guest_total
            with open(setting.data + f'\\{self.yid}.txt', 'a+', encoding='utf-8') as f:
                f.write(f"{self.user_id} 用户已累计招揽 {guest_total} 个顾客, 目前等级为 {level}; ")
        except Exception:
            traceback.print_exc()

    def info(self):
        pass

    def get_sign(self, uri, version_name, channel_name, device_id):
        sign_data = {}
        secret = "gohell"
        nonce_str = uuid.uuid1()
        future = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        expiry = calendar.timegm(future.timetuple())
        secure_link = f"{uri} {version_name} {channel_name} {device_id} {expiry} {nonce_str} {secret}".encode('utf-8')
        hash = hashlib.md5(secure_link).digest()
        base64_hash = base64.urlsafe_b64encode(hash)
        str_hash = base64_hash.decode('utf-8').rstrip('=')
        sign_data["sign"] = str_hash
        sign_data["nonce_str"] = nonce_str
        sign_data["et"] = expiry
        return sign_data


    @classmethod
    def get_code_music_id(cls, code):
        id_hex = code.split('L')[0]
        return str(int(id_hex.upper(), 16))

    def start_test(self):
        for i in range(self.count):
            self.sync_quest()
            self.get_reward()
            time.sleep(0.1)


if __name__ == '__main__':
    """测试配置"""
    yid = "23112311_8535805061"  # 抓包yid
    game_count = 2
    is_test = 1   # 0线上  1测试
    open_verification = 0   # 0开启  1关闭
    version_name = "1.1.2.2"
    channel_name = "base"
    game_version = '1.0.7.4'
    # game_version = '1.0.9.36'
    # channel_name = "vivo"
    device_id = "3b5b7dcc-c635-344a-82e4-4eeb13b68310"  # ab
    # device_id = "574e555e-0226-379c-b850-dad9b752d925"  # ab
    # 年龄端上调
    """"""

    test = ContentTest(yid=yid,
                       game_count=game_count,
                       is_test=is_test,
                       channel_name=channel_name,
                       version_name=version_name,
                       device_id=device_id,
                       game_version=game_version,
                       open_verification=open_verification)
    test.start_test()
