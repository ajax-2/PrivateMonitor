# coding: utf-8

from flask import abort
from src.Interface.GetInterface import GetInterface


class GetHandler(object):

    @staticmethod
    def get(type_id):
        try:
            if type_id == "frequency":
                return GetInterface.get_frequency()
            if type_id.startswith("cluster"):
                return GetInterface.check_cluster(type_id.split("|")[-1])
            return u'未知参数!'
        except Exception as e:
            abort(500, u"未知错误!" % e.message)

    @staticmethod
    def post(type_id):
        try:
            return u'未知参数!'
        except Exception as e:
            abort(500, u"未知错误! %s " % e.message)
