[TOC]

4月 9 11 15 17 23 24 26

# 概述

Subject是当前执行用户，可进行登录登出、访问session、执行权限检查等

SecurityManager负责管理所有用户，是伞结构的骨架，可以引用各种安全组件。

Realms连接Shiro和应用安全数据，负责实际校验用户信息。

Permission对应应用功能。Role和用户也可以绑定多个Permission

```java
//1. Load the INI configuration
Factory<SecurityManager> factory =
new IniSecurityManagerFactory("classpath:shiro.ini");

//2. Create the SecurityManager
SecurityManager securityManager = factory.getInstance();

//3. Make it accessible
SecurityUtils.setSecurityManager(securityManager);
```

# 配置

ini

```
[main]
# Objects and their properties are defined here,
# Such as the securityManager, Realms and anything
# else needed to build the SecurityManager
credentialsMatcher = org.apache.shiro.authc.credential.Sha256CredentialsMatcher
# base64 encoding, not hex in this example:
credentialsMatcher.storedCredentialsHexEncoded = false
credentialsMatcher.hashIterations = 1024
# This next property is only needed in Shiro 1.0\.  Remove it in 1.1 and later:
credentialsMatcher.hashSalted = true

databaseRealm=com.how2java.DatabaseRealm
securityManager.realms=$databaseRealm
databaseRealm.credentialsMatcher=$credentialsMatcher

securityManager.sessionManager.globalSessionTimeout = 1800000

[users]
# The 'users' section is for simple deployments
# when you only need a small number of statically-defined
# set of User accounts.

[roles]
# The 'roles' section is for simple deployments
# when you only need a small number of statically-defined
# roles.

[urls]
# The 'urls' section is used for url-based security
# in web applications.  We'll discuss this section in the
# Web documentation
```

# Realm



## 认证

MyRealm需要实现Realm接口

1. Realm.supports方法确认是否支持此种校验token。比如处理生物识别信息的Realm也许不能处理`UsernamePasswordTokens` 。
2. `Authenticator` 调用这个Realm的 [getAuthenticationInfo(token)](http://shiro.apache.org/static/current/apidocs/org/apache/shiro/realm/Realm.html#getAuthenticationInfo-org.apache.shiro.authc.AuthenticationToken-) 
3. `principal`相当于用户账号，从数据源中查找账户。
4. 数据提交到`CredentialsMatcher` ，检查密码`credentials`是否匹配。默认使用`SimpleCredentialsMatcher` 。
5. 匹配则返回用户数据[AuthenticationInfo](http://shiro.apache.org/static/current/apidocs/org/apache/shiro/authc/AuthenticationInfo.html) 

## 权限校验

需要实现`Authorizer`接口



## 存储密码密文

```ini
[main]
credentialsMatcher=org.apache.shiro.authc.credential.HashedCredentialsMatcher
credentialsMatcher.hashAlgorithmName=md5
#credentialsMatcher.hashAlgorithmName=SHA-256
credentialsMatcher.hashIterations=2
credentialsMatcher.storedCredentialsHexEncoded=true

databaseRealm=com.how2java.DatabaseRealm
databaseRealm.credentialsMatcher=$credentialsMatcher
securityManager.realms=$databaseRealm
```



注意返回时，要将MD5加密后的密码传入构造器

```
SimpleAuthenticationInfo a = new SimpleAuthenticationInfo(userName,userInDB.getPassword(), ByteSource.Util.bytes(userInDB.getSalt()), getName());
```

# 登录



```
//1. Acquire submitted principals and credentials:
AuthenticationToken token =
new UsernamePasswordToken(username, password);
//2. Get the current Subject:
 Subject currentUser = SecurityUtils.getSubject();

//3. Login:
 try {
    currentUser.login(token);
} catch  ( UnknownAccountException uae ) { ...
} catch  ( IncorrectCredentialsException ice ) { ...
} catch  ( LockedAccountException lae ) { ...
} catch  ( ExcessiveAttemptsException eae ) { ...
} ...  your own ...
} catch ( AuthenticationException ae ) {
    //unexpected error?
}
//No problems, show authenticated view…
 
 currentUser.logout(); //removes all identifying information and invalidates their session too.

```





>When the login method is called, the SecurityManager will receive the 
>AuthenticationToken and dispatch it to one or more configured Realms to 
>allow each to perform authentication checks as required. Each Realm has 
>the ability to react to submitted AuthenticationTokens as necessary.

# Permission

- 资源级别。某个表，某类操作
- 实例级别，相当于某一条记录、具体某一个操作
- 属性级别。相当于某条记录的某属性

> It is important to understand that permissions do not have knowledge of *who* can perform the actions– they are just statements of *what* actions can be performed.

# Remember me

subject有两个方法[`isRemembered()`](http://shiro.apache.org/static/current/apidocs/org/apache/shiro/subject/Subject.html#isRemembered--) and [`isAuthenticated()`](http://shiro.apache.org/static/current/apidocs/org/apache/shiro/subject/Subject.html#isAuthenticated--)

敏感信息如修改用户信息，需要isAuthenticated()= True，个性化推荐可以`isRemembered() = TRUE`

# 过滤器

默认过滤器

http://shiro.apache.org/web.html#default-filters

main中配置过滤器，urls中使用过滤器

使用过滤器方法：

- 可以选择启动禁用某些过滤器
-  

