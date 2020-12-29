# coding: utf-8

from src.Implement.MeticImplement import MetricImplement


class MetricInterface(object):

    @staticmethod
    def metrics():
        return MetricImplement.metric()
