mysql-5.5.49
cmake 2.8.12.2
slave ip  10.1.1.73 端口 3306 server-id 73
主 ip  10.1.1.83 端口 3306    server-id 83



注意：修改配置文件cnf后，一定要重启mysql-server进程！


keepalived
10.1.1.83配置：
virtual_server 10.1.1.238 3306
问题：mysql挂掉，mysql.sh无法成功杀死 keepalived
原因：没有对mysql.sh执行chmod +x /usr/local/mysql/bin/mysql.sh


问题： keepalived配置的虚拟IP ping不通
原因：同网段有相同的virtual_router_id
解决办法：把keepalived.conf中 virtual_router_id设置为另一个值

