#!/usr/bin/python
# coding: utf-8

import os
import ConfigParser
import time
import sys


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
        server_url = Main.config.get("server", "server_url")
        cluster = Main.config.get("local", "cluster")
        grafana_url = Main.config.get("local", "grafana_url")
        prometheus_url = Main.config.get("local", "prometheus_url")
        backup_time = Main.config.get("local", "backup_time")
        primary_services = Main.config.get("local", "primary_services")
        try:
            if backup_time:
                int(backup_time)
            if primary_services:
                primary_services.split(',')
        except Exception as e:
            print e.message
            return False
        
        os.putenv("CLUSTER", cluster)
        os.putenv("SERVER_URL", server_url)
        os.putenv("GRAFANA_URL", grafana_url)
        os.putenv("PROMETHEUS_URL", prometheus_url)
        os.putenv("BACKUP_TIME", backup_time)
        os.putenv("PRIMARY_SERVICES", primary_services)
        return True

    # start
    @staticmethod
    def start():
        if not os.path.isfile(Main.abs_path + "/client"):
            print "当前程序client文件不存在， 请拉取client后在运行此项目!"
            sys.exit(1)

        if not os.getenv("SERVER_URL") and not Main.parse():
            print "传入参数不合法， 请查看config.ini"
            sys.exit(1)
        i = 0
        while True:
            if i > 60:
                break
            try:
                os.system(Main.abs_path + "/client > /dev/stdout")
            except Exception as e:
                print e.message
            i += 1
            time.sleep(60)


if __name__ == "__main__":
    Main.start()
