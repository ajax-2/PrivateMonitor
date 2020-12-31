# coding: utf-8

from src.Implement.GetImplement import GetImplement


class GetInterface(object):

    # 获取监控频率
    @staticmethod
    def get_frequency():
        return GetImplement.get_frequency()

    # 检查状态
    @staticmethod
    def check_cluster(cluster_name):
        return GetImplement.check_cluster(cluster_name)
