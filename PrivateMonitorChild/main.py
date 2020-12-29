#!/usr/bin/python
# coding: utf-8

import os
import time
from src.info.ServerInfo import ServerInfo
from src.info.LocalInfo import LocalInfo
from src.client.LocalMonitorServer import LocalMonitorServer


if __name__ == '__main__':
    si = ServerInfo()
    li = LocalInfo()
    # "需要提供 服务端Url： SERVER_URL 本地集群名称: CLUSTER, 本地监控GrafanaUrl: GRAFANA_URL, 本地监控PrometheusUrl: PROMETHEUS_URL"
    s_url = os.getenv("SERVER_URL") or "http://localhost:9200"
    g_url = os.getenv("GRAFANA_URL") or "http://grafana.monitor:80"
    p_url = os.getenv("PROMETHEUS_URL") or "http://prometheus-server.monitor:80"
    c_cluster = os.getenv("CLUSTER")

    # 初始化服务端信息
    if not si.set_server_info(s_url, c_cluster):
        print "需要提供正确的服务端Url： SERVER_URL 本地集群名称: CLUSTER"
        os.abort()
    if not si.init():
        os.abort()

    # 初始化本地信息
    li.set_local_info(c_cluster, g_url, p_url)

    # 启动服务
    while True:
        if not si.check_health():
            time.sleep(60)
            continue
        LocalMonitorServer.start()
        time.sleep(si.server_frequency)
