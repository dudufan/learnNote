[TOC]


#问题
***
##Connection.getStatusCodeReply() 第一行是flush()
意思是将buf的数据写入socket的输出流，并且清空buf(count置0)


##Redis请求协议中二进制安全的具体含义？
http://doc.redisfans.com/topic/protocol.html


##ConnectionTimeout versus SocketTimeout
>A **connection timeout** occurs only upon starting the TCP connection. This usually happens if the remote machine does not answer. This means that the server has been shut down, you used the wrong IP/DNS name or the network connection to the server is down.
 
>A **socket timeout** is dedicated to monitor the continuous incoming data flow. If the data flow is interrupted for the specified timeout the connection is regarded as stalled/broken. Of course this only works with connections where data is received all the time.
 
##Redis以String为基本类型
>A note about String and Binary - what is native?
 
>Redis/Jedis talks a lot about Strings. And here http://redis.io/topics/internals it says Strings are the basic building block of Redis. However, this stress on strings may be misleading. Redis' "String" refer to the C char type (8 bit), which is incompatible with Java Strings (16-bit). Redis sees only 8-bit blocks of data of predefined length, so normally it doesn't interpret the data (it's "binary safe"). Therefore in Java, byte[] data is "native", whereas Strings have to be encoded before being sent, and decoded after being retrieved by the SafeEncoder. This has some minor performance impact. In short: if you have binary data, don't encode it into String, but use the binary versions.
##多线程
> using Jedis in a multithreaded environment
 
>You shouldn't use the same instance from different threads because you'll have strange errors. And sometimes creating lots of Jedis instances is not good enough because it means lots of sockets and connections, which leads to strange errors as well. A single Jedis instance is not threadsafe! To avoid these problems, you should use JedisPool, which is a threadsafe pool of network connections. You can use the pool to reliably create several Jedis instances, given you return the Jedis instance to the pool when done. This way you can overcome those strange errors and achieve great performance.


##subscribe
是阻塞操作，什么时候不再阻塞？

可订阅多个频道


##一致性hash


##ShardedJedis


##commons-pool 驱逐线程配置


##socket
socket是TCP/IP复杂操作抽象出来的接口

>socket起源于UNIX，在Unix一切皆文件哲学的思想下，socket是一种"打开—读/写—关闭"模式的实现，服务器和客户端各自维护一个"文件"，在建立连接打开后，可以向自己文件写入内容供对方读取或者读取对方内容，通讯结束时关闭文件。



>通常服务器在启动的时候都会绑定一个众所周知的地址（如ip地址+端口号），用于提供服务，客户就可以通过它来接连服务器；而客户端就不用指定，有系统自动分配一个端口号和自身的ip地址组合。这就是为什么通常服务器端在listen之前会调用bind()，而客户端就不会调用，而是在connect()时由系统随机生成一个。
#源码类分析
##Overview
***
###实现Jedis客户端：
建立连接 Jedis 组合==> Client 继承==> BinaryClient 继承==> Connection 组合==> Socket
发送命令 Jedis  组合 ==> Client  继承 ==>  BinaryClient   继承 ==>  Connection 组合==> Protocol


     Connection.sendCommand(...) ==> Protocol.sendCommand(...)
接收回复  Jedis  组合 ==> Client  继承 ==>  BinaryClient   继承 ==>  Connection 组合==> Protocol


     Connection.get**Reply()  Connection . readProtocolWithCheckingBroken()
==> Protocol.read(is) Protocol.process( is )




个人理解：
Protocol 工作在客户端-服务器收发协议层(应用层)，包装请求、 解析 回复
Connection 调用socket完成基础的连接，发送命令，接收回复

BinaryClient 提供参数为byte[]接口，如get,set,事务，pipeline
Client 在 BinaryClient上继续封装一层， 提供参数为String的接口
 


###实现Jedis连接池：
JedisFactory 实现==>  PooledObjectFactory<Jedis>
JedisPool 继承==>   JedisPoolAbstract  继承==> Pool  组合 ==>  GenericObjectPool



 
 

  ##JedisSentinelPool
JedisSentinelPool和JedisPool都继承自JedisPoolAbstract



JedisSentinelPool类：

> Set<MasterListener> masterListeners
GenericObjectPoolConfig poolConfig

JedisFactory factory

HostAndPort currentHostMaster

###构造器初始化
使用Set<sentinel>, master_name初始化。master的ip、port由sentinel getaddrbyname获得

initSentinels
返回master地址并监听主


Set中每个sentinel得到对应的jedis连接
由sentinel的jedis获得master的HostAndIP，返回
监听master：
    
    1.  定义内部类MasterListener监听主
     2.  run方法中每个sentinel得到一个jedis，sentinel订阅+switch...频道,可以接收所有实例的切换事 件，并根据得到的事件信息（新master的ip port）调 用initPool
    3. 若主的ip改变，则initPool会更改current_master为当前新的master



返回master的地址和端口 initPool
```
    if (!master.equals(currentHostMaster)) {
      currentHostMaster = master;
      if (factory == null) {
        factory = new JedisFactory(master.getHost(), master.getPort(), connectionTimeout,
            soTimeout, password, database, clientName, false, null, null, null);
        initPool(poolConfig, factory);
      } else {
        factory.setHostAndPort(currentHostMaster);
        // although we clear the pool, we still have to check the
        // returned object
        // in getResource, this call only clears idle instances, not
        // borrowed instances
        internalPool.clear();
      }
```
判断master是否当前主
创建jedis factory
使用poolConfig和jedis的factory调用Pool.initPool 初始化

###getResource
判断当前主和super.getResource()得到的连接是否相同

###destroy
调用每个masterL istener的shutdown方法

##Jedis


Jedis类
> JedisPoolAbstract dataSource;
close


```
/// Jedis implements Closable. Hence, the jedis instance will be auto-closed after the last statement.
try (Jedis jedis = pool.getResource()) {
  /// ... do stuff here ... for example
  jedis.set("foo", "bar");
  String foobar = jedis.get("foo");
  jedis.zadd("sose", 0, "car"); jedis.zadd("sose", 0, "bike");
  Set<String> sose = jedis.zrange("sose", 0, -1);
}
/// ... when closing your application:
pool.destroy();



Jedis
 jedis 
=
 
null
;

try
 {
} 
finally
 {
  
if
 (jedis 
!=
 
null
) {
    jedis
.
close();
  }
}

来源：  https://github.com/xetorthio/jedis/wiki/Getting-started
```
BinaryJedis类
>


构造器调用顺序 BinaryJedis ==> Client ==> BinaryClient ==> Connection



Jedis中组合了Pipeline、client、Transaction，
Jedis、Pipeline、 Transaction都依赖于同一个Client对象（委托）


Jedis3.0后使用Jedis.close()方法释放连接，调用this.dataSource.returnResource()方法
Jedis类中组合了 JedisPoolAbstract 类型的dataSource


##Connection
Connnection类
>host port
Socket socket
RedisOutputStream outputStream;
RedisInputStream inputStream;
connectionTimeout

soTimeout

SSLSocketFactory



connect()方法调用socket进行连接,并包装socket.outputStream()和socket.getOutputStream()
sendCommand()将多个String参数转化为byte[args.length][]


     bargs[i] = SafeEncoder.encode(args[i])



## RedisOutputStream     RedisInputStream  
继承自FilterOutputStream
提供buf
定义多个格式写入输出流的方法
>writeIntCrLf(int value)

writeCrLf



##Protocol 包装cmd，实现Redis协议（请求和回复)
请求协议  http://doc.redisfans.com/topic/protocol.html


请求协议的实现 sendCommand
```
  private static void sendCommand(final RedisOutputStream os, final byte[] command,
      final byte[]... args) {
    try {
      os.write(ASTERISK_BYTE);//*
      os.writeIntCrLf(args.length + 1);//参数个数（命令也算一个参数）
      os.write(DOLLAR_BYTE);//$
      os.writeIntCrLf(command.length);//命令（参数）长度
      os.write(command);//命令（参数）数据
      os.writeCrLf();// \r\n (CRLF)
 
      for (final byte[] arg : args) {
        os.write(DOLLAR_BYTE);
        os.writeIntCrLf(arg.length);
        os.write(arg);
        os.writeCrLf();
      }
    } catch (IOException e) {
      throw new JedisConnectionException(e);
    }
  }
```
以下是请求协议的一般形式：
 
     *<参数数量> CR LF
     $<参数 1 的字节数量> CR LF
     <参数 1 的数据> CR LF
     ...
     $<参数 N 的字节数量> CR LF
     <参数 N 的数据> CR LF
 
译注：命令本身也作为协议的其中一个参数来发送。
 
举个例子， 以下是一个命令协议的打印版本：
 
     *3
     $3
     SET
     $5
     mykey
     $7
     myvalue
 
这个命令的实际协议值如下：


     "*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$7\r\nmyvalue\r\n"


回复：
批量回复。和请求协议类似  "$6 \r\n foobar \r\n "

多条批量回复。如LRANGE的回复，多条批量回复和请求协议相同，区别是多条批量回复的类型多。如，



##Pool （Jedis)
继承体系:


     JedisPool 继承==> JedisAbstract 继承==> Pool<Jedis> 组合==>  GenericObjectPool<T> internal


     JedisFactory ==> PooledObjectFactory<Jedis>



实现连接池:

Pool<Jedis>

>GenericObjectPool<T> internal  = new GenericObjectPool<T>(factory, poolConfig);
returnBrokenResourceObject(final T resource) 调用invalidateObject(T)
T getResource() 调用borrowObject



JedisPool类对象的基类部分也是在 JedisPool构造器中直接赋值的，因为基类（Pool)成员是protected





JedisFactory
>makeOneObject() 返回的是 DefaultPooledObject<Jedis>

destroyObject(PooledObject<Jedis> pooledJedis) 销毁Jedis，实现上就是让Jedis安全退出redis

activateObject(PooledObject<Jedis> pooledJedis) 激活对象，实际上是

passivateObject(){} 空

validateObject(PooledObject<Jedis> pooledJedis) 判断池化对象包装的Jedis连接的主机是否和Pool初始化JedisFactory的HostAndPort一致，并且是否连接上，ping是否返回PONG。都为true则验证通过



JedisFactory 实现PooledObjectFactory<Jedis>接口(提供对池化对象的创建销毁等方法)因此可以作为初始化 对象池的工厂类





##commons-pool


###池化对象工厂
PooledObjectFactory<T>接口
定义了被池化的对象的创建，初始化，激活，钝化以及销毁功能
实现该接口的工厂类：JedisFactory


### 池化对象
PooledObject

池化对象用来包装一般对象，定义了被池化对象的一些附加信息【创建时间，池中状态】；大概流程就是由PooledObjectFactory创建的对象经过PooledObject的包装然后放到ObjectPool里面来。


实现该接口的池化对象类：  DefaultPooledObject<T>


###对象池
GenericObjectPool

对象池 （ObjectPool） 保存池化对象引用，保存池的配置，从宏观上管理池化对象们
定义了对象池要实现的功能【比如怎么存取，怎么过期】



GenericObjectPool
>allObjects 所有和pool关联的对象，最大容量是maxActive.不包括destroyed的

idleObjects 用阻塞队列保存空闲对象引用

addObject() 创建pool后可以执行。调用create()
borrowObject() 得到空闲对象或创建新对象 ==> validateObject

returnObject() 检测对象是否是已分配状态（代表未归还） ==> passivateObject ==> idle对象达到最大则destroy该对象


>invalidateObject(T obj)



>AbandonedConfig abandonedConfig; 配置了 abandonedConfig后，在borrowObject前先根据配置遍历所有obj，invalidateObject满足abandon条件的对象



>destory 销毁池中对象，调用 factory.destroyObject(toDestory)释放该对象持有的资源（比如jedis持有的连接，jedis.quit()）


GenericObjectPool

注：JedisFactory的 passivateObject方法体为空


#MstpMysqlCacheClient实现
>dbCacheMap 缓存Cache层建立连接所需的所有DBCacheConfigVo

initSentilCache(HashMap） 将dbCache和Sentinel分别两个配置列表作为一个Map，初始化dbCacheMap
getInstance() 调用构造器，构造器使用lanuchsentil 为一个主（dbCache Node） 初始化JedisSentinelPool
lanuchsentil（） 


lanuchsentil



     将dbCacheMap中所有配置加入list， 遍历两次list。
    遍历1： sentinel的ip、port转换为String，来构造Set<String> sentinels
    遍历2： 由 Set<String> sentinels、masterName(ip:port) 来构造以每个主的连接池 JedisSentinelPool
    遍历2：每个 JedisSentinelPool都要加入sharingMap,这样在getPool时可以返回第key%modNum个Pool，做一个简单分片

