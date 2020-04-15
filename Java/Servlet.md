## web项目目录结构
src/main/java
src/main/webapp/
 
## build.gradle
```
// 创建Java项目插件，提供了所有构建和测试Java程序所需项目结构
apply plugin: 'java'
// 引入Maven插件，以便Gradle可以引用Maven仓库的Jar包
apply plugin: 'maven'
// 进行打包插件
apply plugin: 'war'
// Web项目服务器插件,此处配置后，不需再单独配置Web服务器
apply plugin: 'jetty'
// Web项目开发插件
apply plugin: 'eclipse'
 
// 启动jetty容器的配置参数, 执行gradle jettyRun时使用
jettyRun {
    // 自动热切换
    reload = "automatic"
    scanIntervalSeconds = 0
    // http端口号
    httpPort = 8088
    // 停止jetty容器
    stopPort = 8082
    stopKey = "stopKey"
}
 
```
 
## web.xml
 
## Servlet
servlet的类不能再默认包里，必须在某个包中
```
package com;
import java.io.IOException;
import java.io.PrintWriter;
 
 
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
 
 
public class HelloWorldSerlet extends HttpServlet{
private static final long serialVersionUID = 1L;
private String message;
public void init() throws ServletException{
message = "Hello World v4.0";
  }
@Override
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
throws ServletException, IOException{
PrintWriter out = resp.getWriter();
// message = "Hello World v2.0";
out.print("<h1>" + message + "</h1>");
out.flush();
out.close();
super.doGet(req, resp);
}
public void destroy()
  {
      // 什么也不做
  }
}
```
对应配置的web.xml如下
```
<? xml   version = "1.0"   encoding = "ISO-8859-1" ?>  
< web-app   xmlns = "http://java.sun.com/xml/ns/javaee"  
     xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"  
     xsi:schemaLocation = "http://java.sun.com/xml/ns/javaee 
    http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" 
     version = "3.0"  
     metadata-complete = "true" >  
< servlet >  
        < servlet-name > example </ servlet-name >  
        < servlet-class > com.HelloWorldSerlet </ servlet-class >  
    </ servlet >  
    < servlet-mapping >  
        < servlet-name > example </ servlet-name >  
        < url-pattern > / helloworld </ url-pattern >  
    </ servlet-mapping >         
</ web-app > 
```