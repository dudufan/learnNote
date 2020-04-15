[TOC]


trace 

show profile for query x

索引优化：

where中不等于操作符，会造成全表扫描

# 安装

## yum安装

下载并安装MySQL官方的 Yum Repository

```shell
yum install wget
wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
yum -y install mysql57-community-release-el7-10.noarch.rpm

# yum安装MySQL
yum -y install mysql-community-server
systemctl start  mysqld.service
systemctl status mysqld.service
# 找出默认root随机密码
grep "password" /var/log/mysqld.log


```

## windows

5.7安装步骤如下

解压后修改my.ini

```ini
[client]
port=3306
default-character-set=utf8
[mysqld] 
# 设置为自己MYSQL的安装目录 
basedir=D:\Program\mysql5.7
# 设置为MYSQL的数据目录 
datadir=D:\Program\mysql5.7\data
port=3306
character_set_server=utf8
sql_mode=NO_ENGINE_SUBSTITUTION,NO_AUTO_CREATE_USER
#开启查询缓存
explicit_defaults_for_timestamp=true
skip-grant-tables
```

目录下新建data

设置mysql/bin到环境变量PATH中

进入Mysql安装目录下的bin文件夹，以管理员身份执行 

```shell
mysqld --initialize
mysqld install 
net start mysql
```

因为my.ini中加入了skip-grant-tables配置，所以可以直接使用 mysql -u root -p   输入任意密码登录 

然后通过SQL语句修改root用户的密码；

```mysql
#将数据库切换至mysql库
mysql> USE mysql;
#修改密码
mysql> update user set authentication_string=PASSWORD('root') where user='root';
alter user 'root'@'localhost' identified by 'root';
#刷新MySQL权限相关的表
mysql> flush privileges;
mysql> exit;
```

## 配置

root登录后，修改mysql密码。为方便测试，给所有ip开通访问权限

```shell
mysql> set global validate_password_policy=0;
mysql> set global validate_password_length=1;

#将数据库切换至mysql库
mysql> USE mysql;
#修改密码
mysql> update user set authentication_string=PASSWORD('root') where user='root';
alter user 'root'@'localhost' identified by 'root';

# 访问权限
update user set host = ’%’ where user = ’root’;
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

#刷新MySQL权限相关的表
mysql> flush privileges;
mysql> exit;


```



# 命令行

mysql登录

```shell
mysql -u <username> -p<password>
mysql -hlocalhost -u<username> -p
```



# 基础配置

**sql忽略表名大小写**

mysql在windows系统下安装好后，默认是对表名大小写不敏感的，但是在linux下，一些系统需要手动设置。

1. 用root登录，打开并修改 /etc/my.cnf；在[mysqld]节点下，加入一行： lower_case_table_names=1。
2. 重启mysql服务

```shell
service mysqld restart
```

# 日志

## 刷脏页

当内存数据页跟磁盘数据页内容不一致的时候，我们称这个内存页为“脏页”。内存数据写入到磁盘后，内存和磁盘上的数据页的内容就一致了，称为“干净页”。

比如在崩溃恢复场景中，InnoDB 如果判断到一个数据页可能在崩溃恢复的时候丢失了更新，就会将它读到内存，然后让 redo log 更新内存内容。更新完成后，内存页变成脏页，就会刷到磁盘上。

**刷脏页有下面4种场景（后两种不用太关注“性能”问题）：**

- **redolog写满了：**redo log 里的容量是有限的，如果数据库一直很忙，更新又很频繁，这个时候 redo log 很快就会被写满了，这个时候就没办法等到空闲的时候再把数据同步到磁盘的，只能暂停其他操作，全身心来把数据同步到磁盘中去的，而这个时候，**就会导致我们平时正常的SQL语句突然执行的很慢**，所以说，数据库在在同步数据到磁盘的时候，就有可能导致我们的SQL语句执行的很慢了。
- **内存不够用了：**如果一次查询较多的数据，恰好碰到所查数据页不在内存中时，需要申请内存，而此时恰好内存不足的时候就需要淘汰一部分内存数据页，如果是干净页，就直接释放，如果恰好是脏页就需要刷脏页。
- **MySQL 认为系统“空闲”的时候：**这时系统没什么压力。
- **MySQL 正常关闭的时候：**这时候，MySQL 会把内存的脏页都 flush 到磁盘上，这样下次 MySQL 启动的时候，就可以直接从磁盘上读数据，启动速度会很快。



## redo log

参考 https://www.cnblogs.com/wupeixuan/p/11734501.html



语句执行过程

![](D:/dudufan108/oneDrive/Nuts/%E5%BC%80%E5%8F%91/img/mysql%E8%AF%AD%E5%8F%A5%E6%89%A7%E8%A1%8C%E6%B5%81%E7%A8%8B.png)

redo log是 InnoDB 存储引擎层的日志，又称重做日志文件。

内容：不是记录数据页更新之后的状态，而是记录数据页做了什么改动

特点：

1. 从头开始写，写到末尾就又回到开头循环写
2. 固定大小的，比如可以配置为一组 4 个文件，每个文件的大小是 1GB，那么日志总共就可以记录 4GB 的操作

作用：有了 redo log 日志，那么在数据库进行异常重启的时候，可以根据 redo log 日志进行恢复，也就达到了 crash-safe（崩溃恢复，即使数据库发生异常重启，之前提交的记录都不会丢失）。



redo log 和 binlog 区别：

1. redo log 是 InnoDB 引擎特有的；binlog 是 MySQL 的 Server 层实现的，所有引擎都可以使用。
2. redo log 是物理日志，记录的是在某个数据页上做了什么修改；binlog 是逻辑日志，记录的是这个语句的原始逻辑。
3. redo log 是循环写的，空间固定会用完；binlog 是可以追加写入的。追加写是指 binlog 文件写到一定大小后会切换到下一个，并不会覆盖以前的日志。

执行器和 InnoDB 引擎在执行这个 `UPDATE T SET c = c + 1 WHERE ID = 2;` 语句时的内部流程。

1. 执行器先找引擎取 ID=2 这一行。ID 是主键，引擎直接用树搜索找到这一行。如果 ID=2 这一行所在的数据页本来就在缓存中，就直接返回给执行器；否则，需要先从磁盘读入内存，然后再返回。
2. 执行器拿到引擎给的行数据，把这个值加上 1，比如原来是 N，现在就是 N+1，得到新的一行数据，再调用引擎API 接口写入这行新数据。
3. 引擎将这行新数据更新到内存（InnoDB Buffer Pool）中，同时将这个更新操作记录到 redo log 里面，此时 redo log 处于 prepare 状态。然后告知执行器执行完成了，随时可以提交事务。
4. 执行器记录binlog（磁盘），调用引擎的提交事务接口，把刚写入的 redo log 改成提交状态，更新完成。

## general log 

 记录mysqld(MySQLserver进程)收到的所有请求的日志 

查看是否开启、存储位置

```sql
mysql> show variables like '%general%';
#  临时开关通用日志查询
set global general_log = on;  
```



## slow log

 用来记录执行时长超过指定时长的查询语句，具体指运行时间超过 `long_query_time` 值的 SQL 语句 

 可以查找出哪些查询语句的执行效率很低，以便进行优化。一般建议开启 

```
slow_query_log : 是否启用慢查询日志，[1 | 0] 或者 [ON | OFF]

slow_query_log_file : MySQL数据库（5.6及以上版本）慢查询日志存储路径。
                    可以不设置该参数，系统则会默认给一个缺省的文件 HOST_NAME-slow.log

long_query_time : 慢查询的阈值，当查询时间超过设定的阈值时，记录该SQL语句到慢查询日志。
```

# SQL执行原理

mysql组件

- 连接器： 身份认证和权限相关(登录 MySQL 的时候)。
- 查询缓存:  执行查询语句的时候，会先查询缓存（MySQL 8.0 版本后移除，因为这个功能不太实用）
- 分析器：词法分析和语法分析。没有命中查询缓存的话，SQL 语句就会经过分析器检查你的 SQL 语句语法是否正确。
- 优化器： 按照 MySQL 认为最优的方案去执行，比如查询时选择索引。
- 执行器:  执行语句，然后从存储引擎返回数据。

查询等过程如下：权限校验---》查询缓存---》分析器---》优化器---》权限校验---》执行器---》引擎

更新等语句执行流程如下：分析器----》权限校验----》执行器---》引擎---redo log prepare---》binlog---》redo log commit

# 字符集及校对规则

字符集指的是一种从二进制编码到某类字符符号的映射。

推荐选择utf8mb4这个字符集，而不选择utf8. 因为MySQL的utf8字符编码只有三个字节，节省空间但不能表达全部的UTF-8



**校对规则**

某种字符集下的排序规则。MySQL中每一种字符集都会对应一系列的校对规则。

MySQL采用的是类似继承的方式指定字符集的默认值，每个数据库以及每张数据表都有自己的默认值，他们逐层继承。比如：某个库中所有表的默认字符集将是该数据库所指定的字符集（这些表在没有指定字符集的情况下，才会采用默认字符集）

常用规则。general_ci 更快，unicode_ci 更准确：

- utf8mb4_unicode_ci：是基于标准的Unicode来排序和比较，能够在各种语言之间精确排序，Unicode排序规则为了能够处理特殊字符的情况，实现了略微复杂的排序算法。

- utf8mb4_general_ci是一个遗留的 校对规则，不支持扩展，它仅能够在字符之间进行逐个比较。utf8_general_ci校对规则进行的比较速度很快，但是与使用 utf8mb4_unicode_ci的校对规则相比，比较正确性较差。
  

# 事务控制

## 事务隔离问题

### 脏读

Dirty Read

脏读意味着一个事务读取了另一个事务未提交的数据,而这个数据是有可能回滚

### 不可重复读

Unrepeatable Read

不可重复读意味着，在数据库访问中，一个事务范围内两个相同的查询却返回了不同数据。这是由于查询时系统中其他事务修改的提交而引起的。
例如：事务B中对某个查询执行两次，当第一次执行完时，事务A对其数据进行了修改。事务B中再次查询时，数据发生了改变

### 幻读

phantom read

幻读,是指当事务不是独立执行时发生的一种现象，例如第一个事务对一个表中的数据进行了修改，这种修改涉及到表中的全部数据行。同时，第二个事务也修改这个表中的数据，这种修改是向表中插入一行新数据。那么，以后就会发生操作第一个事务的用户发现表中还有没有修改的数据行，就好象发生了幻觉一样.



## 锁

### 读锁

- **也叫共享锁 （shared lock）**
- **如何使用**
  `SELECT * FROM table_name WHERE ... LOCK IN SHARE MODE`
- **详解**
  即事务A 使用共享锁 获取了某条（或者某些）记录时，事务B 可以读取这些记录，可以继续添加共享锁，但是不能修改或删除这些记录（当事务B 对这些数据修改或删除时会进入阻塞状态，直至锁等待超时或者事务A提交）
- **使用场景**
  读取结果集的最新版本，同时防止其他事务产生更新该结果集
  主要用在需要数据依存关系时确认某行记录是否存在，并确保没有人对这个记录进行UPDATE或者DELETE操作

### 写锁

- **也叫排它锁（exclusive lock）**
- **如何使用**
  `SELECT * FROM table_name WHERE ... FOR UPDATE`
- **详解**
  一个写锁会阻塞其他的**读锁和写锁**
  即事务A 对某些记录添加**写锁**时，事务B 无法向这些记录添加写锁或者读锁（不添加锁的读取是可以的），事务B 也无法执行对 锁住的数据 update delete
- **使用场景**
  读取结果集的最新版本，同时防止其他事务产生**读取或者更新该结果集**。

innodb是对索引加锁，不使用索引则锁整个表。 只要只用相同的索引如id=5,则需要等待释放锁
 不同事务的不同索引可能会锁定同一条记录



### 间隙锁

幻读问题：id为主键，number字段上有非唯一索引的二级索引，有什么方式可以让该表不能再插入number=5的记录？

间隙锁是为了解决不可重复读的问题。

特点：

- 当查询的索引有唯一属性时，比如主键，这时范围锁降级为行锁。
- 当查询的索引为辅助索引，会锁定该索引值b，以及前后两个间隙范围(a,b),(b,c)

参考https://www.cnblogs.com/crazylqy/p/7821481.html

**间隙锁锁定的区域**
根据检索条件向左寻找最靠近检索条件的记录值A，作为左区间，向右寻找最靠近检索条件的记录值B作为右区间，即锁定的间隙为（A，B）。
图一中，where number=5的话，那么间隙锁的区间范围为（4,11）；

个人理解间隙锁的“间隙”，指的是索引B+树叶子节点之间的间隙。

**间隙锁的目的是为了防止幻读，其主要通过两个方面实现这个目的：**
（1）防止间隙内有新数据被插入
（2）防止已存在的数据，更新成间隙内的数据（例如防止numer=3的记录通过update变成number=5）

**innodb自动使用间隙锁的条件：**
（1）必须在RR级别下
（2）检索条件必须有索引（没有索引的话，mysql会全表扫描，那样会锁定整张表所有的记录，包括不存在的记录，此时其他事务不能修改不能删除不能添加）

### 锁表

通常发生在DDL语句\DML不走索引的语句中

## 当前读

- 像select lock in share mode(共享锁), select for update ; update, insert ,delete(排他锁)这些操作读取的是记录的最新版本
- 读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁。
- 当前读就是悲观锁的具体功能实现 

## 快照读

- 像不加锁的select操作就是快照读

- 读到的有可能是之前的历史版本
- 基于多版本并发控制实现，避免了加锁操作。

## 多版本并发控制

MVCC和事务隔离级别结合实现了innodb的高并发特性。也可以理解为事务隔离级别的功能是在MVCC基础上实现的。

https://www.zhihu.com/question/263820564/answer/289269082

多版本并发控制（MVCC）：

- 多版本存储。为每个修改保存一个版本，版本与事务时间戳关联 
- 解决`读-写冲突`的**无锁并发控制** 
- 解决脏读，幻读，不可重复读等事务隔离问题

Mysql中MVCC依赖记录中的 **`3个隐式字段`**，**`undo日志`** ，**`Read View`** 来实现的。 

隐式字段：

- DB_TRX_ID。最近修改(修改/插入)事务ID
- DB_ROLL_PTR。回滚指针，指向这条记录的上一个版本（存储于回滚段里的undo log）
- DB_ROW_ID。InnoDB会自动以DB_ROW_ID作为隐藏自增主键产生一个聚簇索引

 `undo log`实际上就是存在`rollback segment`中旧记录链 ,写入过程：

- 在事务2修改该行数据时，数据库也先为该行加锁
- 然后把该行数据拷贝到undo log中，作为旧记录，发现该行记录已经有undo log了，那么最新的旧数据作为链表的表头，插在该行记录的undo log最前面
- 修改该行最新数据，并且修改隐藏字段的事务ID为当前事务2的ID，回滚指针指向刚刚拷贝到undo log的副本记录
- 事务提交，释放锁

Read View： 在该事务执行的快照读的那一刻，会生成数据库系统事务执行状态的一个快照。可以用来判断事务的可见性。 



## 事务隔离级别

- 为了解决事务隔离问题
- 事务隔离级别越高，在并发下会产生的问题就越少，但同时付出的性能消耗也将越大

### 可重复读



可重复读是MySQL默认的隔离级别，理论上说应该称作快照（Snapshot）隔离级别。读不加锁，只有写才加锁，读写互不阻塞，并发度相对于可串行化级别要高，但会有Write Skew异常。

事务在开始时创建一个ReadView，当读一条记录时，会遍历版本链表，通过当前事务的ReadView判断可见性，找到第一个对当前事务可见的版本，读这个版本。

对于写操作，包括Locking Read(SELECT ... FOR UPDATE), UPDATE, DELETE，需要加写锁。根据谓词条件上索引使用情形，锁定有不同的方式：

1）有索引：
对于索引上有唯一约束且为等值条件的情形，只锁定索引记录（行锁）。对于其它情形，使用GAP LOCK，相当于谓词锁。
2）没有索引：
由于MySQL没有实现通用的谓词锁，这时就相当于锁全表。

mysql的可重复读并没有完全解决幻读问题。比如当前事务的更新操作可能会更改其他事务提交新增的记录，记录版本号会改为当前事务，后面再查询就能查到那条其他事务新增的记录了。

```mysql
mysql> select * from test ;
+------+----+
| pin  | id |
+------+----+
| xxx1 |  1 |
| xxx1 |  2 |
| xxx1 |  3 |
| xxx1 |  4 |
| xxx2 |  7 |
+------+----+
5 rows in set (0.00 sec)

mysql> update test set pin='xxx';
Query OK, 6 rows affected (0.00 sec)
Rows matched: 6  Changed: 6  Warnings: 0

mysql> select * from test ;
+------+----+
| pin  | id |
+------+----+
| xxx  |  1 |
| xxx  |  2 |
| xxx  |  3 |
| xxx  |  4 |
| xxx  |  7 |
| xxx  |  8 |
+------+----+
6 rows in set (0.00 sec)
```



### 读提交

一个事务从开始到提交之前，所做的任何修改对其他事务都是不可见的。但问题是，如果提交了，其他正在进行的事务会看到，因此可能造成 不可重复读。

MySQL的读已提交实际是语句级别快照。

与可重复读级别主要有两点不同：
1）获得ReadView的时机。每个语句开始执行时，获得ReadView，可见性判断是基于语句级别的ReadView。读的策略与可重复读类似，会查找版本链。

2）写锁的使用方式。这里不需要GAP LOCK，只使用记录锁。并且事务只持有被UPDATE/DELETE记录的写锁（可重复读需要保留全部写锁直到事务结束，而读已提交只保留真正更改的）。

### 读未提交

Read Uncommitted
读最新的数据，不管这条记录是不是已提交。不会遍历版本链，少了查找可见的版本的步骤。这样可能会导致脏读。对写仍需要锁定，策略和读已提交类似，避免脏写。

##  外部一致性

https://www.zhihu.com/question/56073588

 在分布式数据库里，当 A、B 两个事务发生在不同的机器上时，保证先后关系

实现外部一致性的方式：

1.  Google的Spanner数据库使用GPS系统在全球的多个机房之间保持时间同步，并使用原子钟确保本地系统时钟的误差一直维持在很小的范围内
2.  OceanBase数据库是利用一个集中式服务来提供全局一致的版本号。保持硬件通用 

# innodb特性

事务 稳定且经过验证
支持热备份
崩溃恢复块、损坏概率小

# 备份

```
mysqldump
create table t2 select * from t1
```

# 基准测试

http_load通过自定义urls.txt循环测试多个url
sysbench可以进行cpu测试、fileio测试、OLTP基准测试
各测试有价值的信息：
cpu测试        总时间
fileio测试        每秒请求数Requests/sec 吞吐量MB/sec，时间分布（执行时间/总时间）
OLTP基准测试        总的事务数、每秒事务数transactions（xxx per sec.)
时间统计信息per-request statistics（min最小、avg平均、max最大响应时间、95%百分比响应时间approx. 95 percentile）
线程公平性统计信息thread-fairness：用于模拟负载的公平性

TPC-C 模拟真实压力

# 性能剖析

两个步骤：

1. 测量多个（子）任务所花费的时间
2. 对结果进行统计和排序，重要的任务排在前面

Percona Server是MySQL的一个衍生版本
MySQL慢查询日志记录和分析工具
Percona Toolkit中的pt-query-digest
MySQL性能剖析命令
```
set profiling = 1；
show profiles
show profile for query 1；//query_ID
```
会话中所有查询的计数器信息
```
flush status
show status where
```

按照需要格式化输出profile
```
select state，sum（Duration） as Total_R
from information_schema.profiling
where query_id=9
group by state
order total_R desc;
 
show global status也会在show status中出现
```

# schema与数据类型优化

***
更小更好
简单就好 整型优于字符串，操作代价低
尽量避免NULL 可为NULL的列上建索引时，每个索引记录需要额外1个字节

## 日期类型

TIMESTAMP DATETIME都可以存储时间和日期，
但TIMESTAMP只使用DATETIME一半的空间
TIMESTAMP是从格林尼治时间1970-1-1的秒数，和UNIX时间戳相同
TIMESTAMP根据时区变化和更新
TIMESTAMP允许的时间范围小的多
通常尽量使用TIMESTAMP，空间效率更高。不推荐用整数保存UNIX时间戳值
可以使用BIGINT存储微妙级的时间戳

## 整数

TINYINT 8位
BIGINT  64位
整数计算在mysql中都是64位

## 实数

integer、bool、numberic只是别名
浮点和DECIMAL
DECIMAL用于存储精确的小数，打包==>二进制字符串 每4字节存9个数字 小数点前后各4个字节，小数点1个字节
**只在精确计算才使用DECIMAL，比如存储财务数据。**但数据量较大时，考虑使用BIGINT代替。将需要存储的货币单位乘以倍数。

字符串列的字符集和排序规则很影响性能
服务器层面：
存储到char时，会截取末尾空格
存储到varchar时，末尾空格保留
varchar 1到2个字节记录字符串的长度
**适合使用varchar的情况**：
- 字符串列的最大长度比平均长度大很多
- 列的更新很少，所以碎片不是问题
- 使用UTF-8
**CHAR适合存储**
- 短字符串
- 所有值接近一个长度
- 经常变更的数据
存储引擎层面：
不同引擎存储定长和变长字符串的处理方式不同

## 二进制字符串

二进制字符串存储的是字节码，什么意思？
binary, varbinary后面补的是0，而不是空格
二进制字符串比较时根据字节的数值比较，所以对大小写敏感

mysql命令行客户端插入的字符不是utf-8编码的，插入失败。用文本编辑utf-8插入正常，为什么？
答案：经常尝试发现，dos命令窗口不能正确显示utf-8编码的文本

写入utf-8编码的表时：
binary理解：binary写入的就是(编码后的)二进制字节码，比较会根据字节码比较。所以dos窗口启动mysql命令行客户端写入的编码是gbk二进制，而sqlyog、sublime写入的是utf-8。写入的字节码也会不同。
char理解：char存储时，会根据字符串本身和字符集存储为编码后的字符串，比较的时候，会根据排序规则比较。dos窗口写入汉字的gbk二进制会失败，而写入utf-8编码的字符串则正确。char字符串时写入字符的编码和客户端以及连接的字符集都得是utf-8？

更改dos下编码为utf-8 chcp 65001

character_set_client 客户端发送的字符集
character_set_connection 服务器翻译采用的字符集

## BLOB和TEXT

BLOB采用二进制，无字符集
TEXT采用字符存储，有字符集
都只对每个列的最前max_sort_length字节排序，而不是整个字符串

## 枚举类型：

- 内部存储整数
每个值在enum列表中的位置保存为整数，在表的.frm文件中存储数字-字符串映射关系
- 排序按照内部存储的整数。
select e+0 from enum_test;
需要按字母排序时，在定义enum列表时就按照字母顺序
枚举最大缺点：字符串列表固定，需要alter table 改变

整数主键相关联更快，避免基于字符串的值关联
enum可以缩小表的大小。也可以减小主键大小==>减小非主键索引大小

比较操作时enum和set类型的值都会转换为字符串

ENUM和SET类型适合存储固定信息，如有序的状态、产品类型、性别。再额外设计一张枚举类型为主键的查找表，保存描述类型的文本
大部分情况避免枚举类型作为标识列

## BIT类型

MYSQL将BIT当做字符串类型，检索时得到的是数值对应的字符串
比如存储b'00111001',检索得到的是ascii码为57的字符串'9',
而在数字上下文中，也就是select a+0 from bit_test得到的是数字57
应该避免使用BIT类型


需要存储多个true/false数据时，可以使用Set，Set类型是以一系列打包的位的集合来表示的
也可以使用整数打包位集合：第n个项（比如权限）要设为true，就对1做左移n位

## 选择标识列

整数类型最快


大部分情况避免枚举类型作为标识列

避免字符串类型作为主键，很耗空间，慢
完全随机的字符串很使insert和select很慢

IP地址本身就是32位无符号整数，用unsigned int存储比较好
INET_ATON() INET_NTOA() 用来转换ipv4

## 设计陷阱

太多的列：通过行缓冲格式拷贝数据。从行缓冲中将编码过的列转换成行数据结构的操作代价非常高。

太多的关联，解析和优化代价高。 最好一次查询关联在12个表以内

如果枚举列表不是固定的，应该使用整数作为外键关联到查找表。因为枚举列表中每增加一个新的国家时就要做一次alter table，

## 范式和反范式

范式的优点：
数据较好的范式化时，就只有很少的重复数据，只需修改更少的数据。因此更新较快。
范式化的表较小，可以更好的放在内存里，执行操作更快。
更少需要distinct和group by

范式的缺点：
一些列在反范式设计时，如果放在一张表里本可以属于同一个索引
关联代价昂贵

反范式的优点：
全表扫描是顺序IO，避免随机IO
单独的表索引可能更有效

从父表冗余一些数据到子表：
避免完全反范式化，使单表太大
使用父表的autho_name对子表的message排序代价很高昂。但在message表中缓存author_name字段并且建好索引，就可以高效完成排序

## 缓存表和汇总表

缓存表表示从其他表比较简单获取数据（只是比较慢）的表
汇总表：保存的是聚合数据得到的表

e.g.计算过去24小时消息发送量
可以每个小时都进行一次简单的查询，生成一张汇总表
更准确的方法是通过汇总表累加前23个完整的小时的消息数 比如2016-6-13 15:00 到 2016-6-14 14:00，现在时间是14:07，再累加前后不完整时间内的精确消息数（通过message表查询）::
```
SELECT NOW()- INTERVAL 24 HOUR,
lasthr-INTERVAL 23 HOUR,
lasthr-INTERVAL 1 HOUR,
lasthr
FROM
(SELECT CONCAT(LEFT(NOW(),14),'00:00') AS lasthr)X
```
物化视图方便刷新和更新视图，增量更新效率更高
Flexviews实现物化视图

计数器表单独存储比较好
将计数器保存在表的多行，会获得更高的并发。聚合获得统计结果
```
insert into counter(day, slot, cnt)
values (current_date, rand()*100, 1)
on duplicate key update cnt = cnt + 1;
如果主键重复则更新，否则插入新行
```

## alter table

以下技巧慎用，仅在特殊场景使用！
新结构创建新表，锁表，复制数据插入，删除旧表
几个小时 数天

modify column 将导致表重建
方法一：
而alter table会直接修改.frm文件而不涉及表数据，操作很快
```
alter table t1
alter column col1 set default 5;
```
方法二：
直接修改.frm文件
1. 创建相同结构的新表，改结构
2. FLUSH TABLES WITH READ LOCK。关闭所有在使用的表，并禁止被打开
3. 交换.frm。简单通过mv命令改名交换
4. 执行UNLOCK TABLES释放第2步的读锁

高效载入数据到innodb：
1. 删除所有唯一索引
2. 增加新的行
3. 重建删除掉的索引
也可以使用alter table的骇客方法加速这个操作，但一定要备份数据。

# 分页

利用延迟关联或者子查询优化超多分页场景。

说明：MySQL 并不是跳过 offset 行，而是取 (offset+N)行，然后返回放弃前 offset 行，返回 N 行，那当offset 特别大的时候，效率就非常的低下，要么控制返回的总页数，要么对超过特定阈值的页数进行 SQL改写。
解决方案：先快速定位需要获取的 id 段，然后再关联：

```sql
SELECT a.* FROM 表 1 a, (select id from 表 1 where 条件 LIMIT 100000,20 ) b where a.id=b.id
```

#  SQL 性能优化的目标

一个 SQL 执行的很慢，我们要分两种情况讨论：

1、大多数情况下很正常，偶尔很慢，则有如下原因

(1)、数据库在刷新脏页，例如 redo log 写满了需要同步到磁盘。

(2)、执行的时候，遇到锁，如表锁、行锁。

2、这条 SQL 语句一直执行的很慢，则有如下原因。

(1)、没有用上索引：例如该字段没有索引；由于对字段进行运算、函数操作导致无法用索引。

(2)、数据库选错了索引。数据库通过采样预测区分度，区分度越大索引查询越有优势。由于统计的失误，可能导致系统没有走索引，而是走了全表扫描



：至少要达到 range 级别，要求是 ref 级别，如果可以是
consts 最好。
说明：
1） consts 单表中最多只有一个匹配行（主键或者唯一索引），在优化阶段即可读取到数据。
2） ref 指的是使用普通的索引（normal index）。
3） range 对索引进行范围检索。
反例：explain 表的结果，type=index，索引物理文件全扫描，速度非常慢，这个 index 级别比较 range
还低，与全表扫描是小巫见大巫。

# 索引

## 添加索引

```mysql
show index from buy_log #l查看表索引
ALTER TABLE `th_content` DROP INDEX `idx_audit_status`;
ALTER TABLE `th_content` ADD INDEX `idx_status_audit` (`status`, `audit_time`);
```



## B+Tree

扇区是磁盘的最小存储单元
块是文件系统的最小存储单元,比如你保存一个记事本，即使只输入一个字符，也要占用4KB的存储，这就是最小存储的意思。
页是B+树的最小存储单元

索引只是找到数据存放的页，内存加载页后，再找到查找的数据。

B+Tree索引

- 存储引擎从索引的根节点开始搜索
- 根节点存放指向子节点的指针，向下层查找
- 比较节点页的值和要查找的值，找到合适的指针进入下层子节点
- 叶子页也有指针指向下一个叶子页



## 聚簇索引

聚簇索引是存储数据的结构，而不是一种单独的索引类型。

Innodb的数据文件本身按B+树组织存储：

- 叶节点保存键值和数据。数据只是逻辑连续。数据页实际也按照主键顺序排列，但页也是用双向链表维护，也可以不按主键顺序。

- 非叶节点保存键值和指向数据页的偏移量。

优点：

- 减少磁盘IO
- 对于主键的范围查找、排序查找非常快

缺点：插入速度依赖插入顺序。按主键顺序插入速度快。不按顺序插入，optimize table

全表扫描=扫描聚集索引

对应InnoDB 来说如果表没有定义主键，会选择一个唯一的非空索引代替。如果没有这样的索引InnoDB 会隐式定义一个主键来作为聚簇索引。InnoDB 只聚集在同一页面中的记录。

## 辅助索引

指向对主键的引用。

辅助索引也是B+树存储，叶子节点保存的是索引—主键值，而不是索引——行指针。

（primary key1，primary key2，... , key1, key2)

根据辅助索引查找时，则需要先取出主键的值，再走一遍主索引，也就是要需要查找两个B+树。

好处：

- 非聚簇索引的节点不存储行记录，占用空间远小于聚簇索引，因此可以减少IO操作
- InnoDB移动行时无需更新辅助索引中的“指针”** 



## 覆盖索引

也就是从非聚簇索引中就能得到查询的数据，不需要查询聚簇索引。

Explain显示Using index，表示查询的列都在索引的字段中

有两种情况： 

- 主键索引
- 辅助索引保存了行的主键值，也可以做覆盖索引

联合索引一般虽然不能用于只根据b查询，但统计操作可以利用它来做覆盖索引。

## 表扫描

查询整行信息：

- 如果数据较多会优先选择主键作索引，也就是表扫描（table scan）。
- 数据较少可能选择辅助索引，先找到各个数据的主键值，再到聚集索引中分别找到行记录（离散读）。

## index hint

某sql语句可选择的索引很多，index hint可以用于减少优化器的开销，直接指定使用哪种索引。

select * from t Force index(a) where...

## Multi-Range Read

## 唯一索引

业务上具有唯一特性的字段，必须建成唯一索引。原因：

- 唯一索引对插入速度的损耗可以忽略，可以明显提高查找速度

- 即使在应用层做了非常完善的校验控制，只要没有唯一索引，根据墨菲定律，必然有脏数据产生。

## 前缀索引

对varchar可以建立前缀索引，但要保证足够长的前缀满足较高的索引选择性（区分度）。

区分度：不重复的索引值/数据表的记录总数。唯一索引的区分度为1。可以使用 count(distinct left(列名, 索引长度))/count(*)的区分度来确定。

前缀索引的缺点：

- 不能使用它做覆盖扫描、order by、group by

常见应用场景：针对很长的十六进制ID使用8位前缀索引

## 多列索引

多列索引B+树，以索引(a,b)举例：

- 节点也是按键值顺序存放，只是值包含多个键值。（1,2）
- 叶子节点数据如：(1,1)(1,2)(2,1)  -> (2,4)(3,1)(3,2)
- where b=xxx 不能使用这棵B+树索引，因为叶子节点上b的值不是排序的



**有索引a和(a,b)，会 优先用(a,b)，因为一个页能存放的记录更多**

select * from t where a=1 order by b desc

不需要额外的排序操作，因为多列索引(a,b)的B+树已经对b排好序了。

如果强制使用索引(a)，则还需要额外的排序操作，Extra列会显示Using where：Using filesort

思考，索引(a,b,c)

select * from t where a=1 order by c desc

应该还需要额外的排序。



需要它的情况：
多个索引做AND
多个索引做OR。index merge慢。可以关闭索引合并或ignore index
不考虑排序和分组，将选择性最高的列放在多列索引前面
例外情况：某些条件值的基数比正常值高，导致索引基本没用



匹配最左前缀索引

多列索引为INDEX name(lastname, firstname)
where (lastname...) and (firstname...) 索引才会生效，
lastname OR firstname 不会生效



### 最佳实践

- 索引中的数据顺序和查询中的排列顺序一致
- 利用覆盖索引来进行查询操作，避免回表
- 建组合索引的时候，区分度最高的在最左边。
- 关联表比较列时，相同大小、类型、字符集的字段才能更有效的使用索引
- 利用延迟关联或者子查询优化超多分页场景
- 利用延迟关联避免全表扫描，如优化like
- 索引排序需要满足一定条件

**索引顺序**

https://zhuanlan.zhihu.com/p/50521734

如果A列经常使用范围查询，B列等值查询，最好建立索引（B,A)，这样方便排序和回表。如果使用索引（A,B)，那对于覆盖索引查询A < 1000 and B = ‘ONLINE’，需要索引扫描并且扫描的行数不确定。

### 索引排序

利用索引排序的条件：

- 索引的顺序和ORDER BY完全一致
- 最左前缀（前导列可以是常量）

- 正序排序

- 查询条件中不使用范围查询

辅助索引排序

```
 例：WHERE A = 5 ORDER BY ID,考虑不同索引：
 列A的索引就相当于(A,ID)，可以使用索引排序
 索引(A,B)相当于（A,B,ID) ，只能用文件排序
```

###  延迟关联

作用： 避免全表扫描

可以修改为首先扫描辅助索引，因为辅助索引存储索引字段和主键
例1：

```
 select * from (select actor_id from actor where last_name like '%xxx%') as a, actor b
 where a.actor_id = b.actor_id
```

 例2,高效使用(sex,rating)索引进行排序和分页

```
select <cols> from profiles  INNER JOIN(
     select <primary key cols> from profiles
 
     where x.sex='M' ORDER BY rating LIMIT 100000,10
 
) AS x USING(<primary key cols>);
```



索引列使用like '%xxx%'时，可以使用延迟关联的方法 避免全表扫描：

```
 select * from (select actor_id from actor where last_name like '%xxx%') as a, actor b
 where a.actor_id = b.actor_id 
```

### 自定义哈希索引

对于存储很多url的表， 对完整的url字符串做索引，会非常慢
方法：删除url字段上的索引，新增一个被索引的url_crc列，会很高效。
缺陷是需要维护哈希值。可以使用触发器维护。

```
select id  from url
where url= "http:xxx"
and url_crc=CRC32("http:xxx");
```

为了处理哈希冲突，where子句必须包含常量值（被索引的url字段）
统计不精确的记录数，可以只使用哈希值查询即可。

### 索引合并

当单表使用了多个索引，每个索引都可能返回一个结果集，mysql会将其求交集或者并集，或者是交集和并集的组合。也就是说一次查询中可以使用多个索引。如：

```sql
SELECT * FROM tbl_name
  WHERE (key1 = 10 OR key2 = 20) AND non_key = 30;
```

先丢弃`non_key=30`,因为它使用不到索引，where语句就变成了`where key10 or key2=20`,使用索引先根据索引合并并集访问算法

场景：or前使用一个索引，or后另一个索引

explain显示为：Extra：Using Union

### 不能使用索引的情况

    1. 数据类型隐式转换
   2. index_name like '%x'
   3. 查询条件中不包含 多列索引的最左部分
   4. 返回的记录占全表的比例较大，使用索引比全表扫描更慢
   5. 查询的筛选性很低
   6. or前有索引，or后没索引，那么都不被用到（因为or后没有索引肯定需要一次全表扫描，减少IO操作）
   7. 对于联合索引(A, B)，where语句中A是范围查，B等值查，那么B无法直接定位，只能在索引中遍历查找（索引扫描的方式）。

## 索引的缺点

索引会降低插入，删除和更新操作的性能。对于只收集且不经常搜索的表，可以不索引。

 

## 索引案例学习

约会网站

### 设计索引

(sex,country)作为不同组合索引的前缀，因为几乎所有查询都用到性别
非常有效的技巧：查询条件AND SEX IN('m', 'f')可以让MySQL匹配索引的最左前缀。
IN列表不能太长

IN技巧代替范围查询
将对age经常做的范围查询放在最后，因为最左前缀



### 维护索引

修复索引,消除表（聚簇索引）的碎片化


     alter table innodb_tb1 engine=innodb;

# 执行计划

## 概念

type列更准确的说法是“访问类型”



ref
索引和参考值相比较（参考值是前一个表的结果，或者常量），匹配多个行。此类索引访问只有当使用非唯一索引或唯一索引的非唯一性前缀时，才会发生。



eq_ref
索引和参考值相比较时匹配多个行。一般发生在使用主键或唯一性索引。

对索引中所有列都有等值匹配条件，索引是唯一索引。
如果索引不是unique，则type为ref



const,system
对查询的某部分优化为一个常量。比如，where t1.primary_key=xxx,这样就高效的将t1从连接执行中移除。

## Extra

### Using where Using index

查询的列被索引覆盖，但无法直接通过索引查找查询到符合条件的数据

where条件的两种情况：

- where筛选条件是索引列之一但是不是索引的不是前导列
- where筛选条件是索引列前导列的一个范围

### NULL

优化阶段分解查询语句，执行阶段不需要访问表。

比如select 常量，select 索引列的最小值（单独查找索引来完成，不需要在执行时访问表）



### Using where

查询的列未被索引覆盖，通过索引扫描或者表扫描的方式使用where条件过滤记录

where筛选条件包含非索引的前导列或非索引列



### Using index

表示使用了覆盖索引。索引中使用where来过滤不匹配的记录。在存储引擎层完成。



# 查询优化

## count

 count(1)和count(*)都会对全表进行扫描，统计所有记录的条数，包括那些为null的记录，因此，它们的效率可以说是相差无几。而count(字段)则与前两者不同，它会统计该字段不为null的记录条数。 

1）在表没有主键时，count(1)比count(*)快；

2）有主键时，主键作为计算条件，count(主键)效率最高；

3）若表格只有一个字段，则count(*)效率较高。

## 优化关联查询

1. 只需要在关联顺序的第二个表的相应列上建索引
   如表A和B用列col关联时，如果优化器的关联顺序是B、A，那么不需要在B的col上建索引
2. group by和order by只用到一个表的列，这样才能使用索引

## 子查询

mysql5.6不需要用关联代替

## group by和distinct

效率低下

```
 SELECT actor.`first_name`,actor.`last_name`,COUNT(*)
 FROM film_actor
 INNER JOIN actor USING(actor_id)
 GROUP BY actor.`first_name`,actor.`last_name`
```

 

使用标识列（主键或唯一索引）分组的效率更高
利用演员姓名和ID直接相关的特点：

```
 SELECT actor.`first_name`,actor.`last_name`,COUNT(*)
 FROM film_actor
 INNER JOIN actor USING(actor_id)
 GROUP BY actor.`actor_id`
```

## limit

limit 50,5 会扫描不需要的50行让后丢弃！

解决办法：

```
1.  可以使用延迟关联优化 P242
2.  也可以转换为已知范围查询
3. 从上次取数据的位置开始扫描，然后limit 5。前提是主键单调增长
```

##  联合索引




# 索引规范

https://mp.weixin.qq.com/s?__biz=Mzg2OTA0Njk0OA==&mid=2247485117&idx=1&sn=92361755b7c3de488b415ec4c5f46d73&chksm=cea24976f9d5c060babe50c3747616cce63df5d50947903a262704988143c2eeb4069ae45420&token=79317275&lang=zh_CN#rd

- 建议单张表索引不超过 5 个，减少生成执行计划的时间
- 禁止给表中的每一列都建立单独的索引，用联合索引代替

**主键**

每个 Innodb 表必须有个主键，不要使用更新频繁的列作为主键

不使用多列主键（相当于联合索引）。

建议使用自增 ID 值，保证数据的顺序增长



**常见索引列建议**

- 出现在 SELECT、UPDATE、DELETE 语句的 WHERE 从句中的列
- 包含在 ORDER BY、GROUP BY、DISTINCT 中的字段
- 并不要将符合 1 和 2 中的字段的列都建立一个索引， 通常将 1、2 中的字段建立联合索引效果更好
- 多表 join 的关联列

**选择索引列**

建立索引的目的是：希望通过索引进行数据查找，减少随机 IO，增加查询性能 ，索引能过滤出越少的数据，则从磁盘中读入的数据也就越少。

- 区分度最高的放在联合索引的最左侧（区分度=列中不同值的数量/列的总行数）
- 尽量把字段长度小的列放在联合索引的最左侧（因为字段长度越小，一页能存储的数据量越大，IO 性能也就越好）
- 使用最频繁的列放到联合索引的左侧（这样可以比较少的建立一些索引）



删除长期未使用的索引，不用的索引的存在会造成不必要的性能损耗 MySQL 5.7 可以通过查询 sys 库的 chema_unused_indexes 视图来查询哪些索引从未被使用

# 大表优化

当MySQL单表记录数过大时，数据库的CRUD性能会明显下降，一些常见的优化措施如下：

## 限定数据的范围

务必禁止不带任何限制数据范围条件的查询语句。比如：我们当用户在查询订单历史的时候，我们可以控制在一个月的范围内；

## 读/写分离

经典的数据库拆分方案，主库负责写，从库负责读；

## 垂直分区

**根据数据库里面数据表的相关性进行拆分。** 例如，用户表中既有用户的登录信息又有用户的基本信息，可以将用户表拆分成两个单独的表，甚至放到单独的库做分库。

**简单来说垂直拆分是指数据表列的拆分，把一张列比较多的表拆分为多张表。** 如下图所示，这样来说大家应该就更容易理解了。 

- **垂直拆分的优点：** 可以使得列数据变小，在查询时减少读取的Block数，减少I/O次数。此外，垂直分区可以简化表的结构，易于维护。
- **垂直拆分的缺点：** 主键会出现冗余，需要管理冗余列，并会引起Join操作，可以通过在应用层进行Join来解决。此外，垂直分区会让事务变得更加复杂；



## 水平分区

**保持数据表结构不变，通过某种策略存储数据分片。这样每一片数据分散到不同的表或者库中，达到了分布式的目的。 水平拆分可以支撑非常大的数据量。**

水平拆分是指数据表行的拆分，表的行数超过200万行时，就会变慢，这时可以把一张的表的数据拆成多张表来存放。举个例子：我们可以将用户信息表拆分成多个用户信息表，这样就可以避免单一表数据量过大对性能造成影响。水平拆分可以支持非常大的数据量。需要注意的一点是：分表仅仅是解决了单一表数据过大的问题，但由于表的数据还是在同一台机器上，其实对于提升MySQL并发能力没有什么意义，所以 **水平拆分最好分库** 。

水平拆分能够 **支持非常大的数据量存储，应用端改造也少**，但 **分片事务难以解决**  ，跨节点Join性能较差，逻辑复杂。《Java工程师修炼之道》的作者推荐 **尽量不要对数据进行分片，因为拆分会带来逻辑、部署、运维的各种复杂度** ，一般的数据表在优化得当的情况下支撑千万以下的数据量是没有太大问题的。如果实在要分片，尽量选择客户端分片架构，这样可以减少一次和中间件的网络I/O。

**下面补充一下数据库分片的两种常见方案：**

- **客户端代理：**  **分片逻辑在应用端，封装在jar包中，通过修改或者封装JDBC层来实现。** 当当网的 **Sharding-JDBC** 、阿里的TDDL是两种比较常用的实现。
- **中间件代理：** **在应用和数据中间加了一个代理层。分片逻辑统一维护在中间件服务中。** 我们现在谈的 **Mycat** 、360的Atlas、网易的DDB等等都是这种架构的实现。

# 数据库设计规范

## UTF8

UTF8兼容性更好，统一字符集可以避免由于字符集转换产生的乱码，不同的字符集进行比较前需要进行转换会造成索引失效，如果数据库中有存储 emoji 表情的需要，字符集需要采用 utf8mb4 字符集。

## 注释

所有表和字段都需要添加注释

使用 comment 从句添加表和列的备注，从一开始就进行数据字典的维护

## 控制单表数据量

尽量控制单表数据量的大小,建议控制在 500 万以内。

500 万并不是 MySQL 数据库的限制，过大会造成修改表结构，备份，恢复都会有很大的问题。

可以用历史数据归档（应用于日志数据），分库分表（应用于业务数据）等手段来控制数据量大小

## 减小表宽

尽量做到冷热数据分离,减小表的宽度

> MySQL 限制每个表最多存储 4096 列，并且每一行数据的大小不能超过 65535 字节。

减少磁盘 IO,保证热数据的内存缓存命中率（表越宽，把表装载进内存缓冲池时所占用的内存也就越大,也会消耗更多的 IO）；

更有效的利用缓存，避免读入无用的冷数据；

经常一起使用的列放到一个表中（避免更多的关联操作）。

## 不存大文件

禁止在数据库中存储图片,文件等大的二进制数据

通常文件很大，会短时间内造成数据量快速增长，数据库进行数据库读取时，通常会进行大量的随机 IO 操作，文件很大时，IO 操作很耗时。

通常存储于文件服务器，数据库只存储文件地址信息

## 其他

- 禁止在表中建立预留字段。无法见名识义，无法选择合适的类型，并且修改它会锁定表
- 禁止在线上做数据库压力测试
- 禁止从开发环境,测试环境直接连接生成环境数据库

# 字段设计规范

## 最小数据类型

优先选择符合存储需要的最小的数据类型

列的字段越大，建立索引时所需要的空间也就越大，这样一页中所能存储的索引节点的数量也就越少也越少，在遍历时所需要的 IO 次数也就越多，索引的性能也就越差。

方法：

- 将字符串转换成数字类型存储,如:将 IP 地址转换成整形数据

- 对于非负型的数据 (如自增 ID,整型 IP) 来说,要优先使用无符号整型来存储

## NOT NULL

尽可能把所有列定义为 NOT NULL

原因：

索引 NULL 列需要额外的空间来保存，所以要占用更多的空间，可能会导致引擎放弃使用索引而进行全表扫描

进行比较和计算时要对 NULL 值做特别的处理

## 存储时间

使用 TIMESTAMP(4 个字节) 或 DATETIME 类型 (8 个字节) 存储时间

TIMESTAMP 存储的时间范围 1970-01-01 00:00:01 ~ 2038-01-19-03:14:07

TIMESTAMP 占用 4 字节和 INT 相同，但比 INT 可读性高

超出 TIMESTAMP 取值范围的使用 DATETIME 类型存储

经常会有人用字符串存储日期型的数据（不正确的做法）

•缺点 1：无法用日期函数进行计算和比较•缺点 2：用字符串存储日期要占用更多的空间

## decimal保存金额

同财务相关的金额类数据必须使用 decimal 类型

•非精准浮点：float,double•精准浮点：decimal

Decimal 类型为精准浮点数，在计算时不会丢失精度

占用空间由定义的宽度决定，每 4 个字节可以存储 9 位数字，并且小数点要占用一个字节

可用于存储比 bigint 更大的整型数据

#高级特性

##查询缓存
若查询中包含一个不确定的函数，则mysql在查询缓存中找不到缓存结果


最好计算好日期，再查询


查看查询缓存配置


     show variables like "%qcache%"

 





















查看查询缓存状态


     SHOW STATUS LIKE "Qcache%"

 





















## 一级缓存
1st Level Cache

 

Caching the object's state for the duration of a transaction or request is normally not an issue. This is normally called a 1st level cache, or the EntityManager cache, and is required by JPA for proper transaction semantics. If you read the same object twice, you must get the identical object, with the same in-memory changes. The only issues occur with querying and DML.

 

For queries that access the database, the query may not reflect the un-written state of the objects. For example you have persisted a new object, but JPA has not yet inserted this object in the database as it generally only writes to the database on the commit of the transaction. So your query will not return this new object, as it is querying the database, not the 1st level cache. This is normally solved in JPA by the user first calling flush(), or the flushMode automatically triggering a flush. The default flushMode on an EntityManager or Query is to trigger a flush, but this can be disabled if a write to the database before every query is not desired (normally it isn't, as it can be expensive and lead to poor concurrency). Some JPA providers also support conforming the database query results with the object changes in memory, which can be used to get consistent data without triggering a flush. This can work for simple queries, but for complex queries this typically gets very complex to impossible. Applications normally query data at the start of a request before they start making changes, or don't query for objects they have already found, so this is normally not an issue.

 

If you bypass JPA and execute DML directly on the database, either through native SQL queries, JDBC, or JPQL UPDATE or DELETE queries, then the database can be out of synch with the 1st level cache. If you had accessed objects before executing the DML, they will have the old state and not include the changes. Depending on what you are doing this may be ok, otherwise you may want to refresh the affected objects from the database.

 

The 1st level, or EntityManager cache can also span transaction boundaries in JPA. A JTA managed EntityManager will only exist for the duration of the JTA transaction in JEE. Typically the JEE server will inject the application with a proxy to an EntityManager, and after each JTA transaction a new EntityManager will be created automatically or the EntityManager will be cleared, clearing the 1st level cache. In an application managed EntityManager, the 1st level cache will exist for the duration of the EntityManager. This can lead to stale data, or even memory leaks and poor performance if the EntityManager is held too long. This is why it is generally a good idea to create a new EntityManager per request, or per transaction. The 1st level cache can also be cleared using the EntityManager.clear() method, or an object can be refreshed using the EntityManager.refresh() method.

 

重点：jpql、sql等方式更新数据库之后，select到的entity仍然会从1级缓存中取旧的数据，1级缓存和数据库不同步了。必须用flush，refresh更新缓存。


## 二级缓存
@QueryHints可以配置多个选项：

@QueryHints({@QueryHint(name="javax.persistence.cache.retrieveMode",value="BYPASS")})


javax.persistence.cache.retrieveMode  : CacheRetrieveMode
BYPASS  : Ignore the cache, and build the object directly from the database result.
USE  : Allow the query to use the cache. If the object/data is already in the cache, the cached object/data will be used.

javax.persistence.cache.storeMode  : CacheStoreMode
BYPASS  : Do not cache the database results.
REFRESH  : If the object/data is already in the cache, then refresh/replace it with the database results.
USE  : Cache the objects/data returned from the query.


来源：  https://en.wikibooks.org/wiki/Java_Persistence/Caching#JPA_2.0_Cache_API

 

# Emoji存储

mysql的utf8编码的一个字符最多3个字节，但是一个emoji表情为4个字节，所以utf8不支持存储emoji表情。但是utf8的超集utf8mb4一个字符最多能有4字节，所以能支持emoji表情的存储。

# SSL配置

查看server配置

```sql
show global variables like '%ssl%';
```

# 分布式关系数据库

## 访问代理Cobar

负责解析拆分sql，路由合并结果。

利用MySQL数据同步功能做数据迁移，以schema。使用一致性hash算法路由到不同节点，可以

1. Cobar集群初始化时，一开始集群规划未来的规模为1000台，那么一共建1000个shema。hash的除数为1000. Cobar将数据路由到mysql集群的各个schema，而cobar会保存哪个mysql服务器保存哪些schema。
2. 加入新的mysql数据库服务器后，cobar同步其他服务器的schema到新服务器上。
3. cobar服务器更改路由信息，路由数据到新的schema上。
4. 删除原来的schema。



# JDBC

## url

 时区问题,在 JDBC 的连接 url 部分加上 serverTimezone=UTC 即可 

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/stock_db?serverTimezone=UTC&useUnicode=true&characterEncoding=utf-8&allowMultiQueries=true
```

# 查询缓存

> 执行查询语句的时候，会先查询缓存。不过，MySQL 8.0 版本后移除，因为这个功能不太实用

开启查询缓存后在同样的查询条件以及数据情况下，会直接在缓存中返回结果.

缓存虽然能够提升数据库的查询性能，但是缓存同时也带来了额外的开销，每次查询后都要做一次缓存操作，失效后还要销毁。 因此，开启缓存查询要谨慎，尤其对于写密集的应用来说更是如此。