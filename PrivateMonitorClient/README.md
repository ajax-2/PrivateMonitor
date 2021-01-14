### 监控系统之子系统
    向服务端上传本地的集群状态

### 上传请求内容(json内容) 
```
POST /status/CLUSTER
{
    "cluster": CLUSTER,
    "type": Type,
    "detail": Text,
    "status": "success"|"fail"
}
```

### 定时任务
    定期备份审计日志到/home/.audit, 时间在环境变量BACKUP_TIME中设置， 单位小时， 默认为24小时

### 已有监控
    子监控系统监控： grafana prometheus 正常服务
    sshd 异常登录监控， 1000行日志出现超过5次的登录失败，则判定有异常登录
    audit 审计监控， 服务正常运行， 日志没有被删除
    关键服务监控，通过环境变量PRIMARY_SERVICE来进行设置，用英文,隔开，默认为 
        sshd, rsyslog, systemd-journald, cron(centos为crond)

### 使用详解
    将bin目录嵌入到linux机器上, 根据提示设置config.ini， 启动程序即可

### bin/* （调试程序不会用到）
    bin 目录下存放了在linux上执行的可执行文件
    bin/main/main 程序执行文件
    bin/config.conf 配置文件
    bin/run.py 执行文件入口, 会初始化系统环境和更新系统环境变量

### TODO
    定时检查关键服务，并启动
    添加容器和机器模式
    ssh log 设置查看