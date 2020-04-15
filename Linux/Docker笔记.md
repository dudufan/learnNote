# 安装

centos7 内核版本，必须是3.10及以上 

```shell
uname -r
yum install docker
systemctl start docker
docker -v
# 开机启动docker
[root@localhost ~]# systemctl enable docker 
# 停止docker 
[root@localhost ~]# systemctl stop docker

```

# 常用操作

```shell
# 下载镜像
docker pull registry.docker-cn.com/library/redis
# 查看镜像
docker images 
# 启动redis。也可以同时设置挂载目录，指定启动命令
docker run -d -p 6379:6379 --name myredis registry.docker-cn.com/library/redis

# 查看终止的容器
docker ps -a
docker ps | grep bankinfo
docker cp xxxx:/usr/local/SINO/yqt/log /tmp/bankinfo_log

# 启动容器
docker start <container_id>
# 在容器中执行命令
docker exec -it 43f7a65ec7f8 redis-cli
```



## docker run

``` docker run [OPTIONS] IMAGE [COMMAND] [ARG...]```

- **-t:**在新容器内指定一个伪终端或终端。
- **-i:**允许你对容器内的标准输入 (STDIN) 进行交互。

```shell
docker run -i -t ubuntu:15.10 /bin/bash
```

## docker port

 查看端口

启动container时必须通过 -p 宿主机端口：容器内部端口，或 -P（暴露所有内部端口到宿主机的随机端口上）。
这样才能在docker port看到暴露的端口

## 挂载目录

### Docker挂载主机目录Docker访问出现Permission denied的解决办法

Docker挂载主机目录，访问相应的文件出现Premission denied的权限访问问题，
   原因是CentOS7中的安全模块selinux把权限禁掉了，至少有以下三种方式解决挂载的目录没有权限的问题：
   1.在运行容器的时候，给容器加特权，及加上 --privileged=true 参数：
   docker run -i -t -v /soft:/soft --privileged=true 686672a1d0cc /bin/bash
   2.临时关闭selinux：
   setenforce 0
   3.添加selinux规则，改变要挂载的目录的安全性文本

# Docker安装Redis

配置持久化方式启动

```shell
docker run --name some-redis -d redis redis-server --appendonly yes
```



使用redis本地配置文件启动，立刻就退出容器

解决办法：为了保持docker活跃状态，redis必须保持前台运行

# 容器连接



## 问题与实践








## docker Data Volume
docker可以挂载主机目录

`docker 
run
 -d -P --name web -v /src/webapp:/webapp training/webapp python app.py`
也可以挂载一个容器中的卷dbstore, 让db1，db2共享
1. 创建数据卷

`docker 
create
 -v /dbdata 
--name dbstore training/postgres /bin/true`
2. 其他容器可以挂载这个卷，分享数据
    `docker 
    run
   -d --volumes-
    from
   dbstore --name db1 training/postgres`
3. 把共享卷
    dbstore 
    备份到主机目录中
    备份：`docker run --rm --volumes-from dbstore -v $(pwd):/backup --privileged=true ubuntu tar cvf /backup/backup.tar /dbdata`

还原：`docker run --rm --volumes-from db1 --privileged=true -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"`

删除容器卷：


[root@docker ~]# docker rm -v dbstore 


删除最后一个的时候 加上-v参数就行了