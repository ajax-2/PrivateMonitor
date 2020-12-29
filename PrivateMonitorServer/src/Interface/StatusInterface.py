# coding: utf-8

from src.Implement.StatusImplement import StatusImplement


class StatusInterface(object):

    @staticmethod
    def get_status(cluster, data):
        return StatusImplement.get_status(cluster, data)
