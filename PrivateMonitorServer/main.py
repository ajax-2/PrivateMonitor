#!/usr/bin/python
# coding: utf-8

from Config import Config
from src.orm.SqlUtil import SqlUtil
from flask import Flask, request
from src.Handler.MetricHandler import MetricHandler
from src.Handler.MainHandler import MainHandler
from src.Handler.StatusHandler import StatusHandler
from src.Handler.GetHandler import GetHandler
import os
import sys
from src.tools.CronTools import CronCluster, CronMonitor, CronDataExpire

# 初始化参数
conf = Config()
sep = os.path.sep

# flask 初始化
app = Flask(__name__)
web_host = "0.0.0.0"
web_port = 9200
app.static_folder = conf.abs_path + sep + "src" + sep + "static"
app.template_folder = conf.abs_path + sep + "src" + sep + "static" + sep + "html"


# 主界面
@app.route('/', methods=["GET"])
def web_main():
    return MainHandler.main()


# 监控
@app.route('/metrics', methods=["GET"])
def metrics():
    return MetricHandler.metric()


# 健康检查
@app.route('/health', methods=['GET'])
def health():
    return u"Health"


# 获取其他信息
@app.route('/get/<type_id>', methods=["GET", "POST"])
def get(type_id):
    if request.method == "GET":
        return GetHandler.get(type_id)
    elif request.method == "POST":
        return GetHandler.post(type_id)
    else:
        return u'方法不允许!'


# 接收其他子监控的报告
@app.route('/status/<cluster>', methods=["POST"])
def get_status(cluster):
    try:
        data = request.get_json()
        return StatusHandler.get_status(cluster, data)
    except Exception:
        return u'参数错误'


# 程序入口
if __name__ == "__main__":
    # 加载配置
    conf.parse_from_config_ini()
    if not conf.check_config():
        print "Error: 参数配置不正确， 请查看config.ini"
        sys.exit(1)

    # 创建数据库
    su = SqlUtil()
    su.create_tables_all()

    # 启动报告cron任务
    CronMonitor.start()
    # 启动服务端cron任务
    CronCluster.start()
    # 启动数据自动清理
    CronDataExpire.start()
    # 运行web
    app.run(host=web_host, port=web_port, debug=False)
