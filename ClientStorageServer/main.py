#!/usr/bin/python
# coding=utf-8

import flask
import sys
import os
import commands
import ping
import time

app = flask.Flask(__name__)
ip = ""
path = ""
host = ""


# get env
def get_env():
    t_ip = os.getenv("Server")
    if not t_ip:
        print "必须提供有效的存储服务器ip，例如Server=192.168.0.11"
        sys.exit(1)
    result, _, _ = ping.quiet_ping(t_ip, timeout=2, count=1, psize=32)
    if result == 100 or t_ip == "localhost" or t_ip == "127.0.0.1":
        print "必须提供有效的存储服务器ip，例如Server=192.168.0.11"
        sys.exit(1)
    t_path = os.getenv("Path")
    if not t_path or not os.path.isdir(t_path):
        print "必须提供存储介质有效的挂载路径，例如Path=/data"
        sys.exit(1)

    t_host = os.getenv("host")
    if not t_host:
        print "必须提供有效的物理机标识，以便追踪，例如host=client1"
        sys.exit(1)
    return t_ip, t_path, t_host


# latency
def latency_server(result):
    if not isinstance(result, list):
        return False
    package_loss, max_latency, avg_latency = ping.quiet_ping(ip, timeout=2, count=10, psize=64)
    result.append('storage_client{server="%s",type="loss",host="%s",describe="loss package!"} %d\n' % (ip, host, package_loss))
    result.append('storage_client{server="%s",type="max_latency",host="%s",describe="unit ms!"} %d\n' % (ip, host, max_latency))
    result.append('storage_client{server="%s",type="avg_latency",host="%s",describe="unit ms!"} %d\n' % (ip, host, avg_latency))
    if package_loss > 50:
        return False
    return True


# test_read
def test_read(result):
    if not isinstance(result, list):
        return False
    file_name = "%s/%s" % (path, str(time.time()))
    status, _ = commands.getstatusoutput("touch %s" % file_name)
    if status:
        result.append('storage_client{server="%s",type="status",host="%s",describe="1 is fail!"} 1\n' % (ip, host))
        return False
    else:
        result.append('storage_client{server="%s",type="status",host="%s",describe="1 is fail!"} 0\n' % (ip, host))
        os.remove(file_name)
    return True


# disk io
def test_disk_io(result):
    if not isinstance(result, list):
        return False
    file_name = "%s/%s" % (path, str(time.time()))
    try:
        start = time.time()
        os.system("dd if=/dev/zero of=%s bs=512k count=200" % file_name)
        end = time.time()
        speed = 100 / (end - start)
        result.append('storage_client{server="%s",type="disk_write",host="%s", describe="Seq unit Mb/s"} %d\n' % (ip, host, speed))

        start = time.time()
        os.system("dd if=%s of=/dev/null bs=512k" % file_name)
        end = time.time()
        speed = 100 / (end - start)
        result.append('storage_client{server="%s",type="disk_read",host="%s", describe="Seq unit Mb/s"} %d\n' % (ip, host, speed))

    finally:
        os.remove(file_name)


# route
# main
@app.route("/")
def index():
    return u"欢迎!"


# metrics
@app.route("/metrics", methods=["GET"])
def metrics():
    result = []
    if latency_server(result) and test_read(result):
        test_disk_io(result)
    return ''.join(result)


if __name__ == '__main__':
    ip, path, host = get_env()
    app.run("0.0.0.0", 9100)
