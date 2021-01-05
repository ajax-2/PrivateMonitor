#!/usr/bin/python
# coding: utf-8

from Config import Config
from src.orm.SqlUtil import SqlUtil
from src.orm.SqlStrunct import Monitor, Cluster
from datetime import datetime
from src.tools.DateTools import DateTools

# 测试


def test_connect():
    sql = SqlUtil()
    conn = sql.connect()
    assert conn
    print conn


def test_session():
    sql = SqlUtil()
    sql.db_session()
    session, reason = sql.session()
    print session, reason
    assert session


def test_get():
    obj = Cluster
    sql = SqlUtil()
    sql.db_session()
    result, reason = sql.get(obj, 0, 1)
    print result, reason
    assert result
    for obj1 in result:
        print str(obj1)


def test_insert_monitor():
    sql = SqlUtil()
    monitor = Monitor()
    monitor.time = DateTools.date_format(datetime.now())
    monitor.cluster = "test"
    monitor.type = "port"
    monitor.status = True
    monitor.detail = "测试"
    print sql.insert_one_sql(monitor)


def test_insert_cluster():
    sql = SqlUtil()
    cluster = Cluster()
    cluster.name = "HuaweiK8s"
    cluster.detail = "华为数融应用集群"
    cluster.alias = "华为数融应用集群"
    cluster.ip = "116.63.253.139"
    cluster.port = "5443"
    cluster.normal_ports = "ALL"
    cluster.create_time = DateTools.date_format(datetime.now())
    cluster.last_update = DateTools.date_format(datetime.now())
    print sql.insert_one_sql(cluster)


def test_create():
    # 创建数据库
    su = SqlUtil()
    su.create_tables_all()


def test_get_gt_date():
    dt = datetime.now()
    dt1 = DateTools.update_time(dt, days=2, add=False)
    su = SqlUtil()
    r1, _ = su.get_monitor_data_gt_time(Monitor, time=dt)
    r2, _ = su.get_monitor_data_gt_time(Monitor, time=dt1)
    assert not r1
    assert r2
    print r2


def test_update():
    su = SqlUtil()
    objs, _ = su.get_cluster_all()
    obj = objs[-1]
    print obj
    obj.status = False
    obj.last_update = DateTools.date_format(datetime.now())
    su.update_cluster_sql(obj)


def test_delete_monitor_data():
    su = SqlUtil()
    ex_time = datetime.now()
    ex_time_s = DateTools.update_time(ex_time, minutes=1, add=False)
    res, err = su.delete_expire_monitor_data(ex_time_s)
    if err:
        print err
    print res


if __name__ == "__main__":
    conf = Config()
    conf.parse_from_config_ini()
    conf.mysql_host = "192.168.0.201"
    conf.mysql_port = 3307
    # test_connect()
    # test_session()
    # test_get()
    # test_create()
    # test_insert_monitor()
    test_insert_cluster()
    # test_get_gt_date()
    # test_update()
    # test_delete_monitor_data()
