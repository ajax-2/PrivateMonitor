# coding: utf-8

from requests import request
from src.info.ServerInfo import ServerInfo

si = ServerInfo()


# 请求体内容
class RequestTools(object):

    r_cluster = ""
    r_type = ""
    r_status = ""
    r_detail = ""

    content = "application/json"

    # 构造函数
    def __init__(self, r_cluster, r_type, r_status, r_detail):
        self.r_cluster = r_cluster
        self.r_type = r_type
        self.r_status = r_status
        self.r_detail = r_detail

    # 返回请求头
    def get_header(self):
        headers = {
            "Content-Type": self.content,
        }
        return headers

    def get_data(self):
        data = {
            "cluster": self.r_cluster,
            "type": self.r_type,
            "status": u"success" if self.r_status else u"fail",
            "detail": self.r_detail,
        }
        return data

    def send_status(self):
        resp = request("POST", si.server_url + si.server_status_path, json=self.get_data(), headers=self.get_header())
        return resp.status_code, resp.text
