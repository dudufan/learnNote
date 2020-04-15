# 文档

https://kubernetes.io/docs

# 环境配置



## vagrant配置

1. 启动并连接到虚拟机。`vagrant up;vagrant ssh;`
2. minikube start

## centos7安装



1. cento安装gcc，安装或更新kernel-devel、kernel到同一版本

2. 重启后自动安装virtualbox增强功能就不会报错



```

yum install -y gcc gcc-devel gcc-c++ gcc-c++-devel make kernel kernel-devel

```

3. 替换yum源为aliyun镜像源

## Minikube



下载安装minikube



```

curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.30.0/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube

```

minikube info/start 





## 虚拟机内安装virtualbox



1. virtualbox官网上下载yum源的repo文件，放到/etc/yum.repos.d目录下。
2. 更新`yum clean all;yum makecache``
3. `yum install VirtualBox-5.2`



```

yum list | grep VirtualBox

```



https://blog.csdn.net/shilei_zhang/article/details/72811274





## FAQ

**Connection reset by peer**

解决办法：

```shell
systemctl stop firewalld
```

Connection reset by peer的常见原因： 
1）服务器的并发连接数超过了其承载量，服务器会将其中一些连接关闭；
   如果知道实际连接服务器的并发客户数没有超过服务器的承载量，则有可能是中了病毒或者木马，引起网络流量异常。可以使用netstat -an查看网络连接情况。 
2）客户关掉了浏览器，而服务器还在给客户端发送数据；
3）浏览器端按了Stop； 

这两种情况一般不会影响服务器。但是如果对异常信息没有特别处理，有可能在服务器的日志文件中，重复出现该异常，造成服务器日志文件过大，影响服务器的运行。可以对引起异常的部分，使用try...catch捕获该异常，然后不输出或者只输出一句提示信息，避免使用e.printStackTrace();输出全部异常信息。 
4）防火墙的问题；

如果网络连接通过防火墙，而防火墙一般都会有超时的机制，在网络连接长时间不传输数据时，会关闭这个TCP的会话，关闭后在读写，就会导致异常。 
如果关闭防火墙，解决了问题，需要重新配置防火墙，或者自己编写程序实现TCP的长连接。实现TCP的长连接，需要自己定义心跳协议，每隔一段时间，发送一次心跳协议，双方维持连接。
5）JSP的buffer问题。
   JSP页面缺省缓存为8k，当JSP页面数据比较大的时候，有可能JSP没有完全传递给浏览器。这时可以适当调整buffer的大小。 <%@ page buffer="100k"%>



# 核心组件

kubelet 是node agent，重启服务

replication controller pod失败后自动转移到其他机器



**控制组件**

控制组件理论上可以在集群的任何机器上运行，但一般用脚本在master服务器上启动各个控制组件。

[kube-apiserver](https://kubernetes.io/docs/reference/generated/kube-apiserver/) 控制组件的最前端。k8s平台中万物都是api object，所有操作、组件内部之间的通讯都通过REST API调用。kubectl、[kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm/)命令行或者python的kubernetes-client都可以使用api。.yaml中可以表示API对象

etcd key-value形式保存整个集群的状态、数据

kube-scheduler 为新创建的pods选择node来运行，考虑各种因素

kube-controller-manager 打包了多种controller，负责维护集群的状态，比如故障检测、自动扩展、滚动更新等。Node Controller监控汇报node是否挂掉。Replication Controller维护确保pods个数。

cloud-controller-manager 云服务厂商需要实现的适配接口层，未来kube-controller-manager会调用cloud-controller-manager来实现集群控制管理的功能。kube-controller-manager启动时加参数`--cloud-provider` flag to `external`



**Node组件**

运行在node上，共同提供了kubernetes运行环境。

kubelet  Server-Agent架构中的agent，是Node上的pod管家，根据podSpecs保证pod健康运行。每个Node节点都会启动kubelet进程。负责：

- 用来处理Master节点下发到本节点的任务，管理Pod和其中的容器
- kubelet会在API Server上注册节点信息，定期向Master汇报节点资源使用情况，并通过cAdvisor监控容器和节点资源

[kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)是node的网络代理，实现了Service特性的一部分。负责维护node上的网络规则(iptables)，从而能从集群内外访问pods

> 当一个Pod中的容器访问这个地址的时候，这个请求会被转发到本地代理（kube-proxy）,每台机器上均有一个本地代理，然后被转发到相应的后端容器。Kubernetes通过一种轮训机制选择相应的后端容器，这些动态的Pod被替换的时候,Kubeproxy时刻追踪着，所以，服务的 IP地址（dns名称），从来不变。

容器 Docker实现了kubenetes的CRI接口



**插件**

提供集群级别的附件功能，在`kube-system`命名空间内

DNS kubernetes集群必须有Cluster DNS服务器，k8s启动的容器会自动使用它。

Dashboard

Cluster-level Logging

Ingress Controller为服务提供外网入口

# 基础

https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/

## Pod

Pod是kubernetes最小的执行单元，是一个应用的单个实例。

pod相当于一个临时的逻辑主机，封裝了一个到多个容器(可能是不同应用、db、redis、zk）。容器间共享：

- 共享资源，如ip、网络端口和指定的多个共享存储卷。容器间可以通过localhost访问其他容器
- 生命期共享。

“sidecar” container 可以用来从远程资源更新共享文件。![](https://d33wubrfki0l68.cloudfront.net/aecab1f649bc640ebef1f05581bfcc91a48038c4/728d6/images/docs/pod.svg)

Pod的运行阶段：

- 挂起（Pending）：Pod 已被 Kubernetes 系统接受，但有一个或者多个容器镜像尚未创建。等待时间包括调度 Pod 的时间和通过网络下载镜像的时间，这可能需要花点时间。
- 运行中（Running）：该 Pod 已经绑定到了一个节点上，Pod 中所有的容器都已被创建。至少有一个容器正在运行，或者正处于启动或重启状态。
- 成功（Succeeded）：Pod 中的所有容器都被成功终止，并且不会再重启。
- 失败（Failed）：Pod 中的所有容器都已终止了，并且至少有一个容器是因为失败终止。也就是说，容器以非0状态退出或者被系统终止。
- 未知（Unknown）：因为某些原因无法取得 Pod 的状态，通常是因为与 Pod 所在主机通信失败。

Pod的hostname默认时pod的`metadata.name` ，也可以在spec中指定hostname

集群内部的Pod之间可以通过私有Ip互相访问

Pod模板可以定义到Deployment、ReplicationController下，Pod并不能直接更新已创建的Pod，副本控制器可以。



## 容器

Pod中容器的主机名就是pod名称。

容器创建时运行的所有服务的列表都会作为环境变量提供给容器。

容器内使用的端口并不是Node的端口

docker0是docker容器之间的网桥，通过它容器可以访问外网。但外部主机访问容器，必须将容器ip端口通过NAT暴露给外部。



## Nodes

一个Node是一台虚拟主机或物理主机，也可能是一个云服务node。kubernetes创建node，只是创建一个节点信息。创建后检查可用性。

kubenetes的master管理所有Nodes资源。负责创建分发Pods到各个Nodes。

每个kubernetes节点上有kubelet代理（客户端），用于和master节点通信。



```shell
# 查看Pods所在NodeIp
kubectl get pods
# 查看node状态
kubectl describe node <insert-node-name-here>
```

kubelet 带上 `--register-node`，会注册node节点到apiServer

## Service



一组Pods（可以在不同Node上）组成一个服务。Pod的ip地址不对外暴露，service可以定义对外暴露ip端口的策略，

service提供了固定的IP地址和DNS名称，而这些与一系列Pod通过标签进行动态关联。

Service负责一组Pods的销毁、复制、负载均衡、服务发现、路由，屏蔽对其他应用的影响。

Service的ip：

1. *ClusterIP* (default) -Service暴露给集群内部的ip，可以通过clusterIP:内部端口（如8080）来访问Service。这个ip网段不同于pods（docker)的网络。```.spec.clusterIP```
2. *NodePort* - 暴露服务中每个Node的同一个端口出去，让集群之外可以用`<NodeIP>:<NodePort>`来访问。NodeId是该Node所在外部网络的实际ip。NodeIp只能查看主机ip来看:`ip addr`.
3. *LoadBalancer* - 创建一个负载均衡器，分配一个固定ip给外部。

其他应用访问Service：

- 环境变量
- DNS（推荐）

HTTPS访问参考https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/



**创建Service**

```shell
kubectl expose deployment/my-nginx
```

相当于kubectl apply -f以下配置

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
```

实例2

```shell
# 用已有的部署创建service，把内部8080端口映射为nodePort暴露出去
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080

# 查看services的暴露方式和内部cluster-ip、NodePort
kubectl get services
kubectl describe services

# 查看Pods所在NodeIp
kubectl get pods
```

实例3，`Service` 对象会将请求代理到使用 TCP 端口 9376，并且具有标签 `"app=MyApp"` 的 `Pod` 上。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

`Service` 能够将一个接收 `port` 映射到任意的 `targetPort`。默认情况下，`targetPort` 将被设置为与 `port` 字段相同的值



**服务发现**

Pod启动时会加入已使用Service的环境变量，可以用env命令查看

```shell
REDIS_MASTER_SERVICE_HOST=10.0.0.11
REDIS_MASTER_SERVICE_PORT=6379
```

**Service实现**

kube-proxy会写入 iptables 规则，捕获到达该 `Service` 的 `clusterIP`（是虚拟 IP）和 `Port` 的请求，并重定向到代理端口，代理端口再代理请求到 backend `Pod`（round-robin 算法或随机）。

## DNS

`kube-dns`应用（也是一个service）会自动给其他services的固定ip分配一个名称(就是service的名称)

```shell
kubectl get services kube-dns --namespace=kube-system

# 运行一个curl应用测试dns
kubectl run curl --image=radial/busyboxplus:curl -i --tty
# my-nginx是service的name
[ root@curl-131556218-9fnch:/ ]$ nslookup my-nginx
```



## Deployments

`kubectl run <deployment_name> --image=<image_url> --port=<specific port>`

有三个作用：

- 找一个可以运行该应用实例的node节点
- 安排应用在节点上运行
- 需要的时候在一个新的节点上部署应用实例



```shell

# 查看部署的所有应用，并且显示某个应用副本的数量
kubectl get deployments
# 如果AVAILABLE为0，则是没有Pod，则没有启动

# 扩展副本数量到4
kubectl scale deployments/kubernetes-bootcamp --replicas=4
# 查看所有Pods，显示ip、Node
kubectl get pods -o wide

# 查看扩展后的情况
kubectl describe deployments/kubernetes-bootcamp



```

## Controllers

一个控制器至少（一般）会控制一种Kubernetes资源的状态，使它趋近于预期状态。

kubernetes内置的controllers都会通过集群的APIServer来控制。

control plane内部的controllers也是弹性部署的。



可以在yaml中定义几种控制器

ReplicaSet 在 Replication Controller的基础上增加了集合选择器的支持，建议使用 Deployment 而不是直接使用 ReplicaSet

https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

## Volumes

存储遇到的问题：

- 容器中的文件在磁盘上是临时存放的，当容器崩溃时，kubelet 将重新启动容器，容器中的文件将会丢失——因为容器会以干净的状态重建。
- 当在一个 `Pod` 中同时运行多个容器时，常常需要在这些容器之间共享文件

Kubernetes 抽象出 `Volume` 对象来解决这两个问题

Volume的特点：

- 和Pod具有相同的生命周期
- 卷的核心是包含一些数据的目录，Pod 中的容器可以访问该目录
- Kubernetes 支持许多类型和不同数量的卷
- 使用卷时, Pod 声明中需要提供卷的类型 (`.spec.volumes` 字段)和卷挂载的位置 (`.spec.containers.volumeMounts` 字段)。Volume 都挂载在镜像内的指定路径上

## Persistent Volumes

`PersistentVolume` 像node一样的资源

 `PersistentVolumeClaim`用户声明对PersistentVolume的消费，类似Pod

## 计算资源

CPU 的单位是核心数，内存的单位是字节。

Pod 中的每个容器都可以指定以下的一个或者多个值：

- `spec.containers[].resources.limits.cpu`
- `spec.containers[].resources.limits.memory`
- `spec.containers[].resources.requests.cpu`
- `spec.containers[].resources.requests.memory`

## API Object

https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/

每个kubernetes对象有spec和status两属性

spec表示期待的状态

status是kubernetes系统维护的实际状态。任何时候kubernetes控制组件都会让实际状态status去匹配spec。

metadat：

- name，同一个namespace中此种类型唯一，用户可以定义后面的名称。如`/api/v1/pods/some-name`
- UID。集群唯一，kubernetes生成

.yaml文件中每种对象的spec定义都不同，可以参考[Kubernetes API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.17/)

yaml文件表示了对象的信息，kuberctl命令可以读取.yaml文件，转换为Kubernetes api需要的json

> - `apiVersion` - Which version of the Kubernetes API you’re using to create this object
> - `kind` - What kind of object you want to create
> - `metadata` - Data that helps uniquely identify the object, including a `name` string, `UID`, and optional `namespace`
> - `spec` - What state you desire for the object



命名空间：表示虚拟集群，用来给多个用户划分集群资源。

## Labels

labels是附件到object上的key/value对，可以用来过滤选择objects。

给node加标签

```shell
# 获取集群的节点名称
kubectl get nodes
# 将标签添加到你所选择的节点上
kubectl label nodes <node-name> <label-key>=<label-value>
# 查看指定节点的标签完整列表
kubectl describe node "nodename"

```

label的key可选的有个前缀，内容是DNS子域名

```yaml
metadata:
  name: label-demo
  labels:
    environment: production
    app: nginx
```



## Selector

比如service用selector属性来匹配所管理的pods，pod用nodeSelector属性选择node（[node selection](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/))。

```yaml
# 相等
selector:
    component: redis
# 集合    
selector:
  matchLabels:
    component: redis
  matchExpressions:
    - {key: tier, operator: In, values: [cache]}
    - {key: environment, operator: NotIn, values: [dev]}    
```

nodeSelector

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd
```

查询可以使用label,过滤的关键字有=、!=、in、notin、exists。url方式：

`?labelSelector=environment%3Dproduction,tier%3Dfrontend`

kubectl

```shell
kubectl get pods -l environment=production,tier=frontend

kubectl get pods -l 'environment in (production),tier in (frontend)'
```

## annotations

附加一些不用于选择对象的信息

```json
"metadata": {
  "annotations": {
    "key1" : "value1",
    "key2" : "value2"
  }
}
```

# 外部访问

k8s现在提供三种暴露服务的方式：LoadBlancer、NodePort 、Ingress。

## Ingress

以Ingress Nignx为例，实现原理如下。

Ingress Contronler 通过与 Kubernetes API 交互，能够动态的获取cluster中Ingress rules的变化，生成一段 Nginx 配置，再写到 Nginx-ingress-control的 Pod 里，reload pod 使规则生效。从而实现注册的service及其对应域名/IP/Port的动态添加和解析。



# 日志

## 基础方式

日志被写入到标准输出，`kubectl logs`查看日志。一旦发生容器崩溃，您可以使用命令 `kubectl logs` 和参数 `--previous` 检索之前的容器日志。

## Docker日志驱动

Docker容器引擎`stdout` 和 `stderr`这两个输出流重定向到某个 [日志驱动](https://docs.docker.com/engine/admin/logging/overview) ，将日志写入文件

运行容器时，可以通过命令行参数指定logging driver的类型

使用 Docker 的 `log-opt` 选项控制日志轮转

默认情况下，如果容器重启，kubelet 会保留被终止的容器日志。
如果 pod 在工作节点被驱逐，该 pod 中所有的容器也会被驱逐，包括容器日志。

# 配置

## 配置最佳实践

- 相关的配置尽量放到同一个yaml文件里。
- 许多`kubectl`支持目录执行，如kubectl apply
- 避免不必要的指定默认值
- pods最好绑定到[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)下
- 避免使用`hostNetwork`、hostPort，会限制Pod调度
- Use label selectors for `get` and `delete` operations instead of specific object names

## yaml

## 创建部署

```shell
kubectl apply -f https://k8s.io/examples/application/deployment.yaml --record

kubectl diff -R -f configs/
kubectl apply -R -f configs/
```

## Update Rolling



```shell
# 查看所有Pods中容器的镜像版本
kubectl describe pods
# 使用新镜像升级
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2

# 查看升级后版本，以及停止的旧Pods、创建的新Pods
kubectl get pods
# 查看升级后镜像版本
kubectl describe pods

# 升级失败后可以回退
kubectl rollout
```

## kubectl

- **kubectl get** - list resources
- **kubectl describe** - show detailed information about a resource
- **kubectl logs** - print the logs from a container in a pod
- **kubectl exec** - execute a command on a container in a pod

```shell
# 打开容器的bash作为终端
kubectl exec -ti <podname> [-c <container_name>]

# 标签过滤
kubectl get pods或nodes -l <label-key>=<label-value> -o wide或yaml

# svc是service的简写
kubectl describe svc my-nginx
kubectl get svc my-nginx

# 查看pod内的环境变量
kubectl exec <podname> -- printenv


```





