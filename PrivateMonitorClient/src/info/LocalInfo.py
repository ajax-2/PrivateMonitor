# coding: utf-8

import platform
import os


class LocalInfo(object):

    cluster = ""
    grafana_url = ""
    prometheus_url = ""

    # 系统参数
    audit_log_dir = "/var/log/audit"
    ssh_log = ""
    backup_time = None
    private_service = None

    def __init__(self):
        # 设置ssh log文件
        if self.ssh_log:
            pass
        if os.path.isfile(self.audit_log_dir + '/audit.log'):
            self.ssh_log = self.audit_log_dir + '/audit.log'
            pass
        if "ubuntu" in platform.version().lower():
            self.ssh_log = "/var/log/auth.log"
        else:
            self.ssh_log = "/var/log/secure"

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # 设置参数
    def set_local_info(self, cluster, grafana_url, prometheus_url, backup_time, private_service):
        self.prometheus_url = prometheus_url
        self.grafana_url = grafana_url
        self.cluster = cluster
        self.backup_time = int(backup_time) * 60 * 60
        self.private_service = private_service.split(',')
        if "ubuntu" in platform.version().lower():
            self.private_service.append("cron")
        else:
            self.private_service.append("crond")
