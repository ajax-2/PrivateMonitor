### 说明
    此服务是为了检验存储服务器客户端性能， 提供IP:9100/metrics 接口来获取指标，建议指标获取间隔为5分钟一次， 超时时间为1m

### 指标说明
    loss 丢包率
    max_latency 网络最大延迟,ping
    avg_latency 网络平均延迟,ping
    status 是否能正常使用， 0为正常， 1为失败
    disk_read 顺序读
    disk_write 顺序写
    
### 格式
```
storage_client{server="ServerIp",type="loss",host="client",describe="loss package!"} 0
storage_client{server="ServerIp",type="max_latency",host="client",describe="unit ms!"} 44
storage_client{server="ServerIp",type="avg_latency",host="client",describe="unit ms!"} 10
storage_client{server="ServerIp",type="status",host="client",describe="1 is fail!"} 0
storage_client{server="ServerIp",type="disk_write",host="client", describe="Seq unit Mb/s"} 1419
storage_client{server="ServerIp",type="disk_read",host="client", describe="Seq unit Mb/s"} 7246
```