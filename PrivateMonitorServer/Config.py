# coding: utf-8

import ConfigParser
import os


# 解析配置文件
class Config(object):

    # 常量
    config = ConfigParser.ConfigParser()
    abs_path = os.path.split(os.path.abspath(__file__))[0]
    config_file = "config.ini"

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

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    # 解析
    def parse_from_config_ini(self):
        self.config.read(self.abs_path + os.path.sep + self.config_file)
        self.mysql_db = self.config.get("mysql", "mysql_db")
        self.mysql_host = self.config.get("mysql", "mysql_host")
        self.mysql_port = self.config.getint("mysql", "mysql_port")
        self.mysql_user = self.config.get("mysql", "mysql_user")
        self.mysql_password = self.config.get("mysql", "mysql_password")
        self.monitor_frequency = int(self.config.get("config", "monitor_frequency"))
        self.data_keep = int(self.config.get("config", "data_keep"))

    # 检验配置
    def check_config(self):
        if self.mysql_host and self.mysql_db and self.mysql_port and self.mysql_user and self.mysql_password \
                and self.monitor_frequency > 0:
            return True
        return False

    # 测试配置解析
    def test_config(self):
        return self.mysql_host
