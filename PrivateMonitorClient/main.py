#!/usr/bin/python
# coding: utf-8

import os
import time
from src.info.ServerInfo import ServerInfo
from src.info.LocalInfo import LocalInfo
from src.client.LocalMonitorServer import LocalMonitorServer
from src.client.SystemMonitorServer import SystemMonitorServer
from src.CronTools.CronBackup import CronBackup
import threading
import sys


def update_url(url):
    if "http" not in url:
        return "http://" + url
    return url


if __name__ == '__main__':
    si = ServerInfo()
    li = LocalInfo()
    # "需要提供 服务端Url： SERVER_URL 本地集群名称: CLUSTER, 本地监控GrafanaUrl: GRAFANA_URL, 本地监控PrometheusUrl: PROMETHEUS_URL"
    s_url = os.getenv("SERVER_URL") or "http://127.0.0.1:9200"
    g_url = os.getenv("GRAFANA_URL") or "http://127.0.0.1:3000"
    p_url = os.getenv("PROMETHEUS_URL") or "http://127.0.0.1:9090"
    c_cluster = os.getenv("CLUSTER") or "demo"
    b_time = os.getenv("BACKUP_TIME") or "24"
    p_services = os.getenv("PRIMARY_SERVICE") or "sshd,rsyslog,systemd-journald"

    s_url = update_url(s_url)
    g_url = update_url(g_url)
    p_url = update_url(p_url)

    # 初始化服务端信息
    if not si.set_server_info(s_url, c_cluster):
        print "需要提供正确的服务端Url： SERVER_URL 本地集群名称: CLUSTER"
        sys.exit(1)
    if not si.init():
        sys.exit(1)

    # 初始化本地信息
    li.set_local_info(c_cluster, g_url, p_url, b_time, p_services)

    # 启动定时任务
    CronBackup.start()

    # 启动服务
    while True:
        if not si.check_health():
            time.sleep(60)
            continue
        t1 = threading.Thread(target=LocalMonitorServer.start)
        t2 = threading.Thread(target=SystemMonitorServer.start)
        t1.start(); t2.start()
        t1.join(); t2.join()
        time.sleep(si.server_frequency)
