# coding: utf-8

import time
from Config import Config
import threading

conf = Config()


class Auth(object):

    verify_users = {}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_init"):
            cls._init = object.__new__(cls)
        return cls._init

    def add(self, user):
        self.verify_users[user] = int(time.time())

    def delete(self, user):
        self.verify_users.pop(user)

    def get(self, user):
        return user in self.verify_users.keys()

    def expire_user(self, user):
        if int(time.time()) - self.verify_users[user] > 360:
            return True
        return False

    def update_user(self, user):
        self.verify_users[user] = int(time.time())

    def check_login(self):
        import os
        os.system("echo start >> /tmp/demo.log")
        users = self.verify_users
        os.system("echo %s >> /tmp/demo.log" % self.verify_users.keys())
        for user in users.keys():
            os.system("echo 'user: %s , value: %s, expire: %s, now: %s' >> /tmp/demo.log" % (
            user, self.verify_users[user], self.expire_user(user), int(time.time())))
            if self.expire_user(user):
                self.delete(user)

    # cron
    def cron(self):
        while True:
            self.check_login()
            time.sleep(conf.auth_timeout)

    # cron start
    def cron_start(self):
        threading.Thread(target=self.cron).start()
