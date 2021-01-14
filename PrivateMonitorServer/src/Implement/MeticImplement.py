# coding: utf-8

from src.orm.SqlUtil import SqlUtil
from src.orm.SqlStrunct import Monitor
from datetime import datetime
from Config import Config
from src.tools.DateTools import DateTools

conf = Config()


class MetricImplement(object):

    @staticmethod
    def metric():
        metrics = []
        su = SqlUtil()
        # 获取监控表
        dt_now = datetime.now()
        dt = DateTools.update_time(dt_now, minutes=conf.monitor_frequency, add=False)
        monitors, err = su.get_monitor_data_gt_time(Monitor, time=dt)
        if err:
            print "%s Error: %s" % (DateTools.date_format(dt), err)
        else:
            for monitor in monitors:
                metrics.append('private_monitor_env{cluster="%s",type="%s", time="%s", detail="%s"} %d' % (
                    monitor.cluster, monitor.type, monitor.time, monitor.detail, monitor.status
                ))

        # 获取服务主动监控表
        clusters, err = su.get_cluster()
        if err:
            print "%s Error: %s" % (DateTools.date_format(dt), err)
        else:
            for cluster in clusters:
                metrics.append('private_monitor_env{cluster="%s",type="connect", time="%s", detail="%s"} %d' % (
                    cluster.name, cluster.last_update, cluster.detail, cluster.status
                ))
        return metrics
