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

@Legend_town_view.route('/consumption2', methods=['POST'])
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
        log=f"{name} 工厂从 {grade} 级升到 {mgrade} 级共需要消耗 {Unit_conversion(xall)}")
    return AppResponse.response(code=1, data=data)

@Legend_town_view.route('/basic_output', methods=['POST'])
def Basic_output():
    """生产及解锁消耗金币
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
    log.info(idsx)
    if len(idsx) == len(gradex) == len(doublex) == len(acceleratex):
        re = output(idsx, gradex, doublex, acceleratex)
    else:
        return AppResponse.response(code=-1000, message="各个工厂对应等级翻倍长度有误，请重新输入~")
    data = dict(
        sum=re[0],
        output=re[1])
    return AppResponse.response(code=1, data=data)
















