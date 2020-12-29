# coding: utf-8

from Config import Config

conf = Config()


class GetImplement(object):

    # 获取监控频率
    @staticmethod
    def get_frequency():
        return u'%s' % conf.monitor_frequency
