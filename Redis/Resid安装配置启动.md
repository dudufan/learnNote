# Part I. 直接启动 下载

官网下载 安装
tar zxvf redis-2.8.9.tar.gz
cd redis-2.8.9

直接make 编译

make

可使用root用户执行`make install`，将可执行文件拷贝到/usr/local/bin目录下。这样就可以直接敲名字运行程序了。

make install 启动
加上`&`号使redis以后台程序方式运行

.
/redis-server & 检测
检测后台进程是否存在

ps -ef |grep redis


检测6379端口是否在监听

netstat -lntp | grep 
6379
使用`redis-cli`客户端检测连接是否正常

./redis-cli

127.0
.0
.1
:
6379
> keys *
(empty list or 
set
)

127.0
.0
.1
:
6379
> 
set
 key 
"hello world"

OK

127.0
.0
.1
:
6379
> 
get
 key

"hello world" 停止
使用客户端

redis-cli 
shutdown
因为Redis可以妥善处理SIGTERM信号，所以直接kill -9也是可以的
kill
 -
9
 PID #Part II. 通过指定配置文件启动 配置文件

可为redis服务启动指定配置文件，配置文件 redis.conf 在Redis根目录下。
修改daemonize为yes，即默认以后台程序方式运行（还记得前面手动使用&号强制后台运行吗）。

daemonize 
no
可修改默认监听端口

port 
6379
修改生成默认日志文件位置

logfile 
"/home/futeng/logs/redis.log"
配置持久化文件存放位置

dir /home/futeng/data/redisData 启动时指定配置文件
redis-server ./redis.conf

如果更改了端口，使用`redis-cli`客户端连接时，也需要指定端口，例如：

redis-cli -p 6380

其他启停同 直接启动 方式。配置文件是非常重要的配置工具，随着使用的逐渐深入将显得尤为重要，推荐在一开始就使用配置文件。 #Part III. 使用Redis启动脚本设置开机自启动 启动脚本

推荐在生产环境中使用启动脚本方式启动redis服务。启动脚本 redis_init_script 位于位于Redis的 /utils/ 目录下。
大致浏览下该启动脚本，发现redis习惯性用监听的端口名作为配置文件等命名，我们后面也遵循这个约定。
redis服务器监听的端口

REDISPORT=6379

服务端所处位置，在make install后默认存放与`/usr/local/bin/redis-server`，如果未make install则需要修改该路径，下同。

EXEC=/usr/local/bin/redis-server

客户端位置

CLIEXEC=/usr/local/bin/redis-cli

Redis的PID文件位置

PIDFILE=/var/run/redis_
${REDISPORT}
.pid

配置文件位置，需要修改

CONF=
"/etc/redis/
${REDISPORT}
.conf" 配置环境

1. 根据启动脚本要求，将修改好的配置文件以端口为名复制一份到指定目录。需使用root用户。
mkdir
 /etc/redis
cp redis.conf /etc/redis/
6379
.conf

 2. 将启动脚本复制到/etc/init.d目录下，本例将启动脚本命名为redisd（通常都以d结尾表示是后台自启动服务）。
cp redis_init_script /etc/init.d/redisd
启动脚本中默认的路径是/usr/local/bin/...，所以最好先make install，再复制启动脚本

 3.     设置为开机自启动

此处直接配置开启自启动 chkconfig redisd on 将报错误： service redisd does not support chkconfig


mv redis（脚本） /etc/init.d/redis
chmod +x /etc/init.d/redis
chkconfig --add redis
chkconfig redis on 参照 此篇文章 ，在启动脚本开头添加如下两行注释以修改其运行级别：



```
!/bin/sh
 chkconfig:   2345 90 10
 description:  Redis is a persistent key-value database

```

 再设置即可成功。

```
设置为开机自启动服务器

chkconfig redisd on

打开服务

service redisd start

关闭服务

service redisd stop ```

来源：  http://www.tuicool.com/articles/aQbQ3u






 #安装详细教程
##安装Redis服务端
 
官网下载源码：http://redis.io/download
wget http://redis.googlecode.com/files/redis-2.6.14.tar.gz
tar xzf redis-2.6.14.tar.gz
cd redis-2.6.14
 
 
##make
make #redis的安装非常简单，已经有现成的Makefile文件，直接运行make命令即可
 
                   可能出现的报错
 
在/opt/redis-2.6.14/目录下，执行make时报错：/bin/sh: cc: command not found
 
好吧，都没有装相关的编译工具。
 
搜，sudo apt-get install build-essential
 
error 1）：bash: apt-get: command not found
 
    再搜，CentOS的软件安装工具不是apt-get  是yum，
 
    正确的应该是sudo yum -y install gcc gcc-c++ libstdc++-devel
 
    安装成功。
 
error 2）在/opt/redis-2.6.14/目录下，执行make时报错
 
    make[1]: Entering directory `/opt/redis-2.6.14/src'
    CC adlist.o
    In file included from adlist.c:34:
    zmalloc.h:50:31: error: jemalloc/jemalloc.h: No such file or directory
    zmalloc.h:55:2: error: #error "Newer version of jemalloc required"
    make[1]: *** [adlist.o] Error 1
    make[1]: Leaving directory `/opt/redis-2.6.14/src'
    make: *** [all] Error 2
 
    好吧，继续~,发现:http://xueliang1yi.blog.163.com/blog/static/1145570162012102114635764/
 
    好像遇到了类似的情况，文中提到了安装gcc,把他的命令也敲了一边，系统提示最新版本的已经装好了，不需要再装了。
 
    之后执行 make MALLOC=libc 就行
 
error 3）执行完上面的命令后，系统提示 'Hint: To run 'make test' is a good idea'
 
    make test 报错: You need tcl 8.5 or newer in order to run the Redis test
 
　　    发现 sudo yum install tcl 就可以搞定，只是版本是8.5.7的。
 
          终于提示'\o/ All tests passed without errors!'
 
在/opt/redis-2.6.14/目录下，执行make，OK;
 
 
 
 
##复制可执行文件 
手动复制src/redis* 或者make install
make install 会把src中的多个可执行文件复制到/usr/local/bin


注意，默认复制过去的redis.conf文件的daemonize参数为no，所以redis不会在后台运行，这时要测试，我们需要重新开一个终端。修改为yes则为后台运行redis。
另外配置文件中规定了pid文件，log文件和数据文件的地址，如果有需要先修改，默认log信息定向到
stdout。
 
##配置开机自启动redis-server
 
mv redis（脚本） /etc/init.d/redis
chmod +x /etc/init.d/redis
chkconfig --add redis
chkconfig redis on
 
##启动redis：
service redis start
若不成功：可能是redis-server没有权限---->chmod +x redis-server
测试：
 
##打开客户端
 /usr/local/redis/bin/redis-cli
redis 127.0.0.1:6379> set name linuxeye
OK
redis 127.0.0.1:6379> get name
"linuxeye"
关闭redis:
service redis stop