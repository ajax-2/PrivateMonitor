# coding: utf-8

from src.Interface.StatusInterface import StatusInterface


class StatusHandler(object):

    @staticmethod
    def get_status(cluster, data):
        try:
            if not data:
                raise Exception(u"请传入json格式的参数")
            return StatusInterface.get_status(cluster, data)
        except Exception as e:
            return u"Error: 参数传入出错, 必须包含cluster,status,detail,type， Job tracker: %s" % e.message

