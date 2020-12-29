# coding: utf-8

from src.orm.SqlStrunct import Cluster
from src.orm.SqlUtil import SqlUtil


class MainImplement(object):

    # 主页面
    @staticmethod
    def main():
        return SqlUtil().get(Cluster, 0, 20)
