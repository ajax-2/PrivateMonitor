# coding: utf-8

from requests import request


class ServerInfo(object):

    server_url = ""
    server_frequency_path = "/get/frequency"
    server_frequency = 60
    server_status_path = ""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # 健康检查
    def check_health(self):
        resp = request("GET", self.server_url + "/health")
        return resp.status_code == 200

    # 获取服务
    def get_monitor_frequency(self):
        if not self.server_frequency and not self.init():
            return 5 * 60
        return self.server_frequency

    # 设置参数
    def set_server_info(self, server_url, cluster):
        try:
            self.server_url = server_url
            self.server_status_path = "/status/" + cluster
            if not self.check_health():
                raise Exception("获取服务错误， 请查看, url 为 %s" % self.server_url + '/health')
            return True
        except Exception as e:
            print e
            return False

    # 初始化
    def init(self):
        try:
            resp = request("GET", self.server_url + self.server_frequency_path)
            self.server_frequency = int(resp.text) * 60
            return True
        except Exception as e:
            print e.message
            return False
