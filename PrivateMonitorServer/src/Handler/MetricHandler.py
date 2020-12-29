# coding: utf-8

from src.Interface.MeticInterface import MetricInterface
from flask import abort


class MetricHandler(object):

    @staticmethod
    def metric():
        metrics = MetricInterface.metrics()
        if not metrics:
            return ''
        return '\n'.join(metrics)
