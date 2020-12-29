# coding: utf-8

from requests import request
from src.info.LocalInfo import LocalInfo
from src.tools.RequestTools import RequestTools
from datetime import datetime

li = LocalInfo()


class LocalMonitorServer(object):

    @staticmethod
    # 本地监控状态上报
    def start():
        status = u'fail'
        grafana_status = False
        prometheus_status = False
        try:
            grafana_status = request("GET", li.grafana_url).status_code == 200
            prometheus_status = request("GET", li.prometheus_url).status_code == 200
        except Exception:
            pass
        if grafana_status and prometheus_status:
            status = u'success'
        detail = u"grafana 状态: %s, prometheus 状态: %s" % (grafana_status, prometheus_status)
        rt = RequestTools(li.cluster, "child_monitor_system", status, detail)
        code, reason = rt.send_status()
        print "%s Info: code: %s, result: %s" % (datetime.now(), code, reason)
