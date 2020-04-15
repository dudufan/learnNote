```http
http://localhost:8080/restart
http://localhost:8080/reload
http://localhost:8080/exit
#!/bin/bash
export JENKINS_HOME=/d/Programs/jenkins
java -jar jenkins.war > console.log 2>&1 &
```



# 安装



1. 官方中文网上下载war包
2. 插件安装



## 安装插件

步骤如下。

升级站点为http://mirror.xmission.com/jenkins/updates/current/update-center.json，否则会提示离线。

重启jenkins继续进入插件安装页，先不安装

cloudbees-folder.hpi可能需要自己下载放在/usr/local/tomcatJenkins-8090/webapps/jenkins/WEB-INF/detached-plugins。

修改镜像源地址提速

```shell
sed -i 's/http:\/\/updates.jenkins-ci.org\/download/https:\/\/mirrors.tuna.tsinghua.edu.cn\/jenkins/g' default.json && sed -i 's/http:\/\/www.google.com/https:\/\/www.baidu.com/g' default.json
```

重启后继续安装建议插件

# 配置

步骤：

1. 全局配置各类插件的参数
2. 配置Job
3. Python-jenkins可以批量创建Job
4. Jenkins命令行控制台使用Groovy脚本。如清空所有服务的构建历史

# 管理

```http
http://localhost:8080/restart
http://localhost:8080/reload
http://localhost:8080/exit

```

## 批量删除构建历史

jenkins命令行

```groovy
//maxNumber :  最大构建编号,比它大的保留，比它小的删掉
def maxNumber = 0
def jobnames = Jenkins.get().getJobNames()
for(String jobName: jobnames){
	Jenkins.instance.getItemByFullName(jobName).builds.findAll {
          it.number >= maxNumber
        }.each {
          it.delete()
        }
        
}
```

## Job管理

```python
server.create_job('folder', jenkins.EMPTY_FOLDER_XML)  # 创建一个文件夹

server.copy_job('folder/empty', 'folder/empty_copy')  # 复制
server.delete_job('folder/empty_copy')  # 删除job
server.delete_job('folder')  # 删除文件夹

```

如果找不到EMPTY_FOLDER_XML是因为jenkins/__init__.py中没有定义

在jenkins/__init.py中130行后添加

 EMPTY_FOLDER_XML = '''<?xml version='1.0' encoding='UTF-8'?>
 <com.cloudbees.hudson.plugins.folder.Folder plugin="cloudbees-folder@6.1.2">
   <actions/>
   <description></description>
   <properties/>
   <folderViews/>
   <healthMetrics/>
 </com.cloudbees.hudson.plugins.folder.Folder>'''
————————————————
版权声明：本文为CSDN博主「慕清风」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/seeeees/article/details/79397033



脚本创建参数化构建任务

```python
import jenkins
server = jenkins.Jenkins('http://192.168.59.149:28080', username='jenkins', password='jenkins@!23')
server.build_job('jxInstantQuery')
server.build_job('jxInstantQuery2', {'param1': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'param2': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'})
```



# Bug

## SAXParser

Problem:SAX2 driver class org.apache.xerces.parsers.SAXParser not found

解决办法两种：

jenkins启动参数增加

```shell
-Dorg.xml.sax.driver=com.sun.org.apache.xerces.internal.parsers.SAXParser
```

或者在jenkins Web上的脚本命令行控制台执行命令：

```groovy
println System.getProperty('org.xml.sax.driver')
System.setProperty('org.xml.sax.driver', 'com.sun.org.apache.xerces.internal.parsers.SAXParser')
println System.getProperty('org.xml.sax.driver')
```

# Python-jenkins

## 触发构建

## 查询构建信息

```python
server.create_job('empty', jenkins.EMPTY_CONFIG_XML)
jobs = server.get_jobs()
print jobs
my_job = server.get_job_config('cool-job')
print(my_job) # prints XML configuration
server.build_job('empty')
server.disable_job('empty')
server.copy_job('empty', 'empty_copy')
server.enable_job('empty_copy')
server.reconfig_job('empty_copy', jenkins.RECONFIG_XML)

server.delete_job('empty')
server.delete_job('empty_copy')

# build a parameterized job
# requires creating and configuring the api-test job to accept 'param1' & 'param2'
server.build_job('api-test', {'param1': 'test value 1', 'param2': 'test value 2'})
last_build_number = server.get_job_info('api-test')['lastCompletedBuild']['number']
build_info = server.get_build_info('api-test', last_build_number)
print build_info

# get all jobs from the specific view
jobs = server.get_jobs(view_name='View Name')
print jobs
```

# javadoc

当执行javadoc:javadoc后，点击javadoc链接，发现只有主frame，内容不能正常显示。

原因参见<https://wiki.jenkins.io/display/JENKINS/Configuring+Content+Security+Policy> 原来是安全方面的考虑。

修复方法如下：

进入manage jenkins —  script console，执行

```
System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "default-src 'none'; img-src 'self'; style-src 'self'; child-src 'self'; frame-src 'self'; script-src 'unsafe-inline';")
```

即可。

可以参见<https://issues.jenkins-ci.org/browse/JENKINS-32619>