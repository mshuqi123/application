#!/usr/bin/python
# -*- coding: UTF-8 -*-

from utils.response_json import AppResponse
from flask import Blueprint, request
from logger import logs
from models.shard_models import Data2
from utils.tools import Unit_conversion, get_sum2, output
from configs import Basic_output
basic_output = Basic_output.conf

Legend_town_view = Blueprint("Legend_town_view", __name__, url_prefix="/town")  # todo
log = logs.Log(__name__).logger

@Legend_town_view.route('/consumption2', methods=['POST', 'GET'])
def Production_consumption2():
    """生产及解锁消耗金币
    param id: 该参数为工厂id
    param grade: 该参数为工厂当前等级
    param mgrade: 该参数为工厂当前目标要升级到的等级
    """
    id = request.args.get('id')
    grade = request.args.get('grade')
    mgrade = request.args.get('mgrade')
    data = Data2.get_data(id)
    ldata = data[int(grade)-1: int(mgrade)-1]
    all = []
    for n in ldata:
        d = tuple(n)
        all.append(d)
    xall = get_sum2(all)
    name = basic_output[int(id) - 1][1]
    data = dict(
        id=id,
        consumption=Unit_conversion(xall),
        log=f"{name} 从 {grade} 级升到 {mgrade} 级共需要消耗 {Unit_conversion(xall)}")
    return AppResponse.response(code=1, data=data)

@Legend_town_view.route('/consumption', methods=['POST', 'GET'])
def Production_consumption():
    """生产及解锁消耗金币,只能计算小等级的升级消耗
    param id: 该参数为工厂id
    param grade: 该参数为工厂当前等级
    param mgrade: 该参数为工厂从当前等级要升级n次
    param discount: 该参数为工厂当前消耗便宜系数
    """
    id = request.args.get('id')
    grade = request.args.get('grade')
    num = request.args.get('num')
    discount = request.args.get('discount', '1.0')
    xgrade = int(grade)
    all = []
    for n in range(int(num)):
        xgc = Unit_conversion(int(basic_output[int(id) - 1][4]))
        pro = xgc[0] * (float(basic_output[int(id) - 1][5]) ** xgrade) * float(discount)
        xpro = Unit_conversion((pro, xgc[1]))
        all.append(xpro)
        xgrade += 1
    xall = get_sum2(all)
    name = basic_output[int(id) - 1][1]
    data = dict(
        id=id,
        consumption=Unit_conversion(xall),
        log=f"{name} 从 {grade} 级升到 {int(grade) + int(num)} 级共需要消耗 {Unit_conversion(xall)}")
    return AppResponse.response(code=1, data=data)

@Legend_town_view.route('/basic_output', methods=['POST', 'GET'])
def Basic_output():
    """计算工厂实时秒产值
    param ids: 该参数为当前已解锁的全部工厂id，以列表传入
    param grade: 该参数为当前已解锁的全部工厂的当前等级，需要与ids列表内元素纵向一一对应，以列表传入
    param double: 该参数为当前已解锁的全部工厂的当前翻倍数，需要与ids列表内元素纵向一一对应，以列表传入
    param accelerate: 该参数为当前已解锁的全部工厂的当前加速倍率，需要与ids列表内元素纵向一一对应，以列表传入
    """
    ids = request.args.get('ids')
    grade = request.args.get('grade')
    double = request.args.get('double')
    accelerate = request.args.get('accelerate')
    idsx = ids.split(',')
    gradex = grade.split(',')
    doublex = double.split(',')
    acceleratex = accelerate.split(',')
    if len(idsx) == len(gradex) == len(doublex) == len(acceleratex):
        re = output(idsx, gradex, doublex, acceleratex)
    else:
        return AppResponse.response(code=-1000, message="各个工厂对应等级翻倍长度有误，请重新输入~")
    data = dict(
        sum=re[0],
        output=re[1])
    return AppResponse.response(code=1, data=data)

@Legend_town_view.route('/reward', methods=['POST', 'GET'])
def Reward_acquisition():
    """计算招商引资&网红直播&离线收益&钻石兑换
    param ids: 该参数为当前已解锁的全部工厂id，以列表传入
    param grade: 该参数为当前已解锁的全部工厂的当前等级，需要与ids列表内元素纵向一一对应，以列表传入
    param double: 该参数为当前已解锁的全部工厂的当前翻倍数，需要与ids列表内元素纵向一一对应，以列表传入
    param accelerate: 该参数为当前已解锁的全部工厂的当前加速倍率，需要与ids列表内元素纵向一一对应，以列表传入
    param type: 该参数为计算类别，1-招商引资，2-网红直播，3-离线收益，4-钻石兑换；以整形传入
    param time: 该参数为要计算收益的时间，以秒计算，以整形传入
    """
    ids = request.args.get('ids')
    grade = request.args.get('grade')
    double = request.args.get('double')
    accelerate = request.args.get('accelerate')
    type = request.args.get('type')
    time = request.args.get('time')
    idsx = ids.split(',')
    gradex = grade.split(',')
    doublex = double.split(',')
    acceleratex = accelerate.split(',')
    if len(idsx) == len(gradex) == len(doublex) == len(acceleratex):
        re = output(idsx, gradex, doublex, acceleratex)
        attract = re[0][0] * int(time) * 60
        attract = Unit_conversion((attract, re[0][1]))
        if int(type) == 1:
            result = f"本次招商引资获得奖励为：{attract}"
        elif int(type) == 2:
            result = f"本次网红直播获得奖励为：{attract}"
        elif int(type) == 3:
            result = f"本次离线收益获得奖励为：{Unit_conversion((attract[0]* 0.8, attract[1]))}"
        elif int(type) == 4:
            result = f"本次钻石兑换获得奖励为：{attract}"
        else:
            return AppResponse.response(code=-1000, message="奖励类型参数错误，请重新输入~")
    else:
        return AppResponse.response(code=-1000, message="各个工厂对应等级翻倍长度有误，请重新输入~")
    data = dict(
        result=result)
    return AppResponse.response(code=1, data=data)














