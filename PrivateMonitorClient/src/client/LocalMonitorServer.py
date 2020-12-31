# coding: utf-8

from requests import request
from src.info.LocalInfo import LocalInfo
from src.tools.RequestTools import RequestTools
from datetime import datetime

li = LocalInfo()


class LocalMonitorServer(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    @staticmethod
    # 本地监控状态上报
    def start():
        status = False
        grafana_status = False
        prometheus_status = False
        try:
            grafana_status = request("GET", li.grafana_url).status_code == 200
            prometheus_status = request("GET", li.prometheus_url).status_code == 200
        except Exception:
            pass
        if grafana_status and prometheus_status:
            status = True
        detail = u"grafana 状态: %s, prometheus 状态: %s" % (grafana_status, prometheus_status)
        rt = RequestTools(li.cluster, u"child_monitor_system", status, detail)
        code, reason = rt.send_status()
        print "%s Local Monitor Info: code: %s, result: %s" % (datetime.now(), code, reason)
