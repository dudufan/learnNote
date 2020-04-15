[TOC]



# 安装构建

## Linux升级2.7

```shell
cd Python-2.7.15
./configure --enable-optimizations
make && make altinstall
```

查看安装是否成功

```
/usr/local/bin/python2.7 -V
Python 2.7.15
```

建立软连接，使系统默认python指向2.7版本

```shell
mv /usr/bin/python /usr/bin/python2.6.6
ln -s /usr/local/bin/python2.7 /usr/bin/python
```

setuptools安装

```
[root@ ]# wget https://files.pythonhosted.org/packages/a9/23/720c7558ba6ad3e0f5ad01e0d6ea2288b486da32f053c73e259f7c392042/setuptools-36.0.1.zip 
[root@ ]# unzip setuptools-36.7.1.zip 
[root@ ]# cd setuptools-36.7.1
[root@ setuptools-36.7.1]# python setup.py install 
```

pip安装

```
[root@ ]# curl -O https://pypi.python.org/packages/source/p/pip/pip-9.0.1.tar.gz
[root@ ]# [root@ ]# tar xf pip-9.0.1.tar.gz 
[root@ ]# cd pip-9.0.1
[root@ pip-9.0.1]# python setup.py install
```

## Vscode配置

Vscode配置python环境

1. 安装Python插件
2. 命令行安装pylint
`python -m pip install pylint`
3. 修改用户设置配置Python插件、修改lanch.json配置调试
4. F5启动调试

lanch.json配置详解：
stopOnEntry为true，则第一行默认会有个断点

## pip安装库

```shell
pip install --index-url https://pypi.douban.com/simple pyinstaller
```



没pip的话先下载安装pip（方法在上面）


```shell
 pip install -U PackageName
 
 安装时指定源（--index-url）
#例如安装scipy时使用豆瓣的源
 pip install --index-url https://pypi.douban.com/simple scipy
```

 

## tar包安装库

解压tar包

setuptools安装下载的模块（package)

​     /Lib/site-packages/setuptools*

     python setup.py build (tar包需要编译）
     python setup.py install

 http://blog.konghy.cn/2018/04/29/setup-dot-py/

## 发布exe

1. 安装pyinstaller

```
pip install --index-url https://pypi.douban.com/simple pyinstaller
```

2. 安装pywin32

3. 打包。

   ```python
   pyinstaller -F -w D:\project\test.py
   # -w隐藏了控制台
   # -F是合并依赖打出exe
   ```

   在你的py文件所在的目录下，生成build和dist文件夹，如果是选择了-F参数，那么dist文件夹下就是你要的程序，build文件夹可以删除。

   exe相当于py文件的作用，配置目录层级同样。




## 卸载包
     pip uninstall PackageName
     
     或删除 Lib\site-packages下该包目录文件即可

## 离线安装库

```shell
pip install wheel
pip install
```



## 离线批量安装库

1.在可以联网的开发机器上安装好需要的包

例如：

 set PYTHONIOENCODING=UTF-8

`pip install fabric --index-url https://pypi.douban.com/simple`

2.打包已安装的包到自己的目录

```shell
pip3 list #查看安装的包
 
pip3 freeze >requirements.txt
 
pip3 download -r requirements.txt -d packages --index-url https://pypi.douban.com/simple
```

3.离线情况安装打包好的包

`pip install --no-index --find-links=packages -r requirements.txt`



Run time environment

> Distinguish this from Development Environments and Build Environments.

You will tend to find a hierarchy here.
Run time environment - Everything you need to execute a program, but no tools to change it.
Build environment- Given some code written by someone, everything you need to compile it or otherwise prepare an executable that you put into a Run time environment. Build environments are pretty useless unless you can see tests what you have built, so they often include Run too. In Build you can't actually modify the code.
Development environment - Everything you need to write code, build it and test it. Code Editors and other such tools. Typically also includes Build and Run. 

# 命名规范

参考Google开源项目风格指南： https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/

转载一下其中的命名规范：
## 一般命名

module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_VAR_NAME, instance_var_name, function_parameter_name, local_var_name.

应该避免的名称

        单字符名称, 除了计数器和迭代器.
        包/模块名中的连字符(-)
        双下划线开头并结尾的名称(Python保留, 例如__init__)

## 变量命名

        所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的.
        用单下划线(_)开头表示模块变量或函数是protected的(使用import * from时不会包含).
        用双下划线(__)开头的实例变量或方法表示类内私有.
        将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.
        对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存的模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰.

# 编解码



## 头文件编码声明

作用：

- 指定python编译器在读取该.py文件时候，应该用什么格式解码。 所以当你确定你代码编辑时候用的是什么格式编码的，你才能把相应的编码格式写入头文件。 
-  不会更改本地、系统默认编码 

## 系统默认编码

系统默认编码影响解码py文件。在python3编译器读取.py文件时，若没有头文件编码声明，则默认使用“utf-8”来对.py文件进行解码。并且在调用 encode()这个函数时，不传参的话默认是“ utf-8 ” 

## 本地默认编码

python3程序时，若使用了 *open( )函数* ，而不给它传入 *“ encoding ”* 这个参数，那么会自动使用本地默认编码。Windows系统中是默认用gbk

## python2运行时编解码

python2: 对象在内存中字符串的编码是unicode，相当于中间编码。而实际显示、传输都需要具体编码为字节流，比如utf8等格式。

编码: unicode对象→`bytes`对象

```python
str="aabbcc" # aabbcc
bytes=str.encode('utf-8') # b'aabbcc'
```

解码: `bytes`对象→unicode对象





decode的作用是将其他编码的字符串转换成unicode编码

encode的作用是将unicode编码转换成其他编码的字符串

而具体编码的字符串也就可以转换为字节。



在不指定encoding参数时，open()函数默认采用和系统相关的编码方式。而在Windows 系统下，系统相关的编码方式是GBK，不是UTF-8。

## python3

https://zhuanlan.zhihu.com/p/40834093

Linux环境下运行：

```python
#coding=gbk
import sys, locale

s = "小甲"
print(s)  # 灏忕敳
print(type(s)) # <class 'str'> 
print(sys.getdefaultencoding()) # utf-8 python3的编译器的默认编码
print(locale.getdefaultlocale())# Linux结果：('en_US', 'UTF-8') 操作系统的默认编码
# win7结果：('zh_CN', 'cp936') 

with open("utf2","w",encoding = "utf-8") as f:
    f.write(s)
with open("gbk2","w",encoding = "gbk") as f:
    f.write(s)
with open("jis2","w",encoding = "shift-jis") as f:
    f.write(s)

```

以shift-jis编码写入文件发生异常，因为乱码后的 “ 灏忕敳 ”这三个字在日文中没有

```shell
Traceback (most recent call last):
  File "2", line 15, in <module>
    f.write(s)
UnicodeEncodeError: 'shift_jis' codec can't encode character '\u704f' in position 0: illegal multibyte sequence


```

三个写入的文件内容：

```shell
utf2 : 灏忕敳
gbk2 : 小甲
jis2 :
```

gbk2文件内容仍然是“小甲"，原因：

```shell
第1步：  小甲（unicode）   ---用 "utf-8" 编码--->    e5b0 8fe7 94b2 (代码文件是用utf-8编码的，编码后的二进制代码)
第2步：  e5b0 8fe7 94b2   ---用 “gbk” 解码--->     " 灏忕敳 " （unicode）(乱码)
第3步：  “ 灏忕敳 ”     --- 用 “ gbk ” 编码--->     e5b0 8fe7 94b2 ( 第2步的逆向)
第4步 打开文件查看内容：  e5b0 8fe7 94b2     ---用 “ utf-8 ” 解码--->    小甲（unicode） 
```



## 0x04 python2和python3的一些不同

1) python2中默认使用ascii，python3中默认使用utf-8

2) Python2中，str就是编码后的结果bytes，str=bytes,所以s只能decode。

3) python3中的字符串与python2中的u'字符串'，都是unicode，只能encode，所以无论如何打印都不会乱码，因为可以理解为从内存打印到内存，即内存->内存，unicode->unicode

4) python3中，str是unicode，当程序执行时，无需加u，str也会被以unicode形式保存新的内存空间中,str可以直接encode成任意编码格式，s.encode('utf-8')，s.encode('gbk')

```
#unicode(str)-----encode---->utf-8(bytes)
#utf-8(bytes)-----decode---->unicode
```

5)在windows终端编码为gbk，linux是UTF-8.



python3.x来说，官方已经将默认编码改为utf8

python2.x，还需要设置str对象默认解码的方式

### Python2设置str对象默认解码的方式

```java
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

如果不设置可能出现以下问题，

比如有如下代码：

```
#! /usr/bin/env python
# -- coding: utf-8 --
s = '中文字符'  # 这里的 str 是 str 类型的，而不是 unicode
s.encode('gb2312')
```

这句代码将 s 重新编码为 gb2312 的格式，即进行 unicode -> str 的转换。因为 s 本身就是 str 类型的，因此
Python  会自动的先将 s 解码为 unicode ，然后再编码成 gb2312。因为解码是python自动进行的，我们没有指明解码方式，python  就会使用 sys.defaultencoding 指明的方式来解码。很多情况下 sys.defaultencoding为ANSCII，如果 s  不是这个类型就会出错。

```
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position
0: ordinal not in range(128)
```

对于这种情况，我们有两种方法来改正错误：

1. 明确的指示出 s 的编码方式

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
s = '中文字符'
s.decode('utf-8').encode('gb2312')
 
```

1. 更改 sys.defaultencoding 为文件的编码方式

```
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys) # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
 
str = '中文字符'
str.encode('gb2312')
```



## 源代码编码

UTF-8编码读取源代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

第一行注释是为了告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释；

第二行注释是为了告诉Python解释器，按照UTF-8编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码。

申明了UTF-8编码并不意味着你的`.py`文件就是UTF-8编码的，必须并且要确保文本编辑器正在使用UTF-8 without BOM编码：

 



## 路径必须是unicode字符串

root = u"D:\T信银企通\SSP\SSP_Trunk"

unicode字符串加入list后，list中显示的就是编码后的码值，但print单个中文字符串显示的是中文，如print unicode_str_list[0] 

[廖雪峰python教程-字符集](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431664106267f12e9bef7ee14cf6a8776a479bdec9b9000)

http://python.jobbole.com/81244/

##  判断文件编码格式

结果可信度不定

```python
import chardet

f = open(u'加解密1.md','rb')
data = f.read()
print(chardet.detect(data))
```

## 转换文本编码

utf_16_le文件转utf_8文件。decoder参数必须是二进制对象

```python
with open(filename, 'rb') as file:
    content = file.read()
    print(content)

with open(filename, 'rb') as binaryfile:
    charset = chardet.detect(binaryfile.read())
    if not charset['encoding']:
        decoder = codecs.getdecoder('utf_16_le')
if decoder:
    with open(filename, 'w', encoding='utf-8') as utf8_file:

        print(decoder(content))
```



##  设置输出编码

 环境变量 PYTHONIOENCODING 设置为UTF-8

```shell
export PYTHONIOENCODING=UTF-8
```



和命令行窗口保持一致才能正确显示

# 变量

```python
if not isinstance(build_dir_list, list):
    build_dir_list = get_build_list(build_dir_list)
```

## 字符串

也可以使用[]索引和切片

r''可以使字符串不转义

'''adbadfasdf'''可以显示多行内容

 删除s字符串中开头、结尾处，位于 rm删除序列的字符 . 当rm为空时，默认删除空白符（包括'\n', '\r', '\t', ' ') 

```python
 s.strip(rm)
 s.lstrip(rm) s.rstrip(rm)
```



### 格式化

> conversion specifier contains two or more characters and has the following components, which must occur in this order:

1. The   '%'   character, which marks the start of the specifier.
2. Mapping key (optional), consisting of a parenthesised sequence of characters (for example,   (somename) ).
3. Conversion flags (optional), which affect the result of some conversion types.
4. Minimum field width (optional). If specified as an   '*'   (asterisk), the 1. actual width is read from the next element of the tuple in   values , and the object to convert comes after the minimum field width and optional precision.
5. Precision (optional), given as a   '.'   (dot) followed by the precision. If specified as   '*'   (an asterisk), the actual precision is read from the next element of the tuple in   values , and the value to convert comes after the precision.
6. Length modifier (optional).
7. Conversion type.

```python
>>> print('%(language)s has %(number)03d quote types.' %
 
...       {'language': "Python", "number": 2})
 
Python has 002 quote types.
```



## 布尔值

- 布尔值

True False

- 布尔运算

and or not

Python把0、空字符串''和None看成 False，其他数值和非空字符串都看成 True
空列表也是False

## None

无返回的函数实际上返回的是None，代表空值

 

## 整数

没有大小限制

Python对于有符号数，补码存储。

举例，-3的补码是11111111111111111111111111111101，python中,查看-3二进制存储的后8位，可以看出是补码存储

```python
>>> bin(-3 & 0xff)
'0b11111101'
```



## 集合

- list有序可读写，tuple定义后只读

- tuple中的list内容可以修改，但该列表的引用（也就是指向的列表）不可修改

- set和dict的区别是，set没有值，创建一个set需要提供一个list做输入集合

```python
isprime = [1] * n
len() 求长度
t2 索引二维数组
t = (1,) 定义单个元素的tuple
tuple中的list
```



## 切片

左开右闭，不包括最右侧索引

```python
 s[::-1] #-1是从右往左间隔1，可以用来逆序字符串
```



## list
```
if 'a' in list1:
    ...
 
append(ele)
 
insert(i, ele) 插入指定位置
 
pop() 返回并删除末尾元素
```





## dict

```
d[xxx] = xxx 添加新的键值对
"name" in d 判断key是否存在
 
d.get("name") 不存在返回None
 
d.get("name", "Joe") 不存在可以指定自己的value，然后返回的也是这个值
 
d.pop(key) 删除并返回value

for k,v in d.items()
```

### set方法

s = set([1, 2, 3])

add remove

s1 & s2 交集

s1 | s2 并集

 



## 模块、命名空间

### from modulexxx import * 无法修改其他模块变量

相当于导入了代码，在自己的module中增加了几行代码，无论如何修改都不会影响另一个module

用from module import时，其实是copy了一份reference或者pointer，指向一份内存，var和module.var都指向同一份内存
当你修改module.var时，其实你是让它指向了另外一份内存，此时var和module.var指向的是不同的内存
所以，虽然module.var的值变了，var还是指向原来那份内存，原来的值

### 修改全局变量

引用全局变量，不需要golbal声明，修改全局变量，需要使用global声明，特别地，列表、字典等如果只是修改其中元素的值，可以直接使用全局变量，不需要global声明。

###  全局变量的定义和使用

在方法中第一次声明并初始化全局变量

```
global step_num
step_num = 1
```

## callable

```python
value = field.default() if callable(field.default) else field.default
```

## 三元操作符

```python
top_element = stack.pop() if stack else '#'
```

数组

# 函数

函数没有重载

## 函数参数

python的参数类型(函数声明中的参数类型，不是变量type)

在python有一个标准模块inspect, 主要提供了四种用处：

    对是否是模块，框架，函数等进行类型检查。
    获取源码
    获取类或函数的参数的信息
    解析堆栈

很明显第3点就是我们想要的功能，inspect模块有对python函数的参数类型有详细的定义。
有哪几种参数类型？

### 位置或关键字参数

- 如果没有任何*的声明，那么就是`POSITIONAL_OR_KEYWORD`类型的
- 可以通过位置传参调用，也可以过关键字传参。

```
def foo(a):
    pass
 
# 位置传参调用
foo(1)
# 关键字传参调用
foo(a=1)
```

### 可变位置参数

- 这种类型的参数只能通过位置`POSITIONAL`传参调用，不支持关键字`KEYWORD`传参
- 通过一个`*`前缀来声明
- 在函数内部，`VAR_POSITIONAL`类型的参数以一个元祖(`tuple`)显示,,不传任何参数则是空tuple
- 函数声明中VAR_POSITIONAL类型参数只允许存在一个。

```
def foo(*b):
    print(b)
 
# 不传参数不会报错，参数值是一个空元祖
foo() # 结果是 ()
# 可以传入任意个位置参数调用
foo(1, 2.0, '3', True) #结果是 (1, 2.0, '3', True)
```

### 命名关键字参数

- 在`*`参数的后面，不可以用位置传参。因为位置传的参数全让前面的`*`参数接收完了。

如参数c

```python
# 可变位置参数不需要使用时，可以匿名化
def foo(*, c):
    pass
 
# 只能关键字传参调用
foo(c=1)
```

### 可变的关键字参数

只能通过关键字调用，但可以接收任意个（或0个）关键字参数。在函数内部以一个字典(`dict`)显示。`VAR_KEYWORD`类型的参数只允许有一个，只允许在函数的最后声名。

参数d是例子：

```python
def foo(**d):
    print(d)
 
# 不传参数不会报错，参数值是一个空字典
foo() # 结果是 {}
# 可以传入任意个关键字参数调用
foo(a=1, b=2.0, c='3', d=True) # 结果是 {'d': True, 'c': '3', 'b': 2.0, 'a': 1}
```

### 默认参数

- 默认参数必须指向不变对象
- 必选参数在前，默认参数在后，否则Python的解释器会报错
- 当函数有多个参数时，把变化大的参数放前面，变化小的参数放后面。变化小的参数就可以作为默认参数。

正确的示例：


```python
def foo(p1, p2=2.0, *, k1, k2=None):
    a_list = k2 or list()
    pass
 
foo(1, k1='3')
```

### 参数定义顺序
必选参数、默认参数、可变参数、命名关键字参数和关键字参数。

```python
def foo(a, *b, c, **d):
    print(a, b, c, d, sep='\n')
 
foo(1, 2, '3', c=3, x=1, y=2)
 
# a: 1
# b: (2, '3')
# c: 3
# d: {'x': 1, 'y': 2}
```

函数调用时某个参数使用命名参数，后面的参数必须也是命名参数

### unpack可变参数（位置可变参数、关键字可变参数）
`*args`和`**kwargs`语法不仅可以在函数定义中使用，同样可以在函数调用的时候使用。不同的是，如果说在函数定义的位置使用`*args`和`**kwargs`是一个将参数pack的过程，那么在函数调用的时候就是一个将参数unpack的过程了。下面使用一个例子来加深理解：
```python
def test_args(first, second, third, fourth, fifth):
    print 'First argument: ', first
    print 'Second argument: ', second
    print 'Third argument: ', third
    print 'Fourth argument: ', fourth
    print 'Fifth argument: ', fifth
 
# Use *args
args = [1, 2, 3, 4, 5]
test_args(*args)
# results:
# First argument:  1
# Second argument:  2
# Third argument:  3
# Fourth argument:  4
# Fifth argument:  5
 
# Use **kwargs
kwargs = {
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5
}
 
test_args(**kwargs)
# results:
# First argument:  1
# Second argument:  2
# Third argument:  3
# Fourth argument:  4
# Fifth argument:  5
```
使用*args和**kwargs可以非常方便的定义函数，同时可以加强扩展性，以便日后的代码维护。

### 命令行传递keyword参数
```python
if name == 'main':
   parser = argparse.ArgumentParser()
   parser.add_argument('--arg1')
   parser.add_argument('--arg2')
   args = parser.parse_args()
   print args.arg1
   print args.arg2

   my_dict = {'arg1': args.arg1, 'arg2': args.arg2}
   print my_dict

Now, if you try:
  $ python script.py --arg1 3 --arg2 4

you will see:
3
4
{'arg1': '3', 'arg2': '4'}
```



## 函数作用域
Python没有块级作用域，只有函数作用域
Python中有作用域链，变量会由内到外找，先去自己作用域去找，自己没有再去上级去找，直到找不到报错

 

执行结果为“lzl”，分析下上面的代码，f2()执行结果为函数f1的内存地址，即ret=f1；执行ret()等同于执行f1()，执行f1()时与f2()没有任何关系，name=“lzl”与f1()在一个作用域链，函数内部没有变量是会向外找，所以此时变量name值为“lzl”

 

>   在Python中，当引用一个变量的时候，对这个变量的搜索是按找本地作用域(Local)、嵌套作用域(Enclosing function locals)、全局作用域(Global)、内置作用域(builtins模块)的顺序来进行的，即所谓的 LEGB 规则。
然而当在一个函数内部为一个变量赋值时，并不是按照上面所说 LEGB 规则来首先找到变量，之后为该变量赋值。在Python中，在函数中为一个变量赋值时，有下面这样一条规则:


来源：   http://blog.csdn.net/cn_wk/article/details/52723269


  ***“当在函数中给一个变量名赋值是(而不是在一个表达式中对其进行引用)，Python总是创建或改变本地作用域的变量名，除非它已经在那个函数中被声明为全局变量. ”***

 

使用global关键字修饰的变量之前可以并不存在，而使用nonlocal关键字修饰的变量在嵌套作用域中必须已经存在。

```python
 
#作用域链
 
name = "lzl"
 
def f1():
    print (name)
 
def f2():
    name = "eric"
    return f1
 
ret = f2()
ret()
 
#终极版作用域
 
#输出：lzl
 
```



## 根据方法名调用方法

Assuming module foo with method bar: 

```
import foo
method_to_call = getattr(foo, 'bar')
result = method_to_call()

```

 As far as that goes, lines 2 and 3 can be compressed to:

```python
 result = getattr(foo, 'bar')()
```

 if that makes more sense for your use case. You can use getattr in this fashion on class instance bound methods, module-level methods, class methods... the list goes on.

## 动态获取module

module = __import__('foo')
func = getattr(module, 'bar')
func()

## 装饰器

```python
def log():
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

带参数的装饰器。

下面的装饰器，实现捕获异常，并重新抛出异常，主要作用是打印日志并修改异常错误信息为可读的

```python
def catch_err(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as ve:
                traceback.print_exc()
                raise ve
            except Exception as e:
                traceback.print_exc()
                raise ValueError(text)
        return wrapper
    return decorator

@catch_err("加载yaml失败，请检查配置是否存在，格式是否正确！")
def load_configMap(prodName):
    with open(os.path.join(envconfig_dir, '%s.yaml') % prodName) as f:
        configMap = yaml.load(f)
        return configMap
```

## 闭包

概念：

> lambda表达式的闭包是定义在外部上下文（环境）中特定的符号集，它们给这个表达式中的自由符号赋值。它将一个开放的、仍然包含一些未定义的符号lambda表达式变为一个关闭的lambda表达式，使这个lambda表达式不再具有任何自由符号

-  **概念上的闭包**：在实现深约束（解决FUNARG问题）的过程中，函数需要引用到一个环境，而函数和这个环境形成的整体我们称为闭包。可以说闭包无处不在，例如对象。
-  **形式上的闭包**：词法上下文中引用了自由变量的函数，在不同语言中有不同的表现形式，并且衍生了很多运用方式，比如隐藏数据，作为简易对象使用。

闭包就是定义在一个函数内部的函数，它可以引用外部函数的变量。

比如，函数lazy_sum返回了函数sum后，其内部的局部变量args还被sum函数引用

```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
```

**返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。**

以下是错误的写法

```
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs
```

改写后g(j)立即执行，参数i被绑定到g()

```
def count():
    def g(j):
    	return lambda j:j*j
	fs = []
    for i in range(1, 4):
        fs.append(g(i))# g(i)立刻被执行，因此i的当前值被传入g()
    return fs
```

> 闭包避免了使用全局变量，允许将函数与其操作的某些数据（环境）关联起来。这一点和面向对象编程非常类似，对象允许我们将某些数据与一个或多个方法关联。
>
> 一般来说，当对象中只有一个方法时，使用闭包是更好的选择。

因此java8提供了lambda表达式，代替单方法的匿名内部类。

# 内置函数

map 

reduce。可迭代对象如果为空，必须显式指定初始值

```python
from functools import reduce
singleNum = reduce(lambda x,y:x^y, nums)
```

filter



# 迭代

```python
# 左开右闭，不包括最右侧n
for i in range(1, n)
for key in d
for ch in 'ABC'
```

判断是否可迭代

```python
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
```

同时迭代索引和元素本身

```python
for i, value in enumerate(['A', 'B', 'C'])
```

同时引用两个变量

```
for x, y in [(1, 1), (2, 4), (3, 9)]
```

# 列表生成式

偶数的平方

```python
>>> [x * x for x in range(1, 11) if x % 2 == 0] 
[4, 16, 36, 64, 100]
```

使用两层循环生成全排列

```python
>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

`for`循环其实可以同时使用两个甚至多个变量

```
>>> d = {'x': 'A', 'y': 'B', 'z': 'C' }
>>> [k + '=' + v for k, v in d.items()]
['y=B', 'x=A', 'z=C']
```

# 面向对象

## 属性

判断属性是否存在

```python
if hasattr(e, 'code')
```

getter/setter

setter方法在创建实例时也会调用。

```python
class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        print("get name called")
        return self._name

    @name.setter
    def name(self, name):
        print("set name called")
        if not isinstance(name, str):
            raise TypeError("Expected a string")
        self._name = name

person = Person("Tom")
print(person.name)
```

代码的输出为：

```
set name called
get name called
Tom
```



 如果在类中定义了__getitem__()方法，那么他的实例对象（假设为P）就可以这样P[key]取值。当实例对象做P[key]运算时，就会调用类中的__getitem__()方法。 

## 继承

def JJBankParamParse(ParamParser):
    def __init__(self):
        super(JJBankParamParse, self).__init__()



多重继承

```python
class MyTCPServer(TCPServer, CoroutineMixIn):
    pass
```

# 异常处理

## try except
try except也可以处理importError

```python
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
```

## 打印错误信息

```python
import traceback

raise Exception("remove package %s in remote host Error!, errMessage=%s" % (self.packageName, traceback.format_exc()))

```



# 正则表达式


强烈建议使用Python的r前缀，就不用考虑转义的问题了：
```python
s = r'ABC\-001'
# 对应的正则表达式字符串不变：
# 'ABC\-001'
```

### 使用正则表达式切分字符串
```python
>>>
re.split(r'\s+', 'a b   c')
['a','b','c']
```

### group提取子串

简单例子学会一般用法：

re.M与re.S相反

re.M表示将字符串视为多行,从而^匹配每一行的行首,$匹配每一行的行尾

对于多行文本，re.S让.也匹配换行符

```python
 
#!/usr/bin/python
import re
 
line = "Cats are smarter than dogs"
matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
 
if matchObj:
    # group是匹配到的整个字符串，默认分组
   print "matchObj.group() : ", matchObj.group()
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
else:
   print "No match!!"
```



### 正则替换         

正则替换可以使用函数

例如：替换字符串中所有#1.2.3.4#格式中的数字为0

```python
import re

def replace(x):
    def _replace(matched):
        m = matched.group()
        change = re.sub("\d", '0', m)
        return change

    pattern = "#((\d*\.)+\d+)#"
    r = re.sub(pattern, _replace, x)
    return r

x = "ab.c.d.#1.0.3.4# 2.2.2asdf"
r = replace(x)

print x
print r
```

输出：

```python
ab.c.d.#1.0.3.4# 2.2.2asdf
ab.c.d.#0.0.0.0# 2.2.2asdf
```

# 内建模块应用

[参考](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431937554888869fb52b812243dda6103214cd61d0c2000)

# 文件操作

## UTF8编码写入文件

     with open(config_name,'w', encoding='UTF-8') as fp:
         fp.write(content)
## 遍历目录搜索文本

方式一：os.walk

```python
for maindir, subdir, file_name_list in os.walk(dirname):

    print("1:",maindir) #当前主目录
    print("2:",subdir) #当前主目录下的所有目录
    print("3:",file_name_list)  #当前主目录下的所有文件

    for filename in file_name_list:
        apath = os.path.join(maindir, filename)#合并成一个完整路径
        result.append(apath)
```





方式二 os.path.walk

```python
# coding=utf-8
 
import os, sys
 
listonly = False
 
skip_exts = ['.gif', '.exe', '.pyc', '.o', '.a', '.dll', '.lib', '.pdb', '.mdb']  # ignore binary files
 
 
def visitfile(fname, searchKey):  # for each non-dir file
 
    global fcount, vcount
    try:
        if not listonly:
            if os.path.splitext(fname)[1] in skip_exts:
                pass
            elif open(fname).read().find(searchKey) != -1:
                print'%s has %s' % (fname, searchKey)
                fcount += 1
    except: pass
    vcount += 1
 
def visitor(args, directoryName, filesInDirectory):  # called for each dir
    for fname in filesInDirectory:
        fpath = os.path.join(directoryName, fname)
        if not os.path.isdir(fpath):
            visitfile(fpath, args)
 
def searcher(startdir, searchkey):
    print "enter searcher=========="
    global fcount, vcount
    fcount = vcount = 0
    os.path.walk(startdir, visitor, searchkey)
 
if __name__ == '__main__':
    root = u"D:\T信银企通\Tools\svntool"
    key = "SSP-Release"
    searcher(root, key)
    print 'Found in %d files, visited %d' % (fcount, vcount)
```



## random

random.choice 在tuple或list中随机选择一个元素

### 数据库

#### sqllite
```python
 
# -*- coding: utf-8 -*-
import
os, sqlite3
 
 
db_file = os.path.join(os.path.dirname(__file__),'test.db')
 
if os.path.isfile(db_file):
    os.remove(db_file)
 
# 初始数据:
conn=sqlite3.connect(db_file)
cursor=conn.cursor()
 
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)"
)
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
cursor.close()
conn.commit()
conn.close()
 
def get_score_in(low,high):
' 返回指定分数区间的名字，按分数从低到高排序 '
    conn=sqlite3.connect(db_file)
    cursor=conn.cursor()
    cursor.execute('select name from user where score between ? and ? order by score',(low,high))
    values=cursor.fetchall()
    names=list(map(lambda x:x[0], values)
    return names
 
# 测试:
assert get_score_in(80,95)==['Adam']
assert get_score_in(60,80)==['Bart','Lisa']
assert get_score_in(60,100)==['Bart','Lisa','Adam']
print('Pass')
```

# os

```python
os.path.join
os.path.exists
os.path.isdir
# 获取后缀
package_suffix = os.path.splitext(self.packageName)[1]
# 递归删除目录
shutil.rmtree
```

# subprocess

调用shell输出到控制台

```python
import subprocess
subprocess.call("sh mybash.sh", shell=True)
```

Linux上执行如果发生找不到文件或命令的异常，可能是文本换行符是dos的原因。

返回的对象获取到stdout stderr

```python
subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
```

给shell或python传递参数时，带空格的参数都要加双引号

# JSON

序列化中文

```python
json.dumps(dic,ensure_ascii=False)

with open(baffle_name,"w",encoding='UTF-8') as fj:
    json.dump(data,fj,sort_keys=True, indent=4,ensure_ascii=False)

# 从文件读取json字符串
with open(req_json, 'r' ,encoding='UTF-8') as f:
    req_actual = json.load(f)
```



# 第三方库

## flask

### 配置启动

flask自带的http server默认单进程，单线程阻塞模式。

```python
# 1.threaded : 多线程支持，默认为False，即不开启多线程;
app.run(threaded=True)
# 2.processes：进程数量，默认为1.
app.run(processes=True)
ps：多进程或多线程只能选择一个，不能同时开启
```

生产环境需要使用uwsgi做web服务器

### 静态文件

默认flask的静态文件必须放在static中，否则网页会提示“Not Found 404”错误。


### 保护页面
未登录或不是资源的所有者，则后端一定要校验无法编辑，前端不提供编辑的按钮返回公共模板
比如未登录则返回publicrestaurants.html，里面没有提供新建餐厅的选项。
如果未登录或session中的用户不是餐厅所有者，无法新建菜品。


### flask的session会读取浏览器的cookie生成
测试时清空服务器的session，就必须清空浏览器的cookie


### state是用户和服务器之间的令牌
```
@app.route('/login/', methods=['GET', 'POST'])
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('loginweibo.html', STATE=state, REDIRECT_URI=redirect_uri, CLIENT_ID=client_id)
 
 
 
 
@app.route('/gettoken/', methods=['GET', 'POST'])
def gettoken():
    print "weibo gettoken in"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
```


### 获取数据
获取url中的参数值：
```
request.args.get("state")
```


获取POST表单中的参数值：
```
request.form.get("state")
```

直接获取POST的数据：
```
request.data
```

### route
`@app.route('/test', methods=['GET', 'POST'])`
不加`methods=['GET', 'POST']`的话，如果html表单向服务器发送POST请求，flask会在页面提示：
Method Not Allowed
The method is not allowed for the requested URL.

两个都可以访问：
http://localhost:5000/projects 会重定向到/projects/
http://localhost:5000/projects/
```python
@app.route('/projects/')
def projects():
    return 'The project page'
```

http://localhost:5000/about 可以访问
http://localhost:5000/about/ 这个url会返回404（Not Found)
```
@app.route('/about')
def about():
    return 'The about page'
```

### url_for
url_for的第一个参数是端点（默认就是方法名），而不是路径名
其他参数是函数的参数（路径中的xxid）
以下是官方文档：
URL Building

If it can match URLs, can Flask also generate them? Of course it can. To build a URL to a specific function you can use the url_for() function. It accepts the name of the function as first argument and a number of keyword arguments, each corresponding to the variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters. Here are some examples:

```python
>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
...
>>> @app.route('/login')
... def login(): pass
...
>>> @app.route('/user/<username>')
... def profile(username): pass
...
>>> with app.test_request_context():
...  print url_for('index')
...  print url_for('login')
...  print url_for('login', next='/')
...  print url_for('profile', username='John Doe')
...
/
/login
/login?next=/
/user/John%20Doe
```

端点endpoint设置：
```python
@app.route('/greeting/<name>', endpoint='say_hello')
 
def give_greeting(name):
 
    return 'Hello, {0}!'.format(name)
 
```


### flash闪现消息

服务器生成flash消息：
```python
flash("item %s has been deleted" % (menu.name))
```
jinja模板中显示flash消息：
```html
{% with messages = get_flashed_messages() %}
{% if messages %}
<ul>
{% for message in messages %}
    <li><strong>{{message}}</strong></li>
{% endfor %}
</ul>
{% endif %}
{% endwith %}
```
### submit后后端接收input控件的值

input元素的name属性的值是key，value属性的值是value。
flask框架使用

```
<input type = 'text' size = '8' name='price' placeholder = '{{item.price}}'>
 
request.form[' price ']
 
```

## SQLAlchemy

### sqlArchemy关联查询

Model定义时加上外键、以及关联关系字段，查询时就可以通过category、user来引用关联表的数据。

    cat_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(Category)
### sqlArchemy连接sqlite的db文件

```
engine = create_engine('sqlite:///restaurantmenu.db')
# 不会重建已有的表
 
Base.metadata.create_all(engine)
```
### 建立表
```python
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
Base = declarative_base()
 
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    @property
    def serialize(self):
        return {
            "name":self.name,
            "id":self.id,
        }
  
class MenuItem(Base):
     __tablename__ = 'menu_item'
    name = Column(String(80), nullable= False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    // restaurant.id是表明.列名
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
 
    @property
    def serialize(self):
        return {
            "name":self.name,
            "id":self.id,
            "price":self.price,
            "description":self.description,
            "course":self.course,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
 
# 对已有的表不会重新建表
Base.metadata.create_all(engine)
 
```


### Connect to database
Operations with SQLAlchemy

In this lesson, we performed all of our CRUD operations with SQLAlchemy on an SQLite database. Before we perform any operations, we must first import the necessary libraries, connect to our restaurantMenu.db, and create a session to interface with the database:


```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
 
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
```


### CREATE
We created a new Restaurant and called it Pizza Palace:
```
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()
 
We created a cheese pizza menu item and added it to the Pizza Palace Menu:
 
cheesepizza = menuItem(name="Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()
```
### READ
以下打印出来是sql语句
```python
menu = session.query(MenuItem).filter_by(id = menu_id, restaurant_id=restaurant_id)
print menu
```
以下正常获取menu
```python
menu = session.query(MenuItem).filter_by(id = menu_id, restaurant_id=restaurant_id).one()
print menu.name
```
We read out information in our database using the query method in SQLAlchemy:
```
firstResult = session.query(Restaurant).first()
firstResult.name
 
items = session.query(MenuItem).all()
for item in items:
     print item.name
```
### UPDATE

In order to update and existing entry in our database, we must execute the following commands:

    Find Entry
     
    Reset value(s)
     
    Add to session
     
    Execute session.commit()

We found the veggie burger that belonged to the Urban Burger restaurant by executing the following query:

```
veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"
```

Then we updated the price of the veggie burger to $2.99:

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

### DELETE

To delete an item from our database we must follow the following steps:

    Find the entry
    Session.delete(Entry)
    Session.commit()

We deleted spinach Ice Cream from our Menu Items database with the following operations:
```
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()
```

## fabric
### 示例
Overview and tutorial
```python
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
 
env.hosts = ['my_server']
 
def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
 
def commit():
    local("git add -p && git commit")
 
def push():
    local("git push")
 
def prepare_deploy():
    test()
    commit()
    push()
 
def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
```
### 最新fabric通过connection等对象动态执行方法
### 命令用法

**run()**：在远程服务器上执行Linux命令，还有一个重要的参数pty，如果我们执行命令以后需要有一个常驻的服务进程，那么就需要设置pty=False，避免因为Fabric退出导致进程的退出

```python
`run(``'service mysqld start'``,pty``=``False``)`
```

命令执行完返回return_code或实际的字符串输出。

## scrapy

### 安装scrapy

lxml需要libxml2依赖库，手动安装libxml2-python-2.7.7.win32-py2.7.exe和 xml-3.6.0.win-amd64-py2.7.exe 解决
其他需要手动安装的：
pywin32-220.win-amd64-py2.7.exe

VCForPython27.msi
Win64OpenSSL-1_0_2h.exe
vcredist_x64.exe

安装过程中，由于安装的是32位 Python，使用64位库导致import OpenSSL一直出错，把Python换成64位并重新安装Win64OpenSSL-1_0_2h.exe并copy dll到system32下，OK

# Web开发

## Web基础
### 重定向
当浏览器接受到头信息中的 Location: xxxx 后，就会自动跳转到 xxxx 指向的URL地址，这点有点类似用 js 写跳转。但是这个跳转只有浏览器知道，不管体内容里有没有东西，用户都看不到。
### web api 版本控制
客户端请求自定义请求头api-version:n , SpringMvc代码如下
```
@Controller
 
@RequestMapping(headers="apt-version=2")
 
public class TestControllerV2 {
 
}
```


http头设置版本

```
curl https://example.com/api/lists/3 \
 
-H 'Accept: application/vnd.example.v2+json'
 
```
### URL URI区别
URI包括URN、URL。是资源的名称、位置。
URL是资源的网络地址。
```
// URL
ftp://xxxx
mailto:xxx@example.cn
telnet://xxx
 
 
//URI
baidu.com
qq.com
```

### ip地址网段
#### 私网地址
私网地址段：
10.x.x.x、192.168.x.x、172.16.x.x～172.31.x.x、169.254.x.x
这些私网地址段是不允许出现在Internet上的，主用保留用于企业内部组网使用，在一定程度上缓解IP地址不够用的问题。

大型企业的OA网用10地址段的比较多，因为这是一个A类地址段，包含的IP很多。
小公司用192.168.0地址段的比较多。
169.254则主要是分配给DHCP服务使用的。

#### 保留地址段
128.0.x.x、191.255.x.x、192.0.0.x、233.255.255.x
这些地址被保留起来，不做分配且没有明确的用途。

#### 特殊的IP地址段,loopback地址
127.x.x.x是本地loopback地址，在windows和linux上等价于localhost,我们习惯于使用127.0.0.1，实际上ping 127.0.0.1-127.255.255.254之间的任意地址，它们是等价的。

正常的网络包从ip层进入链路层，然后发送到网络上，而发向loopback地址的包，直接在IP层短路了，也就是发到IP层的包直接被IP层接收了，不再向下发送。

#### 其它特殊IP

255.255.255.255是全局广播地址，

主机号全部为1的地址是子网广播地址，如：192.168.1.255

主机号全部为0的地址是代表该子网的网络地址，如：192.168.1.0

#### 0.0.0.0
这个IP相当于java中的this，代表当前设备的IP。

一个主机可以有多个ip，如127.0.0.1，
app.run(host='0.0.0.0',port=5000) 监听本机所有ip的5000端口


## MVC框架
Udacity的MVC：
view和model不直接通信，只通过control。
应用的状态、数据都在model保存，view更新model，model通知所有需要更新的view控件。

 

## 迭代过程

 

### 原型图

 

### Routing
**URL**

实体类别（restaurant)/new

实体类别（restaurant)/实例id/edit or delete
示例：
/restaurant/<int:restaurant_id>/edit

 

每个页面先返回一个mock信息

**flash**消息

 

# 安全认证

## 用户密码

存储hash值防止逆向

加盐后不同用户hash值不同



账户锁定控件

只对在线暴力破解适用。黑客可能会窃取到密码文件，再对该文件进行离线暴力破解。

## 客户端服务器
用户设定密码时，客户端负责校验提示，服务器还需要再次校验（不能存储弱强度密码，防止客户端以非浏览器方式设定密码）

 

# 爬虫

作用：自动化处理

## 爬取前准备

检查域名/robots.txt

描述爬取间隔、不允许链接（否则封禁ip一段时间）



网站地图

robots.txt中包含了sitmap文件地址，但经常缺失。



估算网站大小

baidu中搜索site:www.douban.com/xxx。域名后的url用于过滤，仅关心对自己有用的部分。



识别网站所用技术

```shell
import builtwith
builtwith.parse("http://example.webscraping.com")
```

http://httpstat.us/500

# 测试数据

faker 可以生成各类随机内容，如姓名、地址等

dataFaker 大批量测试数据生成工具