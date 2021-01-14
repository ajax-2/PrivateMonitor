# coding: utf-8

import os


# 解析配置文件
class Config(object):

    # 常量
    abs_path = os.path.split(os.path.abspath(__file__))[0]

    # 需要解析变量
    # mysql
    mysql_db = None
    mysql_host = None
    mysql_port = None
    mysql_user = None
    mysql_password = None
    # config
    monitor_frequency = None
    data_keep = None
    # auth
    username = None
    password = None
    auth_timeout = None

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    # 解析
    def parse_from_config_ini(self):
        self.mysql_db = os.getenv("MYSQL_DB") or "private_monitor"
        self.mysql_host = os.getenv("MYSQL_HOST") or "127.0.0.1"
        self.mysql_port = os.getenv("MYSQL_PORT") or 3306
        self.mysql_user = os.getenv("MYSQL_USER") or "private_monitor"
        self.mysql_password = os.getenv("MYSQL_PASSWORD") or "private_monitor"
        self.monitor_frequency = os.getenv("MONITOR_FREQUENCY") or 5
        self.data_keep = os.getenv("DATA_KEEP") or 30
        self.monitor_frequency = int(self.monitor_frequency)
        self.data_keep = int(self.data_keep)
        self.mysql_port = int(self.mysql_port)
        self.username = os.getenv('USER_NAME') or 'admin'
        self.password = os.getenv('PASS_WORD') or 'Admin@123!'
        self.auth_timeout = os.getenv("AUTH_TIMEOUT") or 10
        self.auth_timeout = int(self.auth_timeout) * 60

    # 检验配置
    def check_config(self):
        if self.mysql_host and self.mysql_db and self.mysql_port and self.mysql_user and self.mysql_password \
                and self.monitor_frequency > 0:
            return True
        return False

    # 测试配置解析
    def test_config(self):
        return self.mysql_host
