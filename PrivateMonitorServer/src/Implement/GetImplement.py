# coding: utf-8

from Config import Config
from src.orm.SqlUtil import SqlUtil
from src.orm.SqlStrunct import Cluster

conf = Config()


class GetImplement(object):

    # 获取监控频率
    @staticmethod
    def get_frequency():
        return u'%s' % conf.monitor_frequency

    # 判断集群名称
    @staticmethod
    def check_cluster(cluster_name):
        su = SqlUtil()
        clusters, _ = su.get_cluster()
        cluster_names = [cluster.name for cluster in clusters]
        if cluster_name not in cluster_names:
            raise Exception("此集群不存在， 请手动添加!")
        return u'可以使用'
