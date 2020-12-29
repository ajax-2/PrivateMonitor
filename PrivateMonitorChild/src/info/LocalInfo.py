# coding: utf-8

from requests import request


class LocalInfo(object):

    cluster = ""
    grafana_url = ""
    prometheus_url = ""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # 设置参数
    def set_local_info(self, cluster, grafana_url, prometheus_url):
        self.prometheus_url = prometheus_url
        self.grafana_url = grafana_url
        self.cluster = cluster
