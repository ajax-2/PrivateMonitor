# coding: utf-8

from src.tools.DateTools import DateTools
from datetime import datetime
from src.orm.SqlStrunct import Monitor
from src.tools.CronTools import CronMonitor


class StatusImplement(object):

    @staticmethod
    def get_status(cluster, data):
        if data['cluster'] != cluster:
            raise Exception(u"传入参数有误，请重新传入")
        if not data['detail'] or not data['type']:
            raise Exception(u"传入参数有误，请重新传入")
        if data['status'] != "success" and data['status'] != "fail":
            raise Exception(u"传入参数有误，请重新传入")
        monitor = Monitor()
        monitor.cluster = cluster
        monitor.detail = data['detail']
        monitor.status = True if data['status'] == "success" else False
        monitor.type = data['type']
        monitor.time = DateTools.date_format(datetime.now())
        ct = CronMonitor()
        ct.insert_monitor(monitor)
        return "Well"
