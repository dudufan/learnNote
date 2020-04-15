# 模板
 
[模板设计者文档](http://docs.jinkan.org/docs/jinja2/templates.html)
 
## Example
 
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>
 
    <h1>My Webpage</h1>
    {{ a_variable }}
</body>
</html>
```
 
## 变量
 
模板中的变量保留它们的对象属性
 
```
{{ foo.bar }}
{{ foo['bar'] }}
```
 
### 过滤器
 
`{{ name|striptags|title }}` 相当于 (`title(striptags(name))`).
 
`{{ listx|join(', ') }}` 相当于(`str.join(', ', listx)`).
 
[内置过滤器清单](http://docs.jinkan.org/docs/jinja2/templates.html#builtin-filters)
 
[内置测试清单](http://docs.jinkan.org/docs/jinja2/templates.html#builtin-tests)
 
### 基础模板
 
```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    {% block head %}
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}{% endblock %} - My Webpage</title>
    {% endblock %}
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2008 by <a href="http://domain.invalid/">you</a>.
        {% endblock %}
    </div>
</body>
```
 
`{% block %}` 标签定义了子模板可以覆盖的块。
 
### 子模板
 
```
{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        .important { color: #336699; }
    </style>
{% endblock %}
{% block content %}
    <h1>Index</h1>
    <p class="important">
      Welcome on my awesome homepage.
    </p>
{% endblock %}
```
 
extends 标签应该是模板中的第一个 标签
 
```
{% extends "layout/default.html" %}
```
 
### 嵌套块和作用域
 
嵌套块可以胜任更复杂的布局。而默认的块不允许访问块外作用域中的变量:
 
```
{% for item in seq %}
    <li>{% block loop_item %}{{ item }}{% endblock %}</li>
{% endfor %}
```
 
### 控制结构
 
#### For
 
```
<dl>
{% for key, value in my_dict.iteritems() %}
    <dt>{{ key|e }}</dt>
    <dd>{{ value|e }}</dd>
{% endfor %}
</dl>
```
 
在一个 for 循环块中你可以访问这些特殊的变量:
 
| 变量           | 描述                                         |
| -------------- | -------------------------------------------- |
| loop.index     | 当前循环迭代的次数（从 1 开始）              |
| loop.index0    | 当前循环迭代的次数（从 0 开始）              |
| loop.revindex  | 到循环结束需要迭代的次数（从 1 开始）        |
| loop.revindex0 | 到循环结束需要迭代的次数（从 0 开始）        |
| loop.first     | 如果是第一次迭代，为 True 。                 |
| loop.last      | 如果是最后一次迭代，为 True 。               |
| loop.length    | 序列中的项目数。                             |
| loop.cycle     | 在一串序列间期取值的辅助函数。见下面的解释。 |
 
比如周期取值：
 
```
{% for row in rows %}
    <li class="{{ loop.cycle('odd', 'even') }}">{{ row }}</li>
{% endfor %}
```
 
**for循环如果迭代的对象为空**
 
```
<ul>
{% for user in users %}
    <li>{{ user.username|e }}</li>
{% else %}
    <li><em>no users found</em></li>
{% endfor %}
</u
```
 
**递归循环**实现了站点地图:
 
```
<ul class="sitemap">
{%- for item in sitemap recursive %}
    <li><a href="{{ item.href|e }}">{{ item.title }}</a>
    {%- if item.children -%}
        <ul class="submenu">{{ loop(item.children) }}</ul>
    {%- endif %}</li>
{%- endfor %}
</ul>
```
 
#### if
 
```
{% if kenny.sick %}
    Kenny is sick.
{% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
{% else %}
    Kenny looks okay --- so far
{% endif %}
```
 
### include包含
 
include 语句用于包含一个模板，并在当前命名空间中返回那个文件的内容渲 染结果:
 
```
{% include 'header.html' %}
    Body
{% include 'footer.html' %}
```