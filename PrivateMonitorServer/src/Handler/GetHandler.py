# coding: utf-8

from flask import abort
from src.Interface.GetInterface import GetInterface


class GetHandler(object):

    @staticmethod
    def get(type_id):
        try:
            if type_id == "frequency":
                return GetInterface.get_frequency()
            return u'未知参数!'
        except Exception as e:
            print e.message
            abort(500, "未知错误!")

    @staticmethod
    def post(type_id):
        try:
            return u'未知参数!'
        except Exception as e:
            print e.message
            abort(500, "未知错误!")