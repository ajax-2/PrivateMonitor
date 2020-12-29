# coding: utf-8

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 数据库模型
class Monitor(Base):

    __tablename__ = "monitor"

    # 字段
    id = Column(Integer, primary_key=True, comment=u"主键id")
    time = Column(DateTime, comment=u"报告时间")
    cluster = Column(String(32), comment=u"集群名")
    type = Column(String(32), comment=u"报告类型")
    status = Column(Boolean, comment=u"状态")
    detail = Column(Text, comment=u"详情，一般承载了type的详细信息")

    def __str__(self):
        return u"id: %s" % self.id + u" status: %s" % self.status


# 私有化环境信息表
class Cluster(Base):

    __tablename__ = "cluster"

    # 字段
    id = Column(Integer, primary_key=True, autoincrement=True, comment=u"主键id")
    name = Column(String(32), comment=u"集群名")
    alias = Column(String(64), comment=u"别名")
    status = Column(Boolean, default=False, comment=u"状态")
    create_time = Column(DateTime, comment=u"创建时间")
    last_update = Column(DateTime, comment=u"最后一次更新时间")
    detail = Column(Text, comment=u"私有化集群详情")
    ip = Column(String(20), comment=u"外网ip")
    port = Column(Integer, comment=u"外网端口")
    normal_ports = Column(String(64), comment=u"外网可连接端口，采用,分割，例如22,33 或者22-33,44", default=u"ALL")

    def __str__(self):
        return u"id: %s" % self.id
