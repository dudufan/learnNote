优点： 
1）社区活跃，用户较多，应用广泛。 
2）MongoDB在内存充足的情况下数据都放入内存且有完整的索引支持，查询效率较高。 
3）MongoDB的分片机制，支持海量数据的存储和扩展。 
缺点： 
1）不支持事务 
2）不支持join、复杂查询 
mongodb 不指定id插入：10000多条/s

﻿##Mongo注意问题





####副本集刚建立时需要几秒来选举primary节点，同步

执行rs.status()（通过pymongo)



    client = pymongo.MongoClient("10.1.1.66", port=27017)
    
    result = client.admin.command("replSetGetStatus")
    
    print result

{u'date': datetime.datetime(2016, 8, 31, 3, 36, 31, 74000), u'myState': 3, u'set': u'shard1', u'ok': 1.0, u'members': [{u'uptime': 5, u'configVersion': 1, u'optime': Timestamp(1472614591, 1), u'name': u'10.1.1.66:27017', u'self': True, u'optimeDate': datetime.datetime(2016, 8, 31, 3, 36, 31), u'state': 3, u'health': 1.0, u'stateStr': u'RECOVERING', u'_id': 0}, {u'uptime': 0, u'configVersion': -2, u'optime': Timestamp(0, 0), u'name': u'10.1.1.66:27018', u'pingMs': 0, u'optimeDate': datetime.datetime(1970, 1, 1, 0, 0), u'state': 0, u'health': 1.0, u'stateStr': u'STARTUP', u'lastHeartbeatRecv': datetime.datetime(1970, 1, 1, 0, 0), u'_id': 1, u'lastHeartbeat': datetime.datetime(2016, 8, 31, 3, 36, 31, 34000)}, {u'uptime': 0, u'configVersion': -2, u'name': u'10.1.1.66:27019', u'pingMs': 0, u'state': 0, u'health': 1.0, u'stateStr': u'STARTUP', u'lastHeartbeatRecv': datetime.datetime(1970, 1, 1, 0, 0), u'_id': 2, u'lastHeartbeat': datetime.datetime(2016, 8, 31, 3, 36, 31, 34000)}]}  

 



####集群备份必须关掉平衡器，fsync并锁住所有从机





####更改块大小

db.setting.save





####mongos处理两个aapserver的插入请求，无法保证唯一索引（即使扫描了所有分片）

解决办法：唯一索引以片键开头





#### mongo couldn't connect to new shard socket

linux防火墙规则没有设





####单机服务器分片修改为单机副本集分片

必须停机操作，见MongoDB权威指南

两种方式：

1. 修改为副本集分片（需要重启），修改所有配置服务器分片信息，重启所有mongos，重启所有分片的主节点

2. 添加新的空副本集 分片 ，移除旧的单机分片。这个过程需要手动迁移数据，也可以先移除，这样mongo自动迁移被分片的数据。





修改配置服务器有风险，应备份。





####mongod的pidfile

     可以复用，并且mongod正常关闭后pidfile仍然存在
    
     而redis的pidfile是临时的，关闭后redis自身将pidfile删除





####虚拟机上启动mongod显示成功，但ps -ef|grep mongo没有

     原因：bind_ip是旧的IP地址，但虚拟机ip已经被主人修改了





####bind_ip绑定到多个ip？





####针对同一字段的查询条件，应该append到同一个document 中

```

{age:{"$gte":18,"$lte":30}}

```

e.g.

```

        FindIterable<Document> iterable = db.getCollection("restaurants").find(

                new Document("grades.score", new Document("$gt",60).append("$lt", 63))

                .append("cuisine", "Italian")

                );

```

####虚拟机的防火墙，使虚拟机内的端口不能被访问？





解决办法：

```

查看Linux防火墙设置

service iptables status



会得到一系列信息，说明防火墙开着。

/etc/init.d/iptables stop

或

service iptables stop

iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 端口号 -j ACCEPT

```

永久关闭:

```

chkconfig --level 35 iptables off

```

####如何使用配置启动？

mongod -f xxx.conf

####如何在副本集secondary节点上读？

secondary上执行命令  rs.setSlaveOk()

####副本集节点阻塞在STARTUP2状态？

解决办法：

1. 关闭防火墙

2. 把副本集各个节点时间修改到大致相同（导致secondary无法同步，阻塞在STARTUP2状态）



##备份

###文件系统快照

linux系统可使用LVM manager创建

如果存储系统不支持快照，则使用cp，rsync。拷贝前停止对mongod写操作（比如在mongo shell中使用 fsynclock()

Linux  mksnap_ffs生成 文件系统快照：

mksnap_ffs /home /home/snapshot20050730

注： 对某一个文件系统进行快照的结果只能放在该文件系统中







LVM快照



   LVM 快照利用一种称为“写时复制（COW - Copy-On-Write）”的技术来跟踪和维持其数据的一致性。它的原理比较简单，就是跟踪原始卷上块的改变， 在这些数据被改变之前将其复制到快照自己的预留空间里（顾名思义称为写时复制）。 当对快照进行读取的时候，被修改的数据从快照的预留空间中读取，未修改的数据则重定向到原始卷上去读取，因此在快照的文件系统与设备之间多了一层COW设备。

     利用快照您可以冻结一个正在使用中的逻辑卷，然后制作一份冻结时刻的备份，由于这个备份是具有一致性的，因此非常的适合于用来备份实时系统。例如，您的运行中的数据库可能即使在备份时刻也是不允许暂停服务的，那么就可以考虑使用LVM的快照模式，然后再针对此快照来进行文件系统级别或者块设备级别的数据备份

。

备份时使

- 不同的mongod进程，它们配置中的dbpath，logpath, pidfilepath一定要单独区别

- mongo连接时，使用 mongo bind_ip:port 格式进行连接，而不使用127.0.0.1：port

- 分片过程中数据需要balancer启动：sh.getBalancerState(), sh.setBalancerState(true)

分片的作用

RAM， 磁盘空间， 负载， 吞吐量 对于分片集群

1. 先disable the balancer

1. 配置服务器以及每个分片在同一时间保存快照



#### mongodump

特点：

排除local数据库

不包括索引，只包含文档

mongorestore恢复数据后必须重建索引

技巧：

可以在备份节点上mongodump





###mongo集群备份工具

MongoDB Cloud Manager Backup

Ops Manager Backup Software





###恢复副本集

不能恢复到三个实例后再创建副本集！





正确流程

方法一：

####恢复单节点副本集

1. mongod --dbpath /data/backdb --replSet <replName>

1. mongo

1. rs. initiate()





###添加副本集成员

1. 关闭已恢复数据的主节点

2. 复制db目录到其他节点

3. 启动主节点，添加其他节点到副本集





方法二：

1. 恢复副本集主节点的数据

2. 添加空节点到副本集

##集群

集群conf配置

logpath=/var/log/mongodb/shard1.log

logappend=true

fork=true

port=27017

storageEngine=wiredTiger

dbpath=/var/data/shard1

pidfilepath=/var/run/mongodb/mongod.pid

bind_ip=10.1.2.69

journal=true





备注：

配置服务器：

configsrv=true

分片：

shardsrv=true

mongos：

configdb = 10.8.0.12:27001



安全认证选项



auth = true







####实际配置虚拟机配置集群方法

1. 配置服务器 10.1.1.85:10000

2. 路由服务器1 10.1.1.93:20000

3. 路由服务器2 10.1.1.81:20000

mongos --port 20000 --configdb 10.1.1.85:10000 --logpath /var/log/mongodb/mongos.log --fork



4.配置分片复制集

93 ==> 81 ==> 88 ==> 84

17 ==> 18 ==> 19

分片复制集1

主节点 10.1.1.93:27017

mongod -f /etc/mongodb/mongod.conf

从节点 10.1.1.81:27018

mongod -f /etc/mongodb/mongodb-shard1-27018.conf

仲裁节点 10.1.1.88:27019

mongod -f /etc/mongodb/mongodb-shard1-27019.conf

分片复制集2

主节点 10.1.1.81:27017

mongod -f /etc/mongodb/mongod.conf

从节点 10.1.1.93:27018

mongod -f /etc/mongodb/mongod-shard2-27018.conf

仲裁节点 10.1.1.84:27019

mongod -f /etc/mongodb/mongod-shard2-27019.conf

分片复制集3

主节点 10.1.1.88:27017

mongod -f /etc/mongodb/mongod.conf

从节点 10.1.1.84:27018

mongod -f /etc/mongodb/mongod-shard3-27018.conf

仲裁节点 10.1.1.93:27019

mongod -f /etc/mongodb/mongod-shard3-27019.conf

分片复制集4

主节点 10.1.1.84:27017

mongod -f /etc/mongodb/mongod.conf

从节点 10.1.1.88:27018

mongod -f /etc/mongodb/mongod-shard4-27018.conf

仲裁节点 10.1.1.81:27019

mongod -f /etc/mongodb/mongod-shard4-27019.conf

设置复制集

config=

{      _id:"shard2",

     members:[
    
     {_id:0,host:'10.1.1.84:27017',priority:10},
    
     {_id:1,host:' 10.1.1.84 :27018',priority:1},
    
     {_id:2,host:' 10.1.1.84 :27019',arbiterOnly:true}
    
                 ]

}

rs.initiate(config)

rs.status()

添加分片

use admin

db.runCommand({"addShard":"shard1/server1,server2,server3"})

备注：

sh.addShard( "mongodb0.example.net:27017" )用来添加独立主机





删除分片：

​    



    use admin



    db.runCommand({removeShard:"Shard1/10.1.5.92:27017"})



修改分片配置，可以在config数据库中修改

 修改maxsize:



    use config
    
    db.shards.update({_id:"s1"},{$set:{maxSize:2000000}})



    注：maxSize设的大小是虚拟机实际可使用容量90%，df -h看到的不准







集群对数据库（集合）未分片时，插入的数据随机放到一个分片副本集上

如果片键只有4个可能的值，那么最多只能有4个分片，再不能进一步分割块了

如果小基数片键要进行大量查询，可以使用组合片键，并且第二个字段有很多不同的值

策略：

1.准升序键+搜索键 控制数据局部化，使磁盘和内存的IO不那么频繁

对数据库分片流程

1. sh.enableSharding("gridfs")

2. db.fs.chunks.ensureIndex({"files_id":"hashed"})

或db.runCommand({"enablesharding":"foo"})

3. sh.shardCollection("gridfs.fs.chunks", {" files_id ":"hashed"})

或db.runCommand({"shardCollection":"foo.bar","key":{" files_id ": "hashed" }})

##Mongodb命令

###插入更新

db.blog.insert(post)

db.blog.find().pretty()

根据查询条件全部替换

db.blog.update({title:"My Blog Post"}, post)

根据id更新

db.blog.save({"_id":"333333333333", ...})

只修改field:key

```

db.blog.update({title:"My Blog Post"}, {$set:{comments:[ 'haha', 'good'] }})

db.blog.update({title:"My Blog Post"}, {$set:{comments:[ 'haha', 'good'] }}, ..., {multi:true})

```

###查询

查询条件用db.blog.find( {全部条件} )

条件AND     { {条件1}，{条件2} }

条件OR      {$or：[ {条件1} ，{条件2}]}

大于 

```

{ score：{$gt : 60} }

```

gt lt gte lte

范围 

```

{ score：{$gt : 60，$lt : 80} }

```

类型 

```

{"title" : {$type : 2}}

```

聚合

```













####注意--host 只输入主机IP，不带有端口号





####启动报错 error 14

可以telnet ip port，发现连接不上。

原因是虚拟机ip改变了，而conf文件bind_ip是旧值





  





###mongodb 副本集

####配置部署

最简单集群：

启动三个进程 port、dbpath、log都必须不同

副本集rs0中2个节点，1个ARBITER节点（仲裁节点）

在primary中

rs.initiate()来启动一个新的副本集

rs.conf()  查看副本集配置

rs.staus()查看副本集状态

rs.add( "host:port" )加入数据节点

rs.addArb("host:port")加入仲裁节点































修改chunkSize大小：

1.    mongos> use config

2.    mongos> db.settings.save( { _id:"chunksize", value: 1 } )

 





db.mycol.aggregate([{$group : {_id : "$user", num_tutorial : {$sum : 1}}}])

{

   "result" : [

      {

         "_id" : "w3cschool.cc",

         "num_tutorial" : 2

      },

      {

         "_id" : "Neo4j",

         "num_tutorial" : 1

      }

   ],

   "ok" : 1

}

```

java客户端代码

```

        AggregateIterable<Document> iterable = db.getCollection("restaurants").aggregate(

                asList(

                new Document("$group", new Document("_id", "$borough")

                        .append("count", new Document("$sum", 1))

                        )

                , new Document("$sort", new Document("count", -1))

                )

                );

        iterable.forEach(new Block<Document>() {

            @Override

            public void apply(final Document document) {

                System.out.println(document.toJson());

            }

        });

```

$match filter document

$sort

$limit

$group group by      _id:$key

以上实例类似sql语句： select by_user, count(*) from mycol group by user 

只有num_tutorial和user可以换成其他单词





e.g.

不显示"data"

db.fs.chunks.find({"files_id":"treeId"}, {"data":0})





####数据分片

默认不对数据分片

数据分片过程：

1. 建索引

2. 指定片键分片。 mongodb自动根据片键拆分数据块 ，每个块包含片键的一个范围。块拆分通过配置服务器更新块信息来完成。

3. 迁移数据块

4. 查询时使用片键，mongos直接将查询发送到分片。不使用片键，则发送到每个分片上。









块拆分：

相同片键的文档必须保存在相同的块。这可能导致特大块问题。





片键类型（该字段变化的规律）：

升序

随机

位置





片键策略

散列片键：升序键如果要随机分发，使用散列片键。例如gridfs的chunks集合上对files_id创建hashed片键。

流水策略





好的片键策略

1. 准升序片键+搜索键

比如{mongth:1,user:1}

优点：保证数据（负载）均匀分布，也能使经常读写的数据保持在内存中（老数据不会频繁迁移）

场景：应用访问新数据比老数据频繁

准升序片键：一个值最好对应几十几百chunk块

搜索键：应用程序查询用到的字段，非升序，分布随机

2. 更一般的情况：

coarseLocality:1, search:1

控制数据局部化字段 + 检索字段









指定集合存储在某个分片上

addShardTag addTagRange







手动数据迁移

关闭均衡器

moveChunk()









