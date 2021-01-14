# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config import Config
from SqlStrunct import Base, Monitor, Cluster


# 工具类
class SqlUtil(object):
    # 定义变量
    engine = None
    DBSession = None
    config = Config()
    connect_idle = 60 * 10

    # 单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    # 创建表
    def create_tables_all(self):
        if not self.engine:
            self.connect()
        Base.metadata.create_all(self.engine)

    # 连接
    def connect(self):
        if not self.engine:
            self.engine = create_engine("mysql+pymysql://%s:%s@%s:%d/%s?charset=utf8" %
                                        (self.config.mysql_user,
                                         self.config.mysql_password,
                                         self.config.mysql_host,
                                         self.config.mysql_port,
                                         self.config.mysql_db),
                                        echo=False,
                                        pool_size=40,
                                        pool_recycle=self.connect_idle)

    # 创建DB会话类型
    def db_session(self):
        if self.DBSession:
            return
        if not self.engine:
            self.connect()
        self.DBSession = sessionmaker(bind=self.engine)

    # 会话
    def session(self):
        if not self.DBSession:
            self.db_session()
        return self.DBSession()

    # 分页获取所有记录, 一次最大不能超过100行
    # obj, 数据表对象
    # start stop 开始 和 结束 行号
    def get(self, obj, start=0, stop=10):
        try:
            if stop - start > 100:
                raise Exception("一次性行数超过100行,当前信息， start: %s, stop: %s" % (start, stop))
            if not isinstance(obj, Base.__class__):
                raise Exception("传入的obj必须是Base类型的子类")
            session = self.session()
            return session.query(obj).slice(start, stop).all(), None
        except Exception as e:
            return None, e.message

    # 获取指定时间后的记录, 不指定time时获取所有, obj 为数据表类型
    def get_monitor_data_gt_time(self, obj, time=None):
        try:
            if not isinstance(obj, Monitor.__class__):
                raise Exception("传入的obj必须是Monitor类型")
            session = self.session()
            if time:
                return session.query(obj).filter(Monitor.time > time).all(), None
            else:
                return session.query(obj).all(), None
        except Exception as e:
            return None, e.message

    # 获取cluster
    def get_cluster(self, cluster_id=None):
        try:
            session = self.session()
            if not cluster_id:
                return session.query(Cluster).all(), None
            else:
                return session.query(Cluster).filter(Cluster.id == cluster_id).one(), None
        except Exception as e:
            return None, e.message

    # 插入单行sql
    def insert_one_sql(self, obj):
        try:
            if not isinstance(obj, Base):
                raise Exception("传入的obj必须是Base类型的子类")
            self.db_session()
            session = self.session()
            session.add(obj)
            session.commit()
            session.close()
            return "Well", None
        except Exception as e:
            return None, e.message

    # 更新单个sql
    def update_cluster_sql(self, obj):
        try:
            if not isinstance(obj, Cluster):
                raise Exception("传入的obj必须是Base类型的子类")
            self.db_session()
            session = self.session()
            session.query(Cluster).filter(Cluster.id == obj.id).update(
                {
                    "status": obj.status,
                    "name": obj.name,
                    "detail": obj.detail,
                    "alias": obj.alias,
                    "ip": obj.ip,
                    "port": obj.port,
                    "normal_ports": obj.normal_ports,
                }
            )
            session.commit()
            session.close()
            return "Well", None
        except Exception as e:
            return None, e.message

    # 删除过期数据
    def delete_expire_monitor_data(self, expire_time):
        try:
            self.db_session()
            session = self.session()
            session.query(Monitor).filter(Monitor.time < expire_time).delete()
            session.commit()
            session.close()
            return "Well", None
        except Exception as e:
            return None, e.message

    # 从私有化监控中删除一个集群
    def delete_cluster(self, cluster_id):
        try:
            self.db_session()
            session = self.session()
            session.query(Cluster).filter(Cluster.id == cluster_id).delete()
            session.commit()
            session.close()
            return "Well", None
        except Exception as e:
            return None, e.message
