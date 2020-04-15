# 概述

目的是解决不同服务之间的调用问题, 一般包含传输协议和序列化协议 

# 原理

1. 服务消费方（client）调用以本地调用方式调用服务；
2. client stub接收到调用后负责将方法、参数等组装成能够进行网络传输的消息体；
3. client stub找到服务地址，并将消息发送到服务端；
4. server stub收到消息后进行解码；
5. server stub根据解码结果调用本地的服务；
6. 本地服务执行并将结果返回给server stub；
7. server stub将返回结果打包成消息并发送至消费方；
8. client stub接收到消息，并进行解码；
9. 服务消费方得到最终结果。

# Dubbo

## 架构

- Provider     暴露服务的服务提供方
- Consumer     调用远程服务的服务消费方
- Registry     服务注册与发现的注册中心
- Monitor     统计服务的调用次数和调用时间的监控中心
- Container     服务运行容器