# 综述
1.DDL（Data Definition Language）数据库定义语言statements are used to define the database structure or schema.
DDL是SQL语言的四大功能之一。
用于定义数据库的三级结构，包括外模式、概念模式、内模式及其相互之间的映像，定义数据的完整性、安全控制等约束
DDL不需要commit.
CREATE
ALTER
DROP
TRUNCATE
COMMENT
RENAME
2.DML（Data Manipulation Language）数据操纵语言statements are used for managing data within schema objects.
由DBMS提供，用于让用户或程序员使用，实现对数据库中数据的操作。
DML分成交互型DML和嵌入型DML两类。
依据语言的级别，DML又可分成过程性DML和非过程性DML两种。
需要commit.
SELECT
INSERT
UPDATE
DELETE
MERGE
CALL
EXPLAIN PLAN
LOCK TABLE
3.DCL（Data Control Language）数据库控制语言  授权，角色控制等
GRANT 授权
REVOKE 取消授权
4.TCL（Transaction Control Language）事务控制语言
SAVEPOINT 设置保存点
ROLLBACK  回滚
SET TRANSACTION
SQL主要分成四部分：
（1）数据定义。（SQL DDL）用于定义SQL模式、基本表、视图和索引的创建和撤消操作。
（2）数据操纵。（SQL DML）数据操纵分成数据查询和数据更新两类。数据更新又分成插入、删除、和修改三种操作。
（3）数据控制。包括对基本表和视图的授权，完整性规则的描述，事务控制等内容。
（4）嵌入式SQL的使用规定。涉及到SQL语句嵌入在宿主语言程序中使用的规则。

# 基本语法

使用 ISNULL() 来判断是否为 NULL 值



当某一列的值全是 NULL 时，count(col)的返回结果为 0，但 sum(col)的返回结果
为 NULL，因此使用 sum()时需注意 NPE 问题



分页查询逻辑时，若 count 为 0 应直接返回，避免执行后面的分页语句

不得使用外键与级联，一切外键概念必须在应用层解决

禁止使用存储过程，存储过程难以调试和扩展，更没有移植性。



数据订正（特别是删除、修改记录操作）时，要先 select ，避免出现误删除，确认无
误才能执行更新语句。

in 操作能避免则避免，若实在避免不了，需要仔细评估 in 后边的集合元素数量，控
制在 1000 个之内。

TRUNCATE TABLE 比 DELETE 速度快，且使用的系统和事务日志资源少，但
TRUNCATE 无事务且不触发 trigger ，有可能造成事故，故不建议在开发代码中使用此语句。

# 多表操作

比较匹配

```sql
where not exist（select null from ... where 匹配语句） 相关子查询
    SELECT film.film_id
     FROM sakila.film
     WHERE NOT EXISTS (SELECT NULL FROM film_actor
     WHERE film.film_id=film_actor.film_id)
where in （select ... from ...)     非相关子查询
    SELECT *
    FROM dept
    WHERE  deptno NOT IN （select deptno from new_dept)
left join ... where ... is null     外 连接 （反连接）
```

注意：

- true OR NULL 结果是true
- deptno=NULL 结果是NULL
-   false OR NULL 结果是NULL而不是false！
-   not NULL 还是NULL
因此，
```
where deptno not in(10,20,NULL) 假定deptno为30，预想结果为where真
执行过程为 
where not (deptno=10 OR deptno=20 OR deptno=NULL)
where not (false OR flase OR NULL)
where not NULL
where NULL
匹配出错！
```
# 更新数据
根据B表中数据（某些字段）更新A表中（满足条件）的记录------使用多个相关子查询
```
update a
set a.col2=(select ... where b.col1=a.col1),
a.col3= (select ... where b.col1=a.col1)
where exists( select null ... where b.col1=a.col1 )
```
# 元数据
mysql中是show指令、information_schema数据库
# 字符串
# 遍历字符串需要使用基干表
## 遍历逐个字符
```
SELECT ename, SUBSTR(ename, iter.pos, 1) AS c
FROM emp,
(SELECT id pos FROM t10) iter
WHERE iter.pos <=LENGTH(ename)
遍历结果
ename   pos  c  
SMITH   1    S  
SMITH   2    M  
SMITH   3    I  
SMITH   4    T  
SMITH   5    H  
ALLEN   1    A  
ALLEN   2    L  
ALLEN   3    L  
ALLEN   4    E  
ALLEN   5    N  
WARD    1    W  
WARD    2    A  
WARD    3    R  
WARD    4    D  
```
## 遍历逐个子串
```
SELECT v.`name`, iter.pos, SUBSTRING_INDEX(SUBSTRING_INDEX(v.`name`, '.', iter.pos),'.',-1) AS sub
FROM v, (SELECT id pos FROM t10) iter
WHERE  iter.pos<=LENGTH(v.`name`)-LENGTH(REPLACE(v.`name`,'.',''))+1
结果：
name                               pos sub
tina.gina.jaunita.regina.leena 5 leena
tina.gina.jaunita.regina.leena 4 regina
tina.gina.jaunita.regina.leena 3 jaunita
tina.gina.jaunita.regina.leena 2 gina
tina.gina.jaunita.regina.leena 1 tina
mo.larry.curly                     1   mo
mo.larry.curly                     2 larry
mo.larry.curly                     3 curly
```
## 遍历项的数目
对于字符串有两种。
遍历逐个字符，很简单，iter.pos <= LENGTH(ename)
遍历子串，需要计算分隔符数量再加1            iter.pos<=LENGTH(v.`name`)-LENGTH(REPLACE(v.`name`,'.',''))+1
# 使用遍历得到的内联视图
## 聚合函数
比如group_concat。需要使用group by
```
SELECT ename, GROUP_CONCAT(c ORDER BY c SEPARATOR '')
FROM(
SELECT ename, SUBSTR(ename, iter.pos, 1) AS c
FROM emp,
(SELECT id pos FROM t10) iter
WHERE iter.pos <=LENGTH(ename)
)v
GROUP BY ename
```
## 根据条件选择遍历的其中一项或多项。例如
```
SELECT sub
FROM(
SELECT v.`name`, iter.pos, SUBSTRING_INDEX(SUBSTRING_INDEX(v.`name`, '.', iter.pos),'.',-1) AS sub
FROM v, (SELECT id pos FROM t10) iter
WHERE  iter.pos<=LENGTH(v.`name`)-LENGTH(REPLACE(v.`name`,'.',''))+1
)X
WHERE pos=2
```
使用数字

聚集函数要注意对NULL值的处理，如count（col） count(*)
统计行数
count(*)会统计值为 NULL 的行。用来统计行数
 count(列名)不会统计此列为 NULL 值的行

# 统计

## 计算累计和

使用标量子查询计算累计和。一定要按取值唯一的列联接，此例中使用 d.ename<=e. ename联接也可以
```
SELECT e.ename, e.sal, (
SELECT SUM(sal)
FROM emp d
WHERE d.empno<=e.empno) AS running_total
FROM emp e
ORDER BY 3
```
```
ename   sal   running_total  
SMITH   800   800            
ALLEN   1600  2400           
WARD    1250  3650           
JONES   2975  6625           
MARTIN  1250  7875           
BLAKE   2850  10725          
CLARK   2450  13175          
SCOTT   3000  16175          
KING    5000  21175          
TURNER  1500  22675          
ADAMS   1100  23775          
JAMES   950   24725          
FORD    3000  27725          
MILLER  1300  29025          
```
## 计算累积
求部分10的员工的工资累积，每个员工对应一个累积值。
使用exp(sum(ln(sal)))
```
SELECT e.ename, e.sal, (
SELECT EXP(SUM(LN(sal)))
FROM emp d
WHERE d.empno<=e.empno
AND d.deptno=e.`DEPTNO`
) AS running_total
FROM emp e
WHERE e.`DEPTNO`=10
```
```
ename   sal   running_total       
CLARK   2450  2449.9999999999995  
KING    5000  12249999.999999996  
MILLER  1300  15925000000.000023  
```
## 计算中位数
1. 数列与自身自连接
3. group by a.sal
4. 使用having ...过滤分组
sum(case when...)语句统计 a.sal=b.sal的次数，和sum(sign(a.sal-b.sal))
只有当sum(case when a.sal =b.sal then 1 else 0 end) >= sum(sign(a.sal-b.sal))时，
a.sal是中位数
计算部门20的员工工资中位数
```
SELECT AVG(sal)
FROM(
SELECT e.sal
FROM emp e, emp d
WHERE e. deptno = d.`DEPTNO`
AND e.deptno = 20
GROUP BY e.sal
HAVING SUM(CASE WHEN e.sal = d.sal THEN 1 ELSE 0 END)
>= ABS(SUM(SIGN(e.sal #### d.sal)))
)v
```
自连接核心代码
```
HAVING SUM(CASE WHEN e.sal = d.sal THEN 1 ELSE 0 END)
>= ABS(SUM(SIGN(e.sal  #### d.sal)))
```
理解这段代码，其实就是理解了中位数的一个体征：
中位数的那个数字在数列中的数量>=中位数减去所有数字的结果的符号值(1,0，-1中的一个)的和的绝对值。
## SELECT CASE WHEN 的用法
select 与case结合使用最大的好处有两点，一是在显示查询结果时可以灵活的组织格式，二是有效避免了多次对同一个表或几个表的访问。下面举个简单的例子来说明。
例如表 students(id, name ,birthday, sex, 
grade)，要求按每个年级统计男生和女生的数量各是多少，统计结果的表头为，年级，男生数量，女生数量。如果不用select case 
when，为了将男女数量并列显示，统计起来非常麻烦，先确定年级信息，再根据年级取男生数和女生数，而且很容易出错。
用select case 
when写法如下：
```
SELECT  grade, COUNT (CASE WHEN sex = 1 THEN 1  
                                           ELSE NULL
                                           END) 男生数,
                           COUNT (CASE WHEN sex = 2 THEN 1
                                           ELSE NULL
                                           END) 女生数
   FROM students GROUP BY grade;
```
来源： 
http://blog.sina.com.cn/s/blog_6a3c4c270100x2zc.html
## 统计部门10工资和占全部百分比
SELECT (SUM(CASE WHEN deptno =10 THEN sal END)/SUM(sal))*100 AS pct
FROM emp 
## 统计平均值（排除最大最小值）
```
SELECT AVG(sal)
FROM emp
WHERE sal NOT IN(
	(SELECT MIN(sal) FROM emp),
	(SELECT MAX(sal) FROM emp)
	)
```
# 日期运算
## 计算两个日期间的工作日（除周六周日）
方法一：
1. 使用两个非相关子查询找出这两个日期
​    
case when， case when可以把两个值返回在一行（表x）里
    MAX MIN可以去掉空值，配合case when使用
2. 表X和基干表t500做笛卡尔积，可以生成两个日期之间包含的行数
    date_add函数给每个日期增加天数
​    
datediff求出总行数（总天数）
    date_format把日期转为星期几
```
SELECT     SUM(CASE WHEN DATE_FORMAT(
            DATE_ADD(jones_hd, 
            INTERVAL t100.id-1 DAY),'%a')
            IN ('SAT', 'SUN')
        THEN 0 ELSE 1 END) AS CNT_workdays
FROM(
    SELECT MAX(CASE WHEN ename = 'BLAKE' THEN hiredate END)  AS blake_hd,
    MIN(CASE WHEN ename = 'JONES' THEN hiredate END)  AS jones_hd
    FROM emp
    WHERE ename IN ('JONES', 'BLAKE')
    )X,
    T500
WHERE t500.id <= DATEDIFF(blake_hd,jones_hd)+1
```
方法二：
单纯的日期数值运算，减去两个日期间的周六周日即可
## 计算日期间相差的时分秒
```
SELECT DATEDIFF(ward_hd,allen_hd) AS DAY,
	DATEDIFF(ward_hd, allen_hd)*24 AS hr,
	DATEDIFF(ward_hd, allen_hd)*24*60 AS MIN,
	DATEDIFF(ward_hd, allen_hd)*24*60*60 AS sec
FROM (
	SELECT MAX(CASE WHEN ename='WARD' THEN HIREDATE END) AS ward_hd,
		MIN(CASE WHEN ename = 'ALLEN' THEN HIREDATE END) AS allen_hd
	FROM emp
	)X
```
## 计算今年几个周一、周二
日期拼接成今天后，是否需要cast as date再进行datediff或date_add？
## 每条记录都计算它的某字段和下一条该字段的差
使用标量子查询找到下一个值（配合MIN)
计算当前记录的日期和下一条的日期差
```
SELECT x.*, DATEDIFF(x.next_hd, x.hiredate)
FROM(
	SELECT e.deptno, e.ename , e.hiredate,
		(SELECT MIN(d.hiredate) FROM emp d
			WHERE d.hiredate>e.hiredate) AS next_hd
	FROM emp e
	WHERE deptno=10
	)X
```
## Last_day(date)返回一个月的最后一天
可以判断是否闰年（2月最后一天29，则为闰年）
## 找到当年的第一天
```
date_add(current_date, interval -dayofyear(current_date)+1 day)
```
## 当月日历
1.  生成当月每一天。借助t100基干表
2. 为每一天都生成一个日序号dm、周序号wk、星期几dw
3. 使用case when，使dm每个值对应星期几
4. max聚集函数，并按照wk（周序号）分组，对结果按wk排序
```
SELECT wk,
    MAX(CASE dw WHEN 2 THEN dm END) AS Mo,
    MAX(CASE  dw WHEN 3 THEN dm END) AS Tu,
    MAX(CASE  dw WHEN 4 THEN dm END) AS We,
    MAX(CASE  dw WHEN 5 THEN dm END) AS Th,
    MAX(CASE  dw WHEN 6 THEN dm END) AS Fr,
    MAX(CASE dw WHEN 7 THEN dm END) AS Sa,
    MAX(CASE dw WHEN 1 THEN dm END) AS Su
FROM(
    SELECT DATE_FORMAT(dy,'%u') wk,
        DATE_FORMAT(dy,'%d') dm,
        DATE_FORMAT(dy,'%w')+1 dw
    FROM(
        SELECT     DATE_ADD(firstday,INTERVAL t100.id-1 DAY) dy,t100.id
            FROM t100,(
                SELECT     DATE_ADD(CURRENT_DATE, INTERVAL -
                    DAY(CURRENT_DATE)+1 DAY) AS firstday,
                    MONTH(DATE_ADD(CURRENT_DATE, INTERVAL -
                    DAY(CURRENT_DATE)+1 DAY)) mth
                    )X
            WHERE MONTH(DATE_ADD(firstday,INTERVAL t100.id-1 DAY)) = x.mth
    )Y
)Z
GROUP BY wk
ORDER BY wk
结果 2016-5：
wk  Mo  Tu  We  Th  Fr  Sa  Su  
17                          01  
18  02  03  04  05  06  07  08  
19  09  10  11  12  13  14  15  
20  16  17  18  19  20  21  22  
21  23  24  25  26  27  28  29  
22  30  31                      
```
## 计算员工最近的生日
需要a,b,c三个查询
- 查询a
计算每位员工的出生日期与当前日期相差的年份
- 查询b
计算每位员工今年生日与明年生日
- 查询c
修改今年生日与明年生日。
如果生日为闰月（2-29）而最近生日（cur，next）为29，
需要给最近生日+1，修改到3-01号
```
SELECT NAME, birthday,
	CASE WHEN cur>today THEN cur
		ELSE NEXT
		END AS birth_day
FROM(
	SELECT NAME ,birthday, today,
	DATE_ADD(cur, INTERVAL IF(DAY(birthday)=29 
					&& DAY(cur) =28,1,0) DAY) AS cur,
	DATE_ADD(NEXT, INTERVAL IF(DAY(birthday)=29 
	&& DAY(NEXT) =28,1,0) DAY) AS NEXT
	FROM(
		SELECT NAME, birthday, today,
			DATE_ADD(birthday, INTERVAL diff YEAR) AS cur,
			DATE_ADD(birthday, INTERVAL diff+1 YEAR) AS NEXT
		FROM(
			SELECT CONCAT(last_name, ' ', first_name) AS NAME,
				birth_date AS birthday,
				(YEAR(NOW()) - YEAR(birth_date)) AS diff,
				NOW() AS today
			FROM employees
			)a
		)b
)Z
结果：
name                birthday    birth_day   
Facello Georgi      1953-09-02  2016-09-02  
Simmel Bezalel      1964-06-02  2016-06-02  
Bamford Parto       1959-12-03  2016-12-03  
Koblick Chirstian   1954-05-01  2017-05-01  
Maliniak Kyoichi    1955-01-21  2017-01-21  
Preusig Anneke      1953-04-20  2017-04-20  
Zielinski Tzvetan   1957-05-23  2017-05-23  
Kalloufi Saniya     1958-02-19  2017-02-19  
Peac Sumant         1952-04-19  2017-04-19  
Piveteau Duangkaew  1963-06-01  2016-06-01  
David Jiang         1972-02-29  2017-03-01  
```
# 范围查询
## 通过自连接可以与其他行比较
比如当前行某字段和下一行的某字段比较
## 补充范围内丢失的值
1. 采用基干表生成十年的每一行
2. 将年份表和表emp左连接，并计数每年聘用的员工。
计算采用count(hiredate),也就是说，一年如果没有招聘员工（该年份只有一项，且对应的hiredate为NULL），统计得到0
```
SELECT hd_grp, COUNT(d.hiredate)
FROM(
	SELECT min_year+t100.id-1 AS hd_grp, t100.`ID` AS id
	FROM t100,(
		SELECT YEAR (MIN('1980-01-01')) AS min_year, 
			YEAR (MIN('1980-01-01'))+10 AS max_year
		FROM emp e
		)X
	WHERE (min_year+t100.id-1)<=max_year
)Y LEFT JOIN emp d
ON YEAR(d.`HIREDATE`) = hd_grp
GROUP BY hd_grp
```
高级查询

## 外层select子句和where子句过滤内部数据
重要！要根据某一列新产生的值过滤，就必须再嵌套一层select
## 生成行序号，跳过某些行
```
SELECT x.ename, x.rank
FROM(
	SELECT e.ename,
		(SELECT COUNT(*) AS rank
		FROM emp d
		WHERE d.ename<=e.`ENAME`
		)rank
	FROM emp e
)X
WHERE MOD(rank,2)=1
ORDER BY rank
```
## 两个表，部分连接，部分不连接（只返回一个表的信息）
方法一：把部分连接的匹配条件移到外联结匹配条件ON子句中去
```
SELECT *
FROM dept d LEFT JOIN emp e
ON (e.deptno = d.`DEPTNO`
	AND (e.`DEPTNO`= 10 OR e.`DEPTNO` = 20))
```
方法二：把筛选移到内联视图中
1. 内联视图E依据EMP.deptno筛选，并返回EMP中所想要的行
2. dept表与内联视图e进行外部连接
```
SELECT *
FROM dept d LEFT JOIN (
			SELECT * FROM emp
			WHERE deptno IN(10,20)) e
ON (e.deptno = d.`DEPTNO`
	)
```
## 找出表中两个字段互换的行
```
SELECT DISTINCT v1.*
FROM v v1, v v2
WHERE v1.`test1`=v2.test2
AND v1.`test2`=v2.`test1`
AND v1.`test1`<=v1.`test2`
```
## 为数值创建等级
按工资拍等级，工资越高等级越高，并筛选出工资等级前5的
```
SELECT ename,sal,rank
FROM(
	SELECT e.ename, e.sal,
		(SELECT COUNT(sal)
		FROM emp d
		WHERE d.sal>=e.sal) AS rank
	FROM emp e
)X
WHERE 
rank
<=5
ORDER BY rank
WHERE 
rank
<=5
类似于，只是直接筛选不能排等级
SELECT ename,sal
FROM emp
ORDER BY sal DESC
LIMIT 5
```
## 筛选出一种员工：紧随其后聘用的员工的工资比他少
方法一：
- 使用子查询，确定他紧随其后聘用的人的日期
- 使用子查询，他之后聘用的第一个工资高于他的员工的聘用日期
```
EXPLAIN SELECT *
FROM(
	SELECT ename, sal,
		(SELECT MIN(d.hiredate) FROM emp d
			WHERE d.hiredate>e.hiredate
		)next_hd,
		(SELECT MIN(d.hiredate) FROM emp d
			WHERE d.`HIREDATE`>e.hiredate
			AND d.`SAL`>e.sal
		)next_hd_sal
	FROM emp e
)X
```
方法二：
```
EXPLAIN SELECT ename,sal,next_sal
FROM(
	SELECT ename, sal,
		(SELECT MIN(a.hiredate)
		FROM emp a
		WHERE a.hiredate =(SELECT MIN(d.hiredate) FROM emp d
			WHERE d.hiredate>e.hiredate)
		)next_sal
	FROM emp e
)X
WHERE sal<next_sal
```
方法二会不会缓存
(SELECT MIN(d.hiredate) FROM emp d 
WHERE d.hiredate>e.hiredate)？
因为e的每一行对应一个select d、一个select a, 但select a每一行都要select d
## 下一档工资和上一档工资
```
SELECT e.ename, e.`SAL`,
	(SELECT MIN(sal) FROM emp d
		WHERE d.sal>e.sal) forword,
	(SELECT MAX(sal) FROM emp d
		WHERE d.sal<e.sal)backword
FROM emp e
ORDER BY 2
```
## 生成简单的预测
```
SELECT o.id, t10.id, order_date,process_date,
	CASE t10.id
	WHEN 1 THEN NULL
	WHEN 2 THEN ADDDATE(process_date,1)
	WHEN 3 THEN ADDDATE(process_date,1)
	END AS process_date1,
	CASE t10.id
	WHEN 1 THEN NULL
	WHEN 2 THEN NULL
	WHEN 3 THEN ADDDATE(process_date,2)
	END AS process_date2	
FROM t10, o
WHERE  t10.id<=3
ORDER BY o.`id`, t10.`ID`
结果：
id  id  order_date  process_date  process_date1  process_date2  
1   1   2016-05-28  2016-05-30                                  
1   2   2016-05-28  2016-05-30    2016-05-31                    
1   3   2016-05-28  2016-05-30    2016-05-31     2016-06-01     
2   1   2016-05-29  2016-05-31                                  
2   2   2016-05-29  2016-05-31    2016-06-01                    
2   3   2016-05-29  2016-05-31    2016-06-01     2016-06-02     
3   1   2016-05-30  2016-06-01                                  
3   2   2016-05-30  2016-06-01    2016-06-02                    
3   3   2016-05-30  2016-06-01    2016-06-02     2016-06-03     
```
## 生成每季度的第一天和最后一天
我的方法：
```
SELECT t10.id AS QTR, 
	DATE_ADD(first_day, 
			INTERVAL (t10.id-1)*3 MONTH) AS Q_start,
	 ADDDATE(DATE_ADD(first_day, 
			INTERVAL t10.id*3 MONTH),-1) AS Q_end
FROM t10,
	(SELECT ADDDATE(CURRENT_DATE,-DAYOFYEAR(CURRENT_DATE)+1) AS first_day)v	
WHERE t10.id<=4
```
cookbook的方法提取了重复计算的 
DATE_ADD(first_day, INTERVAL t10.id*3 MONTH)
这样增加了select的个数，能否提高效率？
```
SELECT X.id AS QTR, 
	DATE_ADD(dy, INTERVAL -3 MONTH) AS Q_start,
	 ADDDATE(dy,-1) AS Q_end
FROM(
	SELECT  t10.id, DATE_ADD(first_day, INTERVAL t10.id*3 MONTH) AS dy               
	FROM t10,
		(SELECT ADDDATE(CURRENT_DATE,-DAYOFYEAR(CURRENT_DATE)+1) AS first_day)v	
	WHERE t10.id<=4
)X
```
## 统计每个月聘用的雇员数
需要生成月列表
```
SELECT mth, COUNT(hiredate)
FROM emp e RIGHT JOIN
	(SELECT DATE_ADD(min_hd,INTERVAL t100.id-1 MONTH) AS mth
	FROM t100,
		(SELECT min_hd, DATE_ADD(max_hd, INTERVAL 11 MONTH) AS max_hd
			FROM (
				SELECT ADDDATE(MIN(hiredate),-DAYOFYEAR(MIN(hiredate))+1)
					AS min_hd,
					ADDDATE(MAX(hiredate),-DAYOFYEAR(MAX(hiredate))+1)
					AS max_hd
				FROM emp
				)v
		)Y
	)Z
ON( YEAR(e.`HIREDATE`)=YEAR(mth) AND MONTH(e.`HIREDATE`) = MONTH(mth))
GROUP BY mth
ORDER BY mth
```
## 按周分组
```
SELECT ADDDATE('1900-01-01',week_id*7) AS week_start,
	ADDDATE('1900-01-01',week_id*7+6) AS week_end,
	sum_cost
FROM
	(SELECT FLOOR(DATEDIFF(DATE,'1900-01-01')/7) AS week_id, SUM(cost) AS sum_cost
	FROM sales
	GROUP BY FLOOR(DATEDIFF(DATE,'1900-01-01')/7)
	)X
```
## 将结果集转置为一行
使用case when、聚集函数如sum或min
```
select sum(case when deptno=10 then 1 else 0 end) as deptno_10,
sum(case when deptno=20 then 1 else 0 end) as deptno_20,
sum(case when deptno=30 then 1 else 0 end) as deptno_30
from emp
```
```
转置前：
article  dealer  price  
0001     A       3.45   
0001     B       3.99   
0002     A       10.99  
0003     B       1.45   
0003     C       1.69   
0003     D       1.25   
0004     D       19.95  
//sql
SELECT MIN(CASE WHEN article=0001 THEN price END )AS price1,
	MIN(CASE WHEN article=0002 THEN price END) AS price2
FROM shop
//转置后
price1  price2  
3.45    10.99   
```