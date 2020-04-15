[TOC]


# 安装
1. virtual vagrant都安装最新版
2. 全局增加box到vagrant。`vagrant box add <boxname> <filepath>`
3. 当前目录初始化vagrantFile，或从别的地方拷贝比如git clone vagrant 下载vagrant配置。`vagrant init <boxname>`
4. vagrant up 启动虚拟机，自动下载软件
5. vagrant ssh 连接到虚拟机
6. vagrant halt 关闭虚拟机

查看ssh连接配置，根据打印的信息可以配置ssh客户端

```shell
# vagrant ssh-config
Host default
  HostName 127.0.0.1
  User vagrant
  Port 2222
  UserKnownHostsFile /dev/null
  StrictHostKeyChecking no
  PasswordAuthentication no
  IdentityFile D:/Learn/vagrant/.vagrant/machines/default/virtualbox/private_key
  IdentitiesOnly yes
  LogLevel FATAL
```



# 导出box

1. 把`D:\Program files\Oracle\VirtualBox`加入到系统环境变量PATH里。后续可以使用virtualbox提供的命令行接口。
2. `vboxmanage list vms`
3. 打包
    `vagrant package --base box_name_1503366286622_12977 --output ./ubuntu_amd64.box`
4. vagrant package --base vagrant_default_1557108892038_60263 --output ./
5.  参数说明：

- --base 要打包的虚拟机名称
- --output 打包后的包名
- -- include 打包需要增加的文件，多个文件以逗号分隔
- --vagrantfile 指定vagrantfile文件


# 共享文件夹
默认Vagrantfile的文件夹就是虚拟机的/vagrant目录
可以在 Vagrantfile中配置.



遇到错误

>Vagrant was unable to mount VirtualBox shared folders. This is usually
>because the filesystem "vboxsf" is not available.

解决办法：

vagrant plugin install vagrant-vbguest

vagrant reload --provision  



vagrant up卡在default: SSH auth method: private key这一行

原因：config.vm.synced_folder "data", "/vagrant" 这一行"data"写错，改为config.vm.synced_folder "D:/Learn/vagrant/data", "/vagrant_data"，并安装vagrant-vbguest解决问题。

# 网络配置

Vagrant的网络有三种模式

## 端口映射

就是将虚拟机中的端口映射到宿主机（host)对应的端口直接使用 ，在Vagrantfile中配置：

```
# guest: 80 表示虚拟机中的80端口， host: 8080 表示映射到宿主机的8080端口。
config.vm.network :forwarded_port, guest: 80, host: 8080
```

## 私网

从host自由访问虚拟机，别人不需要访问虚拟机：

```
 # 192.168.1.104 表示虚拟机的IP，多台虚拟机的话需要互相访问的话，设置在相同网段即可
 config.vm.network :private_network, ip: "192.168.1.104"
```

## 局域网

```
# 将虚拟机作为当前局域网中的一台计算机，由局域网进行DHCP，那么在Vagrantfile中配置：
config.vm.network :public_network
```

# 参考

https://www.jianshu.com/p/3df0c7ec4251
https://segmentfault.com/a/1190000008729625




