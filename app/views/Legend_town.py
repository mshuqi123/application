#!/usr/bin/python
# -*- coding: UTF-8 -*-

from utils.response_json import AppResponse
from flask import Blueprint, request
from logger import logs
from models.shard_models import Data2
from utils.tools import Unit_conversion, get_sum2
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
        message=f"{name} 工厂从 {grade} 级升到 {mgrade} 级共需要消耗 {Unit_conversion(xall)}")
    return AppResponse.response(code=1, data=data)


















