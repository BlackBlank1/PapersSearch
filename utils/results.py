# encoding: utf-8
# @File  : results.py
# @Author: myarme
# @Date  : 2025/01/23/11:09
from flask import jsonify


def error(message, code=400, data=None):

    return jsonify({"code": code, "message": message, "data": data})


def success(message, code=200, data=None):
    print(jsonify({"code": code, "message": message, "data": data}))
    return jsonify({"code": code, "message": message, "data": data})