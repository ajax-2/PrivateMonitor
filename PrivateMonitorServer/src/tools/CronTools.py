# coding: utf-8

from src.orm.SqlStrunct import Monitor
import multiprocessing
from src.orm.SqlUtil import SqlUtil
from src.orm.SqlStrunct import Cluster
import threading
from Config import Config
import time
import telnetlib
from datetime import datetime
from src.tools.DateTools import DateTools
import random

conf = Config()


# monitor cron
class CronMonitor(object):

    queue = multiprocessing.Queue()
    su = SqlUtil()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    def insert_monitor(self, monitor):
        if not isinstance(monitor, Monitor):
            print "Error: monitor 必须是Monitor"
        self.queue.put(monitor)

    # cron进程执行方法
    def cron_exec(self):
        while True:
            obj = self.queue.get()
            if not isinstance(obj, Monitor):
                print "Error, %s" % obj
            self.su.insert_one_sql(obj)

    # 启动进程
    @staticmethod
    def start():
        ct = CronMonitor()
        multiprocessing.Process(target=ct.cron_exec).start()


# cluster cron
class CronCluster(object):

    su = SqlUtil()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # 执行检查端口
    @staticmethod
    def exec_check_port(cluster):
        if not isinstance(cluster, Cluster):
            return
        try:
            telnetlib.Telnet(host=cluster.ip, port=cluster.port)
            cluster.status = True
        except Exception as e:
            cluster.status = False
            cluster.detail = e.message
        cluster.last_update = DateTools.date_format(datetime.now())
        su = CronCluster.su
        su.update_cluster_sql(cluster)

    # 检查端口
    @staticmethod
    def check_port():
        try:
            su = CronCluster.su
            clusters, err = su.get_cluster_all()
            if err:
                print err
                return
            for cluster in clusters:
                enable = False
                while not enable:
                    if threading.activeCount() < 20:
                        threading.Thread(target=CronCluster.exec_check_port, args=(cluster,)).start()
                        enable = True
                    else:
                        time.sleep(5)
        except Exception as e:
            print e.message

    # 执行防火墙检查端口
    @staticmethod
    def exec_check_firewalld(cluster):
        if not isinstance(cluster, Cluster):
            return
        # 如果是全开放，则退出
        if cluster.normal_ports == "ALL":
            return
        # 定义monitor类
        monitor = Monitor()
        monitor.status = True
        monitor.detail = "%s" % cluster.ip
        monitor.cluster = cluster.name
        monitor.time = DateTools.date_format(datetime.now())
        monitor.type = "firewalld"
        # 定义检查端口
        normal_ports = []
        out_ports = cluster.normal_ports.split(",")
        for port in out_ports:
            if '-' in port:
                start, end = port.split('-')
                normal_ports.append(range(int(start), int(end) + 1))
            else:
                normal_ports.append(int(port))
        ports = [22, 80, 443, 7180, 8088, 8888, 11000, 10000, 8998,
                 random.randint(15000, 65535), random.randint(15000, 65535), random.randint(15000, 65535)]
        [ports.remove(port) for port in normal_ports if port in ports]
        for port in ports:
            try:
                telnetlib.Telnet(host=cluster.ip, port=port)
                if monitor.status:
                    monitor.status = False
                    monitor.detail += u"%s 可以正常连接，与预期状态不符合" % port
            except Exception:
                pass
        monitor.detail += u"非法端口检查正常" if monitor.status else u"非法端口检查不正常"
        CronCluster.su.insert_one_sql(monitor)

    # 检查防火墙端口
    @staticmethod
    def check_firewalld():
        try:
            su = CronCluster.su
            clusters, err = su.get_cluster_all()
            if err:
                print err
                return
            for cluster in clusters:
                enable = False
                while not enable:
                    if threading.activeCount() < 20:
                        threading.Thread(target=CronCluster.exec_check_firewalld, args=(cluster,)).start()
                        enable = True
                    else:
                        time.sleep(5)
        except Exception as e:
            print e.message

    # cron进程执行方法
    @staticmethod
    def cron_exec():
        while True:
            threading.Thread(target=CronCluster.check_port).start()
            threading.Thread(target=CronCluster.check_firewalld).start()
            time.sleep(conf.monitor_frequency * 60)

    # 启动进程
    @staticmethod
    def start():
        multiprocessing.Process(target=CronCluster.cron_exec).start()


# Data delete
class CronDataExpire(object):
    su = SqlUtil()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # 执行检查端口
    @staticmethod
    def data_expire_delete():
        data_keep = conf.data_keep
        expire_time = DateTools.update_time(datetime.now(), days=data_keep, add=False)
        CronDataExpire.su.delete_expire_monitor_data(expire_time)

    # cron进程执行方法
    @staticmethod
    def cron_exec():
        while True:
            CronDataExpire.data_expire_delete()
            time.sleep(60 * 60)

    # 启动进程
    @staticmethod
    def start():
        multiprocessing.Process(target=CronDataExpire.cron_exec).start()
