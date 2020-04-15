

# 版本

不加声明，则为Bootstrap4

# 基础

# 使用方法

```html
 
<!DOCTYPE html>
<html>
   <head>
      <title>Bootstrap 模板</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!-- 引入 Bootstrap -->
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
 
      <!-- HTML5 Shiv 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
      <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
      <!--[if lt IE 9]>
         <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
         <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
      <![endif]-->
   </head>
   <body>
      <h1>Hello, world!</h1>
 
      <!-- jQuery (Bootstrap 的 JavaScript 插件需要引入 jQuery) -->
      <script src="https://code.jquery.com/jquery.js"></script>
      <!-- 包括所有已编译的插件 -->
      <script src="js/bootstrap.min.js"></script>
   </body>
</html>
 
```

CDN

```
 
<!-- 新 Bootstrap 核心 CSS 文件 -->
<link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
 
<!-- 可选的Bootstrap主题文件（一般不使用） -->
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"></script>
 
<!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
<script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
 
<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
 
```

# 概览

## 对移动设备友好

```
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## 响应式图像

```
<img src="..." class="img-responsive" alt="响应式图像">
```

```
.img-responsive {
  display: block;
  height: auto;
  max-width: 100%;
}
```

## bootstrap.bundle.js

`bootstrap.bundle.js` 包含Popper

## Reboot

调整样式，适应不同浏览器和设备

## 避免跨浏览器的不一致

Bootstrap 使用 [Normalize](http://necolas.github.io/normalize.css/) 来建立跨浏览器的一致性。

## 媒体查询

下面的媒体查询在 LESS 文件中使用，用来创建 Bootstrap 网格系统中的关键的分界点阈值。

```
/* 超小设备（手机，小于 768px） */
/* Bootstrap 中默认情况下没有媒体查询 */
 
/* 小型设备（平板电脑，768px 起） */
@media (min-width: @screen-sm-min) { ... }
 
/* 中型设备（台式电脑，992px 起） */
@media (min-width: @screen-md-min) { ... }
 
/* 大型设备（大台式电脑，1200px 起） */
@media (min-width: @screen-lg-min) { ... }
```

我们有时候也会在媒体查询代码中包含 **max-width**，从而将 CSS 的影响限制在更小范围的屏幕大小之内。

##  一个简单Bootstrap网页示例

```html
 
<div class="jumbotron text-center" style="margin-bottom:0">
  <h1>我的第一个 Bootstrap 页面</h1>
  <p>重置浏览器窗口大小查看效果！</p>
</div>
 
<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>                       
      </button>
      <a class="navbar-brand" href="#">网站名</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">主页</a></li>
        <li><a href="#">页面 2</a></li>
        <li><a href="#">页面 3</a></li>
      </ul>
    </div>
  </div>
</nav>
 
<div class="container">
  <div class="row">
    <div class="col-sm-4">
      <h2>关于我</h2>
      <h5>我的照片:</h5>
      <div class="fakeimg">这边插入图像</div>
      <p>关于我的介绍..</p>
      <h3>链接</h3>
      <p>描述文本。</p>
      <ul class="nav nav-pills nav-stacked">
        <li class="active"><a href="#">链接 1</a></li>
        <li><a href="#">链接 2</a></li>
        <li><a href="#">链接 3</a></li>
      </ul>
      <hr class="hidden-sm hidden-md hidden-lg">
    </div>
    <div class="col-sm-8">
      <h2>标题</h2>
      <h5>副标题</h5>
      <div class="fakeimg">图像</div>
      <p>一些文本..</p>
      <p>菜鸟教程，学的不仅是技术，更是梦想！！！菜鸟教程，学的不仅是技术，更是梦想！！！菜鸟教程，学的不仅是技术，更是梦想！！！</p>
      <br>
      <h2>标题</h2>
      <h5>副标题</h5>
      <div class="fakeimg">图像</div>
      <p>一些文本..</p>
      <p>菜鸟教程，学的不仅是技术，更是梦想！！！菜鸟教程，学的不仅是技术，更是梦想！！！菜鸟教程，学的不仅是技术，更是梦想！！！</p>
    </div>
  </div>
</div>
 
<div class="jumbotron text-center" style="margin-bottom:0">
  <p>底部内容</p>
</div>
 
```

 

# 网格系统

响应式断点主要使用@media (min-width: xxxpx) { ... }实现，个别场景使用max-width

- 行必须放置在 **.container** class 内，以便获得适当的对齐（alignment）和内边距（padding）。
- 行里面只能直接放列，列中才能放内容。
- 使用比如 **.row** 和 **.col-xs-4**，快速创建网格布局。xs在min-width:0时生效。
- 列通过内边距（padding）来创建列内容之间的间隙。该内边距是通过 **.rows** 上的外边距（margin）取负，表示第一列和最后一列的行偏移。
- 断点基于最小宽度媒体查询，有五种：col col-sm col-md col-lg col-xl

.container fixed width

.container-fluid full width

.col-sm 自动平分页面宽度

.col-sm-4 4/12页面宽度

## container

用于包裹页面上的内容，左右外边距（margin-right、margin-left）交由浏览器决定。

```
.container {
   padding-right: 15px;
   padding-left: 15px;
   margin-right: auto;
   margin-left: auto;
}
```

Bootstrap 3 CSS 有一个申请响应的媒体查询，在不同的媒体查询阈值范围内都为 container 设置了max-width，用以匹配网格系统。

```
@media (min-width: 768px) {
   .container {
      width: 750px;
}
```
导航栏和页面主要内容可以有各自独立的container



## row

用来包裹列，列之间会有padding

## 尺寸

Bootstrap使用em、rem定义大多数尺寸，但用px定义断点和container宽度。因为视图是用px计算的，而不是字体大小。



Grid的断点都是基于最小尺寸媒体查询。col col-4应用于所有。

对列宽度无要求时，使用col会自动均分（剩余）宽度。

> e.g., `.col-sm-4` applies to small, medium, large, and extra large devices, but not the first `xs` breakpoint

列可以嵌套。

`.px-lg-5`可以给container、row、col增加水平方向padding

`.mx-lg-n5` 设置-5的负margin

## 对齐

https://getbootstrap.com/docs/4.3/layout/grid/#alignment

水平对齐

## 偏移列

bootstrap3支持，bootstrap4已经移除列偏移特性，改为由flex实现的元素对齐方式

使用 **.col-md-offset-\*** 类 .这些类会把一个列的左外边距（margin）增加 ***** 列，其中 ***** 范围是从 **1** 到 **11**。

<div class="col-md-6">..</div>，我们将使用 **.col-md-offset-3** class 来居中这个 div。
## 列排序

**.col-md-push-\*** 和 **.col-md-pull-\*** 类能改变内置网格列的顺序，其中 ***** 范围是从 **1** 到 **11**。数字越小越靠左。



# 布局组件

[Boostrap排版-菜鸟](http://www.runoob.com/bootstrap/bootstrap-typography.html)

## 内联副标题

在元素两旁添加 <small>，或者添加 **.small** class，这样子您就能得到一个字号更小的颜色更浅的文本

## 无序列表

使用 class *.list-unstyled* 来移除样式。您也可以通过使用 class *.list-inline* 把所有的列表项放在同一行中。

`dl-horizontal` 可以让 `<dl>` 内的短语及其描述排在一行

```
<dl class="dl-horizontal">
  <dt>Description 1</dt>
  <dd>Item 1</dd>
  <dt>Description 2</dt>
  <dd>Item 2</dd>
</dl>
```

## 按钮

```html
<!-- 标准的按钮 -->
<button type="button" class="btn btn-default">默认按钮</button>
<!-- 提供额外的视觉效果，标识一组按钮中的原始动作 -->
<button type="button" class="btn btn-primary">原始按钮</button>
<!-- 表示一个成功的或积极的动作 -->
<button type="button" class="btn btn-success">成功按钮</button>
<!-- 信息警告消息的上下文按钮 -->
<button type="button" class="btn btn-info">信息按钮</button>
<!-- 表示应谨慎采取的动作 -->
<button type="button" class="btn btn-warning">警告按钮</button>
<!-- 表示一个危险的或潜在的负面动作 -->
<button type="button" class="btn btn-danger">危险按钮</button>
<!-- 并不强调是一个按钮，看起来像一个链接，但同时保持按钮的行为 -->

.btn-block 占满整行
.btn-outline-success 轮廓有颜色，中间无色。更简约
.btn-outline-danger
```

- 可用于```<a>, <button>, 或 <input>``` 元素上
- btn提供基本样式

## 图片

https://getbootstrap.com/docs/4.3/content/images/

| img-rounded    | 为图片添加圆角 (IE8 不支持)       |
| -------------- | --------------------------------- |
| .img-circle    | 将图片变为圆形 (IE8 不支持)       |
| .img-thumbnail | 缩略图功能                        |
| .img-fluid     | 图片响应式 (将很好地扩展到父元素) |

.img-responsive 图片响应式

```html
 图片水平居中
<img src="..." class="rounded mx-auto d-block" alt="...">
<div class="text-center">
  <img src="..." class="img-fluid" alt="...">
</div>
左对齐
<img src="..." class="rounded float-left" alt="...">
```

## 字体、图标

```
<button type="button" class="btn btn-primary btn-lg" style="font-size: 60px">
  <span class="glyphicon glyphicon-user"></span> User
</button>
```

```
style="color: rgb(212, 106, 64);text-shadow: black 5px 3px 3px;font-size: 60px"
```

## 下拉菜单

```
 
<div class="dropdown">
    <button type="button" class="btn dropdown-toggle" id="dropdownMenu1" data-toggle="dropdown">主题
        <span class="caret"></span>
    </button>
    <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
        <li role="presentation" class="dropdown-header">下拉菜单标题</li>
        <li role="presentation">
            <a role="menuitem" tabindex="-1" href="#">Java</a>
        </li>
        <li role="presentation">
            <a role="menuitem" tabindex="-1" href="#">数据挖掘</a>
        </li>
        <li role="presentation">
            <a role="menuitem" tabindex="-1" href="#">数据通信/网络</a>
        </li>
        <li role="presentation" class="divider"></li>
        <li role="presentation" class="dropdown-header">下拉菜单标题</li>
        <li role="presentation">
            <a role="menuitem" tabindex="-1" href="#">分离的链接</a>
        </li>
    </ul>
</div>
 
```

下拉菜单标题把下拉菜单分成两部分了。

## 输入框组

可以很容易地向基于文本的输入框添加作为前缀和后缀的文本或按钮。

 

## 导航元素

```
 
<p>基本的胶囊式导航菜单</p>
<ul class="nav nav-pills">
  <li class="active"><a href="#">Home</a></li>
  <li><a href="#">SVN</a></li>
  <li><a href="#">iOS</a></li>
  <li><a href="#">VB.Net</a></li>
  <li><a href="#">Java</a></li>
  <li><a href="#">PHP</a></li>
</ul>
 
<p>基本的标签式导航菜单</p>
<ul class="nav nav-tabs">
 
```

屏幕大于768时，同时使用 class **.nav-justified**，让标签式或胶囊式导航菜单与父元素等宽。在更小的屏幕上，导航链接会堆叠。

带有下拉菜单的导航菜单：

- 以一个带有 class **.nav** 的无序列表开始。
- 添加 class **.nav-tabs**。**.nav-tabs** class 可以替换为 **.nav-pills**
- 添加带有 **.dropdown-menu** class 的无序列表。

```
 
<p>带有下拉菜单的标签</p>
  <ul class="nav nav-tabs">
    <li class="active"><a href="#">Home</a></li>
    <li><a href="#">SVN</a></li>
    <li><a href="#">iOS</a></li>
    <li><a href="#">VB.Net</a></li>
    <li class="dropdown">
      <a class="dropdown-toggle" data-toggle="dropdown" href="#">
        Java <span class="caret"></span>
      </a>
      <ul class="dropdown-menu">
        <li><a href="#">Swing</a></li>
        <li><a href="#">jMeter</a></li>
        <li><a href="#">EJB</a></li>
        <li class="divider"></li>
        <li><a href="#">分离的链接</a></li>
      </ul>
    </li>
    <li><a href="#">PHP</a></li>
  </ul>
 
```

## 导航栏

导航栏中包含导航元素

[导航栏-菜鸟](http://www.runoob.com/bootstrap/bootstrap-navbar.html)

一个默认的导航栏的步骤如下：

- 向 <nav> 标签添加 class **.navbar、.navbar-default**。
- 向上面的元素添加 **role="navigation"**，有助于增加可访问性。
- 向 <div> 元素添加一个标题 class **.navbar-header**，内部包含了带有 class **navbar-brand** 的 <a> 元素。这会让文本看起来更大一号。
- 为了向导航栏添加链接，只需要简单地添加带有 class **.nav、.navbar-nav** 的无序列表即可。

```html
<nav class="navbar navbar-default" role="navigation">
    <div class="container-fluid">
    <div class="navbar-header">
        <a class="navbar-brand" href="#">菜鸟教程</a>
    </div>
    <div>
        <ul class="nav navbar-nav">
            <li class="active"><a href="#">iOS</a></li>
            <li><a href="#">SVN</a></li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                    Java
                    <b class="caret"></b>
                </a>
                <ul class="dropdown-menu">
                    <li><a href="#">jmeter</a></li>
                    <li><a href="#">EJB</a></li>
                    <li><a href="#">Jasper Report</a></li>
                    <li class="divider"></li>
                    <li><a href="#">分离的链接</a></li>
                    <li class="divider"></li>
                    <li><a href="#">另一个分离的链接</a></li>
                </ul>
            </li>
        </ul>
    </div>
    </div>
</nav>
```



bootstrap支持：

- 响应式的导航栏
- 导航栏中的表单、文本、链接（注册登录）
- 固定导航栏到顶部、底部；静态导航栏
- 黑背景白字导航栏。向 **.navbar** class 添加 **.navbar-inverse** class 即可



## 面包屑导航（Breadcrumbs）

## 分页

页码和上一页、下一页导航

## 徽章（Badges）

显示有多少条消息、多少次评论那个数字

 Jumbotron

# 

# 表单布局

Bootstrap 提供了下列类型的表单布局：

- 垂直表单（默认）
- 内联表单
- 水平表单

## 垂直或基本表单

基本的表单结构是 Bootstrap 自带的，个别的表单控件自动接收一些全局样式。下面列出了创建基本表单的步骤：

- 向父 <form> 元素添加 *role="form"*。
- 把标签和控件放在一个带有 class *.form-group* 的 <div> 中。这是获取最佳间距所必需的。
- 向所有的文本元素 <input>、<textarea> 和 <select> 添加 class ="*form-control*" 。可以让label和input

```
<form role="form">
  <div class="form-group">
    <label for="name">名称</label>
    <input type="text" class="form-control" id="name" placeholder="请输入名称">
  </div>
  <div class="form-group">
    <label for="inputfile">文件输入</label>
    <input type="file" id="inputfile">
    <p class="help-block">这里是块级帮助文本的实例。</p>
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox">请打勾
    </label>
  </div>
  <button type="submit" class="btn btn-default">提交</button>
</form>
 
```

## 内联表单

所有元素是内联的，向左对齐的，标签是并排的.

向 <form> 标签添加 class *.form-inline*。

```
<form class="form-inline" role="form">
  <div class="form-group">
    <label class="sr-only" for="name">名称</label>
    <input type="text" class="form-control" id="name" placeholder="请输入名称">
  </div>
  <div class="form-group">
    <label class="sr-only" for="inputfile">文件输入</label>
    <input type="file" id="inputfile">
  </div>
  <div class="checkbox">
    <label>
      <input type="checkbox">请打勾
    </label>
  </div>
  <button type="submit" class="btn btn-default">提交</button>
</form>
 
```

## 水平表单

水平表单中， 一组标签和控件在一行。做法：

- 向父 <form> 元素添加 class *.form-horizontal*。
- 把标签和控件放在一个带有 class *.form-group* 的 <div> 中。
- 向标签添加 class *.control-label*。

```
 
<form class="form-horizontal" role="form">
  <div class="form-group">
    <label for="firstname" class="col-sm-2 control-label">名字</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="firstname" placeholder="请输入名字">
    </div>
  </div>
  <div class="form-group">
    <label for="lastname" class="col-sm-2 control-label">姓</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" id="lastname" placeholder="请输入姓">
    </div>
  </div>
  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <div class="checkbox">
        <label>
          <input type="checkbox">请记住我
        </label>
      </div>
    </div>
  </div>
  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-default">登录</button>
    </div>
  </div>
</form>
 
```

## 支持的表单控件

Bootstrap 支持最常见的表单控件，主要是 *input、textarea、checkbox、radio 和 select*。

所有文本输入类的元素如 `<input>`，`<textarea>` 和 `<select>` 只要设置 `.form-control` class 就会占满100%的宽度。

```html
<form>
  <div class="form-group">
    <label for="exampleFormControlInput1">Email address</label>
    <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
  </div>
  <div class="form-group">
    <label for="exampleFormControlSelect1">Example select</label>
    <select class="form-control" id="exampleFormControlSelect1">
      <option>1</option>
      <option>2</option>
      <option>3</option>
      <option>4</option>
      <option>5</option>
    </select>
  </div>
  <div class="form-group">
    <label for="exampleFormControlSelect2">Example multiple select</label>
    <select multiple class="form-control" id="exampleFormControlSelect2">
      <option>1</option>
      <option>2</option>
      <option>3</option>
      <option>4</option>
      <option>5</option>
    </select>
  </div>
  <div class="form-group">
    <label for="exampleFormControlTextarea1">Example textarea</label>
    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
  </div>
</form>


    <input type="file" class="form-control-file" id="exampleFormControlFile1">
```

### 尺寸

`form-control-lg` 和 `.form-control-sm`.

```html
<input class="form-control form-control-lg" type="text" placeholder=".form-control-lg">
```

### 输入框（Input）

最常见的表单文本字段是输入框 input。用户可以在其中输入大多数必要的表单数据。Bootstrap 提供了对所有原生的 HTML5 的 input 类型的支持，包括：*text、password、datetime、datetime-local、date、month、time、week、number、email、url、search、tel* 和 *color*。适当的 *type* 声明是必需的，这样才能让 *input* 获得完整的样式。

### 文本框（Textarea）

当您需要进行多行输入的时，则可以使用文本框 textarea。必要时可以改变 *rows* 属性（较少的行 = 较小的盒子，较多的行 = 较大的盒子）。

```html
<div class="form-group text-left">
<label for="extra">Any comments or suggestions?</label>
<textarea class="form-control" id="extra" rows="3"></textarea>
</div>
```

### 复选框（Checkbox）和单选框（Radio）

复选框和单选按钮用于让用户从一系列预设置的选项中进行选择。

- *checkbox*让用户从列表中选择若干个选项
- *radio*只能选择一个选项，请使用。
- 对一系列复选框和单选框使用 *.checkbox-inline* 或 *.radio-inline* class，控制它们显示在同一行上。

简单版

<div class="radio">
    <label>
        <input type="radio" name="optionsRadios" id="optionsRadios1" value="option1" checked> 选项 1
    </label>
</div>

Bootstrap4表单里统一样式

```html
<div class="form-group text-left">
    <p>Would you recommend freeCodeCamp to a friend?</p>
    <label class="form-check"><input name="user-recommend" value="definitely" type="radio" class="form-check-input input-radio" checked />Definitely</label>

    <label class="form-check"><input name="user-recommend" value="maybe" type="radio" class="form-check-input input-radio" />Maybe</label>
    <label class="form-check"><input name="user-recommend" value="not-sure" type="radio" class="form-check-input input-radio" />Not sure</label>
</div>
```

### 选择框（Select）

### 提交

```html
  <button type="submit" class="btn btn-primary">Sign in</button>
```

# 文本

## 引导主体副本

为了给段落添加强调文本，则可以添加 class="lead"，这将得到更大更粗、行高更高的文本。

```<p class="lead">```

## 超大屏幕

https://getbootstrap.com/docs/4.0/components/jumbotron/

Jumbotron

## 文字强调

```html
 
<small>本行内容是在标签内</small><br>
<strong>本行内容是在标签内</strong><br>
<em>本行内容是在标签内，并呈现为斜体</em><br>
<p class="text-left">向左对齐文本</p>
<p class="text-center">居中对齐文本</p>
<p class="text-right">向右对齐文本</p>
<p class="text-muted">本行内容是减弱的</p>
<p class="text-primary">本行内容带有一个 primary class 蓝色</p>
<p class="text-success">本行内容带有一个 success class</p>
<p class="text-info">本行内容带有一个 info class</p>
<p class="text-warning">本行内容带有一个 warning class</p>
<p class="text-danger">本行内容带有一个 danger class</p>
 
```

### 

# Card

https://v4.bootcss.com/docs/components/card/

内容容器

比如提供一定内容深度视觉效果

```html
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>

<div class="card" style="width: 18rem;">
  <div class="card-header">
    Featured
  </div>
  <ul class="list-group list-group-flush">
    <li class="list-group-item">Cras justo odio</li>
    <li class="list-group-item">Dapibus ac facilisis in</li>
    <li class="list-group-item">Vestibulum at eros</li>
  </ul>
</div>


  <div class="card-body">
    <blockquote class="blockquote mb-0">
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.</p>
      <footer class="blockquote-footer">Someone famous in <cite title="Source Title">Source Title</cite></footer>
    </blockquote>
  </div>

  <div class="card-footer text-muted">
    2 days ago
  </div>
```

# Utilities

https://getbootstrap.com/docs/4.3/utilities

## 文本对齐

.text-wrap 方框包裹文字

```html
<p class="font-weight-bold">Bold text.</p>
<p class="font-weight-bolder">Bolder weight text (relative to the parent element).</p>
<p class="font-weight-normal">Normal weight text.</p>
<p class="font-weight-light">Light weight text.</p>
<p class="font-weight-lighter">Lighter weight text (relative to the parent element).</p>
<p class="font-italic">Italic text.</p>
<a href="#" class="text-decoration-none">Non-underlined link</a>
```

## Spacing

https://getbootstrap.com/docs/4.3/utilities/spacing/

size：

| 0    | 0       |
| ---- | ------- |
| 1    | 0.25rem |
| 2    | 0.5rem  |
| 3    | 1rem    |
| 4    | 1.5rem  |
| 5    | 3rem    |
| auto | auto    |

 *property*: m p

sides: t b l r x(左右) y(上下)

组合后如：mb-4

# 响应式工具

以超小屏幕（xs）为例，可用的 .visible-*-* 类是：.visible-xs-block、.visible-xs-inline 和 .visible-xs-inline-block

| 类组                    | CSS display            |
| ----------------------- | ---------------------- |
| .visible-*-block        | display: block;        |
| .visible-*-inline       | display: inline;       |
| .visible-*-inline-block | display: inline-block; |

| visible-xs-*  | 可见 | 隐藏 | 隐藏 | 隐藏 |
| ------------- | ---- | ---- | ---- | ---- |
| .visible-sm-* | 隐藏 | 可见 | 隐藏 | 隐藏 |
| .visible-md-* | 隐藏 | 隐藏 | 可见 | 隐藏 |
| .visible-lg-* | 隐藏 | 隐藏 | 隐藏 | 可见 |
| .hidden-xs    | 隐藏 | 可见 | 可见 | 可见 |
| .hidden-sm    | 可见 | 隐藏 | 可见 | 可见 |
| .hidden-md    | 可见 | 可见 | 隐藏 | 可见 |
| .hidden-lg    | 可见 | 可见 | 可见 | 隐藏 |

总结：visible-只对一种设备可见，hidden只对一种设备隐藏。

#  JavaScript 

## 使用方法

- 插件文件之前引用 jQuery
- 使用 *bootstrap.js* 或压缩版的 *bootstrap.min.js*
- 通过 data 属性 API 就能使用所有的 Bootstrap 插件

## API

链式的，都会返回作用的对象

```js
$('.btn.danger').button('toggle').addClass('fat')
```

All methods should accept an optional options object, a string which  targets a particular method, or nothing (which initiates a plugin with  default behavior):

```js
$('#myModal').modal() // initialized with defaults
$('#myModal').modal({ keyboard: false }) // initialized with no keyboard
$('#myModal').modal('show') // initializes and invokes show immediately
```