[TOC]

# 参考

《http权威指南》  强烈推荐
图解HTTP 

# REST API

## RESTful

### URL Root

两种实践方式：

[https://example.org/api/v1/](https://link.zhihu.com/?target=https%3A//example.org/api/v1/)*
[https://api.example.com/v1/](https://link.zhihu.com/?target=https%3A//api.example.com/v1/)*



### URL使用名词

GET /products : will return the list of all products

POST /products : will add a product to the collection

GET /products/4 : will retrieve product #4

PATCH/PUT /products/4 : will update product #4



### API versioning

versioin可以放在URL里面，也可以用HTTP的header：
/api/v1/

## 框架实现

-- Server --
推荐： Spring MVC 或者 Jersey 或者 Play Framework
教程：
[Getting Started · Building a RESTful Web Service](https://link.zhihu.com/?target=https%3A//spring.io/guides/gs/rest-service/)

-- Web --
推荐随便搞！可以用重量级的AngularJS，也可以用轻量级 Backbone + jQuery 等。
教程：[http://blog.javachen.com/2015/01/06/build-app-with-spring-boot-and-gradle/](https://link.zhihu.com/?target=http%3A//blog.javachen.com/2015/01/06/build-app-with-spring-boot-and-gradle/)



# CROS

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS

跨域资源共享([CORS](https://developer.mozilla.org/en-US/docs/Glossary/CORS)) 是一种机制，它使用额外的 [HTTP](https://developer.mozilla.org/en-US/docs/Glossary/HTTP) 头来告诉浏览器，让运行在一个 origin (domain) 上的Web应用被准许访问来自其他源服务器上的指定资源。

比如，站点 http://domain-a.com 的某 HTML 页面通过 [ 的 src ](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/Img#Attributes)请求 http://domain-b.com/image.jpg。网络上的许多页面都会加载来自不同域的CSS样式表，图像和脚本等资源。

出于安全原因，浏览器限制从脚本内发起的跨源HTTP请求，或者拦截了响应。



## 如何允许跨域

使用 [`Origin`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Origin) 和 [`Access-Control-Allow-Origin`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Access-Control-Allow-Origin) 就能完成最简单的访问控制。Access-Control-Allow-Origin 应当为 * 或者包含由 请求Origin 首部字段所指明的域名。

```http
# 除了 http://foo.example，其它外域均不能访问该资源
Access-Control-Allow-Origin: http://foo.example
# 该资源可以被任意外域访问
Access-Control-Allow-Origin: *

```



预检请求

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS#%E9%A2%84%E6%A3%80%E8%AF%B7%E6%B1%82

## 跨域携带cookie

- 请求使用`XMLHttpRequest `或ajax时， `withCredentials 标志设置为 true`
- 服务器端的响应中携带 `Access-Control-Allow-Credentials: true ，浏览器才会把响应内容返回给请求的发送者。`
- 如果响应中 Access-Control-Allow-Origin 的值为“*”，携带了 Cookie 信息的请求将会失败。而将 Access-Control-Allow-Origin 的值设置为 `http://foo.example，则请求将成功执行。

# 缓存机制

## Cache-Control

HTTP1.1 支持Cache-Control

HTTP1.0 Expires

```html
# 过期，单位秒。请求设置max-age=0会使浏览器向服务器确认本地缓存是否过期，未过期则使用本地缓存。
# 响应中告诉浏览器过期时间
Cache-Control: max-age=31536000


# 每次由客户端发起的请求都会下载完整的响应内容，下载后会缓存
Cache-Control: no-cache
# 不存储任何关于客户端请求和服务端响应的内容（一般不用）
Cache-Control: no-store
Cache-Control: no-cache, no-store

# 每次浏览器都会发请求到服务器确认缓存是否过期
Cache-Control: must-revalidate

#  "private" 则表示该响应是专用于某单个用户的，中间人不能缓存此响应，该响应只能应用于浏览器私有缓存中
Cache-Control: private
Cache-Control: public
```

## 缓存验证

https://www.cnblogs.com/zhaow/p/7832829.html

`Expires`告诉浏览器副本何时过期。

何时校验：

- 浏览器本地的副本已经过期（无论是否开启缓存）
- 请求头强制确认缓存是否过期`Cache-Control: max-age=0`、`Cache-Control: must-revalidate`



如何校验缓存：

- 前一次响应报文有响应头[`ETag`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/ETag)或`Last-Modified`头。

- 给请求附加`If-None-Match`（对应`ETag`)或 `If-Modified-Since`(对应`Last-Modified`)头，然后发给服务器，服务器确认是否新鲜。
- 若服务器返回了 [`304`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304) (Not Modified)（该响应没有Body），则表示此资源副本是新鲜的，节省带宽。
- 若服务器通过 If-None-Match 或 If-Modified-Since判断后发现已过期，那么会带有该资源的实体内容返回。

# CSRF

CSRF（Cross-site request  forgery）跨站请求伪造：攻击者诱导受害者进入第三方网站，在第三方网站中，向被攻击网站发送跨站请求。利用受害者在被攻击网站已经获取的注册凭证，绕过后台的用户验证，达到冒充用户对被攻击的网站执行某项操作的目的。

一个典型的CSRF攻击有着如下的流程：

- 受害者登录a.com，并保留了登录凭证（Cookie）。
- 攻击者引诱受害者访问了b.com。
- b.com通过表单或图片URL等方式向 a.com 发送了一个请求：a.com/act=xx。浏览器会默认携带a.com的Cookie。
- a.com接收到请求后，对请求进行验证，并确认是受害者的凭证，误以为是受害者自己发送的请求。
- a.com以受害者的名义执行了act=xx。
- 攻击完成，攻击者在受害者不知情的情况下，冒充受害者，让a.com执行了自己定义的操作。

**CSRF的特点**

- 攻击一般发起在第三方网站，而不是被攻击的网站。被攻击的网站无法防止攻击发生。
- 攻击利用受害者在被攻击网站的登录凭证，冒充受害者提交操作；而不是直接窃取数据。
- 整个过程攻击者并不能获取到受害者的登录凭证，仅仅是“冒用”。
- 跨站请求可以用各种方式：图片URL、超链接、CORS、Form提交等等。部分请求方式可以直接嵌入在第三方论坛、文章中，难以进行追踪。

## CSRF Token

要求所有的用户请求都携带一个CSRF攻击者无法获取到的Token。服务器通过校验请求是否携带正确的Token，来把正常的请求和攻击的请求区分开，也可以防范CSRF的攻击。

分为三个步骤：

1. 将CSRF Token输出到页面中
2. 页面提交的请求携带这个Token
3. 服务器验证Token是否正确

实现：

Token可以在产生并放于Session之中，然后在每次请求时把Token从Session中拿出，与请求中的Token进行比对

缺点：不能在通用的拦截上统一拦截处理，而需要每一个页面和接口都添加对应的输出和校验，导致工作量巨大

相比而言，验证码和密码其实也可以起到CSRF Token的作用，而且更安全

## 双重Cookie验证

利用CSRF攻击不能获取到用户Cookie的特点，我们可以要求Ajax和表单请求携带一个Cookie中的值。

采用以下流程：

- 在用户访问网站页面时，向请求域名注入一个Cookie，内容为随机字符串（例如`csrfcookie=v8g9e4ksfhw`）。
- 在前端向后端发起请求时，取出Cookie，并添加到URL的参数中（接上例`POST https://www.a.com/comment?csrfcookie=v8g9e4ksfhw`）。
- 后端接口验证Cookie中的字段与URL参数中的字段是否一致，不一致则拒绝。

此方法相对于CSRF Token就简单了许多。可以直接通过前后端拦截的的方法自动化实现。后端校验也更加方便，只需进行请求中字段的对比，而不需要再进行查询和存储Token。

当然，此方法并没有大规模应用，其在大型网站上的安全性还是没有CSRF Token高。

由于任何跨域都会导致前端无法获取Cookie中的字段（包括子域名之间），于是发生了如下情况：

- 如果用户访问的网站为`www.a.com`，而后端的api域名为`api.a.com`。那么在`www.a.com`下，前端拿不到`api.a.com`的Cookie，也就无法完成双重Cookie认证。
- 于是这个认证Cookie必须被种在`a.com`下，这样每个子域都可以访问。
- 任何一个子域都可以修改`a.com`下的Cookie。
- 某个子域名存在漏洞被XSS攻击（例如`upload.a.com`）。虽然这个子域下并没有什么值得窃取的信息。但攻击者修改了`a.com`下的Cookie。
- 攻击者可以直接使用自己配置的Cookie，对XSS中招的用户再向`www.a.com`下，发起CSRF攻击。

## JWT

用来替代session、cookie进行认证授权。

JWT 的原理：

服务器认证以后，生成一个 JSON 对象，发回给用户。

以后，用户与服务端通信的时候，都要发回这个 JSON 对象。服务器完全只靠这个对象认定用户身份。为了防止用户篡改数据，服务器在生成这个对象的时候，会加上签名（详见后文）。

服务器就不保存任何 session 数据了，也就是说，服务器变成无状态了，从而比较容易实现扩展。

使用步骤：

1. 服务器通过`Payload`、`Header`和一个密钥(`secret`)创建令牌（`Token`）并将 `Token` 发送给客户端
2. 客户端将 `Token` 保存在 Cookie 或者 localStorage 里面，以后客户端发出的所有请求都会携带这个令牌。
3. 因为 Cookie 容易受 [CSRF](https://www.owasp.org/index.php/Cross-Site_Request_Forgery) (跨站请求伪造)的影响并且不能跨域，所以更好的做法是放在 HTTP  Header 的 Authorization字段中：` Authorization: Bearer Tokenxxx`
4. 另一种做法是，跨域的时候，JWT 就放在 POST 请求的数据体里面

入门 https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html

https://juejin.im/entry/577b7b56a3413100618c2938



实际的JWT是一个很长的字符串，中间用点（`.`）分隔成三个部分。注意，JWT 内部没有换行：

```js
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiBEb2UiLCJhZG1pbiI6dHJ1ZX0.OLvs36KmqB9cmsUrMpUutfhV52_iSz4bQMYJjkI_TLQ
```



构成：

- Header（头部），描述 JWT 的元数据。
- Payload 部分也是一个 JSON 对象，用来存放实际需要传递的数据
- 签名

**Header**

```javascript
{
  "alg": "HS256",
  "typ": "JWT"
}
```

`alg`属性表示签名的算法（algorithm），默认是 HMAC SHA256（写成 HS256）；`typ`属性表示这个令牌（token）的类型（type），JWT 令牌统一写为`JWT`。

**Payload**

JWT 规定了7个官方字段，供选用，如下面的sub。还可以在这个部分定义私有字段

```javascript
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

注意，JWT 默认是不加密的，任何人都可以读到，所以不要把秘密信息放在这个部分。



示例。生成JWT

```js
var header = {  
        // The signing algorithm.
        "alg": "HS256",
        // The type (typ) property says it's "JWT",
        // because with JWS you can sign any type of data.
        "typ": "JWT"
    },
    // Base64 representation of the header object.
    headerB64 = btoa(JSON.stringify(header)),
    // The payload here is our JWT claims.
    payload = {
        "name": "John Doe",
        "admin": true
    },
    // Base64 representation of the payload object.
    payloadB64 = btoa(JSON.stringify(payload)),
    // The signature is calculated on the base64 representation
    // of the header and the payload.
    signature = signatureCreatingFunction(headerB64 + '.' + payloadB64),
    // Base64 representation of the signature.
    signatureB64 = btoa(signature),
    // Finally, the whole JWS - all base64 parts glued together with a '.'
    jwt = headerB64 + '.' + payloadB64 + '.' + signatureB64;
//得到结果,也就是JWT Token：eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiBEb2UiLCJhZG1pbiI6dHJ1ZX0.OLvs36KmqB9cmsUrMpUutfhV52_iSz4bQMYJjkI_TLQ
```

https://jwt.io/#debugger

特点：

（1）JWT 默认是不加密，但也是可以加密的。生成原始 Token 以后，可以用密钥再加密一次。

（2）JWT 不加密的情况下，不能将秘密数据写入 JWT。

（3）JWT 不仅可以用于认证，也可以用于交换信息。有效使用 JWT，可以降低服务器查询数据库的次数。

（4）JWT 的最大缺点是，由于服务器不保存 session 状态，因此无法在使用过程中废止某个 token，或者更改 token 的权限。也就是说，一旦 JWT 签发了，在到期之前就会始终有效，除非服务器部署额外的逻辑。

（5）JWT 本身包含了认证信息，一旦泄露，任何人都可以获得该令牌的所有权限。为了减少盗用，JWT 的有效期应该设置得比较短。对于一些比较重要的权限，使用时应该再次对用户进行认证。

（6）为了减少盗用，JWT 不应该使用 HTTP 协议明码传输，要使用 HTTPS 协议传输。

# OAuth

简单来说，OAuth 就是一种授权机制。

1. 第三方应用申请授权

2. 数据的所有者告诉系统，同意授权第三方应用进入系统，获取这些数据。
3. 系统从而产生一个短期的进入令牌（token），用来代替密码，供第三方应用使用

OAuth2.0的四种方式 http://www.ruanyifeng.com/blog/2019/04/oauth-grant-types.html

返回access_token一般就是调用微信或github等提供的api，需要跨域。个人理解获取accessToken以及获取用户信息的api，都是允许跨域的

实践 http://www.ruanyifeng.com/blog/2019/04/github-oauth.html

**凭证式授权方式**

凭证式（client credentials），这种方式给出的令牌，是针对第三方应用的，而不是针对用户的，即有可能多个用户共享同一个令牌。

第一步，A 应用在命令行向 B 发出请求。

> ```javascript
> https://oauth.b.com/token?
>   grant_type=client_credentials&
>   client_id=CLIENT_ID&
>   client_secret=CLIENT_SECRET
> ```

上面 URL 中，`grant_type`参数等于`client_credentials`表示采用凭证式，`client_id`和`client_secret`用来让 B 确认 A 的身份。

第二步，B 网站验证通过以后，直接返回令牌。



scope参数: 跳转申请授权页面时带上这个参数，后面获取的code权限范围是相应的

state参数：防止CSRF攻击。https://www.jianshu.com/p/c7c8f51713b6

**SSO与OAuth2.0的区别**

OAuth 是一个行业的标准授权协议，主要用来授权第三方应用获取有限的权限。SSO解决的是一个公司的多个相关的自系统的之间的登陆问题比如京东旗下相关子系统京东金融、京东超市、京东家电等等。



# 锚点

浏览器用锚点URL跳转时，锚点信息不会发到服务器

OAuth 2.0隐藏式的授权不涉及后端，因此微信给A网站授权时跳回https://a.com/callback#token=ACCESS_TOKEN

# OIDC

openID connect在OAuth2基础上优化了认证的部分，兼容OAuth2

和OAuth2的区别：

1. scope提供了“openId”，表示使用OIDC
2. openId服务器除了返回accessToken，还返回了JWT格式的id_token（包含了用户最基本信息）
3. 后续服务通过Header`Authorization` 携带accesstoken访问/userinfo端点，获取用户信息

```http
  GET /userinfo HTTP/1.1
  Host: server.example.com
  Authorization: Bearer SlAV32hkKG
```