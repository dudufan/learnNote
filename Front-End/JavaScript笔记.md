[TOC]

# 推书

javascript dom编程艺术 （基础）
javascript高级程序设计（基础）
高性能网站建设指南（第二版） （前端）
css 揭秘 （进阶强烈推荐）
你不知道的 JavaScript 上卷 （强烈推荐 进阶）
深入浅出 Node.js  （强烈推荐 进阶）

# MVC

## 概念
### model 

管理数据

### collections

collection of model(data)

### controller(viewModel)

1. 从视图读取数据，并向模型发送数据

### views

1. 初始化页面元素。可能需要通过control层获取model
2. 绑定事件到元素上。事件的触发可能会通过control层改变model、改变后更新view。

### routers

可以使用它和应用交互。用于跟踪应用状态

### MVVM

model 服务器持久化应用数据

viewModel 纯代码来表示数据和操作，用来操作数据和UI。如javaScript对象，独立于UI

view 发送指令给viewModel



 

 

# jQuery

## 安装

```
https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js
```

## ajax

jsonp方式调用，返回的是js文件，如```var returnCitySN = {}```

```js
$.ajax({
          url:api,
          data:{
            key:key,
            cityname:cityname
          },
          dataType:'jsonp'
        }).done(function(data) {
            // console.log(data);
            console.log(this);
          that.today = data.result.today;
          that.future = data.result.future;
        });
```



## jQuery对象

`jQuery`对象其实就是DOM对象的集合

**将dom对象包装成为jQuery对象**

例如

```js
$(this)

$({a:1,b:2,c:3})

$(document.getElementById('idstr'))
```
包装后只能使用jQuery对象的方法、属性，不能直接使用原来html元素的属性



**将dom对象包装成为jQuery对象**

例如

```
$(this)
$({a:1,b:2,c:3})
$(document.getElementById('idstr'))
```


jquery对象取出第一个dom对象，为了使用jquery方法，再转jquery对象

```js
$($(".slot")[0])
```




## 定时执行

循环定时执行

```js
  var getAndRun = function() {
    if (arr.length > 0) {
      var n = Math.floor(Math.random() * arr.length + 1) - 1;
      var textObj = $("<div>" + arr[n] + "</div>");
      $(".dm_show").append(textObj);
      moveObj(textObj);
    }

    setTimeout(getAndRun, 3000);
  }
```
## 动画

params是要变成的属性，如位置、颜色等。

```
$(selector).animate({params},speed,callback);
```

animate的执行本身是异步的，如果要在动画执行完成以后才执行，使用回调。

## dom操作

**寻亲**

对于jQuery选择出来的DOM元素，可以遍历它的父亲、祖先、孩子、后代、兄弟
访问树结构 level 含义
.parent() 1 父亲
.parents() many 祖先
.children() 1 孩子
.find() many 后代
.slblings() many 兄弟
备注:
上面可以在括号中可以用选择器过滤
.first() 元素array中第一个
.next() 该元素的下一个兄弟

```js
//获取、添加、移除Class
.toggleClass(className)
.toggleClass(className, boolean:addorRemove)
.addClass
.removeClass

$("body").css('color') // jquery修改css意味着添加inline css
$("#target1").css("color", "red");

//输入的值
.val()
.val('')

// 修改属性。
$("#target1").prop("disabled", true);
var $a = $("<a>").attr("href", item.web_url)
// 元素操作
$("p").append( htmlString or Element or Text or Array or jQuery) //最后添加新对象
var $li = $("<li>").addClass("article"); 
var $textObj = $('<div>' + text + '</div>');  //使用$和标签获得jquery元素
$("#target4").remove(); // 从DOM中移除元素自身
$("#target2").appendTo("#right-well"); // 移动元素
$("#target2").clone().appendTo("#right-well");// 拷贝元素
$("#target1").parent().css("background-color", "red"); // 父元素
$("#right-well").children().css("color", "orange"); // 子元素
$(".target:nth-child(2)").addClass("animated bounce");
$(".target:even").addClass("animated shake");

//修改属性
var $a = $("<a>").attr("href", item.web_url).text(item.headline.main);
var $p = $("<p>").text(item.snippet);

// 淡出效果
$("body").addClass("animated hinge");

//获取尺寸
$textObj.width()
$('.dm_screen').offset().top
$('.dm_screen').height

```

.each

```js
    .done(function( data ) {
      $.each( data.items, function( i, item ) {
        $( "<img>" ).attr( "src", item.media.m ).appendTo( "#images" );
        if ( i === 3 ) {
          return false;
        }
      });
 
    $.getJSON( "ajax/test.json", function( data ) {
      var items = [];
      $.each( data, function( key, val ) {
        items.push( "<li id='" + key + "'>" + val + "</li>" );
      });
 
      $( "<ul/>", {
        "class": "my-new-list",
        html : items.join( "" )
      }).appendTo( "body" );
    });
```

## 选择器

CSS所有的选择器在jQuery中都可以使用 $("selectorString")
不会返回undefined和null，返回的是[]

选出来的元素是按HTML中出现的顺序排列,且不会有重复元素。

**根据多个class查找**

```js
var a = $('.red.green'); // 注意没有空格！
// 符合条件的节点：
// <div class="red green">...</div>
// <div class="blue green red">...</div>
```

**按属性名查询**

```js
// 找出<??? type="password">
var passwordInput = $('[type=password]'); 

// 例如: class="icon-clock", class="abc icon-home"
// 找出所有class包含至少一个以`icon-`开头的DOM
var icons = $('[class^="icon-"]'); 
```

**组合查找**

```js
// 不会找出<div name="email">
var emailInput = $('input[name=email]'); 
var tr = $('tr.red'); // 找出<tr class="red ...">...</tr>
$('p,div'); // 把<p>和<div>都选出来
$('p.red,p.green'); // 把<p class="red">和<p class="green">都选出来. <p class="red green">只会出现一次
```

## 事件

给刚添加的元素绑定事件

```
$().ready(function(){
  $("#click1").bind("click",function(){
​    $("p").append("<div class='new'><b>I'm clicked!</b></div>");
  });
  //on方法要先找到原选择器（p),再找到动态添加的选择器（.new)
  $("p").on("click",".new",function(){
　　　　$(this).remove();
  });
});
```

## 



# 事件

https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Building_blocks/Events

## 基础

当元素被点击时两个函数都会工作

```js
myElement.addEventListener('click', functionA);
myElement.addEventListener('click', functionB);
```

addEventListener的主要优点：

- 可以使用removeEventListener()删除事件处理程序代码.
- 添加多个监听器



## 事件对象



事件对象 `e` 的`target`属性始终是事件刚刚发生的元素的引用



```js
form.onsubmit = function(e) {
  if (fname.value === '' || lname.value === '') {
    e.preventDefault();
    para.textContent = 'You need to fill in both names!';
  }
}
```



当事件发生时，目标元素将调用 回调函数，jQuery 会将含有事件相关信息的 事件对象传递到此函数。该event对象包含 大量可用于 函数主体的信息。此对象通常在 JavaScript 中被引用为 e、evt 或 event，其中包含若干可用于 确定代码流的属性。

```js
//打印记录对象以查看 可用属性：
$( 'article' ).on( 'click', function( evt ) {
    console.log( evt );
});

//你应该注意 target 属性。target 属性包含 作为事件目标的页面元素。如果已为大量元素设置事件侦听器， 这可能会非常有用：


$( 'article' ).on( 'click', function( evt ) {
    $( evt.target ). css ( 'background', 'red' );
});
 
```

在上述示例中，为页面上的每个 article 元素设置了一个事件侦听器。单击某个 article 后，会将包含事件相关信息 的对象传递到回调。evt.target 属性可用于访问刚刚被单击的元素！ jQuery 用于从 DOM 中选择刚才的元素 并将其背景更新为红色。

当你想要阻止浏览器将执行的默认操作时， 事件对象还将派上用场。例如， 在 `anchor` 链接上设置一个 `click` 事件侦听器：

```js
$( '#myAnchor' ).on( 'click', function( evt ) {
    console.log( 'You clicked a link!' );
});
```

单击 #myAnchor 链接会将消息记录到控制台， 但还将导航到该元素的 href 属性， 可能重定向到新的页面。事件对象可用于 阻止默认操作：

```js
$( '#myAnchor' ).on( 'click', function( evt ) {
    evt.preventDefault();
    console.log( 'You clicked a link!' );
});
```

在上述代码中，`evt.preventDefault(); `行指示 浏览器不执行默认操作。
其他用途包括：
​    event.keyCode 用以了解按下了哪个键，如果需要侦听特定键， 则不起作用
​    event.pageX 和 event.pageY 用以了解在页面上的哪个位置进行了单击， 用于分析跟踪
​    event.type 用于发现所发生的事情，在侦听目标的多个事件时 非常有用



## 阻止默认行为

指向 xxxurl 的`<script>`加载失败

原因是表单触发jQuery的submit事件后，跳转页面了
解决办法：阻止submit后页面跳转

```
function loadData(event) {
​    event.preventDefault();
​    // Your code

};
$('#form-container').submit(loadData);
```



其他事件参考：
http://www.w3school.com.cn/jquery/jquery_ref_events.asp





## 回车提交表单

回车提交表单获取文本

```html
<form id="new-note-form" class="new-note-form">
    <input id="new-note-content" class="new-note-content">
</form>
<script>
    var newNoteForm = $('#new-note-form');
    var newNoteContent = $('#new-note-content');
    newNoteForm.submit(function(e){
        octopus.addNewNote(newNoteContent.val());
        newNoteContent.val('');
        e.preventDefault();
    });
</script>

```





# DOM操作

## 选择元素

```js
// 是推荐的主流方法会匹配它在文档中遇到的第一个元素
Document.querySelector()
// 如果想对多个元素进行匹配和操作，你可以使用
Document.querySelectorAll()，
// 这个方法匹配文档中每个匹配选择器的元素，并把它们的引用存储在一个array中。
```



## 创建元素

```js
var placeholder = document.createElement("img");
placeholder.setAttribute("id", "placeholder");
placeholder.setAttribute("src", "http://via.placeholder.com/400x300?text=Loading...");
placeholder.setAttribute("alt", "display user image");
var description = document.createElement("p");
description.setAttribute("id", "description");
var textNode = document.createTextNode("Choose a image.");
```

## 添加删除

Node.appendChild()
Node.cloneNode() 
Node.removeChild()

```js
//在段落中添加文本节点
var text = document.createTextNode(' — the premier source for web development knowledge.');
var linkPara = document.querySelector('p');
linkPara.appendChild(text);

//description元素添加文本节点，然后body添加description元素
description.appendChild(textNode);
document.body.appendChild(description);
```





## 修改css

```js


//在后面追加新的段落


// 内联CSS
HTMLElement.style.XXX =
// 应用css
para.setAttribute('class', 'highlight');

e1.getAttribute
e1.setAttribute
```

节点

    n.childNodes //节点（元素节点或文本节点)的所有子节点（也包括文本节点）
    n.nodeType //1代表元素节点
    n.nodeValue //n为文本节点时，nodeValue可以获取或设置文本
    n.firstChild //n为p时，firstchild为文本节点
    n.lastChild

**在元素之前或之后添加元素**

```js
    parmentEle.insertBefore(newElement, targetElement)
    // insertAfter需要自己编写
    function preparePlaceholder(){
        

    }
 
    addLoadEvent(preparePlaceholder);
 
    //在body最后添加元素
    document.body.appendChild(placeholder);
    document.body.appendChild(description);
    //在body最后添加元素
    document.body.appendChild(placeholder);
    document.body.appendChild(description);
```

**js判断元素是否存在**

判断是否获取：

```
if($("#tt").length > 0) {
​    //元素存在时执行的代码
}

if(document.getElementById("tt")) {//js判断元素是否存在
​    document.getElementById("tt").style.color = "red";
}
```

## 

## HTML-DOM

HTML -DOM可以在web文档中简化写法

```
    //获取元素
    document.getElementsByTagName("form")
    document.forms
    document.getElementsByTagName("body")[0]
    document.body
    //获取元素属性
    element.getAttribute("src")
    element.src
    //设置元素属性
    placeholder.setAttribute("src", source);
    placeholder.src = source;

```

dom看文档的实例：
element.innerHTML属性可以直接插入（覆盖）标签中的内容  也可以读取内容。但只能用在HTML文档中

元素隐藏

方法一：

```
document.getElementById("EleId").style.visibility="hidden";

document.getElementById("EleId").style.visibility="visible";

```
利用上述方法实现隐藏后，页面的位置还被控件占用，显示空白。



方法二：

```
document.getElementById("EleId").style.display="none";

document.getElementById("EleId").style.display="inline";

```
利用上述方法实现隐藏后，页面的位置不被占用。


## 密码md5




```html
<!-- HTML -->
<form id="login-form" method="post" onsubmit="return checkForm()">
    <input type="text" id="username" name="username">
    <input type="password" id="input-password">
    <input type="hidden" id="md5-password" name="password">
    <button type="submit">Submit</button>
</form>

<script>
function checkForm() {
    var input_pwd = document.getElementById('input-password');
    var md5_pwd = document.getElementById('md5-password');
    // 把用户输入的明文变为MD5:
    md5_pwd.value = toMD5(input_pwd.value);
    // 继续下一步:
    return true;
}
</script>

```
## 设置固有属性checked
具有true和false属性的属性，就使用prop()，比如checked    selected   disabled等，其他的使用attr()



# javaScript基础

## 浏览器加载js

浏览器遇到 `async` 脚本时不会阻塞页面渲染，而是直接下载然后运行。当页面的脚本之间彼此独立，且不依赖于本页面的其它任何脚本时，`async` 是最理想的选择

```html
<script src="script.js" async></script>
```



等待页面解析完，并且脚本顺序加载。

```html
<script defer src="js/vendor/jquery.js"></script>

<script defer src="js/script2.js"></script>
```

## 操作符

    === //严格判断相等，比较值和类型
    == //false == “” 的结果是true
    !== 不等于。判断字符串不等可以使用
    && 逻辑与

## 数据类型

基本类型： string numbers booleans undefined null

typeof运算符

    typeof "hello" // 返回 "string"
    typeof true // 返回 "boolean"
    typeof [1, 2, 3] // 返回 "object"（数组是一种对象类型）
    typeof function hello() { } // 返回 "function"
     
    string "4" "xxx"
    number 4
    boolean true false
    array： can be a heterogeneous or jagged array

 
























### Boolean

*   真值 true non-zero numbers "strings" objects arrays functions
*   假值 `false`、`null`、`0`、`""`、`undefined` 和 `NaN`

### String

str[1].toUpperCase() slice(2, str.length) slice(2)

字符串转数组

```js
  var array = str.split('');
  array = array.reverse();
  str = array.join('');
```

String的方法可以给str中每个字符使用

```js
str.substr(0,1).toUpperCase()
str[i].toUpperCase()
```

末尾n个字符

str.substr(str.length- n)

str.slice()

字母移位

```js
function rot13(str) { // LBH QVQ VG!
  // 请把你的代码写在这里
  var s = '';
  for(var i=0;i<str.length;i++){
    var x=str.charCodeAt(i);   
    if(x>=65 && x <=90){
      x = (x-65+13)%(90-65+1) + 65;
    } 
    var c = String.fromCharCode(x);
    s += c;    
  }
  return s;
}
```





### Number

num1.toFixed(2) 四舍五入到小数点后2位

### Array

**数组**

```
复制数组 [... myArray，'new value']
切片复制数组 arrayObject.slice(start,end)
连接数组 arrayObject.concat(arrayX,arrayX,......,arrayX)
```

push pop shift方法

splice push 

pop 删除并返回数组的最后一个元素

shift 删除并返回数组的第一个元素。shift和push可以实现队列，先进先出

sort升序排列数字

```js
  arr.sort(function compareNumbers(a, b) {
  return a - b;
});
```



forEach 

例1

```
    var donuts = ["jelly donut", "chocolate donut", "glazed donut"];
    donuts.forEach(function(donut) {
          donut += " hole";
          donut = donut.toUpperCase();
          console.log(donut);
      });
```


例2


```
    function logArrayElements(element, index, array) {
        console.log("a[" + index + "] = " + element);
    }
    // 注意索引2被跳过了，因为在数组的这个位置没有项
    [2, 5, ,9].forEach(logArrayElements);
 
    [2, 5, undefined ,9].forEach(logArrayElements);
    // a[0] = 2
    // a[1] = 5
    // a[2] = undefined
    // a[3] = 9
```

map 

通过 map() 方法，你可以对数组中的每个元素执行某种操作，然后返回新的数组。


```
    var donuts = ["jelly donut", "chocolate donut", "glazed donut"]
    var improvedDonuts = donuts.map(function(donut) {
      donut += " hole";
      donut = donut.toUpperCase();
      return donut;
    });
```

reduce filter sort reverse concat  split

```js
var array = [4,5,6,7,8];
var singleVal = 0;
//求和。function参数后可以跟一个初始值，默认是数组第一项
singleVal = array.reduce(function(pre, cur) {
    return pre + cur;                       
});
array = array.filter(function(val) {
  return val !== 5;
});
array.sort();
myArray.reverse();
//拼接数组
newArray = oldArray.concat(concatMe);

//reduce默认会把第一个元素作为初始值，因此一般需要指定初始值。
  var array = str.split(' ');
  var maxlen = array.reduce(function(maxlen,y){
    if(maxlen > y.length){
      return maxlen;
    } else {
      return y.length;
    }
  }, 0);
```

指定分隔符将字符串分割为数组

`var array = string.split('s');`

var salad = veggies.join(" and ");



**for in不仅可以对数组,也可以对enumerable对象操作**

```javascript
var A = {a:1,b:2,c:3,d:"hello world"};  
for(let k in A) {  
    console.log(k,A[k]);  
} 
```

### Object

定义Object

```js
var dog = { name : 'Spot', breed : 'Dalmatian' };
```

修改Obj

```js
//增加或更新属性
dog['bark'] = xxx;
dog.bark = xxx;
//删除属性
delete ourDog.bark;
//是否存在key
if(obj.hasOwnProperty("key1"))
// 深拷贝 collection，用于测试
var collectionCopy = JSON.parse(JSON.stringify(collection));

```

forEach也可以遍历Object、json

复制

```js
let newState = Object.assign({}, state);
```



## 语句

```
    prompt("") ; //input something
    confirm("") ; //eg. Do you want to leave me? yes on
    console.log(exp)
    if(true) {}else{}
    var functionName = function( ) {
        // code code code
        // code code code
        // (more lines of code)
    };
    switch(var){
        case '':
            xxx;break;
        case '':
            xxx;break;
        default:
    }
```


for in语法 for(item in object or array) item是index

## 变量和作用域

**只有全局作用域和函数作用域**

方法内定义的变量可以和global变量重名。

尝试访问标识符时，JavaScript 引擎将首先查看当前函数。如果没找到任何内容，则继续查看上一级外部函数，看看能否找到该标识符。将继续这么寻找，直到到达全局作用域。

```js
//实际上x只会在最顶上开始的地方声明一次
var x = 1;
console.log(x);
if (true) {
    var x = 2;
    console.log(x);
}
console.log(x);
```

> 上面的输出其实是：1 2 2。

变量提升：

- JavaScript 会将函数声明和变量声明提升到当前作用域的顶部。当前作用域只要找到该变量的声明，就不会去外层作用域找了。
- 变量赋值不会提升。

这个例子中，由于方法sayHi中声明了变量，所以不会去使用全局变量greeting="Hello"。变量提升，看起来就像变量的声明被自动移动到了函数或全局代码的最顶上。

```js
sayHi("Julia");
var greeting = "Hello";
function sayHi(name) {
    console.log(greeting + " " + name);
    var greeting;
}
output: undefined Julia
```

优秀实践：

*   在脚本的顶部声明函数和变量，这样语法和行为就会相互保持一致。

## 函数

匿名函数通常不会重复使用。

### 回调

函数或匿名函数都可以作为方法参数。

### this指向

this指向的永远是调用它的对象。
例子1：j或者说fn被window调用

```js
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //undefined
            console.log(this); //window
        }
    }
}
var j = o.b.fn;
j();
```

例子2：fn被b对象调用

```js
var o = {
    a:10,
    b:{
        a:12,
        fn:function(){
            console.log(this.a); //12
        }
    }
}
o.b.fn();
```

为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。

```javascript
function AppViewModel() {
    var self = this;
 
    self.firstName = ko.observable('Bob');
    self.lastName = ko.observable('Smith');
    self.fullName = ko.computed(function() {
        return self.firstName() + " " + self.lastName();
    });
    
    // 不使用self而用this
    this.fullName = ko.computed(function() {
        return this.firstName() + " " + this.lastName();
    }, this);
}
//UI
The name is <span data-bind="text: fullName"></span>

```

**new关键字可以改变this的指向**

如果函数返回值是一个对象，那么函数内的this指向的就是那个返回的对象，如果返回值不是一个对象那么this还是指向函数的实例。

```
function fn() {
    this.user = "df";
    return [];
}
var a = new fn();
console.log(a.user);// undefined

function fn() {
    this.user = "df";
    return 1;
}
var a = new fn();
console.log(a.user);// “df"
```

new Fn和new Fn()相同，都是构造出Fn的一个实例。只是new Fn后不能直接加.xxx

**箭头函数的this指向定义函数的环境**

使用function定义的函数，this的指向随着调用环境的变化而变化，而箭头函数中的this指向是固定不变的，一直指向定义函数的环境。

```js
//使用function定义的函数
function foo(){
    console.log(this);
}
var obj = { aa: foo };
foo(); //Window
obj.aa() //obj { aa: foo }
//使用箭头函数定义函数
var foo = () => { console.log(this) };
var obj = { aa:foo };
foo(); //Window
obj.aa(); //Window
```

### 箭头函数

一个返回object的函数

```js
const decAction = () => {
    return {type: DECREMENT};
};
```



### 立即执行

立即执行函数的作用：

- 创造一个作用域空间，防止变量冲突或覆盖。
- 
- 包住函数表达式的括号可以括住参数，也可以不括住，效果是一样的

```js
var cat = (function(){return {name:'nick'}());
var cat = (function(){return {name:'nick'}) () 
```

 页面全加载完再执行

```js
$(function() {//...
})；

$(document).ready(function (){//...
})；
```



## 对象



{} 空对象
String Date Array [] 內建对象
1 undefined 不是对象

### 对象定义

一种极其常见的对象定义模式是，在构造器（函数体）中定义属性、在 `prototype` 属性上定义方法。

```js
// 构造器及其属性定义

function Car(a,b,c,d) {
  // 属性定义
};

// 定义第一个方法
//这样x方法被所有实例对象共享
Car.prototype.x = function () { ... }

// 定义第二个方法

Car.prototype.y = function () { ... }

// 等等……

var myCar = new Car();
//myCard的原型也就是Car的原型。myCar ----> Car.prototype ----> Object.prototype ----> null   //myCard没有prototype这个属性，不过可以用__proto__这个非标准用法来查看。                        
                     
```

一个常用的编程模式像这样：

```js
function Student(props) {
    this.name = props.name || '匿名'; // 默认值为'匿名'
    this.grade = props.grade || 1; // 默认值为1
}

Student.prototype = {
  numLegs: 2,
  eat: function() {
    console.log("nom nom nom");
  },
  describe: function() {
    console.log("My name is " + this.name);
  }
};
//手动给新对象重新设置原型对象，会产生一个重要的副作用：删除了constructor属性
Student.prototype.constructor = Student;
function createStudent(props) {
    return new Student(props || {})
}
```

这个`createStudent()`函数有几个巨大的优点：一是不需要`new`来调用，二是参数非常灵活，可以不传，也可以这么传：

```
var xiaoming = createStudent({
    name: '小明'
});

xiaoming.grade; // 1
```

如果创建的对象有很多属性，我们只需要传递需要的某些属性，剩下的属性可以用默认值。由于参数是一个Object，我们无需记忆参数的顺序。如果恰好从`JSON`拿到了一个对象，就可以直接创建出`xiaoming`。



**记号定义方法**

```js
    var obj = new Object();
    var obj = {};
    var friends = {
        bill: {
        },
        steve:{
        }
    }
 
    var james = {
        job: "programmer",
        married: false,
        sayJob: function() {
        // complete this method
        }
    };
 
    function Rectangle(height, width) {
        this.height = height;
        this.width = width;
        this.calcArea = function() {
            return this.height * this.width;
        };
    }
```

也可以在构造体外定义方法，然后把方法赋给对象

```js
    var calcArea = function() {
        return this.height * this.width;
    };
    rectangle.calcArea = calcArea;
    rectangle.calcArea();
```

公有变量和公有方法使用this.来声明

```javascript
    function Person(name){
        this.name = name;
        this.getBalance = function() {
        }
    }
    
    //knockout observableArray示例
    var SimpleListModel = function(items) {
    this.items = ko.observableArray(items);
    this.itemToAdd = ko.observable("");
    this.addItem = function() {
        if (this.itemToAdd() != "") {
            this.items.push(this.itemToAdd()); // Adds the item. Writing to the "items" observableArray causes any associated UI to update.
            this.itemToAdd(""); // Clears the text box, because it's bound to the "itemToAdd" observable
        }
    }.bind(this);  // Ensure that "this" is always this view model
};
 
ko.applyBindings(new SimpleListModel(["Alpha", "Beta", "Gamma"]));
```

私有变量和私有方法通过var来定义， 并且只能通过公有方法来访问

```javascript
    function Person(name){
        var name ="df";
        var getBalance = function() {
        }
    }
 
    // 公有方法访问私有变量
    function StudentReport() {
        var grade1 = 4;
        var grade2 = 2;
        var grade3 = 1;
        this.getGPA = function() {
            return (grade1 + grade2 + grade3) / 3;
        };
    }
```

### 原型

https://static.liaoxuefeng.com/files/attachments/1024700039819712/l

https://www.liaoxuefeng.com/wiki/1022910821149312/1023022043494624

https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Objects/Object_prototypes#prototype_%E5%B1%9E%E6%80%A7%EF%BC%9A%E7%BB%A7%E6%89%BF%E6%88%90%E5%91%98%E8%A2%AB%E5%AE%9A%E4%B9%89%E7%9A%84%E5%9C%B0%E6%96%B9

每个对象拥有一个**原型对象**(构造函数的prototype属性），对象以其原型为模板、从原型继承方法和属性。原型对象也可能拥有原型，并从中继承方法和属性。

原型更新后，任何由此构造器创建的对象实例都自动获得了这个方法。

```js
Person.prototype.farewell = function() {
  alert(this.name.first + ' has left the building. Bye for now!');
}
person1.farewell();
```

原型对象中也有constructor属性信息

```js
let duck = new Bird();
console.log(duck.constructor === Bird); //输出 true

var person3 = new person1.constructor('Karen', 'Stephenson', 26, 'female', ['playing drums', 'mountain climbing']);

//获得某个对象实例的构造器的名字
instanceName.constructor.name
```



### 继承

 JavaScript 中在对象实例和它的构造器之间建立一个链接（它是__proto__属性，是从构造函数的`prototype`属性派生的），之后通过上溯原型链，在构造器中找到这些属性和方法。

`Object.getPrototypeOf(new Foobar())`和`Foobar.prototype`指向着同一个对象。

js通过原型链实现继承，实际上就是让子类的prototype复制一份父类prototype中的属性.

所有的方法都定义在构造器的原型上，比如：

```js
function Teacher(first, last, age, gender, interests, subject) {
  Person.call(this, first, last, age, gender, interests);

  this.subject = subject;
}

Person.prototype.greeting = function() {
  alert('Hi! I\'m ' + this.name.first + '.');
};
//将Person.prototype的拷贝作为Teacher.prototype的属性值。这意味着Teacher.prototype现在会继承Person.prototype的所有属性和方法。
Teacher.prototype = Object.create(Person.prototype);
//现在Teacher()的prototype的constructor属性指向的是Person(),需要将其正确设置
Teacher.prototype.constructor = Teacher;

Person.prototype.isPrototypeOf(teacher);// 返回 true

//重写继承的方法
teacher.prototype.eat = function() {
   //...
};
```

疑问：继承链如何动态地更新？？

一些库可以实现继承。

方法和属性都会继承

```js
    function Emperor(name){
        this.name = name;
    }
    Emperor.prototype = new Penguin();
```

### 属性

```js
myObje.extraProperty = "value1"; myObj["extraP"] = "value1";
//使用 delete 关键字删除对象属性
delete foods.apples;
```
自身属性是直接在对象上定义的，原型属性是定义在prototype上的

```js
for (let property in duck) {
  if(duck.hasOwnProperty(property)) {
    ownProps.push(property);
  } else {
    prototypeProps.push(property);
  }
}
```

### mixin

`mixin`允许其他对象使用函数集合。

```js
let flyMixin = function(obj) {
  obj.fly = function() {
    console.log("Flying, wooosh!");
  }
};
```

`flyMixin`能接受任何对象，并为其提供`fly`方法。

### getter

闭包的方式访问私有变量

```js
function Bird() {
  let hatchedEgg = 10; // 私有属性

  this.getHatchedEggCount = function() { // bird 对象可以是使用的公有方法
    return hatchedEgg;
  };
}
let ducky = new Bird();
ducky.getHatchedEggCount(); // 返回 10
```



### typeof

`typeof myVar` 结果可以是 object number string array

##  随机数生成

Math.random() 生成[0,1)区间的随机小数

Math.floor(Math.random() * 3) + 1 生成随机整数，范围在1到3之间

## 随机颜色

<< 0是取整数（Integer 10进制）操作

```
var getRandomColor = function() {
  return '#' + (function(h) {
    return new Array(7 - h.length).join("0") + h
  })((Math.random() * 0x1000000 << 0).toString(16))
}
```

## 获取当前时间字符串

```
// 当前时间，Date类型
new Date();
// 当前毫秒
Date.now();
```

## 正则表达式

```js
// 举例
var expressionToGetSoftware = /software/gi;
var softwareCount = testString.match(expressionToGetSoftware).length;
```

# ES6

**let**

使用`var`关键字来声明一个变量的时候，这个变量会被声明成全局变量，或是函数内的局部变量。

使用关键字`let`声明变量，这个变量的作用域就被限制在当前的代码块，语句或表达式之中。

**不可变对象**

`const`和`let`区别：const声明的变量只能被赋值一次

类似java，对象（包括数组和函数）在使用`const`声明的时候依然是可变的，只是不能整体赋值。

`Object.freeze(obj)`可以防止数据改变。

**匿名函数**

```js
const myFunc = () => {
  const myVar = "value";
  return myVar;
}
const doubler = (item) => item * 2;
```

**函数默认值**

```js
function greeting(name = "Anonymous") {
  return "Hello " + name;
}
```

**可变参数**

```js
function howMany(...args) {
  return "You have passed " + args.length + " arguments.";
}
```

**展开操作符**

```js
const arr = [6, 89, 3, 45];
const maximus = Math.max(...arr); // 返回 89
```

**解构语法**

```js
const { x, y, z } = obj; // x = 3.6, y = 7.4, z = 6.54
const a = {
  start: { x: 5, y: 6},
  end: { x: 6, y: -9 }
};
const { start : { x: startX, y: startY }} = a;
console.log(startX, startY); // 5, 6
```

**模板字符串**

```js
const person = {
  name: "Zodiac Hasbro",
  age: 56
};

// string interpolation
const greeting = `Hello, my name is ${person.name}!
I am ${person.age} years old.`;
```

**定义对象的语法糖**

```js
const getMousePosition = (x, y) => ({ x, y });
```

**export导出**

```js
const capitalizeString = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
const foo = "bar";
export { capitalizeString, foo }

//在文件中只有一个值需要导出的时候
export default function add(x,y) {
  return x + y;
}
```

**import函数**

```js
import { functionA } from "file_path_goes_here"

import * as myMathModule from "math_functions";
myMathModule.add(2,3);
myMathModule.subtract(5,3);
```

**默认key**

```js
let obj = {
    type:ADD,
    message
}
```



# 闭包

闭包就是携带状态的函数，并且它的状态可以完全对外隐藏起来。并且这个状态可以在创建闭包时初始化。

在没有`class`机制，只有函数的语言里，借助闭包，同样可以封装一个私有变量。

```javascript
function create_counter(initial) {
    var x = initial || 0;
    return {
        inc: function () {
            x += 1;
            return x;
        }
    }
}

//它用起来像这样：

var c1 = create_counter();
c1.inc(); // 1
c1.inc(); // 2
c1.inc(); // 3

var c2 = create_counter(10);
c2.inc(); // 11
c2.inc(); // 12
c2.inc(); // 13

```



**闭包特性下绑定参数**

事件绑定时，回调函数并不会立即执行，等到事件发生才会执行。

问题：闭包在执行时，内部如果引用了上下文的循环变量，它的值可能会改变。

解决办法：让闭包绑定循环变量每次迭代的临时值，而不是最终值。临时值可以用函数参数传递，并立即执行绑定到闭包上下文

```javascript
for (var name in catMap) {
    var cat = catMap[name];
    // var thisTemplate = catTemplate.replace(/{{name}}/g, cat.name);

    // $catlist.append(thisTemplate);
    // 将这个cat绑定到事件上
    var catElem = document.createElement("li");
    catElem.text = cat.name;
    
    //cat的声明会被提升到函数作用域顶部
    //点击事件是for循环完毕后才开始执行的，执行完毕后闭包中内部变量cat的值已经变成catMap中最后一个cat
    catElem.addEventListener('click', function () {
        control.setCurrentCat(cat);
    });
    
	
    catElem.addEventListener('click', (function (catCopy) {
        return function () {
            control.setCurrentCat(catCopy);
        };
    })(cat));
```

闭包改为让返回函数的函数立即执行，仍然得到一个函数，只不过绑定了临时变量cat

```js
(function(catCopy) {
    return function() {
    	control.setCurrentCat(cat);
    }
})(cat);
```
进一步改写为lambda表达式

```js
(catCopy => {function() {
        control.setCurrentCat(catCopy);
    })(cat);
```



# 常见错误

https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/First_steps/What_went_wrong

# 向后兼容

## 平稳退化

如果想用js给某个网页添加一些行为，就不应该让js代码对这个网页的结构有任何依赖！

把href设为一个真实的值 比如搜索机器人不理解js代码

## 分离javascript

一个弹出窗口的例子
```
    function popUp(url) {
        window.open(url, "Hint", "width=320,height=480");
    }
 
    // add popUp event to some elements
    window.onload = prepareLinks;
    function prepareLinks() {
        if(!document.getElementsByTagName) {
            return false;
        }
        var links = document.getElementsByTagName("a");
        for (var i = 0; i < links.length; i++) {
            var alink = links[i];
            if(alink.getAttribute("class") === "popup") {
                // 键盘tab移动到某个链接然后按下回车键也能触发onclick事件
               alink.onclick = function () {
                   popUp(this.getAttribute("href"));
                   return false; //禁用链接的默认行为
               }
            }
        }
    }
```
html
```
    <a href="http://www.baidu.com/" class="popup">Example</a>
    <script type="text/javascript" src="scripts/showPic.js"></script>
```

## 渐进增强

## 对象检测

比浏览器嗅探脚本更简单、更健壮

# 性能优化

## focus

 [`focus()`](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLElement/focus) 方法让光标在页面加载完毕时自动放置于输入框内

## script放到最后加载

浏览器加载脚本期间不会下载其他资源

## 编程习惯

如果一个函数有多个出口，只要这些出口集中出现在函数的开头部分，就可以接受

## 绑定事件
```
    function addLoadEvent(func) {
        var oldonload = window.onload;
        if (typeof window.onload != 'function') {
            window.onload = func;
        } else {
            window.onload = function () {
                oldonload();
                func();
            };
        }
    }
 
    addLoadEvent(prepareLinks);
    addLoadEvent(prepareGallery);
```







# 浏览器内置语法

## window API

```js
var button = document.querySelector('button');

button.onclick = function() {
    //window.prompt() 函数 存储在一个给定的变量中
  var name = prompt('What is your name?');
    //  window.alert()  
  alert('Hello ' + name + ', nice to see you!');
}

// Number 对象将把传递给它的任何东西转换成一个数字
var myNum = Number(myString);
typeof myNum;

// 每个数字都有一个名为 toString() 的方法
var myNum = 123;
var myString = myNum.toString();
typeof myString;
```



window

```js
window.onresize = function() {
  WIDTH = window.innerWidth;
  HEIGHT = window.innerHeight;
  div.style.width = WIDTH + 'px';
  div.style.height = HEIGHT + 'px';
}
```

### 获取位置

```js
if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(function(position) {
		$("#data").html("latitude: " + position.coords.latitude + "<br>longitude: " + 			position.coords.longitude);
    });
}
```



## fetch api

```js
postData(`http://example.com/answer`, {answer: 42})
  .then(data => console.log(JSON.stringify(data))) // JSON-string from `response.json()` call
  .catch(error => console.error(error));

function postData(url = ``, data = {}) {
  // Default options are marked with *
    return fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    })
    .then(response => response.json()); // parses JSON response into native Javascript objects 
}

fetch('products.json').then(function(response) {
  if(response.ok) {
    response.json().then(function(json) {
      products = json;
      initialize();
    });
  } else {
    console.log('Network request for products.json failed with response ' + response.status + ': ' + response.statusText);
  }
});

fetch(url).then(function(response) {
  if(response.ok) {
    response.blob().then(function(blob) {
      objectURL = URL.createObjectURL(blob);
      showProduct(objectURL, product);
    });
  } else {
    console.log('Network request for "' + product.name + '" image failed with response ' + response.status + ': ' + response.statusText);
  }
});
```

## Promises

https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Client-side_web_APIs/Fetching_data

大多数现代的JavaScript api都是基于promises的

```js
fetch(url).then(function(response) {
  response.text().then(function(text) {
    poemDisplay.textContent = text;
  });
});


```

可以直接将promise块 (`.then()`块, 但也有其他类型) 链接到另一个的尾部, 顺着链条将每个块的结果传到下一个块

```js
fetch(url).then(function(response) {
  return response.text()
}).then(function(text) {
  poemDisplay.textContent = text;
});
```

## Storage

浏览器客户端的localStorage、 sessionStorage都是window对象提供的,用法：

```
window.localStorage.xxx = JSON.stringify( array or object);
localStorage.xxx = JSON.stringify( array or object);
localStorage.setItem("xxx", JSON.stringify( array or object));
```


sessionStorage是人如其名,只针对当前session(会话)有效,关闭标签页即失效;

localStorage则不然,即使关闭了标签页甚至浏览器,依然存在,下次打开页面时,依然可以直接使用,  但是要注意,清除浏览器缓存时,localStorage的内容也会清理掉;

# Bootstrap

## cdn使用

响应式导航栏可能需要以下几个链接：

``` html
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
    crossorigin="anonymous"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js"  integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh"
    crossorigin="anonymous"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js"  integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ"
    crossorigin="anonymous"></script>
```

# font-awesome

字体图标的cdn

``` html
  <script src="https://use.fontawesome.com/be5163cdaa.js"></script>
```



# Knockout

## 绑定上下文

一个绑定上下文就是`ko.applyBindings`加入的viewMode对象。

with、foreach等控制流都会在当前绑定上下文中新建孩子上下文。

具有多个层次，对应viewModel的层次结构。

declarative bindings

UI refresh

dependency tracking



var fnum = ko.observable(value) 生成一个函数（对象）
双向绑定：

fnum(newValue)会更新model，并通知并更新view

view上用户改变输入数据，也会通知并更新model, model再去更新其他view



## 数组

```javascript
var` `myObservableArray = ko.observableArray();    ``// Initially an empty array
myObservableArray.push(``'Some value'``); 

// This observable array initially contains three objects
var anotherObservableArray = ko.observableArray([
    { name: "Bungle", type: "Bear" },
    { name: "George", type: "Hippo" },
    { name: "Zippy", type: "Unknown" }
]);

alert('The length of the array is ' + myObservableArray().length);
alert('The first element is ' + myObservableArray()[0]);

myObservableArray.indexOf('Blah')
myObservableArray.slice(...) 
```

- **Observable Array不监控元素本身的变化：**Observable Array只处理元素个数的变化，比如数组元素删除和添加。元素自身的变化是否能自动监控，取决于**元素本身是普通对象还是Observable对象。**
- **如何既监控数组元素个数，又监控元素内容变化：**往数组中push元素的时候，使用observable元素即可，则该元素可以自动监控自身的变化。

## Foreach

$index 引用当前元素索引

$data 引用当前元素数据（内容）

$parent用于列表项引用foreach之外的viewModel中的属性

```html
// Source code: View
<h4>People</h4>
<ul data-bind="foreach: people">
    <li>
        Name at position <span data-bind="text: $index"> </span>:
        <span data-bind="text: name"> </span>
        <a href="#" data-bind="click: $parent.removePerson">Remove</a>
    </li>
</ul>
<button data-bind="click: addPerson">Add</button>

// Source code: View model
<script>
function AppViewModel() {
    var self = this;

    self.people = ko.observableArray([
        { name: 'Bert' },
        { name: 'Charles' },
        { name: 'Denise' }
    ]);
     
    self.addPerson = function() {
        self.people.push({ name: "New at " + new Date() });
    };
     
    self.removePerson = function() {
        self.people.remove(this);
    }
}

ko.applyBindings(new AppViewModel());
</script>
```

嵌套列表中，给每个元素一个别名（相当于$data)：

```html
<ul data-bind="foreach: { data: categories, as: 'category' }">
    <li>
        <ul data-bind="foreach: { data: items, as: 'item' }">
            <li>
                <span data-bind="text: category.name"></span>:
                <span data-bind="text: item"></span>
            </li>
        </ul>
    </li>
</ul>

<script>
    var viewModel = {
        categories: ko.observableArray([
            { name: 'Fruit', items: [ 'Apple', 'Orange', 'Banana' ] },
            { name: 'Vegetables', items: [ 'Celery', 'Corn', 'Spinach' ] }
        ])
    };
    ko.applyBindings(viewModel);
</script>
```



## Computed

## 判断是否被ko管理

- `ko.isObservable` - returns true for observables, observable arrays, and all computed observables.
- `ko.isWritableObservable` - returns true for observables, observable arrays, and writable computed observables (also aliased as `ko.isWriteableObservable`).

`ko.isComputed`

```javascript
for` `(``var` `prop ``in` `myObject) {
    ``if` `(myObject.hasOwnProperty(prop) && !ko.isComputed(myObject[prop])) {
        ``result[prop] = myObject[prop];
    ``}
}
```

## 扩展

```javascript
myViewModel.fullName = ko.pureComputed(``function``() {
    ``return` `myViewModel.firstName() + ``" "` `+ myViewModel.lastName();
}).extend({ notify: ``'always'` `});

// Ensure updates no more than once per 50-millisecond period
myViewModel.fullName.extend({ rateLimit: 50 });
```

## Example

```javascript
<!DOCTYPE html>
<html>
<head>
	<script type='text/javascript' src='knockout-3.4.2.js'></script>
	<title>Cat Clicker</title>
</head>
<body>
	<div id="cat" data-bind="with: currentCat">
		<h2 id="cat-name" data-bind="text: name"></h2>
		<h3 id="cat-title" data-bind="text: title"></h2>
		<div id="cat-count" data-bind="text: count"></div>
		<img id="cat-img" src="" alt="cute cat" data-bind="click: addCount, attr: {'src':imgSrc}">
		<ul data-bind="foreach: nicknames">
			<li data-bind="text: $data"></li>
		</ul>
	</div>
	<div>
		<h2>Cat List</h2>
		<ul data-bind="foreach: catlist">
			<li data-bind="text: $data.name, click:$parent.setCurrentCat"></li>
		</ul>
	</div>

<script type="text/javascript">
var catlistdata = [
	{
		count:0,
		imgSrc:"https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=3943164443,2487657283&fm=58&bpow=725&bpoh=713",
		name:"Lisa",
		nicknames:["fasfasf", "dog", "baby"]
	},
	{
		count:0,
		imgSrc:"https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=2247692397,1189743173&fm=5",
		name:"Novy",
		nicknames:["Lucy"]
	},
	{
		count:0,
		imgSrc:"https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1667994205,255365672&fm=5",
		name:"Bosi",
		nicknames:["Bear"]
	}
];
function Cat(data) {
	var self = this;
	this.count = ko.observable(data.count);
	this.imgSrc = ko.observable(data.imgSrc);
	this.name = data.name;

	this.nicknames = ko.observableArray(data.nicknames);
	this.title = ko.computed(function(){
		if(self.count() > 10){
			return "Vip";
		} else {
			return "Originary";
		}
	});
	this.addCount = function(){
		self.count(self.count() + 1);
	}

}
function CatViewModel() {
	var self = this;
	self.catlist = ko.observableArray([]);
	catlistdata.forEach(function(cat){
		self.catlist.push(new Cat(cat));
	});
	self.currentCat = ko.observable(self.catlist()[0]);
	self.setCurrentCat = function(){
		self.currentCat(this);
	}

}

ko.applyBindings(new CatViewModel());
</script>

</html>
```



# Vue.js

Vue实例初始化的代码应该放在html加载之后。

创建vue实例，相当于创建一个viewModel。创建时数据的所有属性都会加入vue响应式系统中，当这些属性的值发生改变时，视图将会产生“响应”，即匹配更新为新的值。

采用简洁的模板语法，声明式地将数据渲染进 DOM

`v-bind`绑定数据到元素属性上。缩写：

```html
<a :href="url">...</a>
<a @click="doSomething">...</a>
```

绑定方法和入参

```html
<div class="goods">
    <div class="goods-name">{{item.name}}</div>
    <div class="goods-price">{{item.price}}</div>
    <div class="sub" @click="sub(item.price)">减法操作</div>
    <div class="add" @click="add(item.price)">加法操作</div>
</div>
```

v-if控制dom结构

`v-on` 指令添加一个事件监听器。监听器中通过更新vue的数据来间接更新dom。

`v-for` 指令可以绑定数组的数据来渲染一个item列表

[`created`](https://cn.vuejs.org/v2/api/#created) 钩子可以在一个实例被创建之后执行代码。此外还有 [`mounted`](https://cn.vuejs.org/v2/api/#mounted)、[`updated`](https://cn.vuejs.org/v2/api/#updated) 和 [`destroyed`](https://cn.vuejs.org/v2/api/#destroyed)。生命周期钩子的 `this` 上下文指向调用它的 Vue 实例。

```js
<div id="app-5">
  <p>{{ message }}</p>
  <img src="http://sucimg.itc.cn/avatarimg/43ac66f0463f477a9477fe9a58b8100c_1496397655984_hahahha" v-bind:alt='alt'>
  <p v-if="seen">现在你看到我了</p>
<a v-bind:href="url">...</a>
  <button v-on:click="reverseMessage">反转消息</button>

</div>

<div id="app-4">
  <ol>
    <li v-for="todo in todos">
      {{ todo.text }}
    </li>
  </ol>
</div>

var app5 = new Vue({
  el: '#app-5',
  data: {
    message: 'Hello Vue.js!',
    alt:"Panda",
    seen: true
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')
    }
  },
  //hook
  created: function () {
    // `this` 指向 vm 实例
    console.log('a is: ' + this.a)
  }
})
```

## 生命周期

https://cn.vuejs.org/images/lifecycle.png

# AngularJS

```
//module声明本模块名称为invoice2,依赖于模块finance2。
//controller方法：1. 定义controller名称 2.数组前面部分顺序定义依赖。 3. 这个controller的构造函数，参数是依赖注入的对象。
angular.module('invoice2', ['finance2'])
  .controller('InvoiceController', ['currencyConverter', function(currencyConverter) {
}]);

//factory方法，定义服务
      someModule.factory('greeter', ['$window', function(renamed$window) {
        ...
      }]);
```

## 内置语法

```js
return $http.jsonp(url).success(function(data) {});
```

## 自启动

```html
<html ng-app>
<script src="angular.js">
<!-- 加载 ng-app 指令所指定的 模块 -->
<html ng-app="optionalModuleName">
```

## 编译

Angular编译器直接使用DOM作为模板而不是用字符串模板，生成的是稳定的DOM模板（也就是动态视图）。DOM元素实例和数据模型实例的绑定在绑定期间是不会发生变化的（也就是说不是每次数据改变，最后产生的模板都要变化一次）

## 双向绑定

https://www.angularjs.net.cn/Upload/img/Two_Way_Data_Binding.png

https://www.angularjs.net.cn/tutorial/10.html

ng-model实现双向绑定

input框输入字符后，会自动更新模型

```html
<div ng-app="myApp" ng-controller="myCtrl">
名字: <input ng-model="name">
<h1>你输入了: {{name}}</h1>
</div>

<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.name = "John Doe";
});
</script>
```



## 控制器

作用：控制器只需要负责一个单一视图所需的业务逻辑。

编程规范：

- 将那些不属于控制器的逻辑(有状态或无状态的代码)都封装到服务（services）中，然后在控制器中通过依赖注入调用相关服务。

- 下面的场合**千万不要用控制器**：

  - 控制器只应该包含业务逻辑。ng 提供数据绑定 （[数据绑定](https://www.angularjs.net.cn/tutorial/guide/databinding)） 来实现自动化的DOM操作。如果需要手动进行DOM操作，那么最好将表现层的逻辑封装在 [指令](https://www.angularjs.net.cn/tutorial/5.html) 中

  - 格式化输入：使用 [angular表单控件](https://www.angularjs.net.cn/tutorial/4.html) 代替
  - 过滤输出：使用 [angular过滤器](https://www.angularjs.net.cn/tutorial/8.html) 代替
  - 管理其它部件的生命周期（如手动创建 service 实例）



## 作用域

当一个控制器通过 [`ng-controller`](https://www.angularjs.net.cn/tutorial/2.html) 指令被添加到DOM中时，ng 会调用该控制器的**构造函数**来生成一个控制器对象，这样，就创建了一个新的**子级 作用域(scope)**

controller的$scope相当于它的上下文。



控制器和scope使用：

- `ng-controller` 指令controller和它管理的scope
- 不同层级的DOM结构中添加控制器，就会创建基于继承关系的 scope 层级结构（和DOM层级结构相对应）。



**$rootScope** 可作用于**ng-app** 指令包含的所有 HTML 元素中(整个应用中），相当于全局上下文。

ng-repeat会生成多个子级作用域

Angular会自动为每个拥有作用域的DOM节点加上 `ng-scope` 类

```html
<div ng-app="myApp" ng-controller="myCtrl">
<h1>{{lastname}} 家族成员:</h1>
<ul>
    <li ng-repeat="x in names">{{x}} {{lastname}}</li>
</ul>
</div>
<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $rootScope) {
    $scope.names = ["Emil", "Tobias", "Linus"];
    $rootScope.lastname = "Refsnes";
});
</script>
```



## 依赖注入

优先考虑用**数组标注**定义依赖

```
someModule.controller('MyController', ['$scope', 'greeter', function($scope, greeter) {  
  // ...  
}]);
```

## 服务

https://www.runoob.com/angularjs/angularjs-services.html

内置服务

**$location** 服务，它可以返回当前页面的 URL 地址

**$http** 服务向服务器发送请求

**$timeout** 服务对应了  window.setTimeout 函数, 一定时间后执行

```js
$http.get("welcome.htm").then(function (response) {
    $scope.myWelcome = response.data;
});
$timeout(function () {
    $scope.myHeader = "How are you today?";
}, 2000);

$interval(function () {
    $scope.theTime = new Date().toLocaleTimeString();
}, 1000);
```

自定义服务

```js
app.service('hexafy', function() {
    this.myFunc = function (x) {
        return x.toString(16);
    }
});

```

使用自定义服务

```js
app.controller('myCtrl', function($scope, hexafy) {
    $scope.hex = hexafy.myFunc(255);
});
//自定义filter也可以使用service
```

## 过滤器



过滤器可以应用在视图模板中的表达式中，按如下的格式：

```js
{{ 表达式 | 过滤器名 }}
{{ 表达式 | 过滤器1 | 过滤器2 |...}} 
 {{ 表达式 | 过滤器:参数1:参数2:...}}
  
  {{ctrl.array | filter:'a'}}//会以'a'作为查询字符串来进行过滤数组
```

自定义过滤器

```js
app.filter('myFormat',['hexafy', function(hexafy) {
    return function(x) {
        return hexafy.myFunc(x);
    };
}]);
```

在视图模板中使用过滤器会在每次的更新中重新调用过滤器，当数组很大的时候，开销会很大。

在控制器中直接调用过滤器

```js
angular.module('FilterInControllerModule', []).
controller('FilterController', ['filterFilter', function(filterFilter) {
    this.array = [
        {name: 'asnowwolf'},
        {name: 'why520crazy'},
        {name: 'joe'},
        {name: 'ckken'},
        {name: 'lightma'},
        {name: 'FrankyYang'}
    ];
    this.filteredArray = filterFilter(this.array, 'a');
}]);
```



## Angular提供CSS类

Angular提供了这些CSS类，它们为你的应用提供便于使用的风格。

------

## Angular 使用的CSS类

提供了这些CSS类，它们为你的应用提供便于使用的风格。

- `ng-scope`
- - **用法:** angular把这个类附加到所有创建了新[`作用域(Scope)`](https://www.angularjs.net.cn/tutorial/api/ng.$rootScope.Scope)的HTML元素上。(参见 [作用域](https://www.angularjs.net.cn/tutorial/12.html))
- `ng-binding`
  - **用法:** angular把这个类附加到所有通过 `ng-bind` 或 				 绑定了任何数据的元素上。(参见 [数据绑定](https://www.angularjs.net.cn/tutorial/10.html))
- `ng-invalid`, `ng-valid`
  - **用法:** angular把这个类附加到进行了验证操作的所有input组件元素上。 (参见 [`input`](https://www.angularjs.net.cn/tutorial/13.html) 指令)
- `ng-pristine`, `ng-dirty`
  - **用法:** angular的[`input`](https://www.angularjs.net.cn/tutorial/api/ng.directive:input)指令给所有新的、还没有与用户交互的input元素附加上`ng-pristine`类，当用户有任何输入时，则附加上 `ng-dirty`

# Google Map

API_Key

AIzaSyCVckv70_zczcxqMyM5cogHRhYc1zn-B7Y


# eslint

安装配置

1. 全局安装eslint。`npm install -g eslint`

2. 工程目录下初始化eslint配置文件。`eslint --init`

3. 打开vscode，如果提示缺少此依赖包,在工程目录下 `npm install eslint-plugin-promise --save-dev`

 


# Nytimes
API key: 1195032cef68462fb19edb97a4011070
```

var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json";

url += '?' + $.param({

    'api-key': "1195032cef68462fb19edb97a4011070"

});

$.ajax({

    url: url,
     
    method: 'GET',

}).done(function(result) {

    console.log(result);

}).fail(function(err) {

    throw err;

});

```

# 百度地图

搜索关键字
地址转坐标
http://api.map.baidu.com/geocoder/v2/?address=西安市&output=json&ak=ueFBDG6HBGhWitNPFZhNYBwX3QtG4uzE


1.html部分
```
<!DOCTYPE html >
< html lang="en">
<head>
    <meta charset="UTF-8">
    <title>搜索定位</title>
    <link rel="stylesheet" type="text/ css " href="style. css ">
    <style type="text/ css ">

        #map {
            width: 800px;
            height: 800px;
         }
    </style>
    <script src="jquery.js"></script>
    <script type="text/javascript" src="//api.map.baidu.com/api?v=2.0&ak=你申请的ak码"></script>
</head>
<body>
​    <div id="map">

    </div>
    <input type="text" id="address">
    <button id="btn">搜索</button>
</body>
</ html >
```
2.js部分
```
// 百度地图API功能
var map = new BMap.Map("map");
map.centerAndZoom("杭州", 11);
var top_left_control = new BMap.ScaleControl({anchor: BMAP_ANCHOR_TOP_LEFT});// 左上角，添加比例尺
var top_left_navigation = new BMap.NavigationControl();  //左上角，添加默认缩放平移控件

// 标尺控件
map.addControl(top_left_control);
map.addControl(top_left_navigation);

//定位
function setPlace(value) {
​    var local, point, marker = null;
​    local = new BMap.LocalSearch(map, { //智能搜索
​        onSearchComplete: fn
​    });

    local.search(value);
     
    function fn() {
        //如果搜索的有结果
        if(local.getResults() != undefined) {
            map.clearOverlays(); //清除地图上所有覆盖物
            if(local.getResults().getPoi(0)) {
                point = local.getResults().getPoi(0).point; //获取第一个智能搜索的结果
                map.centerAndZoom(point, 18);
                marker = new BMap.Marker(point); // 创建标注
                map.addOverlay(marker); // 将标注添加到地图中
                marker.enableDragging(); // 可拖拽
                alert("当前定位经度:"+point.lng+"纬度:"+point.lat);
            } else {
                alert("未匹配到地点!可拖动地图上的红色图标到精确位置");
            }
        } else {
            alert("未找到搜索结果")
        }
    }
}
// 按钮事件
$("#btn").click(function(){
​    setPlace($("#address").val());
});
```

# 浏览器相关

## firefox控制台： 指向 xxxurl 的脚本加载失败


## 加载html和渲染的顺序
1. 请求通用的html
2. 请求单独的html
3. 渲染通用
4. 渲染单独



## 获取ip

```js
<script src="http://pv.sohu.com/cityjson?ie=utf-8"></script>
<script type="text/javascript">
    //可以直接使用数据
document.write(returnCitySN["cip"]+','+returnCitySN["cname"])
</script>
```

# Typescript

安装nodejs和typescript

```shell
npm install -g typescript
```

编写.ts文件后，编译成.js文件

```shell
tsc greeter.ts
```

不需要显式实现接口。对象与定义的接口内部结构一致，则实现了接口。

构造器参数上的public自动创建了属性。

```ts
class Student {
    fullName: string;
    constructor(public firstName: string, public middleInitial: string, public lastName: string) {
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
}

interface Person {
    firstName: string;
    lastName: string;
}

function greeter(person: Person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}

let user = new Student("Jane", "M.", "User");

document.body.textContent = greeter(user);
```

ts的接口(interface)是可以多继承的，但类(class)和其他语言一样只能单继承。

ts的属性修饰符除了基础的public,private,protected,static,还有一个readonly。 当你在程序中没有指明修饰符时，默认为public

存取器类似于拦截器，通过getters/setters来截取对对象成员的访问。只带有 get不带有 set的存取器自动被推断为 readonly。

 抽象类主要作为子类的基类使用，很少用于实例化对象。不同于接口，抽象类可以包含成员的实现细节。 

# Angular

## 模板语法

```
*ngFor
*ngIf
插值表达式 {{}}
属性绑定 []
事件绑定 ()
```

## 组件

组件的html可以在指令中使用ts定义的数据和方法。

## 路由

配置url跳转到其他组件。

app.moudule.ts中添加路由，关联URL路径与组件

```ts
@NgModule({
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      { path: '', component: ProductListComponent },
      {path:'products/:productId', component: ProductDetailsComponent},
      {path:'cart', component:CartComponent}
    ])
  ],
  declarations: [
    AppComponent,
    TopBarComponent,
    ProductListComponent,
    ProductAlertsComponent,
    ProductDetailsComponent,
    CartComponent
  ],
  bootstrap: [ AppComponent ],
  providers: [CartService]
})
export class AppModule { }
```

商品列表组件跳转到商品详情URL

```html
<div *ngFor="let product of products; index as productId">

  <h3>
    <a [title]="product.name + ' details'" [routerLink]="['/products', productId]">
      {{ product.name }}
    </a>
  </h3>
<!-- . . . -->
</div>
```

商品详情URLurl中的参数可以用来获取数据，初始化组件( 订阅路由参数并根据其 `productId` 获取商品信息 )

```ts
export class ProductDetailsComponent implements OnInit {

  constructor(private route: ActivatedRoute,) { }

  ngOnInit() {
  this.route.paramMap.subscribe(params => {
    this.product = products[+params.get('productId')];
  });
}

}
```

## 服务

公共的ts服务，不包括html和css。

## HTTP

  `app.module.ts` 中，从 `@angular/common/http` 包中导入 `HttpClientModule`。 

```js
import { HttpClientModule } from '@angular/common/http';
@NgModule({
  imports: [
    BrowserModule,
    HttpClientModule,
```

为购物车服务启用 HttpClient。也可以用来访问本站的json文件

```js
import { HttpClient } from '@angular/common/http';
export class CartService {
  items = [];

  constructor(
    private http: HttpClient
  ) {}
  
	getShippingPrices() {
    return this.http.get('/assets/shipping.json');
  }
}
```

## 表单

给购物者组件导入FormBuilder， 方便关联表单模板和数据

```js
import { FormBuilder } from '@angular/forms';

export class CartComponent {
  items;
  checkoutForm;

  constructor(
    private cartService: CartService,
    private formBuilder: FormBuilder,
  ) {
    this.items = this.cartService.getItems();

    this.checkoutForm = this.formBuilder.group({
      name: '',
      address: ''
    });
  }
    
    onSubmit(customerData) {
    // Process checkout data here
    console.warn('Your order has been submitted', customerData);
 
    this.items = this.cartService.clearCart();
    this.checkoutForm.reset();
  }
}
```

表单模板：

```html
<form [formGroup]="checkoutForm" (ngSubmit)="onSubmit(checkoutForm.value)">
 
  <div>
    <label>Name</label>
    <input type="text" formControlName="name">
  </div>
 
  <div>
    <label>Address</label>
    <input type="text" formControlName="address">
  </div>
 
  <button class="button" type="submit">Purchase</button>
  
</form>
```

# React

React只关注纯粹的view层，也就是用数据渲染UI。而不关注UI输入的数据（view更新model），因此没有双向绑定或者v-model这种语法糖（value 的单向绑定 + onChange 事件侦听）。

## 渲染组件

渲染组件或元素为targetNode的子元素

```js
ReactDOM.render(<TypesOfFood/>,document.getElementById("challenge-node"))
```



服务器上渲染

```react
ReactDOMServer.renderToString(<App/>)
```

可以创造更快的页面加载体验，因为渲染的 HTML 代码量要比整个应用程序的 JavaScript 代码小



## 定义组件

组件可以包含子组件，支持嵌套

render返回的JSX元素中，也可以使用js变量、jsx元素、状态、属性，也可以调用方法如`this.renderButton(1)`

**属性可以传递给子组件**

```react
const CurrentDate = (props) => {
  return (
    <div>
      <p>The current date is: {props.date}</p>
    </div>
  );
};
const List= (props) => {
  return <p>{props.tasks.join(', ')}</p>
};
class Calendar extends React.Component {
  constructor(props) {
    super(props);
      this.state = {
        input: ''
		userAge: 0
      }
  }
  handleChange(event) {
    this.setState({ input: event.target.value })
  }
  submit(event) {
    this.setState({ userAge: event.target.value })
  }
  render() {
    //也可以添加js代码，定义js变量，定义JSX元素。下面JSX元素中可以使用js临时变量{{xxx}}
    const buttonOne = <button onClick={this.submit}>Submit</button>;
    const buttonTwo = <button>You May Enter</button>;
    const buttonThree = <button>You Shall Not Pass</button>;

    const answer = possibleAnswers[this.state.randomIndex];
    
    return (
      <div>
        <h3>What date is it?</h3>
        <CurrentDate date={Date()}/>
        <h2>Today</h2>
        <List tasks={["walk dog", "workout"]}/>
        <p>{answer}</p>
            
        
        <input type="text" style={inputStyle} value={this.state.input} onChange={this.handleChange} />  
        {buttonOne}
        {/*三元操作符 */}            
        { this.state.userAge < 18 ? buttonThree : buttonTwo}
      </div>
    );
  }

};

```

ES6 类组件有一个名为`tempPassword`的 prop，你可以在 JSX 中这样写：`<p>Your temporary password is: <strong>{this.props.tempPassword}</strong></p>`

**校验组件接收的props**

```react
//校验Items组件是否接收了正确类型的 props
Items.propTypes = {quantity:PropTypes.number.isRequired};
```

**组件设置默认属性**

```react
ShoppingCart.defaultProps = {items:0}
```

**回调函数传递给子组件**

```react
//父组件
<GetInput handleChange={this.handleChange} input={this.state.inputValue}/>

//子组件里的input控件输入数据，使用父组件的事件监听函数改变了父组件的state
<input value={this.props.input} onChange={this.props.handleChange}/>
```



## 单向数据流

父组件state中的部分数据可以传递给子组件的props

state 沿着应用程序组件树的一个方向流动，从有状态父组件到子组件，子组件只接收它们需要的 state 数据

state 管理的逻辑与 UI 逻辑分离。复杂的有状态应用程序可以分解成几个，或者可能是一个单一的有状态组件。其余组件只是从父组件简单的接收 state 作为 props，并从该 state 渲染 UI

```react
<Navbar name={this.state.name} />
```

## 监听事件

- JSX元素中使用属性onClick onSubmit等，这些事合成事件
- 将事件处理附加到dom元素上

React提供了**this.setState**方法更新组件状态，一般在回调函数中使用.

示例监听了表单输入框的改变，点击提交按钮后把输入框的数据提交到submit字符串

```react
class ControlledInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      input: '',
      submit:''
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event){
    this.setState({
      input: event.target.value
    });
  }
  handleSubmit(event) {
    event.preventDefault();
    this.setState({
      submit: this.state.input
    })
  }
    //此时this指向是当前实例对象
    handleAdd = ()=> {
        console.log(this)
        this.setState({
            count:5
        })
    }
  render() {
    return (
        <form onSubmit={this.handleSubmit}>
          <h1>{this.state.submit}</h1>
          <input type="text" onChange={this.handleChange} value={this.state.input}/>
          <button type='submit' onSubmit={this.handleSubmit}>Submit!</button>
        </form>
    );
  }
}; 


```



注意可能会用中间变量调用回调函数。为了避免this指向丢失，使得无论事件处理函数如何传递，this指向都是当前实例化对象：

- bind(this)
- 箭头函数绑定this

用UI输入的值更新state

## 重新渲染

父组件调用this.setState后，子组件如果依赖它就会产生新的props（即使`props`没有改变），默认一定会重新渲染。执行顺序如下

```react
componentWillReceiveProps(nextProps) {
    console.log(this.props);
    console.log(nextProps); 
}  
componentWillUpdate() {
    console.log('Component is about to update...');
}
componentDidUpdate() {
    console.log("componentDidUpdate " + this.props.message);
}
render(){
    //...
}
```

使用 shouldComponentUpdate 来优化渲染，比较新旧`props`

## 调用API

React 在生命周期方法`componentDidMount()`中对服务器进行 API 调用，用返回的数据设置 state 时。一旦收到数据，它将自动触发更新。

```react
componentDidMount() {
    setTimeout( () => {
        this.setState({
            activeUsers: 1273
        });
    }, 2500);
}
```

## 样式

样式也可以定义在render函数内，根据条件动态改变样式。state改变后默认会重新调用render

```react

const styles = {color: "purple", fontSize:40, border: "2px solid purple"}
// change code above this line
class Colorful extends React.Component {
  render() {
    // change code below this line
    return (
      <div style={styles}>Style Me!</div>
    );
    // change code above this line
  }
};
```

## Array

map方法动态创建数组时，每个元素都需要一个设置同级别元素唯一的`key`属性。 有助于React提高重新渲染的效率。

```react
render() {
    const items = this.state.toDoList.map(item => <li key={item}>{item}</li>);
    return ...}
```

filter

```react
render() {
	const usersOnline = this.state.users.filter(user => user.online);
    return ...}
```

## Redux

react hook最大的意义是，它允许一个hook函数替调用者（一个函数组件）声明状态、管理状态，然后以**函数返回值**的形式与宿主组件通讯。hooks解决的问题是**如何抽离、复用与状态相关的逻辑**

Redux 是一个状态管理框架，可以与包括 React 在内的许多不同的 Web 技术一起使用。类似框架有Mobx

Redux store 是应用程序状态的唯一真实来源。

**将“发生变化”和“变化引起的效应”从状态组件中解耦**

Redux管理的是变化引起的效应

- action 封装变化的数据
- action creator 构造action的函数
- reducer 接收action返回新的state
- store 使用reducer创建store

Redux的初始状态可以是Object或基本类型

```react
const defaultState = {
  authenticated: false,
};
const authReducer = (state = defaultState, action) => {
  switch(action.type){
    case 'LOGIN':
      return {authenticated:true};
    case 'LOGOUT':
      return {authenticated:false}
    default:
      //无操作，返回当前状态
      return defaultState;

  }

// 修改此行上方的代码
};
let store = Redux.createStore(authReducer);
let currentState = store.getState();
```

组合多个reducer

```react
const rootReducer = Redux.combineReducers({auth: authReducer, count:counterReducer})
```

创建异步action creator来dispatch多个action

```react
const requestingData = () => { return {type: REQUESTING_DATA} }
const receivedData = (data) => { return {type: RECEIVED_DATA, users: data.users} }

const handleAsync = () => {
  return function(dispatch) {
    // 在这里 dispatch 请求的 action
    dispatch(requestingData());

    setTimeout(function() {
      let data = {
        users: ['Jeff', 'William', 'Alice']
      }
      // 在这里 dispatch 接收到的数据 action
      dispatch(receivedData(data));
    }, 2500);
  }
};
```

reducer方法中返回的新state，必须复制原有state再修改，保证不可变

```react
let messageReducer = (state=[], action) => {
  switch(action.type){
    case ADD:
      return [...state, action.message];
    default:
      return state;
  }
}
```

