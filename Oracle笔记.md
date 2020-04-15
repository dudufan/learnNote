[TOC]

# 用户管理

## 以sysdba用户登录oracle
sqlplus / as sysdba;

## 修改密码

alter user xxx identified by xxpwd;

## 取消密码过期时间限制

1、进入sqlplus模式

　　sqlplus / as sysdba;

2、查看用户密码的有效期设置(一般默认的配置文件是DEFAULT)

　　SELECT * FROM dba_profiles WHERE profile='DEFAULT' AND resource_name='PASSWORD_LIFE_TIME';
3、将密码有效期由默认的180天修改成“无限制”，修改之后不需要重启动数据库，会立即生效

　　ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED ;

4、帐户再改一次密码
　　alter user 用户名 identified by 原密码;

5、使用修改后的用户登录，如果报“ORA-28000:用户已被锁”，解锁

　　alter user db_user account unlock;

　　commit;

## 查看sid

select instance_name from V$instance;





查看SID：

lsnrctl status可以看到sid。



## 查看servicename

 使用sqlplus / as sysdba登录后， show parameter service；

## 查看当前登陆用户的表

select count(1) from user_tables;

select count(table_name） from user_tables

select t.table_name,t.num_rows from user_tables t  order by t.num_rows desc;

## 查看更改oracle用户及数据库的字符集编码

查看oracle用户数据

echo $NLS_LANG

登陆oracle sysdba用户后，

```select userenv(‘language’) from dual;```

# ORACLE状态查看

## Oracle实例状态

```sql
select instance_name,host_name,startup_time,status,database_status from v$instance;
```

其中“STATUS”表示Oracle当前的实例状态，必须为“OPEN”；“DATABASE_STATUS”表示Oracle当前数据库的状态，必须为“ACTIVE”。

## Oracle表空间的状态

```sql
select tablespace_name,status from dba_tablespaces;
```

输出结果中STATUS应该都为ONLINE。

## Oracle所有数据文件状态

```sql
select name,status from v$datafile;// method 1
select file_name,status from dba_data_files; // method 2
```

输出结果中“STATUS”应该都为“ONLINE”。

## Oracle初始化文件中相关参数值

```
select resource_name,
max_utilization,
initial_allocation,
limit_value
from v$resource_limit;
```
若LIMIT_VALU-MAX_UTILIZATION<=5，则表明与RESOURCE_NAME相关的Oracle初始化参数需要调整。可以通过修改Oracle初始化参数文件$ORACLE_BASE/admin/CKDB/pfile/initORCL.ora来修改。

# 资源使用情况

### 数据库连接情况

查看当前会话连接数，是否属于正常范围。
```sql
select count(*) from v$session;
select sid,serial#,username,program,machine,status from v$session;
```
其中：SID 会话(session)的ID号；
SERIAL# 会话的序列号，和SID一起用来唯一标识一个会话；
USERNAME 建立该会话的用户名；
PROGRAM 这个会话是用什么工具连接到数据库的；
STATUS 当前这个会话的状态，ACTIVE表示会话正在执行某些任务，INACTIVE表示当前会话没有执行任何操作；

如果建立了过多的连接，会消耗数据库的资源，同时，对一些“挂死”的连接可能需要手工进行清理。如果DBA要手工断开某个会话，则执行：
（一般不建议使用这种方式去杀掉数据库的连接，这样有时候session不会断开。容易引起死连接。建议通过sid查到操作系统的spid,使用ps –ef|grep spidno的方式确认spid不是ORACLE的后台进程。使用操作系统的kill -9命令杀掉连接）
alter system kill session 'SID,SERIAL#';
注意：上例中SID为1到10(USERNAME列为空)的会话，是Oracle的后台进程，不要对这些会话进行任何操作。

### 系统磁盘空间

如果文件系统的剩余空间过小或增长较快，需对其进行确认并删除不用的文件以释放空间。
```shell
[oracle@AS14 ~]$ df -h
 
Filesystem Size Used Avail Use% Mounted on
 
/dev/sda5 9.7G 3.9G 5.4G 42% /
 
/dev/sda1 479M 16M 438M 4% /boot
 
/dev/sda2 49G 19G 28G 41% /data
 
none 1014M 0 1014M 0% /dev/shm
```

### 表空间使用情况
```sql
select f.tablespace_name,
a.total,
f.free,
round((f.free / a.total) * 100) "% Free"
from (select tablespace_name, sum(bytes / (1024 * 1024)) total
from dba_data_files
group by tablespace_name) a,
(select tablespace_name, round(sum(bytes / (1024 * 1024))) free
from dba_free_space
group by tablespace_name) f
WHERE a.tablespace_name = f.tablespace_name(+)
order by "% Free";
```
如果空闲率%Free小于10%以上（包含10%），则注意要增加数据文件来扩展表空间而不要是用数据文件的自动扩展功能。请不要对表空间增加过多的数据文件，增加数据文件的原则是每个数据文件大小为2G或者4G，自动扩展的最大限制在8G。


### 查看数据库连接(process)数

```sql
 select count(*) from v$process ;    --当前的数据库连接数
```
数据库允许的最大连接数
```sql
select value from v$parameter where name ='processes';  --数据库允许的最大连接数
```
修改数据库最大连接数
```sql
alter system set processes = 300 scope = spfile;  --修改最大连接数:
```
关闭/重启数据库
```sql
shutdown immediate; --关闭数据库
startup; --重启数据库
```



# ORACLE和MySQL区别

## USING
oracle: 如果USING(templetId), select后不能给templetId前加表名
mysql: 加不加表名都可




### column_a ca


mysql oracle都支持 as给列起别名
### as给表起别名
mysql支持as给表起别名，但oracle不支持
## select count


### distinct
distinct类似group by，仅用于去重操作。
注意：order by的字段，必须出现在select distinct后


### insert values() ,()
### 时间函数不同
### 分组group by




MySQL分组查询的时候允许查询非分组字段，所以当我们执行select * from …group by…时，每个分组只显示该分组的第一条记录。


ORACLE 分组查询的时候不允许查询非分组字段，也就是说， group by后必须列出所有select的字段。


## oracle列别名不能使用 as 'dailyLimit'


Mysql可以写成  as 'dailyLimit'


ORACLE写成as 'dailyLimit'会报错，提示from keyword not found where expected


### 大小写
MySQL:
1. 在Windows下，数据库名、表名、字段名不区分大小写。
2. 大Linux/Unix下，数据库名、表名区分大小写，字段名不区分大小写。
3. 编辑/etc/my.cnf，设置lower_case_table_names可以让MySQL是否区分表名的大小写。0：区分大小写,1：不区分大小写。


Oracle:
1、在Oracle中，如果字段名称被双引号（""）包裹，Oracle会区分大小写；
2、如果字段名称没有被双引号（""）包裹，则全部转换成大写来执行。
3、如果表结构设计时，字段名称使用了数据库的保留字，SQL中的字段名称必须用双引号（""）包裹，以避免SQL语句执行出错。不建议用数据库的保留字来做表名和字段名。


以下SQL语句在Oracle中执行时，字段 stat_time, interval 没有被双引号（""）包裹，不区分大小写： 
insert into smsc_flow(stat_time,interval,"MODULEID","SMSCNO","ICPNO","MT_OK","MT_FAIL","MT_DELAY","MO_OK","MO_FAIL","STATUS_OK","STATUS_FAIL","SUCCESS_STATUS","COUNT") values('20101010112',1,'MT001',1,1,1,1,1,1,1,1,1,1,1) 


以下SQL语句在Oracle中执行时，字段 stat_time, interval 被双引号（""）包裹，全部转换成大写执行： 
insert into smsc_flow("stat_time","interval","MODULEID","SMSCNO","ICPNO","MT_OK","MT_FAIL","MT_DELAY","MO_OK","MO_FAIL","STATUS_OK","STATUS_FAIL","SUCCESS_STATUS","count") values('20101010111','20101010111',1,'MT001',1,1,1,1,1,1,1,1,1,1,1) 


来源：  http://itindex.net/detail/50615-mysql-oracle-%E5%B0%8F%E5%86%99


### oracle中in语句后的list元素个数不能超过1000
### oracle中不支持等号比较字符串
比如：日期字段 ='年月日字符串'，会报错：
Oracle 异常 ORA-01861: literal does not match format string（字符串格式不匹配）

## oracle插入更新操作需要事务commit

## 反引号

Oracle 认为字段名两边的反引号非法。日期写入、比较必须用TODATE指定格式转换。TO_DATE('2016-12-31 23:59:59','yyyy-mm-dd hh24:mi:ss') 

# 升级脚本示例

```shell
[ -z "ORACLE_SID" ] && echo "ORACLE_SID变量未配置,退出" && exit 1
[ -z "ORACLE_BASE" ] && echo "ORACLE_BASE变量未配置,退出" && exit 1
```



# Shell脚本字符集设置

1. 以超级管理员身份登录Oracle。conn / as sysdba

2. 检查Oracle的字符集。select parameter, value from nls_database_parameters;

3. 在linux上执行这个命令：echo $NLS_LANG

   结果如果不是之前查出来的三个参数组合起来的值，设置NLS_LANG。比如export NLS_LANG=AMERICAN_AMERICA.UTF8

4. 设置LANG变量：export LANG=en_US.UTF-8

5. 再执行脚本。

# 新建用户
```shell
sqlplus /nolog<<EOF
conn / as sysdba
CREATE USER sinosunts1 IDENTIFIED BY sinosunts;
ALTER USER sinosunts1 DEFAULT TABLESPACE ts_Data TEMPORARY TABLESPACE ts_Temp;
GRANT CREATE SESSION ,CONNECT ,RESOURCE ,CREATE VIEW  to sinosunts1;
EOF
```



# 导出/导入老表

su - oracle下执行

```shell
exp sinosunts/sinosunts file=./tables/sinosunts grants=n owner=sinosunts
imp sinosunts1/sinosunts file=./tables/sinosunts.dmp fromuser=sinosunts touser=sinosunts1
```

# 升级表结构
```shell
sqlplus sinosunts1/sinosunts<<EOF
@ ./tables/ts_upgrade.sql
EOF
```

grant select, delete, update, insert on zone_service_table to mstp_dbuser;

-- 新建序列并赋权
create sequence HIBERNATE_SEQUENCE
minvalue 1
maxvalue 9999999999999999999999999999
start with 1
increment by 1
cache 20;

grant select on hibernate_sequence to mstp_dbuser;

-- 导入初始化数据
@ ./tables/cds_tag.sql
EOF

# 对mstp_dbuser用户进行一些必要的升级
sqlplus mstp_dbuser/sinosun<<EOF
drop synonym hibernate_sequence;
drop synonym cds_share_nodes;
create synonym hibernate_sequence for mstp_owner1.hibernate_sequence;
create synonym cds_share_nodes for mstp_owner1.cds_share_nodes;
EOF

# 用户改名
```shell
sqlplus /nolog<<EOF
-- 原来用户改名备份
conn / as sysdba
update user$ set name='SINOSUNTS_BAK' where name = 'SINOSUNTS';
commit;
alter system checkpoint;
alter system flush shared_pool;

update user$ set name='MSTP_OWNER_BAK' where name = 'MSTP_OWNER';
commit;
alter system checkpoint;
alter system flush shared_pool;

-- 新用户改名
update user$ set name='SINOSUNTS' where name = 'SINOSUNTS1';
commit;
alter system checkpoint;
alter system flush shared_pool;

update user$ set name='MSTP_OWNER' where name = 'MSTP_OWNER1';
commit;
alter system checkpoint;
alter system flush shared_pool;
EOF

```

# 创建链接到其他库

1. 需要有create database link权限. grant create database link to sinosunts;

2. 创建link

   ```
   create public database link dblink_name connect to SYSTEM using '192.168.1.73:1521/oracle';
   ```

3.  访问B数据库的test表，可以“表名@数据链接名”。`select * from test@db_1 t`

# Merge into

```sql
merge into 目标表 a
using 源表 b
on(a.条件字段1=b.条件字段1 and a.条件字段2=b.条件字段2 ……)  
when matched then update set a.更新字段=b.字段
when  not matched then insert into a(字段1,字段2……)values(值1,值2……)
```

示例

```sql
merge into t_yqt_corptf a USING (select b.Companyid, b.mcode from t_wdss_pubaccount b where sys_valid > 0 group by Companyid,mcode ) c 
ON(c.companyid = a.companyid and c.mcode = a.tfid)
WHEN not MATCHED THEN
  insert (a.id,a.Companyid,a.tftype,a.tfid) values (Fn_get_nextval('T_YQT_CorpTF'), c.CompanyId, 1, c.mcode); ----tftype对公 1
```



# 单表备份

create table t_yqt_croptf_bak as select * from t_yqt_croptf;

# SQL查询

## 整数

表中字段如果是整型，查询条件可以是字符串或整数

```sql
select * from T_Pub_Region where regionId = 1390;
select * from T_Pub_Region where regionId = '1390';
```

# BLOB批量插入

应用管理模板批量导入时，当模板内容字段超过4000字节时，insert select语句会把该字段转换为LONG类型，而插入BLOB字段就会报ORA-01461错误。

一种解决办法：可以在数据库分别为oracle和mysql建立相同接口的存储过程。oracle做带BLOB的批量插入时，使用begin end语法一次提交多条插入语句。mysql使用insert select union all语句。

mybatis16可以使用支持不同数据库的动态sql。