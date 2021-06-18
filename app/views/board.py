#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from utils.response_json import AppResponse
from flask import Blueprint, request
from models.basics_model import Board, Info
# from .. import dbmongo as db

board_view = Blueprint("board_view", __name__, url_prefix="/board")  # todo


@board_view.route('/add', methods=['POST'])
def add():
    """
    添加留言
    :return:
    """
    messager_name = request.args.get('messager_name')
    content = request.args.get('content')
    messager_age = request.args.get('messager_age')
    messager_sex = request.args.get('messager_sex')
    receiver = request.args.get('receiver')
    create_time = request.args.get('create_time')
    data = dict(messager_name=messager_name,
                content=content,
                messager_age=messager_age,
                receiver=receiver,
                create_time=create_time,
                messager_sex=messager_sex)
    Board(messager_name=messager_name, content=content, messager_age=messager_age, receiver=receiver, create_time=create_time, messager_sex=messager_sex).save()
    return AppResponse.response(code=1, data=data)


@board_view.route('/get', methods=['GET'])
def get():
    """
    获取留言
    :return:
    """
    boards = list(Board.objects().all())
    data = dict(messager_name=boards[0]["messager_name"],
                content=boards[0]["content"],
                messager_age=boards[0]["messager_age"],
                receiver=boards[0]["receiver"],
                create_time=str(boards[0]["create_time"]),
                messager_sex=boards[0]["messager_sex"])
    return AppResponse.response(code=1, data=data)


@board_view.route('/info', methods=['POST'])
def info():
    """
    获取留言
    :return:
    """
    name_id = request.args.get('name_id')
    age = request.args.get('age')
    name = request.args.get('name')
    gender = request.args.get('gender')
    data = dict(name_id=name_id,
                age=age,
                name=name,
                gender=gender)
    Info(name_id=name_id, age=age, name=name, gender=gender).save()
    return AppResponse.response(code=1, data=data)






