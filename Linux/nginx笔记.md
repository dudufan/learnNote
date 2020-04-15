[TOC]

# 安装

预先安装

```
 sudo yum install yum-utils
```

设置yum源

```
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key

[nginx-mainline]
name=nginx mainline repo
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
```

安装nginx

```
sudo yum install nginx
```

也可以rpm包离线安装。

# 管理

```shell
nginx -s <signal>

signal: stop quit reload reopen
```

## 启动

```shell
service nginx start

systemctl start nginx.service

# 查看启动日志
systemctl status nginx.service

```

解决pid无法创建或打开的问题，给nginx工作进程（nginx用户）赋予写入权限



# 基础

main

​	stream

​	http

​		upstream

​		server

​			location

- 可以包含其他block的block叫上下文。
- 配置文件中未包含在上下文中的配置项，默认都在main这个上下文中。

upstream配置的是负载均衡策略。

```nginx
# 定义一个servers的pool
upstream backend {  
    # 负载均衡算法
    #  least_conn least_time hash ip_hash
    # 代表目的地
    server 10.10.12.45:80      weight=1;
    # weight不配置默认是1,weight=2表示请求是1的两倍
    server app.example.com:80  weight=2;
} 
```

ip_hash仅用于HTTP，根据请求的客户端ip路由。适用于session、文件分片等数据不被多个应用服务器共享的场景。

`hash $request_uri;`对同一个资源（比如文件缓存）的请求会到达同一台Server，减少对第三方云存储的访问。

Nginx Plus限制连接数

```nginx
upstream backend {    zone backends 64k;    queue 750 timeout=30s;
    server webserver1.example.com max_conns=25;    server webserver2.example.com max_conns=15; }
```

常用模块指令：

http://nginx.org/en/docs/http/ngx_http_upstream_module.html

http://nginx.org/en/docs/http/ngx_http_proxy_module.html

http://nginx.org/en/docs/http/ngx_http_api_module.html

# Nginx Plus会话保持

```nginx
upstream backend {    
    server backend1.example.com;    
    server backend2.example.com;    
    sticky cookie            
        affinity  # cookie名称          
        expires=1h            
        domain=.example.com  # 能访问该cookie的域           
        httponly  #客户端浏览器能否使用cookie          
        secure    # 是否可以被非安全协议传输
        path=/; # 该cookie能让path路径下的页面访问
}
```

sticky learn

sticky route 细粒度控制

# HTTP负载均衡

```nginx
# 定义一个servers的pool
upstream backend {  
    # 负载均衡算法
    #  least_conn least_time hash ip_hash
    # 代表目的地
    server 10.10.12.45:80      weight=1;
    # weight不配置默认是1,weight=2表示请求是1的两倍
    server app.example.com:80  weight=2;
} 
server {    
    location / {
        proxy_pass http://backend;
    } 
}
```

## upstream

http://nginx.org/en/docs/http/ngx_http_upstream_module.html#keepalive

keepalive。nginx和后端建立长连接个数。可以给http和tcp udp都使用。

```nginx
upstream http_backend {
    server 127.0.0.1:8080;

    keepalive 16;
}

server {
    ...

    location /http/ {
        proxy_pass http://http_backend;
        # 使用keepalive + http时设置
        proxy_http_version 1.1;
        # 使用keepalive + http时设置
        proxy_set_header Connection "";
        ...
    }
}
```

# HTTP Server

## 静态资源Server

```nginx
http {
    server {
        ...
        location /images/ {
            # Set the root directory to search for the file
            root /data/www;

            # Disable logging of errors related to file existence
            open_file_cache_errors off;

            # Make an internal redirect if the file is not found
            error_page 404 = /fetch$uri;
        }

        location /fetch/ {
            proxy_pass http://backend/;
        }
    
        location / {
        	# 指定
        	root /data/www;
            # 指定index文件
            index index.html index.php;
    	}
        
        location /images/ {
            # 自动为目录../生成index.html	
            autoindex on;
		}
    }
}
```

访问nginx静态文件出现403 forbidden问题原因：

1. 权限配置不正确。nginx的工作进程（默认属于nginx用户）既需要文件的读权限,又需要文件所有父目录的可执行权限。
2. 将SELINUX=enforcing 修改为 SELINUX=disabled 状态。`/usr/sbin/sestatus;vi /etc/selinux/config`

## 反向代理

### server block

可以定义多个virtual server监听同一个端口。如果server_name都未匹配到，路由到默认server（第一个）。

```nginx
server {
    listen      80;
    server_name example.net www.example.net;
    ...
}


# 对于路径/的请求，1. 找/data/www/index.php 2. 内部重定向到\.php$。
server {
    listen      80;
    server_name example.org www.example.org;
    root        /data/www;

    location / {
        index   index.html index.php;
    }

    location ~* \.(gif|jpg|png)$ {
        expires 30d;
    }

    location ~ \.php$ {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME
                      $document_root$fastcgi_script_name;
        include       fastcgi_params;
    }
}
```

可以重写uri

### location block

https://docs.nginx.com/nginx/admin-guide/web-server/web-server/

> 正则 location 匹配让步普通 location 的严格精确匹配结果；但覆盖普通 location 的最大前缀匹配结果。

- 匹配请求路径时，正则表达式前加~
- location只测试URI中不带参数的部分，因为参数顺序不定。
- ^~表示这个location一旦匹配上，不需要继续正则匹配。

检查顺序：

1. 查看所有普通前缀匹配的location
2. 遇到=则停止匹配。
3. 遇到^~则当做普通前缀匹配（精确匹配）考虑，并不再继续正则匹配。
4. 保存最长前缀匹配到的串。
5. 正则匹配（可能被跳过）。匹配第一个location，停止匹配。
6. 使用最长前缀匹配对应的location。





```nginx
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
    # 现有路径变动，可以指定错误码和重定向
    location /wrong/url {
  	  	return 404;
	}
    location /permanently/moved/url {
        return 301 http://www.example.com/moved/here;
    }
    location /users/ {
        rewrite ^/users/(.*)$ /show?user=$1 break;
	}
    location / {
        # 替换HTTP响应内容
        sub_filter     'href="http://127.0.0.1:8080/'    'href="https://$host/';
        sub_filter     'img src="http://127.0.0.1:8080/' 'img src="https://$host/';
        # 一个location连续应用sub_filter
        sub_filter_once on;
    }  
    location /old/path.html {
        error_page 404 =301 http:/example.com/new/path.html;
    }
}
```

### rewrite

- Break 和 last 都能阻止继续执行后面的 rewrite 指令

- last 在 location 下用的话，对于重写后的 URI 会重新匹配 location 
- break 不会重新匹配 location 

用法：break在匹配后改写url。last修改url为其他location可以匹配到的url。

### uwsgi协议

[uwsgi](http://nginx.org/en/docs/http/ngx_http_uwsgi_module.html)

监听http端口，然后把请求转发给uwsgi服务器，如Dango，flask

### 设置请求Header

```nginx
location /some/path/ {
    # 默认nginx把Host设为目标的代理ip，这里设为目标的域名
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    # 去掉某个request header
    proxy_set_header Accept-Encoding "";
    proxy_pass http://localhost:8000;
}
```

### 缓冲

当客户端处理速度不够快时，nginx可以缓冲响应，让Server尽可能快的处理。

```nginx
location /some/path/ {
    proxy_buffers 16 4k;
    proxy_buffer_size 2k;
    proxy_pass http://localhost:8000;
}
```

### 压缩和解压缩

gzip gunzip都可以放在http/server/location中。

```nginx
server {
    gzip on;
    gzip_types      text/plain application/xml;
    gzip_proxied    no-cache no-store private expired auth;
    gzip_min_length 1000;
    ...
}

location /storage/ {
    gunzip on;
    ...
}
```

### HTTPS

https://www.jianshu.com/p/398c9ab538b7

http://nginx.org/en/docs/http/configuring_https_servers.html

证书ssl_certificate会发给每个客户端。ssl_certificate_key是私钥文件，需要控制访问权限，nginx主进程必须能读。

一个基础配置

```nginx
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     www.example.com.crt;
    ssl_certificate_key www.example.com.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    #...
}
```

### 容错

```nginx
    server {
        listen 8080;
        server_name test;
#charset koi8-r;
#access_log  logs/host.access.log  main;
        location / {
            root html;
            index index.html index.htm;
#对应上面的test,代理的地址
            proxy_pass http://test;
#故障转移
            proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504 http_403 http_404 http_429 non_idempotent;
#将请求传递到下一个服务器可以通过尝试次数和时间来限制,限制请求可以传递到下一个服务器的时间。 0值关闭此限制。
            proxy_next_upstream_timeout 0;
#限制将请求传递到下一个服务器的可能尝试次数。 0值关闭此限制。
            proxy_next_upstream_tries 0;
            proxy_read_timeout 5s;
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
        }
        location = /50x.html {
            root html;
        }
#error_page  404              /404.html;
# redirect server error pages to the static page /50x.html
#
        error_page 500 502 503 504  /50x.html;
    }
```

## 变量

内建变量：大部分都是和一个特定请求关联的。如`$remote_addr`表示客户端ip 、`$uri` 是当前请求uri。

http://nginx.org/en/docs/http/ngx_http_core_module.html#variables

自定义变量：

[`set`](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html#set), [`map`](http://nginx.org/en/docs/http/ngx_http_map_module.html#map), and [`geo`](http://nginx.org/en/docs/http/ngx_http_geo_module.html#geo) 

# TCP负载均衡

```nginx
stream {    
    upstream mysql_read {
        # mysql有两个读副本集
        server read1.example.com:3306  weight=5;        
        server read2.example.com:3306;
        # 前两台主down掉后，第三台备份会启动。
        server 10.10.12.34:3306        backup;    
    }
    server { 
        # 可以指定监听的ip
        # listen 127.0.0.1:3306;
        listen 3306;
        proxy_pass mysql_read;    
    } 
    # tcp的ssl卸载
    
    upstream mstp_pcs {
        server 10.6.95.212:8082;
    }
    server {
        listen              8082 ssl;
        ssl_certificate     www.example.com.pem;
        ssl_certificate_key www.example.com.key;
        
        ssl_session_cache   shared:SSL1:1m;
        ssl_session_timeout 5m;
		
        ssl_ciphers         HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        proxy_pass mstp_pcs;
        #...
    }

} 
```

# 健康检查

nginx只能被动检查：监控连接和响应。重试转发机制，max_fails=1 fail_timeout=10s（10s内有1次失败，就标记为不可用屏蔽该目的地10s）

nginx plus可以主动定期发送请求检查响应。详见zone命令、slow start命令、health_check命令。

```nginx
stream {
    server {
        listen 3306;
        proxy_pass read_backend;
        # nginx plus 才支持
        health_check interval=10 passes=2 fails=3;
    }
}
```

# 隐藏版本号

http中加入server_tokens off;