# coding: utf-8

from src.Implement.MainImplement import MainImplement


class MainInterface(object):

    # 主页面
    @staticmethod
    def main():
        return MainImplement.main()

    # 登录验证
    @staticmethod
    def login_verify(data):
        return MainImplement.login_verify(data)

    # 添加一个集群到私有化监控平台
    @staticmethod
    def add_cluster(data):
        return MainImplement.add_cluster(data)

    # 从私有化监控中删除一个集群
    @staticmethod
    def delete_cluster(cluster_id):
        return MainImplement.delete_cluster(cluster_id)

    # 从私有化监控中更新一个集群
    @staticmethod
    def get_update_cluster(cluster_id):
        return MainImplement.get_update_cluster(cluster_id)

    # 从私有化监控中更新一个集群
    @staticmethod
    def update_cluster(cluster_id, data):
        return MainImplement.update_cluster(cluster_id, data)
