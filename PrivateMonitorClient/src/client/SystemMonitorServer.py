# coding: utf-8

import commands
from src.info.LocalInfo import LocalInfo
import os
from src.tools.RequestTools import RequestTools
from datetime import datetime
import threading

li = LocalInfo()


class SystemMonitorServer(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    # ssh 日志监控
    @staticmethod
    def ssh_log_monitor():
        rt = RequestTools(li.cluster, u"child_sshd", True, u"ssh 异常登录检查:")
        _, number = commands.getstatusoutput("tail -n 500 %s |grep sshd|grep -i failed|wc -l" % li.ssh_log)
        if int(number) > 5:
            rt.r_status = False
            rt.r_detail += u"日志中存在大量异常登录，超过%s次" % number
        else:
            rt.r_detail += u"无异常登录发生"
        code, reason = rt.send_status()
        print "%s SSH LOG Info: code: %s, result: %s" % (datetime.now(), code, reason)

    # 审计服务以及日志监控
    @staticmethod
    def audit_monitor():
        rt = RequestTools(li.cluster, u"child_audit", True, u"审计状态: ")
        # 检查审计服务
        status, _ = commands.getstatusoutput("systemctl status auditd")
        if status:
            rt.r_status = False
            rt.r_detail += u"审计服务未开启,"
            code, reason = rt.send_status()
            print "%s Audit Info: code: %s, result: %s" % (datetime.now(), code, reason)
            return
        else:
            rt.r_detail += u"审计服务已开启,"
        # 检查审计目录是否正确， 查看上一个文件的最后一条和这个文件的第一条记录， 时间上是否相差过大
        if os.path.isfile(li.audit_log_dir + '/audit.log.1'):
            _, old_audit_log = commands.getstatusoutput("tac %s/audit.log.1|head -n 1 |awk '{print $2}'"
                                                        % li.audit_log_dir)
            _, new_audit_log = commands.getstatusoutput("cat %s/audit.log |head -n 1|awk '{print $2}'"
                                                        % li.audit_log_dir)
            get_data = lambda(x): int(x.split("audit")[-1].replace('(', '').split('.')[0])
            if get_data(new_audit_log) - get_data(old_audit_log) > 3600:
                rt.r_status = False
                rt.r_detail += u"日志文件超过1小时没有更新"
            else:
                rt.r_detail += u"日志文件检查正常"
            if not os.path.isfile("/run/audit.status"):
                os.system("touch /run/audit.status")
        elif os.path.isfile("/run/audit.status"):
            rt.r_status = False
            rt.r_detail += u"日志文件被删除, 请查看以前日志 /home/.audit"
        else:
            rt.r_detail += u"日志检查正常"
        code, reason = rt.send_status()
        print "%s Audit Info: code: %s, result: %s" % (datetime.now(), code, reason)

    # 监控关键服务
    @staticmethod
    def service_monitor():
        rt = RequestTools(li.cluster, u"child_private_services", True, u"关键服务: ")
        # 检查系统关键服务
        for service in li.private_service:
            status, _ = commands.getstatusoutput("systemctl status %s" % service)
            if status:
                rt.r_status = False
                rt.r_detail += u"服务: %s 状态检查失败," % service
            else:
                rt.r_detail += u"服务: %s 状态检查正常," % service
        code, reason = rt.send_status()
        print "%s Private Service Info: code: %s, result: %s" % (datetime.now(), code, reason)

    # 开启系统监控
    @staticmethod
    def start():
        sms = SystemMonitorServer()
        t1 = threading.Thread(target=sms.audit_monitor)
        t2 = threading.Thread(target=sms.ssh_log_monitor)
        t3 = threading.Thread(target=sms.service_monitor)
        t1.start(); t2.start(); t3.start()
        t1.join(); t2.join(); t3.join()

