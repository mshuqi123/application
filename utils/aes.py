# coding=utf-8

import base64
import hashlib
import json

from Crypto.Cipher import AES


class AESTool(object):

    def __init__(self, aes_iv, app_secret):
        self.version = '2.0'
        self.aes_mode = AES.MODE_CBC
        self.aes_iv = aes_iv
        self.app_secret = app_secret

    # 补位
    def pad(self, src):
        padding = 16 - (len(src.encode('utf-8')) % 16)
        return src + (chr(padding) * padding)

    # 解析去补位
    def unpad(self, src):
        return src[0:-ord(src[-1])]

    # 加密
    def encrypt(self, src):
        return base64.b64encode(
            AES.new(self.app_secret.encode('utf-8'), self.aes_mode, self.aes_iv.encode('utf-8')).encrypt(
                self.pad(src).encode('utf-8')))

    # 解密
    def decrypt(self, text):
        return self.unpad(AES.new(self.app_secret.encode('utf-8'), self.aes_mode, self.aes_iv.encode('utf-8')).decrypt(
            base64.urlsafe_b64decode(text)).decode('utf-8'))

    def aes(self, data):
        return self.encrypt(json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':')))

    def sign(self, data):
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        sign_before_str = self.app_secret + json_str
        sign = hashlib.md5(sign_before_str.encode('utf-8')).hexdigest()
        data['sign'] = sign
        return data


if __name__ == '__main__':
    ob = AESTool(aes_iv="0000000000000000", app_secret="ad_config_199201")
    s = {'index': '1'}
    s = json.dumps(s)
    bb = ob.encrypt(s)
    print(bb)
    aa = 'vKQD0pJPmZ55+Mnc+c5CoQ=='
    # print(aa, type(aa))
    ori = ob.decrypt(aa)
    ori = json.loads(ori)
    print(ori, type(ori))
