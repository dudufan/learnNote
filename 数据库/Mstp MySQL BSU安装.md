[TOC]


#mysql BSU安装配置
##安装
     1. 解压并执行安装脚本
    2. 过程中指定server-id，双主下两台机器不同

    3. 数据库初始化 执行脚本init_mysql.sh

    4. 启动停止操作

##配置主主复制
###配置


配置Master A



    1. 执行配置脚本，需要登录密码

    2. 输入A的IP

    3. 输入B登录密码

    4. 输入B的IP
MasterB配置类似
测试Mysql主主
执行脚本安装keepalived
配置A的keepalived


    1. 启动配置脚本

    2. 输入A的网卡名如eth1，虚拟IP

    3. 输入A的IP

    4. 设置virtual_router_id（A和B相同）
    5.  设置优先级（A和B不同）：A为80

配置B的keepalived，虚拟IP同A，IP、网卡名、优先级不同

初始化mysql数据库表


#cache安装配置
##安装
     1. 解压并执行安装脚本


##配置
主服务器：


     1. 执行配置脚本

     2. 输入本地IP
     3. 主或从？yes
从服务器：


     1. 执行配置脚本

     2. 输入本地IP
     3. 主或从？no
    4. 输入服务器优先级（一般小于100）：90



##启动和测试
    1.  修改防火墙开启6379端口
    2. 启动主从的redis:      redis-server redis.conf
    3. 检查redis的角色：redis-cli登录并输入role

    4. 连接到GeneralDB的每个Sentinel，输入命令配置



#GridFS集群
##安装：
    1. 解压二进制包，拷贝bin文件到/usr/local/SINO/mongodb/bin
    2. 修改iptables规则，允许10000 20000 27017等端口，service iptables save

    3. 在7台服务器上搭建集群
