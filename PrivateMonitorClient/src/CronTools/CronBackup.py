# coding: utf-8

import multiprocessing
import time
import os
from src.info.LocalInfo import LocalInfo
import threading

li = LocalInfo()


# 备份数据
class CronBackup(object):

    # 审计备份
    @staticmethod
    def audit_backup():
        if not os.path.isdir("/home/.audit"):
            os.mkdir("/home/.audit")
        for num in range(10, 0, -1):
            if os.path.isfile("/home/.audit/audit.%s" % (num - 1)):
                os.system("mv -f /home/.audit/audit.%s /home/.audit/audit.%s" % (num - 1, num))
        os.system("tar -zcf /home/.audit/audit.0 %s" % li.audit_log_dir)

    # 开始备份
    @staticmethod
    def exec_backup():
        while True:
            t1 = threading.Thread(target=CronBackup.audit_backup)
            t1.start()
            t1.join()
            time.sleep(li.backup_time)

    # 入口
    @staticmethod
    def start():
        multiprocessing.Process(target=CronBackup.exec_backup).start()
