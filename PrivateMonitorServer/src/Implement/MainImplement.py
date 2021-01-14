# coding: utf-8

from src.orm.SqlStrunct import Cluster
from src.orm.SqlUtil import SqlUtil
from src.tools.DateTools import DateTools
from datetime import datetime
from Config import Config

config = Config()

sql = SqlUtil()


class MainImplement(object):

    # 主页面
    @staticmethod
    def main():
        return SqlUtil().get(Cluster, 0, 20)

    # 登录验证
    @staticmethod
    def login_verify(data):
        if data['username'] == config.username and data['password'] == config.password:
            return True
        return False

    # 添加一个集群到私有化监控中
    @staticmethod
    def add_cluster(data):
        cluster = Cluster()
        cluster.name = data['name']
        cluster.detail = data['detail']
        cluster.alias = data['alias']
        cluster.ip = data['ip']
        cluster.port = data['port']
        cluster.normal_ports = data['normal_ports']
        cluster.create_time = DateTools.date_format(datetime.now())
        cluster.last_update = DateTools.date_format(datetime.now())
        return sql.insert_one_sql(cluster)

    # 从私有化监控中删除一个集群
    @staticmethod
    def delete_cluster(cluster_id):
        return sql.delete_cluster(cluster_id)

    # 获取集群信息
    @staticmethod
    def get_update_cluster(cluster_id):
        return sql.get_cluster(cluster_id)

    # 从私有化监控中更新一个集群
    @staticmethod
    def update_cluster(cluster_id, data):
        cluster = Cluster()
        cluster.id = cluster_id
        cluster.name = data['name']
        cluster.detail = data['detail'] + "update Time: " + DateTools.date_format(datetime.now())
        cluster.alias = data['alias']
        cluster.ip = data['ip']
        cluster.port = data['port']
        cluster.normal_ports = data['normal_ports']
        return sql.update_cluster_sql(cluster)
