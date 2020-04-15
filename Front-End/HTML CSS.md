[TOC]




# 外部资源

[MDN HTML 元素参考]( https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element#Content_sectioning)
[CSS Almanac](https://css-tricks.com/almanac/)
[MDN CSS 参考](https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference)


# HTML


## head

文档的标题（浏览器标签中显示的文本）： 

` <title>About Me</title>` 。

相关的 CSS 文件（针对样式）：

` <link rel="stylesheet" type="text/css" href="style.css">` 。或者`<style>p{}</style>`（也可以放在body里）

相关的 JavaScript 文件（更改渲染和行为的多用途脚本）：

` <script src="animations.js"></script>` 。

网页使用的字符集（文本的 编码 ）：

` <meta charset="utf-8">` 。

关键字、作者和描述（通常对 搜索引擎优化（SEO） 起作用）： 

` <meta name="description" content="This is what my website is all about!">` 。



html5响应式

```html
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
```

# 设计方法

原型图

多画几种宽度的设计稿.从最小尺寸的屏幕开始，完成后再设计下一种。



分析总体布局：
1. 理顺页面结构  
2. 从设计稿入手，将页面上的内容划分为多个方框
3. 添加html标签
4. 确定这些box的大小
5. 定位这些box在屏幕中的位置

 

编码测试优化：
1. 寻找重复出现的样式和语义元素
2. 将这些元素和html标签关联
3. 写html
4. 应用样式（从最大到最小）
5. 修改
6. 重复步骤4和5

一般把页面大致划分为几个区域（section）后，每个区域高度需要设定。

区域可以用flex布局，调整元素间距的方式有：

- 设置元素宽度
- 设置对齐方式
- 设置margin

# 盒模型

content-box指width、height都是按content内容计算，不包括margin、padding。



每个小部件都有自己的边框，填充和边距的规则。必须使用[`box-sizing`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/box-sizing) 属性。

border, padding，content都是盒子的内部空间 
```
// 默认计算尺寸的方式. width是content的宽度，并没有包含padding和border
box-sizing:content-box;
//width包括border，将其视为元素内。一般使用这种方式计算尺寸
  -webkit-box-sizing: border-box; /* For legacy WebKit based browsers */
     -moz-box-sizing: border-box; /* For legacy (Firefox <29) Gecko based browsers */
          box-sizing: border-box;

```

父元素一定，子元素增大margin、padding、border：

- 横向首先会挤压content，从content获取空间。而不是外边距和内边距获得空间的。
- ccontent宽度为0后，横向继续增大margin、border、padding，都会伸出父元素外。从窗口溢出，此时会出现滚动条。

- 纵向扩大会把它下面的元素向下推。

height和border都忽略百分比宽度设置。

## width

[`width`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/width) 被设置为可用空间的100%。更改了浏览器窗口的宽度，那么框将会变大或变小，以保持包含在输出窗口中。

## height

高度忽略百分比宽度设置. max-height:100%不会生效

## padding

对于尺寸确定的块级元素，padding填充后没有超出元素边界，border尺寸不变。如果超出border，则原尺寸无效。

块元素未限制尺寸，则padding会撑大border

inline元素无法设置padding来撑大，需要改为inline-block

>padding-left;padding-right同样有效果,与块元素效果相同。
>
>padding-top和padding-bottom不会影响它的高度，但是会影响他的背景高度。

## margin

边距如果不重叠，会把相邻元素推开

- 水平方向，不同元素的margin不会重叠
- 块级元素间竖直方向的外边距会重叠，取最大值，并且垂直方向的margin可能会超出父元素边框之外。
- 设置了display:inline-block的元素，垂直margin不会重叠，甚至和他们的子元素之间也是一样。
- 子元素的margin-left，其值实际上是子元素的左边框距离父元素左padding内侧的距离。
- 外边距可以接受负数，这可以用来引起元素框的重叠
- 可以对元素的*margin*设置*百分数*,*百分数*是相对于父元素的width计算

块元素竖直方向边距重叠的几种情况：

- 父元素和第一个子元素上边距重叠
- 同级元素上边距和下边距重叠

实例

- body默认四周都有margin （8 8 8 8）
- div的margin border padding默认都为0
- 标题都是上下margin

## Overflow

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Introduction_to_CSS/Box_model#Overflow

- `auto`: 当内容过多，溢流的内容被隐藏，然后出现滚动条来让我们滚动查看所有的内容。
- `hidden`: 当内容过多，溢流的内容被隐藏。
- `visible`: 当内容过多，溢流的内容被显示在盒子的外边（这个是默认的行为）

## Outline

Outline被勾画于在border之外，外边距区域之内，并不改变框的尺寸。

## 约束宽和高

灵活布局，又不想让太宽或太窄

```css
width: 70%;
max-width: 1280px;
min-width: 480px;
```

在它的父容器内居中

```css
margin: 0 auto;
```

将媒体（例如图像和视频）限制在容器内部

```css
display: block;
margin: 0 auto;
max-width: 100%;
```

## 背景

元素的背景是指，在元素内容、内边距和边界下层的区域。



```css
aside li {
    list-style-type: none;
    padding-left: 2rem;
    background-image: url(icon-destination.svg);
    /*background-image也可以定义线性渐变*/
    background-image: linear-gradient(to bottom, yellow, #dddd00 50%, orange);
    background-position: 0 0;
    background-size: 1.6rem 1.6rem;
    background-repeat: no-repeat;
    /*简写*/
    background: #00FF00 url(bgimage.gif) no-repeat fixed top;
    background: yellow linear-gradient(to bottom, yellow, #dddd00 50%, orange) no-repeat 99% center;
}
```

```<body>```标签的背景图起始位置永远在浏览器窗口的左上角**，因此一般不要给body背景图。



### 多个背景

background属性可以用**逗号分隔，指定多个背景**（和该背景对应的属性设置），同时指定背景色渐变。背景图和背景色可以重复。需要为第一个背景指定所有普通属性

示例，简单的叠加两个背景图、一个渐变

```css
background: url(../image/top-image.png) no-repeat left top,
    url(../image/bottom-image.png)  no-repeat left bottom,
    linear-gradient(to bottom, #838383, rgba(237, 237, 237, 0.74) 10%,  rgba(237, 237, 237, 0.74) 60%, #838383) no-repeat left center scroll;

```

background如果不指定颜色，则使用默认，并且会覆盖上面指定的background-color

### 固定背景

```css
/*背景图固定不随内容滚动*/
background-attachment: fixed;
```
### 正片叠底

颜色和背景图通过**正片叠底**的方式叠加

```css
.wrap3 {
    position: relative;
    width: 1200px;
    height: 400px;
    background: url(ban8.jpg) rgba(0, 0, 0, .5) no-repeat center center;
    background-blend-mode: multiply;
    /*背景图固定不随内容滚动*/
    background-attachment: fixed;
}
```

示例，漂亮按钮

```css
p {
    display: block;
    font-size: 1.7rem;
    width: 18rem;
    height: calc(18rem * 0.3);
    line-height: calc(18rem * 0.3);
    color: #469fea;
    text-align: center;
    text-shadow: 2px 2px 2px black;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 8px;
    border: 1px solid #376ca6;
    background: #469fea linear-gradient(to bottom right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.2) 30%, rgba(0, 0, 0, 0.2) 30%);
    filter: drop-shadow(3px 2px 2px rgba(0, 0, 0, 0.59));
    box-shadow: inset 2px 3px 5px rgba(255,255,255,0.5),
    inset -2px -3px 5px rgba(0,0,0,0.5);
}
```

背景和颜色叠加

```css
body {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.4;
  color: var(--color-white);
  margin: 0;
}

/* mobile friendly alternative to using background-attachment: fixed */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  z-index: -1;
  background: var(--color-darkblue);
  background-image: linear-gradient(
      115deg,
      rgba(58, 58, 158, 0.8),
      rgba(136, 136, 206, 0.7)
    ),
    url(https://raw.githubusercontent.com/lasjorg/fcc-form-example-image/master/67103817-7c51e200-f18b-11e9-975f-f74561336a9a-lj.jpg);
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
```



## Filter

作用于形状而不是box。

```css
.filter {
  -webkit-filter: drop-shadow(5px 5px 1px rgba(0,0,0,0.7));
  filter: drop-shadow(5px 5px 1px rgba(0,0,0,0.7));
}
```

## pisition相对定位

相对定位的应用场景：

- 相对定位元素经常被用来作为**绝对定位元素**的**容器块**。
- 通常用来对布局进行微调，比如将一个图标往下调一点，以便放置文字
- relative相对定位元素的定位是相对其正常位置。
- ***移动***相对定位元素，但它***原本所占的空间不会改变***。

```css
.positioned {
  position: relative;
  background: yellow;
  /*把它看成是左边和顶部的元素被“推开”一定距离，这就导致了它的向下向右移动*/
  top: 30px;
  left: 30px;
}
```

 

## pisition绝对定位

绝对定位用于将元素移动到web页面的任何位置，以创建复杂的布局。

和`relative`定位不一样，`absolute`定位会将元素从当前的文档流里面移除，周围的元素会忽略它。可以用 CSS 的 top、bottom、left 和 right 属性来调整元素的位置。

`absolute`定位比较特殊的一点是元素的定位参照于最近的已定位祖先元素。如果它的父元素没有添加定位规则（默认是`position:relative;`）,浏览器会继续寻找直到默认的 body 标签。

```css
.positioned {
  position: absolute;
  background: yellow;
    /*相对于最近已定位父元素的顶部往右往下*/
  top: 30px;
  left: 30px;
}
```

## fixed定位

`fixed`定位，它是一种特殊的绝对（absolute）定位，区别是其包含块是浏览器窗口。和绝对定位类似，`fixed`定位使用 top、bottom、left 和 right 属性来调整元素的位置，并且会将元素从当前的文档流里面移除，其它元素会忽略它的存在。

`fixed`定位和`absolute`定位的最明显的区别是`fixed`定位元素不会随着屏幕滚动而移动。

示例，固定导航栏

```css
#header {
    position: fixed;
    top: 0;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    background-color: darkred;
    width: 100%;
    height: 4rem;
}

.nav-list {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0;
}

.nav-list > li {
    padding: 1rem;
    margin-right: 2.5rem;
}
.nav-list a {
    color: white;
}

.container {
    margin-top: 6rem;
}
```



## inline box

- 它的内容会随着文字部分的流动而打乱、断行

- 对行内盒设置宽高无效。**通过设置内容的尺寸来控制行内盒子最终尺寸**
- 设置padding, margin 和 border都会更新周围文字的位置，但是对于周围的的块框（ `block` box）不会有影响

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Introduction_to_CSS/Box_model#CSS_%E6%A1%86%E7%B1%BB%E5%9E%8B

### 内联元素跨行

padding, border, or margin水平方向

>***如果内联元素宽度比可用空间少，内容会自动换行。可以理解为一个元素断成了两个，每行的文本框上下都有边框。但第一行 只 有左边框，第二行只有右边框。 ==|***

>当一个内联框跨行(两行或者是多行)时，在逻辑上它仍然是单一的框，并没有变成两个框，这意味着任何水平的padding, border, or margin只会运用在这个内联框的第一行的开始部分和最后一行的结尾部分。


padding和margin在竖直方向没有效果

>运用于元素垂直方向上的padding, border也不会把它上面或者是下面的元素挤开。(垂直方向上的margin是没有效果的)



### 内联元素水平居中

text-align 属性可控制内容在块元素中的**内联元素内容**水平居中（对齐），针对内联元素、内联块。

注意text-align如名称所示，控制的是文字内容。而flex布局justify-content、align-items控制的是容器对齐方式

比如：

```html
<div class="text-center"><em >The man who saved a billion lives</em></div>
```

### 内联元素垂直相邻放置

vertical-align控制元素在同一行上垂直相邻放置的方式，针对内联元素、内联块。

对表单元格使用 vertical-align 的示例。

默认情况下，所有内联元素均使用其父项的基线开始 baseline 。可以将基线视为“行”底部的假想线。vertical-align的值为时 super 和 sub 可以用于在内联元素（即其名称）上添加上标注和下标注

### 文本垂直居中

方法一：父元素设为flex容器，内部的inline-box可以垂直居中

```css
.nav-list li{
    display: flex;
    align-items: center;
}
```

方法二：让行高等于内联元素总高度-padding(竖直方向)

```css
display: inline-block;
height: 3em;
padding: 0.5em 1em;
line-height: 2em;
```

### 文本换行

### 

```css
/*强制不换行*/
div{
    white-space:nowrap;
}

/*自动换行*/
div{
    word-wrap: break-word;
    word-break: normal;
}

/*强制英文单词断行*/
div{
    word-break:break-all;
}
```

## Block box

`block` box 定义为堆放在其他框上的框。

- 内容会独占一行，而且可以设置它的宽高
- 尽可能占据多的宽度（content会补到最大宽度）
- 尽可能占据少的高度（content的高度）
- **对于块级元素，可以直接设置大小，也可以通过设置子元素尺寸来决定父元素实际尺寸**

### 块级元素左右居中

块级元素设置其本身的left 和 right margins为auto即可

### 块级元素右对齐

margin-left: auto;

也可以用flex布局实现。元素内部的item左对齐:

```css
display: flex;
justify-content: right;
```



### margin溢出

div中子元素的margin可能会溢出到div以外，为了方便布局，可以把溢出的margin去掉换成padding

## `inline-block` box

行内块状框

- 它不会重新另起一行，保持了其块特性的完整性，它不会在段落行中断开
- 能够设置宽高
- 随着周围文字而流动

## 浮动

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Floats

http://www.runoob.com/css/css-float.html

浮动有些奇怪的问题

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Floats#%E6%B5%AE%E5%8A%A8%E9%97%AE%E9%A2%98

## z-index

```css
.wrap2 {
    position: relative;
    width: 1200px;
    height: 400px;
    background: url(ban8.jpg) no-repeat center center;
    background-size: cover;
}

.wrap2::before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    background-color: rgba(0, 0, 0, .5);
    z-index: 2;
}
```

# 响应式设计

## 基础

### 设备像素

设备像素（device pixel）：物理像素，设备能控制显示的最小单位。 

设备独立像素（Device Independent Pixel、css pixel）：也叫 **密度无关像素** ，可以认为是计算机坐标系统中的一个点，这个点表示一个可以由程序使用并控制的虚拟像素，可以由相关系统转换为物理像素。不同设备上， 1dip的实际尺寸各不相同，依赖于PPI

设备像素比（DPR）：设备像素比是指一个方向上，一个设备像素对应多少设备独立像素（CSS像素）。 如果手机浏览器视图宽度是650 dips, 650 dips实际上被硬件扩展到了1920的硬件像素宽度 那么横向上（宽度）的设备像素比为1920/650。



Chrome 浏览器控制台 console 中输入 

```text
window.devicePixelRatio
结果：1.5
```

图片保存的分辨率实际对应设备像素，如果电脑上一张图片实际宽度200px，那么浏览器css里设置图片宽度为(200/1.5)px，就能清晰显示图片，再大就会失真。

### 设置窗口 

```
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

 `width=device-width` 使页面内容匹配不同的屏幕尺寸 `initial-scale=1.0` 初始缩放比例，也就是设备独立像素和CSS像素的比例为1

如果当前页面的 layout viewport 大于移动设备的 dips 宽度，为了使得页面不出现横向滚动条，提高用户体验，移动设备通常会自动给整个网页设置一个默认的缩放值来缩小页面。

设置 initial-scale=1 来保证网页在浏览器中一开始就根据屏幕尺寸 1：1 缩放或扩大。需要注意的是，设置 initial-scale=1 其实是让 dips 像素与 CSS 像素的比例达到 1：1。

### PPI

https://www.zhihu.com/question/29226201

**PPI 即像素密度，表示每英寸所拥有的物理像素数量。**

思考：在 viewport 缩放比例都为 1 （或缩放比例相同即可）的情况下，为什么同样大小的字体（比如16px）或者同一个 app 的 icon 在不同的移动设备下人眼看起来的大小不一样？

已知：iphone7 PPI 为 326，DPR 为 2; iphone7 plus PPI 为401,DPR 为 3. 

xps13 9350 chrome浏览器DPR是1.5，firefox DPR=1.367，因此chrome默认尺寸也会大些

下面计算iphone7和7Plus上，1px或1dip的实际长度

```css
# 推导如何计算1dip的长度
dpLength = 1/PPI inch
dipLength = dpLength * DPR = DPR/PPI inch

iphone7: dipLength = 2/326 约等于 0.00613497
iphone7 Plus: dipLength = 3/401 约等于 0.0074813
# 所以 iphone7 plus 上的 app 图标和字比 iphone7 要大。
```





## 内容自适应

width是百分比或视图宽度动态改变时，可以指定最小宽度是多少px

```css
#navbar {
    position: absolute;
    width: 95%;
    min-width: 10rem;
    height: 10rem;
}
```

calc用来动态计算尺寸。比如实现响应式的一行3列

```css
.col-3{
    width: calc(100%/3 - 5px); 
    margin-right: calc(5px*3 /2); 
}
```



## 改变主轴方向

媒体查询实现在页面小于650px时，列变为主轴

```css
@media (max-width: 650px)
nav > ul {
    flex-direction: column;
}

nav > ul {
    width: 35vw;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
}
```

展示多个卡片。pricing是父元素div，product是子元素div

```css
@media (max-width: 800px) {
    #pricing {
        flex-direction: column;
    }
    .product {
        width: 100%;
    }
}

#pricing {
    margin: 5rem auto;
    font-size: 2rem;
    display: flex;
    justify-content: space-around;
    align-items: center;
    /*flex-wrap: wrap;*/

}

.product {
    /*min-width: 20rem;*/
    width: 30%;
    border: black 1px solid;
    border-radius: 3px;
    margin-top: 3rem;
}
```

## 侧边导航栏

对侧边导航栏，大屏幕时固定在左侧，小屏幕时放到顶部绝对定位（不固定）

nav里的ul作为滚动条容器，ul里的多个li是内容

```css
/*大屏幕时固定在左侧*/
#navbar {
    position: fixed;
    width: 20rem;
    height: 80vh;
}

/*侧边栏滚动条的容器,高度必须确定。内容是li*/
#navbar ul {
    list-style-type: none;
    padding: 0;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
}

/*页面主体*/
#main-doc {
    position: absolute;
    /*左侧要让出侧栏的宽度*/
    margin-left: 22rem;
}

@media (max-width: 800px) {
/*小屏幕时放到顶部绝对定位（不固定）*/    
    #navbar {
        position: absolute;
        width: 95%;
        /*导航栏不能过窄*/
        min-width: 13rem;
        height: 10rem;
    }

    #navbar ul {
        border: black 1px solid;
    }

    #main-doc {
        /*保证放在navbar之下*/
        margin-top: 11rem;
        margin-left: 0px;
    }

}
```



# 长度单位

## px

可点击元素尺寸宽度和高度最少都得是48px 

## 百分比

容器百分比超过100%, 会跑出父容器。

一般是父元素有明确的宽度或最大宽度(如正文container)，子元素宽度设为百分比就可以自适应宽度。

header没有明确宽度或最大宽度，因此宽度就是子元素的总宽度，logo和nav设为百分比宽度只能决定相对宽度但不能保证占满整个窗口

## 视窗单位

除了用 `em` 或 `px` 去设置文本大小, 你还可以用视窗单位来做响应式排版。视窗单位还有百分比，它们都是相对单位，但却基于不同的参照物。视窗单位相对于设备的视窗尺寸 (宽度或高度) ，百分比是相对于父级元素的大小。

四个不同的视窗单位分别是：

- `vw`：如 `10vw` 的意思是视窗宽度的 10%。
- `vh：` 如 `3vh` 的意思是视窗高度的 3%。
- `vmin：` 如 `70vmin` 的意思是视窗中较小尺寸的 70% (高度 VS 宽度)。
- `vmax：` 如 `100vmax` 的意思是视窗中较大尺寸的 100% (高度 VS 宽度)。

适用于header

## em

https://www.w3cplus.com/css/rem-vs-em.html

em是一个当前元素内字体大小的长度单位。如果设置font-size的单位为em，则1em的大小从父元素继承。如果设置margin、padding的单位为em，则1em是当前元素的font-size实际大小。

```css
h1 
{ font-size: 2em; /* 1em = 16px */ 
    margin-bottom: 1em; /* 1em = 32px */ 
} 

p { font-size: 1em; /* 1em = 16px */ 
    margin-bottom: 1em; /* 1em = 16px */ 
}

著作权归作者所有。
商业转载请联系作者获得授权,非商业转载请注明出处。
原文: https://www.w3cplus.com/css/rem-vs-em.html © w3cplus.com
```

当本元素未设置font-size时，font-size从父元素那里继承，等同于给该元素设置`font-size: 1em;`。因此当本元素不设font-size或者设为1em时，本元素的em和父元素的em才相同。



## rem

指根html元素的em。`1rem`等同于`<html>`中的`font-size`。
rem方便计算元素实际尺寸，但会使组件缺少模块化。

## em和rem使用原则

如果这个属性根据它的`font-size`进行测量，则使用`em`

其他的一切事物均使用`rem`.

**例子**

可以同时使用em和rem就可以简化代码。

案例1：两个不同大小的标题，第二个标题边缘空间调的相应大一点。

```css
.header { font-size: 1rem; 
    padding: 0.5em 0.75em; 
    background: #7F7CFF; } 

.header--large { font-size: 2rem; }

```

案例2：两个不同大小的标题，顶部和底部padding相同的尺寸（根据根font-size），左右padding根据当前元素font-size设置。

```css
.header 
{ padding: 0.5em 0.75rem; 
    font-size: 1em; background: #7F7CFF; } 

.header--large { font-size: 2em; }

```



## 倍数因子

设置简单。1.5倍字体大小的行高

```css
p {
  line-height: 1.5;
}
```

# HTML元素

## 语义化元素

```html
<article>  
    <header><h1>计算机各类语言介绍</h1></header>   
    <p>本文列举了部分计算机语言的一些介绍</p>   
    <section>  
      <h2>JavaScript</h2>  
      <p>js是一门……</p>  
    </section> 
    <section>  
      <h2>HTML</h2>  
      <p>HTML是一门……</p>  
    </section>  
    <footer>版权归微也所有</footer>  
  </article>
```



## 表单

### 控件

```html
<form action="/my-handling-form-page" method="post"> 
  <div>
    <label for="name">Name:</label>
    <input type="text" id="name" name="user_name" />
  </div>
  <div>
    <label for="mail">E-mail:</label>
    <input type="email" id="mail" name="user_email" />
  </div>
  <div>
    <label for="msg">Message:</label>
    <textarea id="msg" name="user_message"></textarea>
  </div>
    
<!-- 隐藏input，如密码的md5值 -->
<input type="hidden"> 
```

label。input可以放到label里面，也可以分开用for表示关联关系

```html
<label for="name">
  Name: <input type="text" id="name" name="user_name">
</label>
```

radio。checkbox也是类似

```html
<style>
    label {
        display: flex;
        font-size: 1.125rem;
        align-items: center;
        /*margin-bottom: 0.5rem;*/
    }
    .input-check {
        display: inline-block;
        margin-right: 0.625rem;
        /*保证radio或checkbox的尺寸*/
        min-height: 1.25rem;
        min-width: 1.25rem;
    }
</style>
<div class="form-group text-left">
    <p>Would you recommend freeCodeCamp to a friend?</p>
    <label><input name="user-recommend" value="definitely" type="radio" class="input-check" checked=""/>Definitely</label>

    <label><input name="user-recommend" value="maybe" type="radio" class="input-check" />Maybe</label>
    <label><input name="user-recommend" value="not-sure" type="radio" class="input-check" />Not sure</label>
</div>
```


可以在所有浏览器中单击标签来激活相应的小部件。

```html
<input type="email" id="email" name="email" multiple>
<input type="password" id="pwd" name="pwd">
<input type="search" id="search" name="search">
<input type="url" id="url" name="url">
<input type="tel" id="tel" name="tel">
<textarea cols="30" rows="10"></textarea>
```



### 表单传输

POST方法默认提交后Resquest

```html
POST / HTTP/1.1
Host: foo.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

say=Hi&to=Mom
```

`multipart/form-data`支持多个键值对，值也可以是文件，所以支持多文件上传。

raw。body就是json/xml等内容。

二进制。Content-Type:application/octet-stream

发送数据可以通过js。https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Forms/Sending_forms_through_JavaScript

在表单不填就提交的情况下，text类型和textarea类型的表单域，提交到服务端为空

checkbox、readio、select等表单域在为不填情况下不会提交到服务器，也就是说服务器接收不到这些表单值的值，所以就相当于null了

### 表单校验

HTML5表单校验，通过表单元素的[校验属性](https://developer.mozilla.org/zh-CN/docs/Web/Guide/HTML/HTML5/Constraint_validation)实现。

- CSS 伪类 [`:valid`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/:valid)   [`:invalid`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/:invalid) 进行特殊的样式化。

- input元素支持必选、正则表达式校验
- 所有文本框 ([``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/input) 或 [``](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/textarea)) 可以强制使用`minlength` 和 `maxlength` 属性. 
- 在数字条目中 (i.e. `<input type="number">`), 该 `min` 和 `max` 属性也能强制验证长度. 

```html
<style>
input:invalid {
  border: 2px dashed red;
}

input:valid {
  border: 2px solid black;
}
</style>
<form>
  <label for="choose">Would you prefer a banana or a cherry?</label>
  <input id="choose" name="i_like" required pattern="banana|cherry">
  <button>Submit</button>
</form>
```

完整例子：

https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Forms/Data_form_validation

js也内置了表单验证API。

独立的库（原生 Javascript 实现）：   

- [Validate.js](http://rickharrison.github.com/validate.js/)

jQuery 插件:   

- [Validation](http://bassistance.de/jquery-plugins/jquery-plugin-validation/)
- [Valid8](http://unwrongest.com/projects/valid8/)

远程校验可以使用ajax。

自定义表单控件。https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Forms/How_to_build_custom_form_widgets

### 表单样式

https://developer.mozilla.org/zh-CN/docs/Learn/HTML/Forms/Styling_HTML_forms

搜索框在基于WebKit的浏览器（Chrome，Safari等）上，必须使用`-webkit-appearance`专有属性调整

```css
input[type=search] {
  border: 1px dotted #999;
  border-radius: 0;
# 平台无关
  -webkit-appearance: none;
}
```

许多浏览器使用系统默认的字体和文本。让form表单的外观和其他内容保持一致:

```css
button, input, select, textarea {
  font-family : inherit;
  font-size   : 100%;
}
```

**单选多选框**

<form action="/submit-cat-photo">
  <label><input type="radio" name="indoor-outdoor" checked> Indoor</label>
  <label><input type="radio" name="indoor-outdoor"> Outdoor</label>
  <label><input type="checkbox" name="personality" checked> Loving</label>
  <label><input type="checkbox" name="personality"> Lazy</label>
  <label><input type="checkbox" name="personality"> Energetic</label>
  <input type="text" placeholder="cat photo URL" required>
  <button type="submit">Submit</button>
</form>

##列表

ul li是block元素。

ul ol dl

默认样式：

ul ol dl p默认上下margin为2em

ul ol的padding-left为40px

li dt无margin

dd有margin-left 40px



[`list-style-type`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/list-style-type) 

[`list-style-position`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/list-style-position) 

[`list-style-image`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/list-style-image) 

```html
ul {
  list-style: square url(example.png) inside;
}
```

定制项目符号

```css
ul {
  padding-left: 2rem;
  list-style-type: none;
}

ul li {
  padding-left: 2rem;
  background-image: url(star.svg);
  background-position: 0 0;
  background-size: 1.6rem 1.6rem;
  background-repeat: no-repeat;
}
```

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/%E4%B8%BA%E6%96%87%E6%9C%AC%E6%B7%BB%E5%8A%A0%E6%A0%B7%E5%BC%8F/Styling_lists



计数开始值

```html
<ol start="4" reversed>
	  <li value="2">Toast pitta, leave to cool, then slice down the edge.</li>
</ol>
```

li自适应占满ul

```css
.nav-list {
    display: flex;
    height: 100%;
    justify-content: flex-end;
    margin-bottom: 0;
}
.nav-list li{
    display: flex;
    align-items: center;
    padding: 0 2rem;
}
```

## 链接

链接的样式是建立在另一个样式之上的，比如第一个规则的样式会应用到所有后续的样式，如果当一个链接被激活 (activated) 的时候，它也是处于悬停 (hover) 状态的

记忆：**L**o**V**e **F**ears **HA**te.

```html
<style>
body {
  width: 300px;
  margin: 0 auto;
  font-size: 1.2rem;
  font-family: sans-serif;
}

p {
  line-height: 1.4;
}

a {
  outline: none;
  text-decoration: none;
  padding: 2px 1px 0;
}

a:link {
  color: #265301;
}

a:visited {
  color: #437A16;
}

a:focus {
  border-bottom: 1px solid;
  background: #BAE498;
}

a:hover {
  border-bottom: 1px solid;     
  background: #CDFEAA;
}
/*a:active 用来给链接一个不同的配色方案，当链接被激活 (activated) 时，让链接被激活的时候更加明显。*/
a:active {
  background: #265301;
  color: #CDFEAA;
}
    
a[href*="http"] {
  background: url('https://mdn.mozillademos.org/files/12982/external-link-52.png') no-repeat 100% 0;
  background-size: 16px 16px;
  /* */
  padding-right: 19px;
}
</style>
<p>There are several browsers available, such as <a href="https://www.mozilla.org/zh-CN/firefox/">Mozilla
Firefox</a>, <a href="https://www.google.com/chrome/index.html">Google Chrome</a>, and
<a href="https://www.microsoft.com/zh-CN/windows/microsoft-edge">Microsoft Edge</a>.</p>
```

包含图标

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/%E4%B8%BA%E6%96%87%E6%9C%AC%E6%B7%BB%E5%8A%A0%E6%A0%B7%E5%BC%8F/Styling_links#%E5%9C%A8%E9%93%BE%E6%8E%A5%E4%B8%AD%E5%8C%85%E5%90%AB%E5%9B%BE%E6%A0%87

样式化为按钮

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/%E4%B8%BA%E6%96%87%E6%9C%AC%E6%B7%BB%E5%8A%A0%E6%A0%B7%E5%BC%8F/Styling_links#%E6%A0%B7%E5%BC%8F%E5%8C%96%E9%93%BE%E6%8E%A5%E4%B8%BA%E6%8C%89%E9%92%AE

悬停在父元素上时，改变子元素的样式

```css
.code {
    color: var(--main-gray);
    transition: color 0.3s ease-out;
}
.project:hover {
    color: white;
    text-decoration: none;
}
.project:hover .code {
    color: #ff7f50;
}
```

## 表格

表格内滚动

```
div.contaned_table {
 
    width: 100%;
 
    overflow-x-auto;
 
}
```

##  图片

CSS图片自适应

```java
img {
  max-width: 100%;
  display: block;
  height: auto;
}
```

object-fit属性和background-size类似，常用的有

- contain: 保持原有尺寸比例。保证替换内容尺寸一定可以在容器里面放得下。因此，此参数可能会在容器内留下空白。

- cover: 保持原有尺寸比例。保证替换内容尺寸一定大于容器尺寸，宽度和高度至少有一个和容器一致。因此，此参数可能会让替换内容（如[图片](https://www.ylefu.com/tags/58/)）部分区域不可见。

```css
.project-img {
    width: 100%;
    height: calc(100% - 4rem);
    object-fit: cover;
}
```

为优化图片在高分辨率设备下的显示效果，最简单的方式是定义它们的 `width` 和 `height` 值为源文件宽高的一半。

## 视频

可以插入优酷视频页面的通用代码

```html
<iframe height=498 width=510 src='http://player.youku.com/embed/XNDUyMDA5NDgwOA==' frameborder=0 allowfullscreen="true"></iframe>
```

# 伪元素

```html
<style>
    /* 所有含有"href"属性并且值以"http"开始的元素，
将会在其内容后增加一个箭头（去表明它是外部链接）
*/

[href^=http]::after {
  content: '⤴';
}
</style>
<ul>
  <li><a href="https://developer.mozilla.org/en-US/docs/Glossary/CSS">CSS</a> defined in the MDN glossary.</li>
  <li><a href="https://developer.mozilla.org/en-US/docs/Glossary/HTML">HTML</a> defined in the MDN glossary.</li>
</ul>
```

段落的第一行使用粗体字，它的第一个单词首字母大写并给它一种老式的感觉。

```html
p::first-line {
  font-weight: bold;
}

p::first-letter {
  font-size: 3em;
  border: 1px solid black;
  background: red;
  display: block;
  float: left;
  padding: 2px;
  margin-right: 4px;
}
```



# 选择器

## 选择器种类



```css
<!-- 通配选择器  -->
* {color:red;}
 
<!-- class -->
.xxx{}
<!-- id -->
#xxx{}
 
p:nth-child(3) {}  备注：()中的数字是指第n个节点，而不是第n个p节点
 
<!-- 选择器分组 -->
h2, p {color:gray;}
 
<!-- 多个类选择器链接，与的关系 -->
<!-- 可以匹配 <p class="important urgent">以及
<p class="important urgent warning">This paragraph is a very important and
urgent warning. </p> -->
.important.urgent {background:silver;}
 
<!-- 后代选择器（descendant selector）又称为包含选择器。
后代选择器可以选择作为某元素后代的元素。 -->
<!-- 作为 h1 元素后代的任何 em 元素 -->
h1 em {color:red;}
 
<!-- 与后代选择器相比，子元素选择器（Child selectors）只能选择作为某元素子元素的元素。
-->
h1 > strong {color:red;}
 
```

属性选择器
[abc^="def"]     选择 abc 属性值以 "def" 开头的所有元素

[abc$="def"]     选择 abc 属性值以 "def" 结尾的所有元素

[abc*="def"]     选择 abc 属性值中包含子串 "def" 的所有元素

## 组合选择器

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Introduction_to_CSS/Combinators_and_multiple_selectors

```css
/* 基本的table样式 */
#wrapper * {
    padding:20px;
}
table {
  font: 1em sans-serif;
  border-collapse: collapse;
  border-spacing: 0;
}

/* 所有在table里的td以及th，这里的逗号不是一个组合器，
它只是允许你把几个选择器对应到相同的CSS规则上.*/
table td, table th {
  border : 1px solid black;
  padding: 0.5em 0.5em 0.4em;
}

/* 所有table里的thead里的所有th */
table thead th {
  color: white;
  background: black;
}

/* 所有table里的tbody里的所有td（第一个除外），每个td都是由它上边的td选择 */
table tbody td + td {
  text-align: center;
}

/*table里所有的tbody里的td当中的最后一个 */
table tbody td:last-child {
  text-align: right
}

/* 所有table里的tfoot里的th */
table tfoot th {
  text-align: right;
  border-top-width: 5px;
  border-left: none;
  border-bottom: none;
}

/* 在table当中，所有的th之后的td */
table th + td {
  text-align: right;
  border-top-width: 5px;
  color: white;
  background: black;
}

/* 定位在“with-currency”类中拥有属性lang并且这个属性值为en-US的元素中的，最后td(:last-child)节点的前面（::before）*/
.with-currency[lang="en-US"] td:last-child::before {
  content: '$';
}

/* 定位在“with-currency”类中拥有属性lang并且这个属性值为fr的元素中的，最后td(:last-child)节点的后面（::after） */
.with-currency[lang="fr"] td:last-child::after {
  content: ' €';
}
```



```html
<style>
    ul {
  padding: 0;
  list-style-type: none;
}

 ul a{
  text-decoration: none;
  display: block;
  color: black;
  background-color: red;
  padding: 5px;
  margin-bottom: 10px;
}

ul a:hover {
  color: red;
  background-color: black;
}

div h1 ~ p {
  font-style: bold;
  color: blue;
}
</style>
<ul>
  <li><a href="#">Home</a></li>
  <li><a href="#">Portfolio</a></li>  
  <li><a href="#">About</a></li>
</ul>
<div>
<h1>Welcome to my website</h1>

<p>Hello, and welcome! I hope you enjoy your time here.</p>

<h2>My philosophy</h2>

<p>I am a believer in chilling out, and not getting grumpy. I think everyone else should follow this ideal, and <a href="#">drink green tea</a>.</p>
</div>
```



## 伪类

```css
a:focus {
  color: darkred;
  text-decoration: none;
}

/* 兄弟元素的偶数个li */
li:nth-of-type(2n) {
  background-color: #ccc;
}

li:nth-of-type(2n+1) {
  background-color: #eee;
}

/* 该元素是p，且是某父元素第一个子元素 */
p:first-child
{
background-color:yellow;
}

/*属于其父元素的第二个 p 元素的每个 p*/
p:nth-of-type(2)
{
background:#ff0000;
}

```

# CSS变量

:root是html的父元素，定义变量让html都能使用

```css
:root {
    --main-white: #f0f0f0;
    --main-red: #be3144;
    --main-blue: #45567d;
    --main-gray: #303841;
}
```

# CSS层叠

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Introduction_to_CSS/Cascade_and_inheritance

哪个选择器的该属性优先级决定于：

1. 重要性（Importance）
2. 专用性（Specificity）
3. 源代码次序（Source order）

属性优先级如何确定：

1. 重要性取决于是否添加!important。不建议使用 `!important` 。

2. 专用性衡量选择器需要计算分值。具体见上面文档。
3. 如果多个相互竞争的选择器具有相同的重要性和专用性，则由源代码次序决定。
4. **层叠都发生在属性级别**。当多个CSS规则匹配相同的元素时，它们都被应用到该元素中。只有在这之后，任何相互冲突的属性才会被评估，以确定哪种风格会战胜其他类型。

选择器优先级简单概括：

- 选择器样式优先级:  id > class > div p > p > *
- 选择器：后定义的css覆盖之前的。与`class=“”`引用顺序无关
- 内联样式覆盖选择器样式
- 使用`color: pink !important;`覆盖所有其他样式.





# CSS继承



```css
有继承性的属性
1、字体系列属性
font：组合字体
font-family：规定元素的字体系列
font-weight：设置字体的粗细
font-size：设置字体的尺寸
font-style：定义字体的风格
font-variant：设置小型大写字母的字体显示文本，这意味着所有的小写字母均会被转换为大写，但是所有使用小型大写字体的字母与其余文本相比，其字体尺寸更小。
font-stretch：对当前的 font-family 进行伸缩变形。所有主流浏览器都不支持。
font-size-adjust：为某个元素规定一个 aspect 值，这样就可以保持首选字体的 x-height。
2、文本系列属性
text-indent：文本缩进
text-align：文本水平对齐
line-height：行高
word-spacing：增加或减少单词间的空白（即字间隔）
letter-spacing：增加或减少字符间的空白（字符间距）
text-transform：控制文本大小写
direction：规定文本的书写方向
color：文本颜色
3、元素可见性：visibility
4、表格布局属性：caption-side、border-collapse、border-spacing、empty-cells、table-layout
5、列表布局属性：list-style-type、list-style-image、list-style-position、list-style
6、生成内容属性：quotes
7、光标属性：cursor
8、页面样式属性：page、page-break-inside、windows、orphans
9、声音样式属性：speak、speak-punctuation、speak-numeral、speak-header、speech-rate、volume、voice-family、pitch、pitch-range、stress、richness、、azimuth、elevation
 
三、所有元素可以继承的属性
1、元素可见性：visibility
2、光标属性：cursor
 
四、内联元素可以继承的属性
1、字体系列属性
2、除text-indent、text-align之外的文本系列属性
 
五、块级元素可以继承的属性
1、text-indent、text-align
```

# 文本

## 对比度

对比度是通过比较两种颜色的相对亮度值来计算的，其范围是从相同颜色的 1 : 1（无对比度）到白色与黑色的最高对比度 21 : 1

正常文本的对比度至少为 4.5 : 1

## 字体样式

元素中的文本是作为一个单一的实体，要改变样式，必须要用适合的元素来包装它们，比如span、strong 或者使用伪元素

字体加粗font-weight可以增加质感

```css
html {
  font-size: 10px;
}

h1 {
  font-size: 2.6rem;
  text-transform: capitalize;
}

h1 + p {
  font-weight: bold;
}

p {
  font-size: 1.4rem;
  color: red;
  font-family: Helvetica, Arial, sans-serif;
}
```

## 文字阴影

```css
text-shadow: -1px -1px 1px #aaa,
             0px 4px 1px rgba(0,0,0,0.5),
             4px 4px 5px rgba(0,0,0,0.7),
             0px 0px 7px rgba(0,0,0,0.4);
```

其他样式

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/%E4%B8%BA%E6%96%87%E6%9C%AC%E6%B7%BB%E5%8A%A0%E6%A0%B7%E5%BC%8F/Fundamentals#%E5%85%B6%E4%BB%96%E4%B8%80%E4%BA%9B%E5%80%BC%E5%BE%97%E7%9C%8B%E4%B8%80%E4%B8%8B%E7%9A%84%E5%B1%9E%E6%80%A7

## font-size

推荐将根元素的font-size设为10px

## 行高

文本行高设置为字体高度的1.5倍

```css
line-height: 1.5;
```

## 安全字体和字体降级

当某种字体不可用时，你可以让浏览器`自动降级`到另一种字体

p {
  font-family: Helvetica, Sans-Serif;
}



Web安全字体列表：

- Helvetica
- Arial
- Courier New
- Times
- Verdana

CSS 定义了 5 个常用的字体名称:  `serif, ``sans-serif, ``monospace`, `cursive,`和 `fantasy. `

优秀字体推荐

Rubik

font-family: "Segoe UI","Helvetica Neue","Helvetica",Arial,sans-serif;

font-weight: 500;（300 400 500）



Google Lobster

`<link href="https://fonts.gdgdocs.org/css?family=Lobster" rel="stylesheet" type="text/css">`

或css导入

```css
@import url('https://fonts.font.im/css?family=Roboto');
```



## 字体下载

免费的字体经销商：这是一个可以下载免费字体的网站(可能还有一些许可条件，比如对字体创建者的信赖)。比如： [Font Squirre](https://www.fontsquirrel.com/)，[dafont](http://www.dafont.com/) 和 [Everything Fonts](https://everythingfonts.com/)。

## 文本布局

[`text-align`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/text-align) 属性用来控制文本如何和它所在的box对齐,和word左右对齐类似


# 颜色

IDEA、Chrom开发工具的拾色器取色板很好用

去除背景色

.css("background", "none")



色彩用十六进制或rgb表示，依次红绿蓝

```
# 使用 6 位十六进制数字来表示颜色，每 2 位分别表示红色 (R)、绿色 (G) 和蓝色 (B) 成分。
<style>
  body {
    background-color: #000000;
  }
</style>
```

不透明度

``` css
/* Red with RGBA */
p:nth-child(1) {
  background-color: rgba(255,0,0,0.5);
}

/* Red with opacity */

p:nth-child(2) {
  background-color: rgb(255,0,0);
  opacity: 0.5;
}
```

图片能透过标题显示，且标题的文本显示不受影响，此时应该使用RGBA修改标题背景色的透明度；让整个UI元素从完全隐藏到可见，此时应该使用不透明度（Opacity）



# flex弹性容器布局

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox

阮一峰讲flex语法和实例
http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html

效果实例https://yoksel.github.io/flex-cheatsheet/

属性动画

https://segmentfault.com/a/1190000018233450

 

## flex container

采用 Flex 布局的元素，称为 Flex 容器（flex container）,flex container的所有子元素自动成为容器成员（flex item）

容器默认存在两根轴：水平的主轴（main axis）和垂直的侧轴（cross axis）。主轴的开始位置（与边框的交叉点）叫做main start，结束位置叫做main end；侧轴的开始位置叫做cross start，结束位置叫做cross end。

 item默认沿主轴排列。单个item占据的主轴空间叫做main size，占据的侧轴空间叫做cross size。



flex container是块级元素，默认单独成一行



轴空间

![clipboard.png](https://segmentfault.com/img/bVTiJQ?w=563&h=333)

![](https://upload-images.jianshu.io/upload_images/14001103-ffb02ce0407b4cfd.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200)

容器属性概览

![clipboard.png](https://segmentfault.com/img/bVboFvE?w=949&h=735)

### flex-direction 主轴方向

子元素的排列方向

默认是row，子元素（flex item)从左往右排。

```css
.box {
 flex-direction: row | row-reverse | column | column-reverse;
}
```



### flex-wrap 换行

默认情况下，item都排在一条线（又称"轴线"）上。

`flex-wrap`属性定义，如果一条轴线排不下，如何换行。

```css
display: flex;
/*nowrap不换行，wrap换行且第一行在上方，wrap-reverse 换行且第一行在下方*/
flex-wrap: wrap;
 
```

### flex-flow 方向&换行简写

flex-flow是flex-direction属性和flex-wrap属性的简写形式，默认值为row nowrap

 

### justify-content 主轴方向对齐方式

项目在主轴上的对齐（或者说排列）方式 justify-content，相当于word中水平方向左对齐、右对齐等等。

也就是改变justify-content属性，会让items沿主轴方向移动

```CSS
.box {
 justify-content: flex-start | flex-end | center | space-between | space-around;
}
 
```

- `flex-start`（默认值）：左对齐
- `flex-end`：右对齐
- `center`： 居中
- `space-around` 会使所有 flex 项沿着主轴均匀地分布，在任意一端都会留有一点空间。
-  `space-between`和 `space-around` 非常相似，只是它不会在两端留下任何空间。



项目在侧轴上的对齐方式 align-items

```css
.box {
  align-items: flex-start | flex-end | center | baseline | stretch;
}
 
```

 改变align-items属性，会让items沿侧轴（默认垂直）方向移动

`flex-start`：侧轴的起点对齐

`flex-end`：侧轴的终点对齐

`center`：侧轴的中点对齐

`stretch`（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度

## flex item

display失效



https://image-static.segmentfault.com/135/113/1351137673-5c6e4bb591ac9_articlex

### width

width失效，max-width可以起作用

### order

order属性定义项目的排列顺序。数值越小，排列越靠前，默认为0。

### flex-grow

flex-grow属性定义项目的放大比例，默认为0，即如果存在剩余空间，也不放大。

如果所有项目的flex-grow属性都为1，则它们将等分剩余空间（如果有的话）。如果一个项目的flex-grow属性为2，其他项目都为1，则前者占据的剩余空间将比其他项多一倍。

```css
  .item {
 	flex-grow: <number>; /* default 0 */
 }
```



### flex-shrink

flex-shrink属性定义了项目的缩小比例，默认为1，即如果空间不足，该项目将缩小。

如果所有项目的flex-shrink属性都为1，当空间不足时，都将等比例缩小。如果一个项目的flex-shrink属性为0，其他项目都为1，则空间不足时，前者不缩小

```
    .item {
 
      flex-shrink: <number>; /* default 1 */
 
    }
 
```



###  flex-basis

flex-basis属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小。

它可以设为跟width或height属性一样的值（比如350px），则项目将占据固定空间。

```
    .item {
 
      flex-basis: <length> | auto; /* default auto */
 
    }
 
```



### flex简写

建议尽量使用简写。

flex属性是flex-grow, flex-shrink 和 flex-basis的简写，默认值为0 1 auto。后两个属性可选。

该属性有两个快捷值：auto (1 1 auto) 和 none (0 0 auto)。

建议优先使用这个属性，而不是单独写三个分离的属性，因为浏览器会推算相关值。

```
    .item {
      flex: none | [ <'flex-grow'> <'flex-shrink'>? || <'flex-basis'> ]
    }
```

可以指定 flex 项目的最小主轴长度。实例中，每个flex 项将首先给出200px的可用空间，然后，剩余的可用空间将根据分配的比例共享

```css
article {
  flex: 1 200px;
}

article:nth-of-type(3) {
  flex: 2 200px;
}
```

### align-self

align-self 属性定义flex子项单独在侧轴（纵轴）方向上的对齐方式。

[`align-self`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/align-self) 属性覆盖 [`align-items`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/align-items) 的行为。比如，你可以这样：

```css
button:first-child {
  align-self: flex-end;
}
```

这个元素因为放在最后，所以可以用flex-grow:1让它占据主轴（横向）剩余空间。

```
flex-grow:1
```

### 元素中的内容右对齐

为了让该元素中的内容右对齐，可以把它变成一个flex容器

```
display: flex;//将它设置为flex,就可以单独对他进行主轴右对齐
justify-content: flex-end;
```



### flex 嵌套

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Flexbox#flex_%E5%B5%8C%E5%A5%97

## flex实现三种布局

http://www.ruanyifeng.com/blog/2015/07/flex-examples.html

平均分配只需要设置flex-grow:1。 
百分比网格，某个网格的宽度为固定的百分比，其余网格平均分配剩余的空间，并设置所有网格flex-grow:1 。

#  Grid布局

http://www.ruanyifeng.com/blog/2019/03/grid-layout-tutorial.html



分container和item

container中定义行和列的尺寸

```css
.container {
  display: grid;
  /*默认情况下，容器元素都是块级元素，但也可以设成行内元素。*/
  display: inline-grid;

  grid-template-columns: 100px 100px 100px;
  /*也可以使用百分比*/
  grid-template-columns: 33.33% 33.33% 33.33%;
  /*repeat简化*/
    grid-template-columns: repeat(2, 100px 20px 80px);
  grid-template-rows: 100px 100px 100px;
}
```

## item尺寸单位

`fr`：设置列或行占剩余空间的一个比例，

`auto`：设置列宽或行高自动等于它的内容的宽度或高度，

`%`：将列或行调整为它的容器宽度或高度的百分比，

## 自动填充

auto-fill是根据容器的大小，尽可能多地放入指定大小的行或列。一旦放入足够的列之后，后面就会有剩余空间（不足以放入下一个列或再没有多余的列）。

`auto-fit`效果几乎和`auto-fill`一样。不同点仅在于，当容器的大小大于各网格项之和时，`auto-fill`将会持续地在一端放入空行或空列，这样就会使所有网格项挤到另一边；而`auto-fit`则不会在一端放入空行或空列，而是会将所有网格项拉伸至合适的大小。

```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, 100px);
}
```
![img](https://www.wangbase.com/blogimg/asset/201903/bg2019032508.png)

## minmax

`minmax()`函数接受两个参数，一个最小值和一个最大值。如果定义的最大值小于最小值，它将会被忽略，函数会被视为只设置了一个最小值。

参考https://www.w3cplus.com/css3/how-the-minmax-function-works.html

`minmax()`函数接受六种类型的值：

- 长度值`<length>`
- 百分比值
- 弹性值
- `max-content`
- `min-content`
- `auto`

下面这个自适应的网格有多行，每行的多个列等宽。各个行的item个数相同。这个flex布局难以实现

```css
.projects-grid {
    display: grid;
    /*列是等宽自适应的, 最小宽度是320px*/
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    grid-gap: 4rem;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    margin-bottom: 6rem;
}
```

## 对齐

[使用 justify-self 水平对齐项目](https://learn.freecodecamp.one/responsive-web-design/css-grid/align-an-item-horizontally-using-justify-self)

[使用 align-self 垂直对齐项目](https://learn.freecodecamp.one/responsive-web-design/css-grid/align-an-item-vertically-using-align-self)

[使用 justify-items 水平对齐所有项目](https://learn.freecodecamp.one/responsive-web-design/css-grid/align-all-items-horizontally-using-justify-items)

[使用 align-items 垂直对齐所有项目](https://learn.freecodecamp.one/responsive-web-design/css-grid/align-all-items-vertically-using-align-items)

## grid-gap

行、列间距

```css
grid-gap: <grid-row-gap> <grid-column-gap>;
```

如果`grid-gap`省略了第二个值，浏览器认为第二个值等于第一个值



每个item的高如果不指定，那就取决于其中item中的内容。个人理解是一行最高的那个。

比如item是a标签，子元素p增大内部padding后会把item拉高

```css
.project-img {
    width: 100%;
    height: calc(100% - 7.5rem);
    object-fit: cover;
}

.project-title {
    font-size: 1.5rem;
    padding: 3rem;
}
```

## 命名定义网格

grid-area声明网格item的名称

grid-template-areas引用各个item的名称定义网格

```html
<style>
    .header {
        background: LightSkyBlue;
        grid-area: header;
    }

    .advert {
        background: LightSalmon;
        grid-area: advert;
    }

    .content {
        background: PaleTurquoise;
        grid-area: content;
    }

    .footer {
        background: lightpink;
        grid-area: footer;
    }

    .container {
        font-size: 1.5em;
        min-height: 300px;
        width: 100%;
        background: LightGray;
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: 50px auto 1fr auto;
        grid-gap: 10px;
        grid-template-areas:
                "header"
                "advert"
                "content"
                "footer";
    }

    @media (min-width: 300px){
        .container{
            grid-template-columns: auto 1fr;
            grid-template-rows: auto 1fr auto;
            grid-template-areas:
                    "advert header"
                    "advert content"
                    "advert footer";
        }
    }

    
    @media (min-width: 400px) {
        
    }
</style>

<div class="container">
    <div class="header">header</div>
    <div class="advert">advert</div>
    <div class="content">content</div>
    <div class="footer">footer</div>
</div>	
```

# 语义化元素

HTML5 添加了诸如`main`、`header`、`footer`、`nav`、`article`、`section`等大量新标签，这些新标签为开发人员提供更多的选择和辅助特性。

默认情况下，浏览器呈现这些新标签的方式与`div`相似。然而，合理地使用它们，可以使你的标签更加的语义化。辅助技术（如：屏幕阅读器）可以通过这些标签为用户提供更加准确的、易于理解的页面信息。



`main`只应包含与页面中心主题相关的信息，而不应包含如导航连接、网页横幅等可以在多个页面中重复出现的内容。

`header`也是一个具有语义化的、提升页面可访问性的 HTML5 标签。它可以为父级标签呈现简介信息或者导航链接，适用于那些在多个页面顶部重复出现的内容。

`nav`也是一个具有语义化特性的 HTML5 标签，用于呈现页面中的主导航链接。

`section`用于对与主题相关的内容进行分组。如果一本书是一个`article`的话，那么每个章节就是`section`。也就是section可以包含多个article，一个article也可以包含多个section

`article`是一个分段标签，用于呈现独立及完整的内容。这个标签适用于博客入口、论坛帖子或者新闻文章。

audio元素表示音频内容

figure

```html
<figure>
  <img src="roundhouseDestruction.jpeg" alt="Photo of Camper Cat executing a roundhouse kick">
  <br>
  <figcaption>
    Master Camper Cat demonstrates proper form of a roundhouse kick.
  </figcaption>
</figure>
```

`label`标签用于呈现特定表单控件的文本，通常是选项的名称。这些文本代表了选项的含义，使表单具有更好的可读性。`label`标签的`for`属性指定了与`label`绑定的表单控件，并且屏幕阅读器也会读取`for`属性。

# 设计模式

 

## 掉落列模型

手机上每一个大块站一行，随着屏幕尺寸增加形成多个column列。随着屏幕缩小，列掉落

举例： 所有的列都垂直排列为一列 --> 第2个元素（列）和第一个并排显示 --> 不再扩大只是增加左右外边距

 

## 大体流动模型

 

举例： 所有的列都垂直排列为一列 --> 网格 --> 不再扩大只是增加左右外边距

 

```
        @media screen and (min-width: 700px) {
 
            width: 700px;
 
            margin-left: auto;
 
            margin-right: auto;
 
        }
```

 



默认order为0，设为-1则出现在最前面。 为了实现|=这样的布局，可以把两个div（也就是=）放到一个id为container2的div中。根据断点调整container2的宽度为50%

##  抽屉式设计

屏幕不够宽时，隐藏，可以通过按钮呼出

## 流行的设计

 

课程目录页面：左侧一个窄列、右侧一个宽列 ----============ 精选课程页面：四分 ----====----====

所有网站的网格都是12列，方便划分为2、3、4列

 

# 调试

## 验证器

[W3C HTML验证器](https://validator.w3.org/)

http://jigsaw.w3.org/css-validator/validator

对于一个大型的样式表，首先要通过这个服务来消除任何基本的语法错误，然后再依赖浏览器开发人员工具来确定其他问题。

## chrome开发工具远程调试安卓

**连接步骤** 

1. 手机设置为开发者模式（调试模式）
2. 数据线链接手机和电脑
3. 手机和电脑都打开chrome，电脑输入地址chrome://inspect

# 辅助工具

## 占位图服务

随机小动物  

`http://lorempixel.com/350/150/animals/`

 

# 图标

font-awesome

```
<div class="row">
    <div class="col-xs-4">
      <button class="btn btn-block btn-primary"><i class="fa fa-thumbs-up"></i> Like</button>
    </div>
    <div class="col-xs-4">
      <button class="btn btn-block btn-info"><i class="fa fa-info-circle"></i>Info</button>
    </div>
    <div class="col-xs-4">
      <button class="btn btn-block btn-danger"><i class="fa fa-trash"></i>Delete</button>
    </div>
  </div>
```

# 跨平台

本地把H5资源做成小网站

React Native 移动端 将H5打包到Native包里

Electron PC端

PWA谷歌） H5会比CDN更快推到手机端。Mpass也是

# 组件自动发现

eventbus

