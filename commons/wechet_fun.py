#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import base64
import hmac
from settings import Settings

# 生成token, 有效时间为600min
def generate_token(key, expire=Settings.EXPIRE):
    r'''
    @Args:
    key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
    expire: int(最大有效时间，单位为s)
    @Return:
    state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

# 解析token
def certify_token(key, token):
    r'''
    @Args:
    key: str
    token: str
    @Returns:
    boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
    # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True

# g = generate_token('15369333504')
# print(g)
# print(certify_token('15369333504', g))