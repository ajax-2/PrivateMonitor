# coding: utf-8

from flask import render_template, abort, redirect, url_for
from src.Interface.MainInterface import MainInterface
from src.auth.Auth import Auth

auth = Auth()


class MainHandler(object):

    # 主页面
    @staticmethod
    def main():
        clusters, error = MainInterface.main()
        return render_template("index.html", clusters=clusters, error=error)

    # 登录
    @staticmethod
    def login(url):
        return render_template("login.html", url=url)

    # 验证
    @staticmethod
    def login_verify(data, ip):
        try:
            if not data['username'] or not data['password']:
                raise Exception(u"用户名密码不能为空!")
            verify = MainInterface.login_verify(data)
            url = data['url']
            if not verify:
                return redirect('/login?url=%s' % url)
            auth.add(ip)
            return redirect(url)
        except Exception as e:
            abort(500, e.message)

    # 返回添加页面
    @staticmethod
    def return_add_html(ip):
        if not auth.get(ip):
            return redirect("/login?url=add")
        auth.update_user(ip)
        return render_template("add_cluster.html")

    # 添加集群到私有化监控平台
    @staticmethod
    def add_cluster(data, ip):
        if not auth.get(ip):
            return redirect("/login/add")
        auth.update_user(ip)
        try:
            if not data:
                raise Exception(u"请传入form data格式的参数")
            for key in data.keys():
                if not data[key]:
                    raise Exception(u"%s 参数不能为空" % key)
            data['port'] = int(data['port'])
            status, err = MainInterface.add_cluster(data)
            if err:
                raise Exception(err)
            return redirect("/")
        except Exception as e:
            abort(500, u"Error: 访问出错: %s" % e.message)

    # 从私有化监控中删除集群
    @staticmethod
    def delete_cluster(cluster_id, ip):
        if not auth.get(ip):
            return u"noAuth"
        auth.update_user(ip)
        try:
            if not cluster_id:
                raise Exception(u"需要提供cluster id")
            cluster_id = int(cluster_id)
            status, err = MainInterface.delete_cluster(cluster_id)
            if err:
                raise Exception(err)
            return "Success"
        except Exception as e:
            abort(500, u"Error: 访问出错: %s" % e.message)

    # 从私有化监控中更新集群
    @staticmethod
    def get_update_cluster(cluster_id, ip):
        if not auth.get(ip):
            return redirect("/login?url=/update/" + cluster_id)
        auth.update_user(ip)
        try:
            if not cluster_id:
                raise Exception(u"需要提供cluster id")
            cluster_id = int(cluster_id)
            data, err = MainInterface.get_update_cluster(cluster_id)
            return render_template("update_cluster.html", data=data, error=err, cluster_id=cluster_id)
        except Exception as e:
            abort(500, u"Error: 访问出错: %s" % e.message)

    # 从私有化监控中更新集群
    @staticmethod
    def update_cluster(cluster_id, data, ip):
        if not auth.get(ip):
            return redirect("/login?url=/update" + cluster_id)
        auth.update_user(ip)
        try:
            if not cluster_id:
                raise Exception(u"需要提供cluster id")
            cluster_id = int(cluster_id)
            for key in data.keys():
                if not data[key]:
                    raise Exception(u"%s 参数不能为空" % key)
            data['port'] = int(data['port'])
            status, err = MainInterface.update_cluster(cluster_id, data)
            if err:
                raise Exception(err)
            return redirect("/")

        except Exception as e:
            abort(500, u"Error: 访问出错: %s" % e.message)


