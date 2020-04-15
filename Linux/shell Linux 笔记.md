[TOC]

```shell
find . -name 'build.gradle' | egrep -v 'SSP-In|SSP-Bis|SSP-Base'
```



# Unix

计算机=终端+主机

终端=输入设施+输出设施

一个计算机可能有多个终端，控制台是用来管理系统的特殊终端



# 终端和Shell

注销（停止使用Unix）：logout exit login

查看最近某用户登录记录

```last <username> ```



## 键映射

^W -- 删除整个单词

^U 删除整行

^C 中断。可以结束程序

^D 发送文件结束信号eof

stty命令可以修改键映射：

stty erase ^H 将^H映射到erase信号上（删除单个字符）

## 返回和换行

返回字符=^M (也就是RETURN Enter键)

换行字符=新行字符=^J

一般文件中每行文本必须以一个新行字符结尾

按下Return键时，将发送一个返回字符，unix自动将返回字符改变为新行字符

终端显示数据时，每行必须以字符序列“返回+新行”结束。因此当数据从文件发送到终端显示时，Unix自动将每行末尾的新行字符改为返回+换行字符。

windows文本文件用^M^J

which 精确定位一个程序

users 查看哪些用户当前登录

who  显示关于当前在本地系统上的所有用户的信息，比users更详细

w命令 



less/more/vim中通用命令

q 退出

h 帮助

space/f 下一屏

b 上一屏

/pattern

?pattern

/或n 向下搜索上一模式

？或N 向上搜索上一模式

g G移动到页的顶部、底部



man命令阅读说明书页时，可以执行其他指令，如

```shell
!man whatis<Return>
```

Unix手册

```shell
# Unix手册有8节，可以查看某个小节的intro页
man <n> intro
# 指定某小节搜索该命令的手册
man <n> kill
# 快速查询命令的用途，相当于whatis
man -f time date 
# 看手册包含什么内容
whatis intro 
# 搜索命令
man -k
apropos
```

info系统

```shell
d 跳转到主菜单
l 跳转到上一个节点
space/b
Return 进入节点
```



命令语法

选项是- + 单个字母，或-- + 单词

```shell
ls -help #会被解析成ls -h -e -l -p
```

1. 方括号中都代表零或多个
2. 参数是斜体字
3. ls [-aAcCdf] [*filename*...] 所有参数在选项之后
4. man [-P *pager*] [-s *sectionlist*] name...  个别选项必须和参数一起使用
5. who [-abd] [file | arg1 arg2] 竖线表示多选一。如who /var/run/utmp , who am i



uptime查看系统启动了多久



less /etc/shells 中配置了当前系统可用shell的路径

chsh 可以改变当前或其他用户的登录shell

echo $SHELL



登录时或输入bash，启动的shell是交互式的。

运行shell脚本时，自动启动一个新shell，它是非交互式（非登录）shell。

shopt [-q] login_shell测试当前shell是否是登录shell

centos交互式登录shell或非交互式shell加--login参数时，加载配置顺序：

```shell
/etc/profile --> /etc/profile.d/*.sh
~/.bash_profile --> ~/.bashrc --> /etc/bashrc 
```

交互式非登录shell，比如执行bash命令

```shell
/etc/profile
~/.bash_profile --> ~/.bashrc --> /etc/bashrc --> /etc/profile.d/*.sh
```



https://images2017.cnblogs.com/blog/733013/201708/733013-20170823124232324-1537864058.png



对于Bourne shell家族，比如bash，变量既是局部变量也是环境变量，都是用大写字母。但不会有只属于环境变量的变量。

环境变量并不是真正的全局变量，因为子shell进程对环境变量的修改并不能传递会父进程。

父shell的局部变量无法传递给子shell



set 显示shell变量。结果中一部分变量一定也是全局变量。

创建变量，等号两边不能加空格：

NAME=value

导出到环境变量：

export NAME;

export NAME="a b";

unset命令删除变量



设置shell选项

```shell
set -o # 查看当前shell选项设置
set +o # 查看当前shell选项设置
set -o <option> # 设置开启shell选项
set +o <option> # 复位关闭shell选项
```



Unix中，单词“escape”有两种使用方法，最常见的就是从一种模式转义到另一种模式。vim中，Esc键从插入模式转义到命令模式。

shell中，escape被用作引用的同义词。 \;

单引号内引用（也就是转义）所有元字符，双引号内会保留$ \ `三个元字符的含义。

反斜线引用任何单个字符，包括新行字符

单引号是强引用，防止字符被解释，直至使用它们。



shell的内置命令会在当前shell进程内运行，输入外部命令时，shell将搜索合适的程序，然后以一个单独的进程运行。

type可以查看命令是否是内置的，或者其路径



help | less 查看所有内置命令

help [-s] [command...]



shell提示符

Bourne shell: $ date

任何一种shell，root登录： # date

bash修改提示使用环境变量，export PS1=“${USER}@\w $ "





export PS1="Your lucky number is ${RANDOM} $"

linux会使用PS1对应的字符串，使用时解析字符串里的$字符。



shell命令替换

一条命令中嵌入另一条命令。首先执行嵌入的命令，并用输出替换该命令，然后shell再执行整个命令。

```shell
echo "Current users: `users`"
```



历史命令，替换参数执行

25 vi tempfile

fc -s tempfile=data 25

export HISTSIZE=50

cd \!* && export PS1="($PWD)"

当某些内容需要被解析不止一次时，该内容必须被引用（转义）多次。

```shell
alias cd='cd $* && export PS1="($PWD) bash[\\!]$"'
```



bash默认模式下，一个用户的登录文件是.bash_profile或.bash_login，环境文件是.bashrc,注销文件.bash_logout

针对系统公共的配置：登录文件/etc/profile，环境文件/etc/bashrc

.bashrc执行了/etc/bashrc

.bash_profile执行了.bashrc



通常，点文件是被程序默认使用的配置文件

环境初始化文件名称一般以rc结尾。(run commands)



ls -a显示包括点文件



bash的登录shell：执行登录文件、环境文件

非登录shell：只执行环境文件

登录文件的内容：

- 设置PATH、PAGER等变量
- umask设置文件创建掩码
- stty键映射修改
- 其他登录相关

环境文件的内容：

- 设置自定义项，如shell选项、alias、函数



Unix设计准则：

- 每个程序或命令只完成一件事情，要做到最好
- 当需要新工具时，最好对现有的工具组合，而不是编写一个新工具
- 概括来说就是，small is beautiful

unix设计准则的缺点：

- vi很复杂但却很流行
- CLI无法处理图形图像、不是纯文本的文件

Unix新设计准则：除非程序无法更小，否则小的就是完美的。



登录时，shell自动将标准输入设置为键盘，标准输出和标准错误设置为屏幕。

每次输入命令时，可以告诉shell在此命令执行期间重置标准输入、标准输出、标准错误。

标准输出重定向到文件时（> >>)，错误仍显示在显示器上。

sort默认从键盘读入。同时制定stdin、stdout，排序后写入文件：

sort < /etc/passwd > report.txt



Unix进程中，每个输入源、输出目标都用文件描述符标识。

重定向输入输出的正式语法：

```shell
calculate 8> results
command 0< inputfile
command 1< outputfile
command 2< errfile
sort 0< /etc/passwd 1> report.txt 2>errors

# bash 输出、错误都重定向到一个文件
sort 1> output 2>&1
# bash
sort &> output
# bash 输出、错误都追加到同一个文件
sort >> output 2>&1
# 丢弃输出或错误
command 2> /dev/null

# 输出+错误通过管道传送给另一条命令
command 2>&1 | command2
```

默认，Unix为每个进程提供3个预定义的文件描述符，大多数时候够用。

0 标准输入

1 标准输出

2 标准错误



管道符号：

一个程序的标准输出成为下一个程序的标准输入

tee从标准输入读入，向标准输入和文件发送数据

```shell
cat name1 name2 | tee file1 file2 | grep Harley
tee [-a] file... # a选项追加
```





## 子shell

shell中，如果输入的是外部命令，则：

1. 查找合适的程序
2. 以一个新的shell子进程运行这个程序
3. 子shell继承父shell的环境，但子shell对环境的任何改变都不会传递回父shell。
4. 程序终止时，shell父进程重新获得控制权，并等待输入另一条命令

为了将环境重置回原来的状态，可以在子shell中运行多条命令：

```shell
(cd ../dir; export DATA=statistics; calculate)
```



## 条件执行

```shell
# command1执行成功才执行command2
grep Halry peopel > /dev/null && sort people > contacts
# command1执行失败才执行command2
update || echo "Update Failed."
```

## shell过滤器

过滤器：从标准输入读取文本数据，向标准输出每次一行的写入数据。

管道线命令的第一条和最后一条可以不是过滤器。

cat

```shell
# 键盘输入几行内容，追加到文件
cat >> data
# 查看文件末尾
# 连接多个文件
cat file1 file2 | sort
```

tac反转行的顺序



cut

抽取数据列

```shell
# 抽取数据列的方式，抽取用户标识
who | cut -c 1-8
# -f意思是filed，抽取数据字段 -d指定delimiter
cut -f 1 -d ':' /etc/passwd | sort
cut -f 1,3-5 -d ':' /etc/passwd | sort
```

colrm

删除数据列

```shell
colrm 14 30 # 删除14-30列（包括这两列）
```

rev

反转字符顺序



paste 组合多个文件的数据列为一个大表

nl 添加行号



wc 默认统计行数、单词数目、字符数

wc -lwc



grep

可以alias grep=‘egrep’

```shell
ls -F # 给子目录后追加反斜线
grep -c # 统计行的数量
-v #抽取不包含该模式的行
-i # 忽略大小写
-n #给输出添加该行作为输入时的行号
-l #仅显示包含该模式的行的文件名称
-w # 仅搜索完整的单词
-r # 递归搜索目录树
-E # 模式支持正则
-sx
# 统计/etc目录下所有子目录的数量
ls -F /etc | grep -c "/"
```



uniq

默认去重

-d 查看重复行

-u 查看唯一行

-c 去重+统计每行重复次数



tr ‘\r’ ‘\n’ < macfile > unixfile

# shell基本语法

## 调试

```shell
sh -x xx.sh
```



-n选项，shell不运行命令，只检查语法错误

-v shell将在执行命令之前回显每个命令

-x选项 跟踪脚本执行，可以看到变量和命令的值

## 脚本传递参数

脚本参数和函数参数都可以用：

```shell
$0 代表脚本本身，档名
$@ 所有参数的列表，可以for var in $@这样迭代
$1 
$n 第n个参数
$# 变数个数
$@ #全部参数，不包括脚本自身
${@:2} #第二个

```

判断检查参数个数

```shell
#!/bin/bash
if [ $# -ne 2 ];then
    echo "没有带参数";
fi
mem=$2
```



可变参数必须放在后面。前面的参数比如$1如果为空，那么后面的$2就会变成$1

## 返回值

方法只能返回0和1

返回数据可以通过修改全局变量

## exit

exit 0 成功后退出

其他状态值表示异常

## set

set -- 将所有参数设为位置参数，之后的命令可以通过`$1、$@`来引用



## declare

声明变量类型

declare -iarx sum=3

a 数组  i 整数  r 只读 x 环境变量

 

## export unset

提升为环境变量

`export sum`

 

扩增变量内容

```shell
PATH="$PATH":/home/bin
export PATH=$PATH:/usr/local/apache/bin
```



引用变量

```shell
echo $PATH
echo ${PATH}
echo "$PATH"
```

查看一些重要变量：

```shell
查看环境变量 env
查看所有变量 set
set中重要的环境变量
PS1：命令提示符
$:当前shell的PID
？:上一条执行指令的回传值 0代表执行成功
-：
echo $-
查看-i信息（是否是交互式脚本启动的bash）
hB 非交互式
himBH 交互式
```



## 变量内容操作

 去掉后缀

```shell
tardir=${tarname%.*}

#当前目录名
cwd=$(pwd)
echo ${cwd##*/}
```

## unset

取消变量

unset sum

 

str不存在输出错误信息“expr”

var=${str?expr}

 

## login shell和non login shell

login shell启动读取和执行两个配置文件

系统整体设定 /etc/profile

个人设定 ~/.bash_profile 或 ~/.bash_login 或 ~/.profile 其中之一

退出读取和执行 ~./.bash_logout

non login shell

只读取    ~/.bashrc

 

stty 终端的输入环境设定

 

set

设定指令输入输出环境，例如记录历史命令，显示错误内容等等。

set -u

set -x

 

 

组合热键

执行结果

Ctrl + C 终止目前 的 命令

Ctrl + D 输入结束 (EOF),例如邮件结束 的 时候;

Ctrl + M 就是 Enter 啦!

Ctrl + S 暂停屏幕 的 输出

Ctrl + Q 恢复屏幕 的 输出

Ctrl + U 在提示字符下,将整列命令初除

Ctrl + Z 『暂停』目前 的 命令

 

last 近期登录信息



## 命令结果赋值给变量

```
 
content=$(cat test.xml);
 
curl -d "$content" xxxurl
 
```

## 多条命令逻辑运算实例

请问 foo1 && foo2 | foo3 > foo4 ,这个 指 令串当中, foo1/foo2/foo3/foo4 是 指 令还是档

案? 整串 指 令 的 意义为?

foo1, foo2 不 foo3 都是 指 令, foo4 是装置 或 档案。整串 指 令意义为:

(1)当 foo1 执行结果有错诨时,则该 指 令串结束;

(2)若 foo1 执行结果没有错诨时,则执行 foo2 | foo3 > foo4 ;其中:

(2-1)foo2 将 stdout 输出 的 结果传给 foo3 处理;

(2-2)foo3 将杢自 foo2  的  stdout 当成 stdin ,处理完后将数据流重新导向 foo4 这个装置/档案



ls /mydir && echo "exist" || echo "not exist"



## 条件判断



[ ] 中每个组件都要用空格分开，用于容纳判断语句


```shell
[ 判断条件1 -o 条件2] #或
[ 判断条件1 -a 条件2] #与


# 文件表达式
if [ "$svnenv" = "sandbox" ]
if [ -e  fileOrDir ] #如果存在
if [ -f  file ]    #如果文件存在
if [ -d ...   ]    #如果目录存在
if [ ! -d "/myfolder" ]; then #如果不目录存在
  mkdir /myfolder
fi
if [ "ls -A $DIRECTORY" = "" ] #目录下是否有文件
```

整数变量表达式


```shell
 if [ int1 -eq int2 ]    #如果int1等于int2 
 if [ int1 -ne int2 ]    #如果不等于  
 if [ int1 -ge int2 ]     #  如果>=
 if [ int1 -gt int2 ]      # 如果>
 if [ int1 -le int2 ]       #如果<=
 if [ int1 -lt int2 ]       #如果<
```

字符串变量表达式


     If  [ $a == $b ]                 如果string1等于string2   字符串允许使用赋值号做等号
     if  [ $string1 !=  $string2 ]   如果string1不等于string2     
     if  [ -n $string  ]             如果string 非空(非0），返回0(true)
     if  [ -z $string  ]             如果string 为空
     if  [ $sting ]                  如果string 非空，返回0 (和-n类似) 

 



















## [[ ]]

目前我没用过。

这是个shell 关键字，使用如


     [[ -d $DESDIR ]]
     
     [[ -z "$1" || -z "$2"  || -z "$3"  ]]
     
     [[ "$oldtarname" = '' ]]


## sh命令

sh -n script.sh 查询语法问题

sh -x .sh 列出执行过程

## 默认shell

centos的默认shell是bash，/bin/sh是指向bash的软连接

# 进程

unix一个处理器一次只能执行一个进程，每个进程轮流在一个时间片（10毫秒）内使用处理器，执行完挂起，调度器决定接下来执行哪一个进程。

/proc/下进程有对应子目录，放置该进程的相关信息，如cwd

进程使用系统调用和内核通信。

运行外部进程的过程：

1. fork出子进程
2. 子进程使用exec系统调用运行外部程序
3. 父进程使用wait暂停
4. 外部程序结束，子进程使用exit停止自身，成为僵进程

## 空闲进程

1. 引导过程末尾，内核创建一个特殊进程，pid为0，不通过分叉。也叫空闲进程
2. 分叉创建#1号（init)进程，然后执行简单的循环，donothing。
3. init进程执行设置内核及结束引导过程的剩余步骤。
4. 没有进程执行时，调度器就运行空闲进程。此时它就像消失一样。

## 初始化进程

进程表中的第一个进程

1. 打开系统控制台，挂载根文件系统
2. 运行/etc/inittab中的shell脚本，过程中多次分叉，创建运行系统所需基本进程，并允许用户登录。init是其他进程的祖先。
3. 一直存在直到系统关闭。init进程会自动收养孤儿进程，清除僵进程

## 作业控制

后台运行

> 命令末尾键入&字符，让程序后台运行。但不改变标准I/O，而且标准输入会无法连接上（与/dev/null相连）
>
> 如果后台进程试图从stdin读取输入，stdin没有任何内容，该进程将无限期地暂停，等待输入。唯一的办法是用fg命令将进程移到前台。

将每条输入的命令视为一个作业，由作业ID来标识。通过一系列命令、变量、终端设置、shell变量、shell选项一起使用。

作业控制命令

```shell
jobs # 显示作业列表
jobs -l # 显示作业列表和对应进程号
ps
fg # 重新启动当前作业
fg <job>
bg
suspend #挂起当前shell
^Z #挂起当前作业(暂停，还可以继续运行)
kill或^C #终止作业
kill [-9] <pid> # -9不释放正在使用的资源（文件、内存）
kill [-9] %<jobId>

echo $$ 显示当前shell的PID
echo $! 显示上一条到后台的命令的PID

stty tostop # 挂起视图向终端写数据的后台作业
stty -tostop

set -o monitor 允许作业控制
set +o monitor 关闭作业控制
set -o notify 当后台作业结束时立即通报
set +o nofity 关闭notify
```

运行耗时长的命令时，可以先挂起再移至后台

```shell
^Z
bg
```





suspend挂起shell后，会回到上一个shell。比如可以用来：

1. 挂起超级权限的shell，返回自己用户登录的shell。
2. 需要继续完成管理工作时，fg命令将超级用户的shell移回到前台。

jobs的输出：

- 减号表示当前作业，是最近挂起的作业，如果没有挂起的作业，则是最近移到后台的作业。
- 当前作业的下一个作业

## ps ptree

 

查看进程是否存在

```shell
cnt=ps -ef|grep mysqld_safe | wc -l
if [ $cnt -gt "0" ];then
echo "MySQL daemon is Ok!"
fi
```

查看mysql从的状态

```shell
status=mysql -uroot -p123456 -e "show slave status \G" | grep Last_Errno
echo $status
```



ptree -p 进程号/用户标识

## 守护进程

ps 输入列tty如果是?，表示该进程没有控制终端。守护进程不与任何终端相连，后台静静运行，提供服务。

守护进程的特点

1. 许多名称以“d”结尾
2. 最终都是进程#1的孩子
3. 由/etc/rc.d/init.d目录下的shell脚本启动、停止、重启

ps -ly查看状态S

```shell
D 不可中断睡眠，一般是IO
I 空闲
R 正在运行或可运行
S 可中断睡眠
T 挂起
Z 僵进程
```

ps -ef 显示系统中正在运行的所有进程

## 作业和进程

内核使用进程表记录进程

作业由shell控制，使用作业表记录作业。





```shell
# 生成一个单独的进程和作业
date；
# 生成4个进程和一个作业
who | cut -c 1-8 | sort | uniq -c
# 生成4个进程和4个作业
date;who;uptime;cal 12 2008
```

## 后台执行

```
 nohup command > filename 2>&1 &
```



## top

top工作在原始模式下，可以键入不同的命令

```shell
h 帮助
Space 立即刷新显示
-d 指定间隔s
-p 显示一个进程的信息

```

 动态查看进程变化

M 按%MEM排序

P 恢复按%CPU排序



top命令中VIRT、RES和SHR的含义

VIRT表示的是进程虚拟内存空间大小。VIRT包含了在已经映射到物理内存空间的部分和尚未映射到物理内存空间的部分总和。

RES：进程虚拟内存空间中已经映射到物理内存空间的那部分的大小。看进程在运行过程中占用了多少内存应该看RES的值而不是VIRT的值。

SHR: shared memory。 多个进程都会依赖于外部的动态库(.so) ,动态库加载后的物理内存会映射到进程的虚拟内存空间。

进程独占内存：RES的值减去SHR

## kill

```shell
kill -signal PID 或 %jobnumber
kill -l 查看signal
kill -1 类似重新启动
-9 -15
# 停止所有java进程
ps -ef|egrep 'java' | grep -v grep | awk '{print $2}' | xargs kill -9

```









## netstat -ntlpu

-a 所有连接、监听、socket数据

-t 列出tcp数据包

-u udp包

-l 列出listen的服务

-p PID

# 系统管理





## 启动日志

dmesg | less

b向后移动一屏，space向前移动一屏 q退出 h帮助



运行级别

指定Unix将提供哪些基本的服务（进程组）

Linux默认引导至级别3（多用户 命令行）或级别5（多用户 GUI）

运行级别0 关机

运行级别6 重启

超级用户下修改运行级别：

```shell
sudo init 0 #相当于shutdown
sudo init 6 #reboot
```





/etc/passwd 每个用户标识的基本信息

## 版本

cat /etc/redhat-release 查看centos版本

 cat /proc/version

uname -a 内核信息

```shell
[root@linuxprobe ~]# reboot
[root@linuxprobe ~]# poweroff
```



## free -mt 

内存使用情况

-m MB

-t 包括swap

 

## uname 

查看系统与内核相关信息

uname -a

 shutdown

-t 秒数           过几秒关机

-r 系统服务停掉后重启

-h  系统服务停掉后立即关机

 

## 忘记密码

1. 重启读秒时按任意键
2. e进入kernel
3. 输入single 再按b 进入单人维护模式
4. passwd修改root密码

## SELINUX

查看SELINUX状态的命令：sestatus 

[root@tt~]# sestatus -b | grep ftp
ftp_home_dir                                off

[root@tt~]# setsebool -P  ftp_home_dir  on

setsebool -P ftpd_disable_trans on

setsebool -P ftpd_disable_trans 1    

# 

## 开机启动流程

/etc下是系统服务daemon的配置文件

/etc/init.d/下是一般daemon（可独立启动）的启动配置脚本

/etc/xinetd.d/下是超级daemon程序xinet管理的服务配置文件

/etc/services 服务与端口号对应关系

/etc/sysconfig/iptables

iptables和TCP warppers都是防火墙

TCP warppers针对服务设定：

```
 /etc/hosts.allow
 
/etc/hosts.deny
```

开机流程：

BIOS ==> MBR（里面有boot loader，也就是grub,用来加载kernel)

==> kernel ==> 解压initrd档案作为虚拟文件系统

==> 加载核心模块（USB SATA LVM RAID等驱动程序）

==> 由/etc/inittab配置文件启动init程序    

```
     设定runlevel
 
      执行/etc/rc.d/rc.sysinit 系统初始化
```

==>  daemon start /etc/rc.d/rc[0-6].d/*

==> 加载本机设定 /etc/rc.d/rc.local

每个用户登录都会执行/etc/profile, 然后执行.bash_profile 

## 服务自启动

chkconfig 会在/etc/rc.d/rc[0-5]目录下创建联结 /etc/init.d/下的脚本
rc.local下的脚本开机会自动执行

 

图形接口是runlevel5


chkconfig --list [service_name] 查看服务开机启动状态

chkconfig [--level [0123456]] [服务名称] [on|off]


    e.g.:  chkconfig  service_name

 























































chkconfig也可以管理super daemon 管理的服务、以及自定义服务（/etc/init.d下的）

 

 

network 网络设定

portmap 辅助RPC

sshd     远程联机（比起telnet，有加密）

sendmail

xinet     也就是super daemon

syslog     系统日志，产生的信息包含/var/log/messages

 

## 开机执行命令

将命令加入/etc/rc.d/rc.local或 /etc/rc.local（软连接）

 

# 文件管理

Unix文件系统是一个逻辑上的目录树形结构。

实际工作的是虚拟文件系统（VFS)和各个设备文件系统。

1. 程序需要IO操作，向VFS发送请求
2. VFS定位合适的文件系统，通知设备驱动程序执行IO
3. VFS相当于程序与各种设备文件系统之间的中间层。

用户标识和程序有相同的权限。

## 启动

开机自检后，引导加载程序从引导设备中读取数据，将操作系统加载到内存中。引导设备一般是本地硬盘驱动器上的一个分区，也可以是网络设备、闪存等。

引导设备上的根文件系统自动挂载，包括/下这些目录：

/bin /boot /dev /etc /lib /root /sbin /tmp

有3个其他文件系统可能位于单独设备上：

/usr /var /home

## 组织结构

```shell
/   - home
	- usr	- bin
    ...		- include 
    		- local
    		...

```

顶级目录

```shell
/bin 基本程序
/boot 启动所需文件。内核必须在这个目录
/dev 设备文件
/etc 配置文件
/lib 包含运行/bin /sbin目录中程序所需的基本库和内核模块
/lost+found 未正常关机，仅完成部分写入的文件将受到损坏。下次启动时自动修复的文件放在这里
/mnt，不能挂载在其他位置上的固定介质的挂载点（如额外的硬盘）
/media 可移动介质（如软盘）的挂载点
/opt 第三方应用程序（可选软件）
/proc
/root root用户的home目录
/sbin root用户运行的基本系统管理程序
/tmp 临时文件，重启后丢失
/usr 静态数据使用的辅助文件系统，通常挂载
/var 可变数据使用的辅助文件系统，通常挂载文件系统。存放日志、邮件消息等。主要针对系统管理员
```

usr

根文件系统只存放最重要的文件，即启动和解决问题所必须的文件，其他的文件都存储在usr文件系统上。

/home也常属于辅助文件系统，单独挂载

## 磁盘分配单元和块	

文件系统中，空间以块分配，大小有512字节、1KB、2KB、4KB。

查看系统块大小

```shell
dumpe2fs /dev/hda1 | grep "Block size"
```



磁盘也以固定大小的分配单元分配空间。

查看分配单元大小

```shell
echo "D" > temp
du -h temp
```

## 链接

Unix创建文件：

1. 存储设备上保留一块空间存储数据
2. 创建索引节点inode，存放文件基本信息。inode包含使用文件所需的全部文件系统信息。

```shell
stat
# 查看inode编号
ls -i
```

链接将文件名和文件本身连接起来。inode不包含文件名，它可以被不止一个文件名引用。

链接是cp、mv、rm、ln的基础。

```shell
# 可以显示该文件有的硬链接。第一个数字是link数
ls -l 
```

软连接是符号链接，类似快捷方式，因此可以跨不同的设备文件系统

```shell
ln -s srcfile desfile
```

增加一个新档案，block存储源文件名

用途广泛



ls -al 

## 文件句柄

  进程使用的Fd数量(统计进程打开的句柄数)。

`ls -l /proc/<pid>/fd | wc -l` 

## locate

locate使用数据库，定期更新文件索引

```shell
# 使用正则
locate -r '.jpg$'
# 只匹配basename
locate -br '^temp$'

```

## find

find path… test… action…

find命令分为3部分：

1. 路径
2. 测试，也就是查找条件，如-name
3. 动作。搜索完成后执行的操作，如-print

```shell
# 测试
-type f
-mmin -30 #30分钟内修改过的文件
-atime +180 -print #180天来没有使用过的文件
# 对测试取反
-type f \!

# 动作
-print
-ls
-delete
-exec command {} \; # {}指代匹配的文件名
-ok # exec每一条前都确认
```

### 查询日志

查找返回code非0的响应记录

```shell
find . -name 'console*' | xargs egrep 'Action.commit.*return.*code":[1-9]'
```

查找时间段日志

例如查找`2013-08-08`到`2013-09-01`号之间的文件，使用如下命令即可：

```shell
find /log/ -name 'production.log-2013*' -newermt '2013-08-08' ! -newermt '2013-09-0
```

查找最近15分钟内修改过的日志

```shell
find . -regextype 'posix-egrep' -regex  '.*/console.*log.*|.*/nohup.out' -type f  -mmin -15 | xargs grep 'code":508'
```

-mtime 单位是天

linux不存储创建时间

 mtime是修改时间

atime 访问时间

ctime inode更改时间

### 拷贝文件

```shell
mkdir outputdir;
find . -name '*.tar' $JENKINS_HOME/workspace/$foldername -mmin -180 -exec cp {} outputdir \;
```



## stat

```shell
stat file.txt 
```

### 根据文件名和内容搜索并作为参数执行

`find / -name "mongod.lock" -exec rm -f {} \;`

`find / -name "mongod.lock" | xargs rm -f {} \;`

### 递归搜索目录下文本并替换

`find -name  "console.*"`

`find -name "*.properties" | xargs grep "字符串1" -l | xargs sed -i "s/字符串1/字符串2/g"`

sed不支持{n}语法

## xargs

find的结果给xargs批量处理

```shell
# -i可以多次使用参数
xargs -i mv {} ~/backups/{}.old
```



## 挂载

存储设备都有自己的小文件系统，如果要访问，必须附加到主目录树上。

这种方式连接小型文件系统时，称作挂载该文件系统。

附加到的目录叫做挂载点。

断开文件系统时，称作卸载该文件系统。

系统每次启动时，会挂载一些本地文件系统。一般超级用户才能挂载文件系统。



mount -l

mount 文件系统装置 /dev/... dirpath 挂载

umount -f(force) 卸载

mount -o loop /root/centos5.2_x86_64.iso 特殊装置loop挂载（映像不刻录就挂载使用）

 

开机挂载的配置文件 /etc/fstab

实际挂载文件记录 /etc/mtab 与/proc/mounts（内存中）

 

## ls tree

```shell
# 显示目录总大小或文件大小、以及目录中文件大小
ls -s /bin
# human-readable
ls -sh /bin

# 下面选项ls tree都有
-a 包括点文件
-t 按修改时间排序
-F 显示文件或目录类型
-s 显示文件大小

tree -d # 仅显示目录
-f #显示完整路径
-i # 省略缩进
tree -dif / |grep '/bin$'
```



## du

disk usage，显示文件大小

```shell
# 总和、人类可读(自动调节单位)
du -sh ~ 
# 统计多个目录
du -csh /usr/bin /bin /etc 2>/dev/null

# 统计目录总大小
du -h --max-depth=0 /u01/workspace
# 统计目录总大小及子目录大小
du -h --max-depth=1 /u01/workspace
```



## setuid

setuid权限允许其他用户以超级用户权限运行该程序，这样该程序就能完成一些超级用户才能做的任务（如修改/etc/passwd文件）

设置后，x权限被s权限替代。

## umask

unix创建新文件时，根据类型指定初始模式：

666 不可执行文件

777 可执行文件、目录

初始模式上减去掩码，得到创建后的权限值。

## rm 

rm -if 防止误删文件

****

## touch

用来改变文件访问时间、修改时间

## chown chmod

```
 
chown
 
chgrp
 
chmod u=rwx,g=rx,o=r filename
 
 
chmod 754 filename
 
```

目录权限

r 读：可查看目录下的内容

w 写：修改目录下的内容

x 可执行：可将目录作为当前工作目录，可对目录中的文件执行。在目录下新增文件

t 非拥有者/root 不能删除移动

文件权限：

s :执行时，一般使用者暂时获得属主/属组权限

 

档案具有SUID的特殊权限时：

代表此用户执行此一binary程序时，在执行过程中用户会暂时具有程序拥有者的权限

方便group其他用户和other用户获得owner权限，以修改其他档案

如，

[root@www ~]# ls -ld /tmp ; ls -l /usr/bin/passwd

drwxrwxrwt 7 root root 4096 Sep 27 18:23 /tmp

-rwsr-xr-x 1 root root 22984 Jan  7  2007 /usr/bin/passwd

 

 

sgid权限作用在档案上和suid类似

作用在目录上：

目录具有SGID的特殊权限时，代表用户在这个目录底下新建的档案之群组都会与该目录组名相同。可以理解为，在此目录下即为执行该目录，执行过程中用户的群组都临时和该目录群组相同

 

目录 具有SBIT的特殊权限时，代表在该目录下用户建立的档案只有自己和root能够删除！

suse的初始群组是users，方便大家共享家目录内的数据

## dev

存放表示设备的伪文件，提供设备的访问功能，如硬盘hda、SATA硬盘sda、终端tty、伪终端、随机数生成器。

## proc

存放的伪文件，提供内核数据的访问功能。

/proc/kcore实际不占空间

## 扩展根目录

linux虚拟机扩展根目录

新建分区为了加入根目录所在LVM，必须创建为主分区（和根分区相同）。扩展分区不能转换为lvm分区

# 编译安装

 

## rpm安装

rpm的优点在于：提供了二进制 + 该软件所需的依赖说明

 


Red Hat 释出的 RPM 档案，通常无法直接在 SuSE 上面迚行安装的

相同 distribution 的不同版本间也可能无法互通，例如 CentOS 4.x 的 RPM 档案就无法直接套用在 CentOS 5.x

 

 

     1. 软件档案安装的环境必须不打包时的环境需求一致或相当；

 























































     2. 需要满足软件的相依属性需求；

 























































     3. 反安装时需要特别小心，最底层的软件不可先移除，否则可能造成整个系统的问题！

 


























































安装rpm包：

 


     [root@www ~]# rpm -ivh package_name
     
     选项参数：
     
     -i ：install 的意思
     
     -v ：察看更绅部的安装信息画面
     
     -h ：以安装信息列显示安装迚度

 




























































查看软件包是否存在（安装）：


     [root@cen ~]# rpm -qa | grep 'gcc'
     libgcc-4.4.7-17.el6.x86_64
     gcc-c++-4.4.7-17.el6.x86_64
     gcc-4.4.7-17.el6.x86_64
     [root@cen ~]# which gcc
     /usr/bin/gcc

 























































     [root@cen ~]# whereis gcc
    gcc: /usr/bin/gcc /usr/lib/gcc /usr/libexec/gcc /usr/share/man/man1/gcc.1.gz

 
























































查看依赖


     rpm -qR filename.rpm

 























































rpm卸载


    rpm -e

 

























































平台说明：

noarch 无硬件等级限制。里面没二进制程序，可能是shell script

 挂载光盘，使用： mount /dev/cdrom /media

 找出档案的实际路径：find /media -name 'pam-devel*'

 测试此软件是否具有相依性： rpm -ivh pam-devel... --test

##  SRPM

SRPM的格式 .src.rpm

SRPM包含依赖说明，源码，configure,makefile,必须先编译为rpm才能安装

 

 

 

 

##  md5sum sha1sum

md5sum filename 查看文件md5校验码

 


可以建立重要文件的MD5校验和数据库，防止被篡改，提高文件系统安全性

 

##  ldd

查看binary档案含有哪些动态函数库

 

##  ldconfig /etc/ld.so.conf

加载动态函数库到高速缓存

 


可以在/etc/ld.so.conf里添加自己的lib目录:

vim /etc/ld.so.conf

ldconfig 重启

ldconfig -p 列出已加载的.so

 


## patch -p mainpatchfile

## gcc

gcc编译流程：

1. gcc -c file1.c file2.c ... 编译多个文件

2. gcc -o targetBinaryfile file1.o file2.o ...

3. ./ targetBinaryfile  可以执行啦

 

##  make

实现Tarball原始码（原始码压缩为tar.gz等格式）安装，比gcc手动编译方便

需要建立makefile：configure自动侦测作业环境，如linux系统信息，软件属性，建立makefile

 


软件放在/usr/local下：

/usr/local/etc

/usr/local/bin

/usr/local/lib


/usr/local/man

 

 

软件放在/usr/local/apache下,需要把bin加入PATH，man page路径加入/etc/man.config

/usr/local/apache/etc

/usr/local/apache/ bin

/usr/local/apache/ lib


/usr/local/apache/ man

 

##  yum

yum -y list java*
yum -y install java-1.7.0-openjdk*

yum groupinstall "Development Tools"



更换yum源

1. 备份原镜像文件。`mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup`
2. `wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo`
3. 生成缓存.`yum clean all；yum makecache`

# 定时任务

 

##  at 单一排程

at 选项 TIME

-v 列出任务时间表

e.g.

TIME格式多种

04:00 2009-03-17

04pm March 17

04pm + 3 days

now + 5 minutes

 


at中的工作可以脱机后台执行，不需要一直putty联机到linux上

 

##  crontab -e

每小时任务：

30 15 * * 1-5 /usr/local/bin/tea_time.sh


anacron 配合/etc/anacrontab的设定，可执行关机期间系统未进行的crontab任务。默认只有系统计划。

 



 

 

# 用户管理命令

##  useradd vbird

执行流程：

在 /etc/passwd 里面建立一行不账号相关的数据，包括建立 UID/GID/家目录等；

在 /etc/shadow 里面将此账号的密码相关参数填入，但是尚未有密码；

在 /etc/group 里面加入一个与账号名称一模一样的组名；

在 /home 底下建立一个不账号同名的目录作为用户家目录，且权限为 700


-u 指定uid

-g 指定初始化群组组名

-r 建立系统账号，UID将会小于500

-D 设定均按照默认值

-s 指定shell 比如 /sbin/nologin

-d 指定家目录

 


suse的初始群组是users，方便大家共享家目录内的数据

 

 

##  usermod 

修改账号相关信息

和useradd用法很相似

usermod -d /home/nginx nginx

 

 

 

##  userdel

-r 连同家目录一起删除

删除用户也可以删除/etc/passwd /etc/shadow中该账号条目

 


完整删除xi，可以

find / -user username找出档案再删除

 

## passwd 

修改账号密码


passwd 修改自己的密码

passwd + 账号

 

UID/GID和账号、家目录信息在/etc/passwd保存

密码信息在/etc/shadow


## groupadd

-r 组名

-g gid

 


groupmod

 


## su

 su xx 仅切换用户，不切换环境



若要完整的切换到新使用者的环境，必须要使用『 su - username 』或『 su -l username 』， 才会连同 PATH/USER/MAIL 等变量都转成新用户的环境；

 如果仅想要执行一次 root 的指令，可以用『 su - -c "指令串" 』的方式处理；

 使用 root 切换成为任何使用者时，需要输入新用户的密码；

 

## gpasswd 

加群主管理员 设群组密码 加群组成员

gpasswd依次修改的都是/etc/gshadow中的信息

- gpasswd testgroup
- gpasswd -A vbird testgroup 设vbird为群组管理员

然后vbird就可以把成员（包括自己）加入testgroup

- gpasswd -a vbird testgroup

## sudo

-u username

-b 后台执行




以系统账号执行比较方便

```
e.g.

[root@www ~]# sudo -u vbird1 sh -c "mkdir ~vbird1/www; cd ~vbird1/www; \ >  echo 'This is index.html file' > index.html"
 

sudo搭配su - 使用用户自己的密码转换为root身份

[root@www ~]# visudo User_Alias  ADMINS = pro1, pro2, pro3, myuser1 ADMINS ALL=(root)  /bin/su -
```



**sudo重置环境变量问题**

现象： 

sudo ./bin/WDSS start导致启动的classpath缺少/usr/java/jdk1.7.0_79

而root用户下执行 ./bin/WDSS start，就正常启动了。

原因：sudo命令会重置环境变量，默认的环境变量需要在/etc/sudoers中配置。导致JAVA_HOME为空

解决办法：sudo -E command 或者 su - root后再执行命令



**添加sudo用户sino**

通过visudo打开/etc/sudoers文件，添加以下行并保存

` sino  ALL=(ALL)       NOPASSWD: ALL` 



# 文本显示

## hexdump

显示二进制文件

## vi

vi命令 ：单字母或双字母开头，比如w、dd、ZZ保存并退出

ex命令：:开头，Return键结尾。如:%s/harley/Harley/g，:1,5d

移动光标

```shell
h 左
j 下
k 上
l 右
- 上一行开头
+/Return下一行开头
0 当前行开头
$ 当前行末尾
^
w 下一单词词首
e 下一单词词尾
b 上一单词词首
（ ) 句子跳
{ } 段落跳
nG 跳转第n行
G 最后一行
gg 第一行
V 行选择
```

替换命令:s

```shell
.代表当前行，$最后一行
:s 当前行替换
:n1,n2s/word1/word2/g
:1,$s/word1/word2/gc 全部替换（c表示确认）
:%s 相当于1,$s，很常用
:s/UNIX//g 删除模式
```

删除文本

```shell
:lined 删除指定行
```

撤销

```shell
u
U
```

设置

```shell
:set nu 显示行号
:set showmode 显示处于哪种模式

查看文件行结束格式 
:set ff 或 :set fileformat
修改
:set ff=unix 或 :set fileformat=unix 
:wq
:set all
```

不停止vi，输入shell命令

```shell
:!date
:sh
```



:sp (filename)
ctrl+w+j/k切换窗口



多个文件工作

```shell
:n
:N
:files
#:r命令
:0r file1 读取file1插入到当前文件开头
:0r !ls 执行命令把输出插入
```

vi -R 只读

vi -r 异常关机后，从临时文件恢复文件

^L 重新显示各行

## less

-m 显示当前到文档的%多少

-i 搜索时不区分大小写

export LESS=‘-CFMs’

终端驱动程序的line disciplie有两种：

- 规范模式（成熟模式 cooked mode） 
- 原始模式（raw mode)

## grep

grep命令逐行匹配文本，匹配到的行才显示出来

```shell
# 得到<行号>:  
grep -n xxx filexxx
egrep ‘walter|metal’ filexxx


grep -v 反向选择

#取出首字符非字母的行
grep -n '^[:alpha:]' regular_express.txt

e.g.
ls | grep '^a.*'
ls -al | grep '^l.*'
grep '*' $(find /etc -type f) 找到包含*的文件

# 不忽略二进制数据。否则会提示“binary file matches”错误
svn list <paht> | grep -a
```

## tail head

```shell
head tail -n 数字的符号区分
-n后面的数字无符号，表示行数。如 tail -n 5 1.txt 后5行；
   正数：表示从正数第几行起。 如 tail -n +5 1.txt 从前面开始的第5行到结束
   负数：表示从倒数第几行起。如 tail -n -5 1.txt 从后面数第5行到结束
head一样：head -n 5 1.txt 前5行
 head -n +5 1.txt 从前面开始的第5行之前的部分
 head -n -5 1.txt 从后面开始的第5行之前的部分 
```

显示一个文件的内容的前多少行

```shell
# 前10行
head -n 10 /etc/profile
# 倒数第1行之前的（不包括最后一行）
head -n -1 /etc/profile
# 找出IN目录下最新的一个目录或文件路径
path=`ls -t ../IN | head -n 1`
```



## awk

awk工作流程：

1. 执行BEGIN
2. 读取文件，读入有/n换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0则表示所有域,$1表示第一个域,$n表示第n个域,随后开始执行模式所对应的动作action。接着开始读入第二条记录······直到所有的记录都读完，
3. 执行END操作。

```shell
awk '{pattern + action}' {filenames}
```

awk提供的内建变量可以在{}以外使用，内建函数必须

示例

```shell
# 空格分割并丢弃，取出第6个元素
awk '{print $6}'
# 搜索/etc/passwd有root关键字的所有行，并显示对应的shell
awk -F: '/root/{print $7}' /etc/passwd

free -m | awk 'BEGIN{time=strftime("%m/%d/%Y %H:%M:%S", systime())} /Swap/ {print time,"Swap used:"$3"MB"}';
```

## 搜索指定目录下超过指定大小的文件

```shell
#显示文件用户、属组
find /u01/app/oracle/oradata/prod/  -type f -size +500M  -print0 | xargs -0 ls –l
#显示文件详细size
find /u01/app/oracle/oradata/prod/ -type f -size +500M  -print0 | xargs -0 du –h
# 按大小排序
find /u01/app/oracle/oradata/prod/  -type f -size +500M  -print0 | xargs -0 du -h | sort -nr
```





## Linux windows转换

**换行符**

Linux是\n, 显示出来是^M

windows是\r

## diff

比较两个文件夹中文件差异

diff -Nrq folder1 folder2

r递归，q简洁输出只写明相同还是不同，N会比较列出新文件

## ls

`ls -l /usr/bin/X*`

```shell
ls -lt /dirname/ | grep filename | head -n 1 |awk '{print $9}'
逐条解释：
ls -lt /dirname/
列出此目录下的所有文件并按照时间先后排序
grep filename
过滤出包含关键字的文件
head -n 1
查看排名第一的文件
awk '{print $9}'
打印出第九字段，此处为文件名

ls -t dir | head -1

# Linux保留最近10个Adapter服务包文件，其余的全部删除。
rm `ls -t  | grep Adapter | tail -n +11`
```

## 数据流导向命令

1> file1  2>&1

&> file

 

std in 重定向

cat > catfile <~/.bashrc

用.bashrc作为输入代替stdin，输入catfile文件

mail kiki < /home/dmtsai/lover.txt :

 

 

## echo

echo -e “” 可使用转义字符

 

## 管线命令

cut 对同一行的数据分解

|cut -c 12-

|cut -d':' -f 3

 

cat -An regular_express.txt | head -n 10|tail -n 6

 

 





## sed命令

sed编辑器逐行处理文件流（或输入），并将结果发送到屏幕。sed每处理完一行就将其从临时缓冲区删除，然后将下一行读入，进行处理和显示。
sed使用的正则表达式是括在斜杠线"/"之间的模式

```shell
/正则表达式/
/^#/ 所有以#开头的行
/^$/ 所有空行
```

p命令

```
sed -n '2,4p' 只列出2-4行。没有-n则为重复2-4行 
```

s命令

-i 原地替换，对输入文件的改变是永久的，无法撤销

默认只改变每一行第一个匹配的字符串。后缀g会改变所有匹配字符串

正则里```$```匹配每一行的末尾，```$```前也就是新行字符（换行符）的前面。

```shell
 
sed 's/word1/word2/g'
"s/[0-9]\{1,4\}/256/g" #sed 替换 [0-9]+ 
 
sed 's/\/usr/root_path/g' 将/usr替换为root_path
sed -i 's/xxx/yyy/g' conf/logback.xml
 
```

-e选项可以指定多个命令

```shell
sed -i \
-e 's/mon/Monday/g' \
-e 's/tue/Tuesday/g' \
calendar
```





a命令

```shell
 nl /etc/passwd | sed '2a Drink tea or ......\ > drink beer ?'
```

e.g. 得到ip地址

```
ifconfig结果：
eth0     
Link encap:Ethernet  HWaddr 00:90:CC:A6:34:84          
inet addr:192.168.1.100  Bcast:192.168.1.255  Mask:255.255.255.0      
inet6 addr: fe80::290:ccff:fea6:3484/64 Scope:Link         
UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1 .....(

/sbin/ifconfig eth0 | grep 'inet addr' | \ >  sed 's/^.*addr://g' | sed 's/Bcast.*$//g'
结果： 
inet addr:192.168.1.100
```

d命令

```shell
sed '/^$/d' 删除空行
sed '/^#/d' 删除#开头的行 
# 删除文件空白行
sed -i '/^\s*$/d' *
```



## sort

-t指定分隔符 默认tab

-k 4指定order by 第四咧

-n 按数字排序

 

## uniq  去重

-c 计数

-i 忽略大小写

配合sort 排序后

 

tee -a filename

双重导向数据流 一个输出到屏幕

 

## 字符转换函数 tr col join paste

col tab取代为空格

tr 删除替换字符

join 相当于内连接 join -t':' -1 4 /file1 -2 3 /file2

-1 -2后接档案的字段号

join之前需要sort处理

paste 将两个文档逐行粘在一起 tab隔开

 

 

 

# 文件处理

##  tar

压缩tar

```shell
# 仅打包，不压缩。tar包中包含该目录。
tar -cvf /tmp/etc.tar /etc
#  压缩为.gz
tar  -zcvf 目标名.gz 目录1 目录2 ...
# 解压
tar -zxvf 目标名.gz -C 目录名
# -j和-z对应bz2和gz
# -p复制原有权限

# 排除部分文件或目录
tar -zcvf jenkins.tgz * --exclude=jenkins/workspace --exclude=dir1
```

## zip

zip -r &

unzip

# 网络命令

## netstat

统计TCP状态情况 

 ```shell
netstat -n | awk '/^tcp/ {++state[$NF]} END {for(key in state) print key,"\t",state[key]}'
 ```



## ssh

### SSH超时问题

方法一：export TMOUT = 0，但记得先echo下这个变量之后改回去

方法二：ClientAliveInterval 60

在/etc/ssh/sshd_config中增加ClientAliveInterval 60, ClientAliveInterval指定了服务器端向客户端请求消息的时间间隔, 默认是0, 不发送.而ClientAliveInterval 60表示每分钟发送一次, 然后客户端响应, 这样就保持长连接了.这里比较怪的地方是:不是客户端主动发起保持连接的请求(如FTerm, CTerm等),而是需要服务器先主动.

另外,至于ClientAliveCountMax, 使用默认值3即可.ClientAliveCountMax表示服务器发出请求后客户端没有响应的次数达到一定值, 就自动断开. 正常情况下, 客户端不会不响应.

##  tcpdump

`tcpdump -S -nn port 6666 and host <目标ip>`

## curl 

### 测试Get请求

加上 `-v` 参数看详细的请求信息，

```shell
curl localhost:9999/api/daizhige/article -v
```

### 测试post请求

 `-X POST` 申明请求方法。

`-d`默认就是POST请求

-H 增加Header

`$ curl -d "user=nickwolfe&password=12345"`

### 测试端口连通性

`curl ip:9999`

### 下载文件

curl -sf -o 目标文件名 -L 文件URL

### 模拟表单提交

```
# 模拟表单提交
curl \
   -F "userid=1" \
   -F "filecomment=This is an image file" \
   -F "image=@/home/user1/Desktop/test.jpg" \
   localhost/uploader.php
```







# 辅助命令

## date

以“+”号开头的参数，指定格式来输出系统的时间或日期

```shell
[root@linuxprobe ~]# date "+%Y-%m-%d %H:%M:%S"
2017-08-24 16:29:12
[root@linuxprobe ~]# date "+%j"
244

currtime=`date "+%Y-%m-%d"`
LOCAL_DIR="v$VERSION"_"$currtime"

date在脚本中的几个用法：
date +%Y 以四位数字格式打印年份
date +%y 以二位数字格式打印年份
date +%m 月份
date +%d 日期
date +%H 小时
date +%M 分钟
date +%S 秒
date +%w 星期，如果结果显示0，则表示周日
```

设置系统时间

```shell
[root@linuxprobe ~]# date -s "20170901 8:30:00"
Fri Sep 1 08:30:00 CST 2017
```



 


## ctrl+d

代表键盘输入结束，也相当于exit

 


## alias

alias pse='ps -ef|grep'

unalias pse

alias lm=‘ls -al’

 

 

## history

history 50 >> ~/.myhistory

echo $HISTSIZE

!n !命令开头 配合history使用，执行命令

如：

!4 

!al

 


## type

查看指令的类型和路径


type -tpa 指令名

-t 查看指令类型 file alias builtin

-p 查看外部指令路径

-a 列出PATH下所有同名指令，包括alias

uname -r linux kernel核心版本号

##  rename

```shell
# 把文件名包含字符串INCT的文件，文件名开头的BANCS_去掉。
find -name '*INCT' -type f | xargs rename BANCS_ ""
```







# Vim

## 查看和设置文件格式

文件的格式要是 unix. 可以通过 VI 命令 :set ff?

:set fileformat=unix

## 替换

:%s/old_str/new_str/g

 


# test命令

test -e /mydir && echo "exist" || echo "not exist"


test -z 空字符串则true test ！-z

test -n 非空字符串则true

 

 

# 第三方中间件

# 网络

## 查看端口占用

```shell
lsof -i:8000 #用于查看某一端口的占用情况
netstat -aptn |grep -i 端口号 # 用于查看指定的端口号的进程情况
```

## ssh



修改ssh服务器配置文件 /etc/ssh/sshd_config

```shell
PermitRootLogin yes
# 允许密码登录
PasswordAuthentication yes
#服务器端要设置客户的超时重连
ClientAliveCountMax 3    #默认重连3次
ClientAliveInterval 30   #30s重连一次

```

修改完成后执行

```shell
systemctl restart sshd
```

客户端要设置服务器端的超时重连(user 设置文件在~/.ssh/下)：

```shell
ServerAliveCountMax 3
ServerAliveInterval 30
```

## 设置的静态ip被局域网中其他主机占用

导致虚拟机在桥接模式下不能上网

 

1. sudo apt-get install linux-headers-generic 代替kernel-devel

2. apt-get update

   apt-get upgrade

```
然后重启
```

 

## 修改静态IP

vim ifcfg-eth0

```
 
DEVICE=eth0
 
TYPE=Ethernet
 
UUID=7f9bd4cc-2968-4db6-bb35-71b823bc1ae4
 
ONBOOT=yes
 
NM_CONTROLLED=yes
 
BOOTPROTO=static
 
IPADDR=10.1.1.80
 
NETMASK=255.255.255.0
 
GATEWAY=10.1.1.1
 
#BRIDGE="br0"
 
#HWADDR=00:0c:29:f3:55:33
 
DEFROUTE=yes
 
PEERDNS=yes
 
PEERROUTES=yes
 
IPV4_FAILURE_FATAL=yes
 
IPV6INIT=no
 
NAME="System eth0"
 
NETWORKING=yes
 
DNS1=8.8.8.8
 
DNS2=8.8.4.4
 
```

## 防火墙iptables

```
 iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 端口号 -j ACCEPT
```

# SVN

常用命令

```shell
#上传
svn import $localfile $SVN_DIR/$SERVICE/$localfile --username $USERNAME --password $PASSWORD -m "$msg"
# 复制
svn cp $SVN_DIR/$SERVICE/$pkg_dir $target/$SERVICE/$pkg_dir -m "sync $SERVICE/$pkg_dir to Production"
# 下载
svn export $SVN_DIR/$SERVICE/$LAST_DIR
```



```shell
#!/bin/bash
# svn import svn.txt https://sz-its-svn-001.sino.sz/svn/TChat/TChat%20Publish/Production/ReleaseApps/BankAddress/svn.txt --username dufa --password redis@123 -m 'test svn import'


SANDBOX_RELEASEAPPS=https://sz-its-svn-001.sino.sz/svn/TChat/TChat%20Publish/SandBox/ReleaseApps
PRODUCTION_RELEASEAPPS=https://sz-its-svn-001.sino.sz/svn/TChat/TChat%20Publish/Production/ReleaseApps
JJBANK_SSP=https://sz-its-svn-001.sino.sz/svn/TChat/银企通银行项目/开发库/九江银行/1.DOC/4-项目交付/SSP
USERNAME=dufa
PASSWORD=sinosun_df

SVN_DIR=''
LOCAL_DIR=''
VERSION=''
SERVICE=''

set_svn_dir() {
	svnenv=$1
	if [ "$svnenv" = "sandbox" ];then
	SVN_DIR=$SANDBOX_RELEASEAPPS
	fi
	if [ "$svnenv" = "pro" ];then
	SVN_DIR=$PRODUCTION_RELEASEAPPS
	fi
	if [ "$svnenv" = "jjb" ];then
	SVN_DIR=$JJBANK_SSP
	fi	
}

svn_import() {
	localfile=$1
	SERVICE=$2
	svnenv=$3
	set_svn_dir $svnenv
	msg="$svnenv uploaded:\n$SVN_DIR/$SERVICE/$localfile"
	msg=$(git log --oneline | head -n 2)
	svn import $localfile $SVN_DIR/$SERVICE/$localfile --username $USERNAME --password $PASSWORD -m "$msg"
}


svn_list() {
	SERVICE=$1
	svnenv=$2
	set_svn_dir $svnenv
	svn list $SVN_DIR/$path
}


create_dir() {
	VERSION=$1
	currtime=`date "+%Y-%m-%d"`
	
	LOCAL_DIR="v$VERSION"_"$currtime"
	echo "LOCAL_DIR:$LOCAL_DIR"
	mkdir $LOCAL_DIR
}


#svn cp index.html svn://192.168.8.194/hello/index_bak.html -m 

copy2Production() {
	service=$1
	pkg_dir=$2
	svn cp $SANDBOX_RELEASEAPPS/$service/$pkg_dir $PRODUCTION_RELEASEAPPS/$service/$pkg_dir -m 'sync $service/$pkg_dir to Production'
}
publish() {
	#cwd=$(cd `dirname $0`; pwd)
	if [ -f "build.gradle" ] ;then
		gradle -DconfigDir=bbox clean distTar
		cd build/distributions
	fi
	SERVICE=$1
	svnenv=$2
	set_svn_dir $svnenv
	
	if [ ! -n "$3" ] ;then
		lastdir=$(svn list $SVN_DIR/$SERVICE | egrep 'v'  | tail -n 1)
		lastpublish=$(svn list $SVN_DIR/$SERVICE/$lastdir)
		echo -e "lastdir:$lastdir"
		echo -e "last publish content:\n$lastpublish"
		exit 1
	else
    	VERSION=$3
	fi
	tarname=`ls *.tar  | head -n 1`
	newservicename=`echo ${tarname%.tar} | sed "s/[0-9]\..*/${VERSION}-PRO/"`
	tar xf $tarname
	mv $tarname $newservicename
	tar cf ${newservicename}.tar $newservicename
	rm -rf $newservicename
	echo "New Tar:$newservicename"

	create_dir $VERSION
	mv *.tar $LOCAL_DIR
	#mv *.txt* $LOCAL_DIR
	cd $LOCAL_DIR	
	md5sum.exe ${newservicename}.tar | sed 's/ \*.*$ //' > ${newservicename}.tar.md5
	cd ..

	svn_import $LOCAL_DIR $SERVICE $svnenv
}
```

# 故障排除

## 查看CPU占用高的线程

`ps` `H -eo user,pid,ppid,tid,``time``,%cpu|``sort` `-rnk6 |``head` `-10`

## CPU

系统负载（System Load）是系统CPU繁忙程度的度量，即有多少进程在等待被CPU调度（单核上进程等待队列的长度）。因此无论对于单核还是多核CPU，平均值接近1是比较理想的。

平均负载（Load Average）是一段时间内系统的平均负载，这个一段时间一般取1分钟、5分钟、15分钟。

 一般来说只要每个CPU的当前活动进程数不大于3那么系统的性能就是良好的，如果每个CPU的任务数大于5，那么就表示这台机器的性能有严重问题。对于  上面的例子来说，假设系统有两个CPU，那么其每个CPU的当前任务数为：8.13/2=4.065。这表示该系统的性能是可以接受的。 

top命令，w命令，uptime等命令都可以查看系统负载：

```shell
[root@opendigest root]# uptime
　　7:51pm up 2 days, 5:43, 2 users, load average: 8.13, 5.90, 4.94
```

如上所示，机器1分钟平均负载，5分钟平均负载，15分钟平均负载分别是1.58、2.58、5.58

三个时间段的平均负载能看出系统负载变化的趋势。



top
关注load、cpu、mem、swap
可按照线程查看资源信息(版本大于3.2.7)



 lscpu查看cpu架构信息 

```shell
[xxx@localhost ~]$ lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                4　　　　　　　　　　#总处理器核心数量
On-line CPU(s) list:   0-3
Thread(s) per core:    1　　　　　　　　　　#每个核心支持的线程数量。1表示只支持一个线程，即不支持超线程
Core(s) per socket:    1　　　　　　　　　　#每个处理器的核心数量
Socket(s):             4　　　　　　　　　　#处理器数量
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 63
Stepping:              0
CPU MHz:               2599.998
BogoMIPS:              5199.99
Hypervisor vendor:     VMware　　　　　　　#管理程序供应商
Virtualization type:   full
L1d cache:             32K
L1i cache:             32K
L2 cache:              256K
L3 cache:              30720K
NUMA node0 CPU(s):     0-3
```



cat /proc/cpuinfo：查看CPU详细信息 

```shell
[xxx@localhost ~]$ cat /proc/cpuinfo
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 63
model name      : Intel(R) Xeon(R) CPU E5-2690 v3 @ 2.60GHz
stepping        : 0
cpu MHz         : 2599.998
cache size      : 30720 KB
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf unfair_spinlock pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx hypervisor lahf_lm ida arat epb pln pts dts
bogomips        : 5199.99
clflush size    : 64
cache_alignment : 64
address sizes   : 40 bits physical, 48 bits virtual
power management:

processor       : 1
vendor_id       : GenuineIntel
cpu family      : 6
model           : 63
model name      : Intel(R) Xeon(R) CPU E5-2690 v3 @ 2.60GHz
stepping        : 0
cpu MHz         : 2599.998
cache size      : 30720 KB
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf unfair_spinlock pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx hypervisor lahf_lm ida arat epb pln pts dts
bogomips        : 5199.99
clflush size    : 64
cache_alignment : 64
address sizes   : 40 bits physical, 48 bits virtual
power management:

processor       : 2
vendor_id       : GenuineIntel
cpu family      : 6
model           : 63
model name      : Intel(R) Xeon(R) CPU E5-2690 v3 @ 2.60GHz
stepping        : 0
cpu MHz         : 2599.998
cache size      : 30720 KB
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf unfair_spinlock pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx hypervisor lahf_lm ida arat epb pln pts dts
bogomips        : 5199.99
clflush size    : 64
cache_alignment : 64
address sizes   : 40 bits physical, 48 bits virtual
power management:

processor       : 3
vendor_id       : GenuineIntel
cpu family      : 6
model           : 63
model name      : Intel(R) Xeon(R) CPU E5-2690 v3 @ 2.60GHz
stepping        : 0
cpu MHz         : 2599.998
cache size      : 30720 KB
fpu             : yes
fpu_exception   : yes
cpuid level     : 13
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts mmx fxsr sse sse2 ss syscall nx rdtscp lm constant_tsc arch_perfmon pebs bts xtopology tsc_reliable nonstop_tsc aperfmperf unfair_spinlock pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx hypervisor lahf_lm ida arat epb pln pts dts
bogomips        : 5199.99
clflush size    : 64
cache_alignment : 64
address sizes   : 40 bits physical, 48 bits virtual
power management:
```

## 内存

cat /proc/meminfo 查看内存配置

## IO负载

iostat：查看读写压力

iostat -x 1 2

如果 %util 接近 100%，说明产生的I/O请求太多，I/O系统已经满负荷，该磁盘可能存在瓶颈。

## 系统日志

操作系统错误日志

```
grep -i error /var/log/messages;
grep -i fail /var/log/messages
```

## 网络监控

netstat -i 检查端口是否存在

sar -n dev 检查网络流量(rxpck/s, txpck/s)是否过高

执行命令sar -n EDEV 
 执行命令netstat -i，检查发送、接收包是否有ERROR

sar：查看CPU 网络IO IO，开启参数可以查看历史数据

执行命令 netstat -nao|grep 9783; 
 netstat -nao|grep 9991;netstat -nao|grep 8088



vmstat

## 抓包

tcpdump

定位网络问题神器，可以看到TCPIP报文的细节，需要同时熟悉TCPIP协议，可以和wireshark结合使用。
常见场景分析网络延迟、网络丢包，复杂环境的网络问题分析。  



