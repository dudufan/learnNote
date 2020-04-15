[TOC]

# 集群

## sentinel监控原理
sentinel启动时加载配置文件，与监控的主建立两条连接


    连接1：订阅主的__sentinel__:hello频道，来获取其他sentinel的信息。每2秒发布自己信息
    
    连接2：每10秒向主发送info，获得从的信息。每1秒向主、从、其他sentinel发送PING



# 事务
redis事务只能保证命令连续执行，也就是说中间不会有其他客户端的插入。但不能保证**在提交事务（exec)之前，命令所依赖的数据不被其他客户端改变**！
解决办法：multi开启事务前使用watch命令加乐观锁。watch后exec之前，如果其他客户端（当前客户端改变也会导致事务无效）改动了事务使用的键，那当前整个事务都会被取消


为了保

# Redis数据类型

## String

> **常用命令:**  set,get,decr,incr,mget 等。

String数据结构是简单的key-value类型，value其实不仅可以是String，也可以是数字。 常规key-value缓存应用； 常规计数：微博数，粉丝数等。

## hash

> **常用命令：** hget,hset,hgetall 等。

hash 特别适合用于存储对象，后续操作的时候，你可以直接仅仅修改这个对象中的某个字段的值

使用场景：

1. 当做全局map来用，相当于查找表。比如用一个hash类型的键slug.to.id,记录文章网址缩略名和ID之间的映射关系
2. 存储对象。每篇文章也是一个hash类型的键，如post:42 

## List

> **常用命令:** lpush,rpush,lpop,rpop,lrange等

Redis最重要的数据结构之一

使用场景：微博的关注列表，粉丝列表，消息列表等功能

实现：Redis list 的实现为一个双向链表，即可以支持反向查找和遍历，更方便操作，不过带来了部分额外的内存开销。

**分页**

可以通过 lrange 命令，就是从某个元素开始读取多少个元素，可以基于 list 实现分页查询，因此可以基于 redis 实现简单的高性能分页，做类似微博那种下拉不断分页的东西（一页一页的往下走）。

## Set

集合用于表达对象间关系。

使用场景：

1. 去重
2. 交集、并集、差集的操作。

实例：

1. 比如在微博应用中，可以将一个用户所有的关注人存在一个集合中，这样就方便实现共同关注、共同粉丝、共同喜好等功能
2. 标签功能

```shell
sadd 添加到不存在的集合或已有集合
spop  随机pop出一个值
scard 统计基数
smembers 获取全部元素
sismember myset 1 2 3
srandmember 随机返回一个值，不删除
sinter 求交集
sunionstore 求交集，结果放入第一个参数。可以用来拷贝set	
```



## lists
lpush list1 a b c d
rpush  lpop rpop
lrange list1 0 -1 获取全部元素
用途：获取最新的10张照片


ltrim 保留元素 
用途：配合lpush存储最近的项，实现上限列表
lpush list1 a b c d e f
ltrim list1 0 2


BLPOP BRPOP 
阻塞操作，可指定多个list返回第一个元素，以及阻塞时间 用途：生产消费者模式
blpop tasks1 tasks2 5

## sorted sets

> **常用命令：** zadd,zrange,zrem,zcard等

和set相比，sorted set增加了一个权重参数score，使得集合中的元素能够按score进行有序排列。

场景：适合经常更新分数的场合，比如排行榜

举例： 在直播系统中，实时排行信息包含直播间在线用户列表，各种礼物排行榜，弹幕消息（可以理解为按消息维度的消息排行榜）等信息，适合使用 Redis 中的 Sorted Set 结构进行存储。


```shell
zadd hackers 1940 "Alan Kay"
zrange hackers 0 -1 升序
zrevrange hackers 0 -1 降序

zrange hackers 0 -1 withscores 带分数

zrangebyscores hackers -inf 1950
zrank hackers "Anita Borg" 查询元素排序位置
```



## BItmaps
节省空间，比如，在一个系统中，不同用户由递增的用户 ID 来表示，可以使用 512MB 的内存来表示 400 万用户的单个位信息(例如他们是否需要接收信件)。


位图的通用场景：
各种实时分析
需要高性能和高效率的空间利用来存储与对象 ID 关联的布尔信息。

> setbit key 10 1 
> (integer) 1 
> getbit key 10 
> (integer) 1 
> getbit key 11 
> (integer) 0  

# Redis服务端配置

```properties
# 设置客户端连接时的超时时间，单位为秒。当客户端在这段时间内没有发出任何指令，那么关闭该连接
# 0是关闭此设置
timeout 0
```

https://www.cnblogs.com/AlanLee/p/7053577.html

动态修改redis配置

```shell
redis 127.0.0.1:6379> CONFIG GET CONFIG_SETTING_NAME
> config set timeout 0
```

# 过期

对于设置了过期时间的key，redis采取定期删除+惰性删除的机制淘汰数据

- **定期删除**：redis默认是每隔 100ms 就**随机抽取**一些设置了过期时间的key，检查其是否过期，如果过期就删除。
- **惰性删除** ：定期删除可能会导致很多过期 key 到了时间并没有被删除掉。所以就有了惰性删除。假如你的过期 key，靠定期删除没有被删除掉，还停留在内存里，除非你的系统去查一下那个 key，才会被redis给删除掉

如果大量过期key堆积在内存里，导致redis内存块耗尽，那么需要使用redis 内存淘汰策略。

# 事务

Redis 通过 MULTI、EXEC、WATCH  等命令来实现事务。

特点：

1. 实现一次性、按顺序执行多个命令的机制
2. 在事务执行期间，服务器不会中断事务而改去执行其他客户端的命令请求
3. redis同一个事务中如果有一条命令执行失败，其后的命令仍然会被执行，没有回滚。

Redis不支持回滚的原因:

1. 只有当发生语法错误(这个问题在命令队列时无法检测到)了，Redis命令才会执行失败,    或对keys赋予了一个类型错误的数据：这意味着这些都是程序性错误，这类错误在开发的过程中就能够发现并解决掉，几乎不会出现在生产环境。
2. 由于不需要回滚，这使得Redis内部更加简单，而且运行速度更快。

Redis也具有事务的ACID性质。

# 持久化

## 快照持久化

RDB

Redis可以通过创建快照来获得存储在内存里面的数据在某个时间点上的副本。Redis创建快照之后，可以对快照进行备份，可以将快照复制到其他服务器从而创建具有相同数据的服务器副本（Redis主从结构，主要用来提高Redis性能），还可以将快照留在原地以便重启服务器的时候使用。

快照持久化是Redis默认采用的持久化方式，在redis.conf配置文件中默认有此下配置：

```
save 900 1           #在900秒(15分钟)之后，如果至少有1个key发生变化，Redis就会自动触发BGSAVE命令创建快照。

save 300 10          #在300秒(5分钟)之后，如果至少有10个key发生变化，Redis就会自动触发BGSAVE命令创建快照。

save 60 10000        #在60秒(1分钟)之后，如果至少有10000个key发生变化，Redis就会自动触发BGSAVE命令创建快照。
```

## AOF持久化

与快照持久化相比，AOF持久化 的实时性更好，因此已成为主流的持久化方案。默认情况下Redis没有开启AOF（append only file）方式的持久化，可以通过appendonly参数开启：

```
appendonly yes
```

开启AOF持久化后，每执行一条会更改Redis中的数据的命令，Redis就会将该命令写入硬盘中的AOF文件。它们分别是：

```
appendfsync always    #每次有数据修改发生时都会写入AOF文件,这样会严重降低Redis的速度
appendfsync everysec  #每秒钟同步一次，显示地将多个写命令同步到硬盘
appendfsync no        #让操作系统决定何时进行同步
```

为了兼顾数据和写入性能，用户可以考虑 appendfsync everysec选项  ，让Redis每秒同步一次AOF文件，Redis性能几乎没受到任何影响。而且这样即使出现系统崩溃，用户最多只会丢失一秒之内产生的数据。当硬盘忙于执行写入操作的时候，Redis还会优雅的放慢自己的速度以便适应硬盘的最大写入速度。

## 混合持久化

Redis 4.0 开始支持 RDB 和 AOF 的混合持久化（默认关闭，可以通过配置项 `aof-use-rdb-preamble` 开启）。

如果把混合持久化打开，AOF 重写的时候就直接把 RDB 的内容写到 AOF 文件开头。这样做的好处是可以结合 RDB 和 AOF  的优点, 快速加载同时避免丢失过多的数据。当然缺点也是有的， AOF 里面的 RDB 部分是压缩格式不再是 AOF 格式，可读性较差。

# Jedis配置

```properties
#### env:${env}
redis.maxIdle=80

##最小空闲数
redis.minIdle=10

##最大连接数：能够同时建立的“最大链接个数”
redis.maxTotal=500

#每次最大连接数
redis.numTestsPerEvictionRun=1024

##最大建立连接等待时间：单位ms
##当borrow一个jedis实例时，最大的等待时间，如果超过等待时间，则直接抛出JedisConnectionException；
redis.maxWait=5000

##使用连接时，检测连接是否成功 
redis.testOnBorrow=true

#连接耗尽时是否阻塞，false报异常，true阻塞超时,默认true
redis.blockWhenExhausted=false

##在return给pool时，是否提前进行validate操作
redis.testOnReturn=true
 
##当客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能，单位毫秒
redis.timeout=3000

#在空闲时检查有效性，默认false
redis.testWhileIdle=true

#连接的最小空闲时间，连接池中连接可空闲的时间
redis.minEvictableIdleTimeMills=30000
        
#释放扫描的扫描间隔，单位毫秒数；检查一次连接池中空闲的连接,把空闲时间超过minEvictableIdleTimeMillis毫秒的连接断开，直到连接池中的连接数到minIdle为止
redis.timeBetweenEvictionRunsMillis=60000
```

# Unexpect end of stream

https://www.jianshu.com/p/d4bde8b7135b

JedisConnectionException: Unexpected end of stream

场景：

1. 连接空闲了一定时间后，被redis杀死
2. jedis连接池的失效连接未清理掉，使用后异常

两种解决方案：

1. 设置redis配置中的timeout=0
2. 设置jedis配置：minEvictableIdleTimeMillis 、 softMinEvictableIdleTimeMillis 

 `CONFIG SET parameter value` 





## 文章发布与投票

hash存储文章，包含发布时间，投票数。单个文章

article:1234 

zset记录对该文章已投票的用户。全局存

voted:1234



zset根据时间排序文章。 全局

time:



zset 根据评分（投票数）排序文章。全局

score:



## 登录cookie

一个大的hash存储令牌和用户id的键值对

login:





zset存储最近登录token和对应timestamp。可以限制在线用户数（得到待删除的token)

recent:





zset存储登录token浏览过的商品

viewed:tokenId





hash存储会话session 购物车（商品）

viewed:session

## 购物车cookie

# 缓存宕机

问题：缓存同一时间大面积的失效，所以，后面的请求都会落到数据库上，造成数据库短时间内承受大量请求而崩掉。

解决办法：

- 事前：尽量保证整个 redis 集群的高可用性，发现机器宕机尽快补上。选择合适的内存淘汰策略。
- 事中：本地ehcache缓存 + hystrix限流&降级，避免MySQL崩掉
- 事后：利用 redis 持久化机制保存的数据尽快恢复缓存

# 布隆过滤器

**Redis 4.0** 提供了插件功能之后，布隆过滤器作为一个插件加载到 Redis Server中。

自定义创建过滤器

`bf.reserve` 有三个参数，分别是 `key`、`error_rate` *(错误率)* 和 `initial_size`：

- **error_rate 越低，需要的空间越大**，对于不需要过于精确的场合，设置稍大一些也没有关系，比如上面说的推送系统，只会让一小部分的内容被过滤掉，整体的观看体验还是不会受到很大影响的；
- **initial_size 表示预计放入的元素数量**，当实际数量超过这个值时，误判率就会提升，所以需要提前设置一个较大的数值避免超出导致误判率升高；

如果不使用 `bf.reserve`，默认的 `error_rate` 是 `0.01`，默认的 `initial_size` 是 `100`。

默认参数的布隆过滤器使用：

```mysql
127.0.0.1:6379> bf.add codehole user1
(integer) 1
127.0.0.1:6379> bf.exists codehole user1
(integer) 1
127.0.0.1:6379> bf.exists codehole user4
(integer) 0
127.0.0.1:6379> bf.madd codehole user4 user5 user6
1) (integer) 1
2) (integer) 1
3) (integer) 1
127.0.0.1:6379> bf.mexists codehole user4 user5 user6 user7
1) (integer) 1
2) (integer) 1
3) (integer) 1
4) (integer) 0
```