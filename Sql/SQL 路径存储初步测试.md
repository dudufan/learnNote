线程数10 用户数为10000
每个用户500数据
每个线程负责插入固定范围的用户，不同线程隔离开
增加插入数（每个用户），测得的效率也不同




500条数据的容量大小：
meta集合
数据 1100MB
索引 853MB


share集合
数据 801MB
索引 1544MB


```
select concat(round(sum(data_length/1024/1024),2),'MB') as data from information_schema.tables where table_schema='cds_test' and table_name='share';


select concat(round(sum(index_length/1024/1024),2),'MB') as data from information_schema.tables where table_schema='cds_test' and table_name='share';


select concat(round(sum(data_length/1024/1024),2),'MB') as data from information_schema.tables where table_schema='cds_test' and table_name='meta1';


select concat(round(sum( index_length /1024/1024),2),'MB') as data from information_schema.tables where table_schema='cds_test' and table_name='meta1';
```


 


