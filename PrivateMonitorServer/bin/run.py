#!/usr/bin/python
# coding: utf-8

import sys
import os
import ConfigParser


class Main(object):

    config = ConfigParser.ConfigParser()
    abs_path = os.path.split(os.path.abspath(__file__))[0]

    # 解析变量
    @staticmethod
    def parse():
        config_file = Main.abs_path + "/config.ini"
        if not os.path.isfile(config_file):
            print "当前config.ini 文件不存在，当前路径为: %s,请查看" % config_file
            return False
        Main.config.read(config_file)
        mysql_db = Main.config.get("mysql", "mysql_db")
        mysql_host = Main.config.get("mysql", "mysql_host")
        mysql_port = Main.config.get("mysql", "mysql_port")
        mysql_user = Main.config.get("mysql", "mysql_user")
        mysql_password = Main.config.get("mysql", "mysql_password")
        monitor_frequency = Main.config.get("config", "monitor_frequency")
        data_keep = Main.config.get("config", "data_keep")
        username = Main.config.get('auth', "user_name")
        password = Main.config.get('auth', "pass_word")
        auth_timeout = Main.config.get('auth', "auth_timeout")
        try:
            if monitor_frequency:
                int(monitor_frequency)
            if data_keep:
                int(data_keep)
            if auth_timeout:
                int(auth_timeout)
        except Exception as e:
            print e.message
            return False
        os.putenv("MYSQL_DB", mysql_db)
        os.putenv("MYSQL_HOST", mysql_host)
        os.putenv("MYSQL_PORT", mysql_port)
        os.putenv("MYSQL_USER", mysql_user)
        os.putenv("MYSQL_PASSWORD", mysql_password)
        os.putenv("MONITOR_FREQUENCY", monitor_frequency)
        os.putenv("DATA_KEEP", data_keep)
        os.putenv('USER_NAME', username)
        os.putenv('PASS_WORD', password)
        os.putenv("AUTH_TIMEOUT", auth_timeout)
        return True

    # start
    @staticmethod
    def start():
        if not os.path.isfile(Main.abs_path + "/main/main"):
            print "当前程序main文件不存在， 请拉取main后在运行此项目!"
            sys.exit(1)
        if not os.getenv("MYSQL_HOST"):
            if not Main.parse():
                sys.exit(1)
        os.system(Main.abs_path + "/main/main > /dev/stdout")


if __name__ == "__main__":
    Main.start()
