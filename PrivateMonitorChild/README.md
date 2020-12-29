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