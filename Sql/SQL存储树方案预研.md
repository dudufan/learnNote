问题：
1. 用户数增加，mysql分表吗？和查询效率，锁是什么关系？
2. 网盘有哪些操作需要事务保证？单个终端不需要事务
3. 网盘可能很频繁的操作：
查询（列出）目录下的文件夹或文件
上传文件
创建文件夹
删除文件或文件夹
4. 删除、移动目录时，如果单个节点数据移动失败，之前不做回滚，那么mysql的事务怎么用？


结论：递归查询（oracle）、路径枚举或闭包可能比较适合网盘


#邻接表
查找父亲节点，O(1)
查找祖先
查找子节点，O(1)
移动单个节点，O(1)。修改parent即可
查找叶子节点,O(1)。一个自联结
由根节点查找所有子节点或子树，需要递归查找。若知道树的深度，可以使用自联结
更新节点，需要更新它所有子节点的parent。


##数据库实现方式：
SQL99支持With关键字进行递归查询

oracle：connect by prior

> Oracle中start with...connect by prior子句用法 connect by 是结构化查询中用到的，其基本语法是：
select ... from tablename start with 条件1
connect by 条件2
where 条件3;
例：
select * from table
start with org_id = 'HBHqfWGWPy'
connect by prior org_id = parent_id;
 
> 简单说来是将一个树状结构存储在一张表里，比如一个表中存在两个字段:
org_id,parent_id那么通过表示每一条记录的parent是谁，就可以形成一个树状结构。
     用上述语法的查询可以取得这棵树的所有记录。
     其中：
     条件1 是根结点的限定语句，当然可以放宽限定条件，以取得多个根结点，实际就是多棵树。
     条件2 是连接条件，其中用PRIOR表示上一条记录，比如 CONNECT BY PRIOR org_id = parent_id就是说上一条记录的org_id 是本条记录的parent_id，即本记录的父亲是上一条记录。
     条件3 是过滤条件，用于对返回的所有记录进行过滤。
 
mysql不支持递归


##缺点
不易查询所有的子节点（子树）


   树的每一层都对应一次自联结，并且一条sql中自联结数目却必须是固定的。
   联结时通过加入更多的列来拓展深度，导致难以计算聚合，如count()


查询一个给定节点的多个祖先，代价昂贵


删除非叶节点（在网盘中是删除子树），需要多次查询从最低层级开始删除子节点，这样才能满足（外键）完整性。如果删除操作频繁，可以使用外键和ON DELETE CASCADE 来自动删除


##优点
添加新节点，指定parent参数，直接添加
移动单个节点（叶节点或者子树的根节点），修改parent即可
检索直接的父亲或孩子节点
注：现有mongo方案移动文件或文件夹，需要更新1. 被移动节点的parentId 2. parent的childList 3. 目标文件夹节点的child_list 4.移动前还需要预判断重名，可能需要修改name


##检查表避免以下错误：
a是b的父亲，b是a的父亲 ==> 避免循环
自己是自己的父亲
存在孤立点 ==> edgeNum = nodeNum -1
多个root节点 ==> only one root


#路径枚举模型


插入一个新节点，需要插入和更新path（如果使用自增主键）


优点：
查找子树（多个子节点），一条sql，使用like
删除子树（多节点），一条sql，使用like
删除单节点，还需要删除部分路径上的该节点
缺点：
应用代码需要保证路径字符串是正确有效的（路径正确并且节点都存在）
查询子树，索引需要扫描一遍
移动子树时查询子树节点很简单，但charu


检查表避免以下错误：

路径中节点重复
路径中节点数比总节点数多


#嵌套集合
优点：
适用于频繁查询子树，而不是操作个别的节点们。 适合静态的树
特点：
插入、移动操作和删除操作复杂


#闭包表模型 closure Table


删除子树
删除以下路径：ancestor是根节点6的祖先（不包括6),descendant是6及6的子孙
DELETE FROM TreePaths
WHERE descendant IN (SELECT descendant
FROM TreePaths
WHERE ancestor = 6)
AND ancestor IN (SELECT ancestor
FROM TreePaths
WHERE descendant = 6 AND ancestor != descendant);  
插入子树
子树的根节点6添加到节点3下，需要添加以下路径： ancestor是插入位置3的祖先（包括3),descendant是6及6的子孙
INSERT INTO TreePaths (ancestor, descendant)
SELECT supertree.ancestor, subtree.descendant
FROM TreePaths AS supertree
CROSS JOIN TreePaths AS subtree
WHERE supertree.descendant = 3 AND subtree.ancestor = 6;  
 

优点：
方便找到所有祖先或所有下属
允许一个节点属于多个树


另一个表表示所有的ancestor- descendant 传递关系



