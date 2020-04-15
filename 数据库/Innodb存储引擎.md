[TOC]


#问题与实践


##事务中插入或更新子表时，需要锁住父表
因为其他事务如果修改了父表，比如删除了父表的记录并提交，这样会导致当前事务插入失败。但当前事务select读取仍然是一致性读（删除父表记录之前的状态）。报出如下错误：


     ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`test`.`z_child`, CONSTRAINT `z_child_ibfk_1` FOREIGN KEY (`a_id`) REFERENCES `z` (`a`))




##缓
冲池
##insert Buffer
工作原理：
二级索引页在缓冲池中，则直接插入索引页；若不在，先放到insert Buffer中



存储位置：
缓冲池只是记录insert Buffer的信息，实际上insert Buffer在ibdata1中存储辅助索引。
insert Buffer B+树中非叶子节点保存的是(space, offset)------表空间id、页所在偏移


如何合并二级索引页：
随机取insert buffer页：
    
     innodb引擎随机选择 insert Buffer B+树的一个页，读取该页中的space及所需数量的页


顺序写入二级索引页：


     二级索引页在 insert Buffer B+树中已经排好序，可按照(space, offset)的排序顺序进行页的选择


innodb 1.2.x开始改为 change buffer 可对DML操作缓冲，insert、delete、update


##doublewrite
作用：宕机时innodb可能只写入页的一部分(partial page write),页本身发生损坏（页最后的checksum损坏）。而redo log中记录的是对页的物理操作，页损坏后redo log无法应用。 doublewrite解决由于 partial page write导致的数据丢失


组成：内存中的doublewrite、共享表空间的doublewrite。都是2M大小


应用 redo log写入数据的过程：
1. 缓冲池的脏页copy到内存的doublewrite buffer
2. 分两次顺序写入表空间的doublewrite。这个过程可以 合并多个页的写入
3. 写入redo log，通过redolog将数据写入磁盘


如果页写入磁盘过程中崩溃，恢复过程如下：
1. 从共享表空间找到该页的一个副本，复制到表空间文件
2. 应用redo log





##异步IO（AIO）
AIO应用：
预读取方式的读
脏页刷新（磁盘写入）
 


#B+树索引
##使用
OLAP:每个用户的消费情况，销售额同比，环比增长
不需要在OLAP中对姓名字段进行索引，因为很少对单个用户查询


二级索引
使用primary聚集索引，也就是表扫描。
二级索引才可能做覆盖索引！


#事务
事务提交时，先写二进制日志，再写重做日志。这个过程是在一个内部事务中完成，避免主从不一致。
重做日志默认事务提交时调用fsync，把日志从文件系统缓存刷到磁盘
二进制日志默认sync_binlog=0.  sync_binlog=1 表示事务commit之前二进制日志立即同步写入磁盘
锁定的一致性读
避免不可重复读或幻读。比如银行取款，先select查询余额，再update取款
If you query data and then insert or update related data within the same transaction, the regular SELECT statement does not give enough protection. Other transactions can update or delete the same rows you just queried. InnoDB supports two types of locking reads that offer extra safety: 


来源：  http://dev.mysql.com/doc/refman/5.5/en/innodb-locking-reads.html


丢失更新
例子，同一个10000元银行账户向外转账9000元和1元，最后竟然剩下9999元。


| T1 | T2 |

| ------------- |:-------------:|
| begin;                                      |     begin; |
|   select b into @b from z where a=3;  |            |

|                                               |   select b into @b from z where a=3;  |  
|   update z set b=@b-9000 where a=3;  |                                             |

|   commit;   |          |                                                              
|                                              |       update z set b=@b-1 where a=3;   |  
|                                                    |   commit;   |  
解决办法：
| T1 | T2 |

| ------------- |:-------------:|
|begin;|                                        begin;|
|select b into @b from z ||
|where a=3 for update；||
||                                             select b into @b from z  where a=3 for update； #等待 |
| update z set b=@b-9000 where a=3;||
|commit;||
||                                               update z set b=@b-1 where a=3;|

||                                              commit;|
添加排它锁，使事务在这种情况下串行化。


类似丢失更新的错误，会造成主键冲突


>For another example, consider an integer counter field in a table CHILD_CODES , used to assign a unique identifier to each child added to table CHILD . Do not use either consistent read or a shared mode read to read the present value of the counter, because two users of the database could see the same value for the counter, and a duplicate-key error occurs if two transactions attempt to add rows with the same identifier to the CHILD table.

Here, LOCK IN SHARE MODE is not a good solution because if two users read the counter at the same time, at least one of them ends up in deadlock when it attempts to update the counter.

To implement reading and incrementing the counter, first perform a locking read of the counter using FOR UPDATE , and then increment the counter. For example:



    SELECT counter_field FROM child_codes FOR UPDATE;
    UPDATE child_codes SET counter_field = counter_field + 1;



>A SELECT ... FOR UPDATE reads the latest available data, setting exclusive locks on each row it reads. Thus, it sets the same locks a searched SQL UPDATE would set on the rows.

 

>The preceding description is merely an example of how SELECT ... FOR UPDATE works. In MySQL, the specific task of generating a unique identifier actually can be accomplished using only a single access to the table:

 

    
UPDATE child_codes SET counter_field = LAST_INSERT_ID(counter_field + 1);

    
SELECT LAST_INSERT_ID();

 

> SELECT statement merely retrieves the identifier information (specific to the current connection). It does not access any table. 



来源： 
http://www.jianshu.com/p/sTeAbC