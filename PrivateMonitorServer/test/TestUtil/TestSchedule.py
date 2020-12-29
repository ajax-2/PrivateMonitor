# coding: utf-8

from src.tools.CronTools import CronMonitor, CronCluster
from Config import Config


def test_monitor():
    CronMonitor.start()


def test_cluster():
    CronCluster.check_port()


if __name__ == "__main__":
    Config().parse_from_config_ini()
    test_cluster()
