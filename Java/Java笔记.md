# Java语言特点

- 面向对象
- 平台无关性
- 支持网络编程并且很方便

# JDK

JDK ：

-  Java Development Kit，它是功能齐全的 Java SDK
- jdk包含 JRE，还有编译器（javac）和工具（如 javadoc 和 jdb）。能够创建和编译程序。

JRE 是 Java 运行时环境。它是运行已编译 Java 程序所需的所有内容的集合，包括 Java 虚拟机（JVM），Java 类库，java 命令和其他的一些基础构件。但是，它不能用于创建新程序。

主类是 Java 程序执行的入口点。

# 推书

淘宝技术这十年
企业应用架构模式
Clean Architecture
面向模式的软件体系结构

# Guava

ImmutableMap.of 不可变集合

```java

```

# Lambda表达式

HeroChecker c3 = (Hero h) ->h.hp>100 && h.damage<50;

 把 参数类型和圆括号去掉(只有一个参数的时候，才可以去掉圆括号)



引用静态方法

TestLambda::testHero

引用对象方法

 testLambda::testHero

引用容器中对象的方法

Hero::matched

引用构造器

比如ArrayList::new，相当于()->new ArrayList()



# 方法引用

有些情况下，我们用Lambda表达式仅仅是调用一些已经存在的方法，除了调用动作外，没有其他任何多余的动作，在这种情况下，我们倾向于通过方法名来调用它。

举例，按年龄对多个Persion排序。

```java
//比较器
Arrays.sort(rosterAsArray, new PersonAgeComparator());
//lambda表达式
Arrays.sort(rosterAsArray, (x,y) -> x.age().compareTo(y.age()));
//按年龄比较两个人的方法如果已经定义，这里对lambda表达式简化
Arrays.sort(rosterAsArray, Person::compareByAge);
```

实例方法引用 this::

构造方法引用

```java
Supplier<List<User>> userSupplier = () -> new ArrayList<>();
List<User> user = userSupplier.get();
 
Supplier<List<User>> userSupplier2 = ArrayList<User>::new;    // 构造方法引用写法
List<User> user2 = userSupplier.get();
```

对象方法引用

```java
   BiPredicate<String,String> bp = (x, y) -> x.equals(y);
   BiPredicate<String,String> bp1 = String::equals;

   boolean test = bp1.test("xy", "xx");
   System.out.println(test);
```



#  函数式接口

定义：接口中只有一个抽象方法的接口

可以使用Lambda表达式来表示一个函数式接口的实现

如

```java
@FunctionalInterface
interface GreetingService 
{
    void sayMessage(String message);
}

GreetingService greetService1 = message -> System.out.println("Hello " + message);

Thread thread = new Thread(() -> System.out.println("Hello World"));
```

- java.util.function提供支持

  

## 接口的默认方法

Java 8使我们能够通过使用 `default` 关键字向接口添加非抽象方法实现。

## Consumer

表示只消费不返回。比如forEach(Consumer)

```java
void accept(T t);
```

## Function

Function 提供一种转换功能，将t转换为R。Function是最基础通用的

类似的有IntFunction、longFunction等等，只是t和R的参数类型不同。

```java
R apply(T t);
```

Stream.map用到了

```java
//参数泛型的必须是已接收的泛型的子类
<R> Stream<R> map(Function<? super T, ? extends R> mapper);
```

## Operator

表示运算。没有最基础的Operator

BinaryOperator二元操作

IntBinaryOperator int的二元操作

BinaryOperator（继承自BiFunction）和IntBinaryOperator（石头里蹦出来的）没有继承关系

## Supplier

Supplier不传入参数，返回一个值,这种结构很适合作为工厂来产生对象 

```java
Supplier<Student> supplier = () -> new Student();
Student student = supplier.get(); 
Student student2 = supplier.get();
System.out.println(student); //com.test.Student@6e8cf4c6
System.out.println(student2);//com.test.Student@12edcd21

//toCollection方法的入参就是一个supplier接口对象
Collectors.toCollection(JSONArray::new);
//generate方法入参是supplier接口对象
Stream.generate(()->2)
    .limit(10)
    .forEach(System.out::println);
```



## Optional类

[Optional 类](https://www.runoob.com/java/java8-optional-class.html)

提供NullObject的实现



对象的初始值是 null，使用orElse指定的默认值。

orElse 始终执行orElse内的方法。

orElseGet 对象为null才执行方法。

```java
        for (Future<Book> futureBook : futureBooks) {
            try {
                ret = Optional.ofNullable(futureBook.get(100, TimeUnit.MILLISECONDS));
            } catch (TimeoutException |InterruptedException|ExecutionException e) {
                continue;
            }
            if (ret.isPresent()) {
                break;
            }
        }
```

## Predicate

 Predicate断言、判断，对输入的数据根据某种标准进行评判，最终返回boolean值

```java
@FunctionalInterface
public interface Predicate<T> {

boolean test(T t);

default Predicate<T> and(Predicate<? super T> other) {
    Objects.requireNonNull(other);
    return (t) -> test(t) && other.test(t);
}

```

举例，Stream.filter

```java
Stream<T> filter(Predicate<? super T> predicate);
```

# Stream

 聚合操作，首先要建立Stream和管道的概念
Stream 和Collection结构化的数据不一样，Stream是一系列的元素，就像是生产线上的罐头一样，一串串的出来。

## 管道

管道指的是一系列的聚合操作。

管道分3个部分

- 管道源：在这个例子里，源是一个List
- 中间操作： 每个中间操作，又会返回一个Stream，比如.filter()又返回一个Stream, 中间操作是“懒”操作，并不会真正进行遍历。
- 结束操作：当这个操作执行后，流就被使用“光”了，无法再被操作。所以这必定是流的最后一个操作。  结束操作不会返回Stream，但是会返回int、float、String、 Collection。或者像forEach，什么都不返回,  结束操作才进行真正的遍历行为，在遍历的时候，才会去进行中间操作的相关判断  

中间操作有8种。

>1. collect 收集操作，将所有数据收集起来，这个操作非常重要，官方的提供的Collectors 提供了非常多收集器，可以说Stream 的核心在于Collectors。
>2. count 统计操作，统计最终的数据个数。
>3. findFirst、findAny 查找操作，查找第一个、查找任何一个 返回的类型为Optional。
>4. noneMatch、allMatch、anyMatch 匹配操作，数据流中是否存在符合条件的元素 返回值为bool 值。
>5. min、max 最值操作，需要自定义比较器，返回数据流中最大最小的值。
>6. reduce 规约操作，将整个数据流的值规约为一个值，count、min、max底层就是使用reduce。
>7. forEach、forEachOrdered 遍历操作，这里就是对最终的数据进行消费了。
>8. toArray 数组操作，将数据流的元素转换成数组。可以对IntStream使用

```java
//flatmap作用就是将元素拍平拍扁 ，将拍扁的元素重新组成Stream，并将这些Stream 串行合并成一条Stream
Stream.of("a-b-c-d","e-f-i-g-h")
                .flatMap(e->Stream.of(e.split("-")))
                .forEach(e->System.out.println(e));

//mapToInt 将数据流中得元素转成Int，这限定了转换的类型Int，最终产生的流为IntStream，及结果只能转化成int。
Stream.of("apple", "banana", "orange", "waltermaleon", "grape")
    .mapToInt(e -> e.length()) //转成int
    .forEach(e -> System.out.println(e));

//forEach不仅仅是是Stream 中得操作符还是各种集合中得一个语法糖
```

**IntStream**、**LongStream**、**DoubleStream**，这三个流实现了一些特有的操作符

终止操作

```java
package lambda;
  
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
 
import org.omg.Messaging.SYNC_WITH_TRANSPORT;
 
import charactor.Hero;
  
public class TestAggregate {
  
    public static void main(String[] args) {
        Random r = new Random();
        List<Hero> heros = new ArrayList<Hero>();
        for (int i = 0; i < 5; i++) {
            heros.add(new Hero("hero " + i, r.nextInt(1000), r.nextInt(100)));
        }
        System.out.println("遍历集合中的每个数据");
        heros
            .stream()
            .forEach(h->System.out.print(h));
        System.out.println("返回一个数组");
        Object[] hs= heros
            .stream()
            .toArray();
        System.out.println(Arrays.toString(hs));
        System.out.println("返回伤害最低的那个英雄");
        Hero minDamageHero =
        heros
            .stream()
            .min((h1,h2)->h1.damage-h2.damage)
            .get();
        System.out.print(minDamageHero);
        System.out.println("返回伤害最高的那个英雄");
 
        Hero mxnDamageHero =
                heros
                .stream()
                .max((h1,h2)->h1.damage-h2.damage)
                .get();
        System.out.print(mxnDamageHero);     
         
        System.out.println("流中数据的总数");
        long count = heros
                .stream()
                .count();
        System.out.println(count);
 
        System.out.println("第一个英雄");
        Hero firstHero =
                heros
                .stream()
                .findFirst()
                .get();
         
        System.out.println(firstHero);
         
    }
}
```

## 收集

https://www.jianshu.com/p/6ee7e4cd5314

Collectors.toCollection比较通用

Collectors.joining()，拼接

```java
JSONArray bankArr = queryRet.getJSONArray("bankList").stream().filter(i -> {
    JSONObject each = (JSONObject) i;
    return WenziUtil.containSpecialChar(each.getString("bankName"), "[a-zA-Z]");
}).collect(Collectors.toCollection(JSONArray::new));

Collectors.toList()
    
    
    public List<String> fizzBuzz(int n) {
        return IntStream.range(1, n + 1).mapToObj(i -> {
            if (i % 3 == 0 && i % 5 == 0) return "FizzBuzz";
            if (i % 3 == 0) return "Fizz";
            if (i % 5 == 0) return "Buzz";
            return String.valueOf(i);
        }).collect(Collectors.toList());
    }
```

## 格式转换

```java
// int[]转HashSet
Set<Integer> set = Arrays.stream(arcs).flatMapToInt(Arrays::stream)
  .collect(Collectors.toCollection(() -> new HashSet<>()));
// HashSet转int[]
int[] ret = intersectSet.stream().mapToInt(Number::intValue).toArray();

```

## 数组遍历

```java
Arrays.stream(T[]).forEach
```



# 基本类型

只有boolean和char是无符号数。

## double

float赋值给double会精度丢失

以下只是定义了一个无限接近34.37的小数34.36999999999...

```java
double yuan=Double.valueOf("34.37");
double yuan=34.37;
```

因此(long)Math.floor(yuan * 100)

## 字符

字符常量：

- 相当于一个整型值( ASCII 值),可以参加表达式运算
- 字符常量（**char**）只占 2 个字节; 字符串常量占若干个字节

## 字符串

>字符串变量共享问题
>只有字符串常量是共享的，而+和substring产生的结果不共享



**字符串转换其他类型**

new String(byte[], "UTF-8")

str.getBytes()

Double.valueOf(String)

String.valueOf(double)

**可变性**

String 类中使用 final 关键字修饰字符数组来保存字符串，`private final char value[]`，所以 String 对象是不可变的。

而 StringBuilder 与 StringBuffer 都继承自 AbstractStringBuilder 类，在 AbstractStringBuilder 中也是使用字符数组保存字符串`char[]value` 但是没有用 final 关键字修饰，所以这两种对象都是可变的。

**线程安全性**

String 对象是不可变的，线程安全。

StringBuffer 对方法加了同步锁或者对调用的方法加了同步锁，所以是线程安全的。

StringBuilder 并没有对方法进行加同步锁，所以是非线程安全的。

**性能**

每次对 String 类型进行改变的时候，都会生成一个新的 String 对象，然后将指针指向新的 String  对象。StringBuffer 每次都会对 StringBuffer 对象本身进行操作，而不是生成新的对象并改变对象引用。相同情况下使用  StringBuilder 相比使用 StringBuffer 仅能获得 10%~15% 左右的性能提升，但却要冒多线程不安全的风险。

**对于三者使用的总结：**

1. 操作少量的数据: 适用 String
2. 单线程操作字符串缓冲区下操作大量数据: 适用 StringBuilder
3. 多线程操作字符串缓冲区下操作大量数据: 适用 StringBuffer



# 集合框架

## List

 **Arraylist：** Object数组 

## Map

```java
map.forEach((k, v) -> System.out.println("key:value = " + k + ":" + v));

Map<Integer, String> map = new HashMap<Integer, String>() {
            {
                put(3, "fizz");
                put(5, "Buzz");
            }
        };
```

## Collections类

**排序操作**

```java
void reverse(List list)//反转
void shuffle(List list)//随机排序
void sort(List list)//按自然排序的升序排序
void sort(List list, Comparator c)//定制排序，由Comparator控制排序逻辑
void swap(List list, int i , int j)//交换两个索引位置的元素
void rotate(List list, int distance)//旋转。当distance为正数时，将list后distance个元素整体移到前面。当distance为负数时，将 list的前distance个元素整体移到后面。
```

 **查找,替换操作**

```java
int binarySearch(List list, Object key)//对List进行二分查找，返回索引，注意List必须是有序的
int max(Collection coll)//根据元素的自然顺序，返回最大的元素。 类比int min(Collection coll)
int max(Collection coll, Comparator c)//根据定制排序，返回最大元素，排序规则由Comparatator类控制。类比int min(Collection coll, Comparator c)
void fill(List list, Object obj)//用指定的元素代替指定list中的所有元素。
int frequency(Collection c, Object o)//统计元素出现次数
int indexOfSubList(List list, List target)//统计target在list中第一次出现的索引，找不到则返回-1，类比int lastIndexOfSubList(List source, list target).
```

Collections提供了多个`synchronizedXxx()`方法

还可以设置不可变集合

## Arrays类

1. 排序 : `sort()` 
2. 查找 : `binarySearch()` 
3. 比较: `equals()` 
4. 填充 : `fill()` 
5. 转列表:  `asList()` 
6. 转字符串 : `toString()` 
7. 复制: `copyOf()` 




## HashMap

 **底层数据结构：** JDK1.8 以后的 HashMap 在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为8）时，将链表转化为红黑树，以减少搜索时间 

**Null**: HashMap 中，null 可以作为键，这样的键只有一个，可以有一个或多个键所对应的值为 null。 

**源码阅读**

查找的核心逻辑是封装在 getNode 方法中。确定桶位置，其实现代码如下：

```java
first = tab[(n - 1) & hash]
```

位HashMap 中桶数组的大小 n总是2的幂，此时，`(n - 1) & hash` 等价于`hash % n`。



还有一个计算 hash 的方法。这个方法源码如下：

```java
/**
 * 计算键的 hash 值
 */
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

当我们覆写 hashCode 方法时，可能会写出分布性不佳的 hashCode 方法，进而导致 hash 的冲突率比较高。hash 高4位数据与低4位数据进行异或运算，即 `hash ^ (hash >>> 4)`。通过移位和异或运算，让高位数据与低位数据进行异或，以此加大低位信息的随机性，变相的让高位数据参与到计算中，可以让 hash 变得更复杂，进而影响 hash 的分布性。

键值hashcode相同的对象，会被放到同一个bucket里。hash定位bucket，equals查找这个对象。

> TreeMap、TreeSet以及JDK1.8之后的HashMap底层都用到了红黑树。红黑树就是为了解决二叉查找树的缺陷，因为二叉查找树在某些情况下会退化成一个线性结构。
**推荐阅读：**

- 《Java 8系列之重新认识HashMap》 ：https://zhuanlan.zhihu.com/p/21673805

## 底层数据结构总结

List

- **Arraylist：** Object数组
- **Vector：** Object数组
- **LinkedList：** 双向链表(JDK1.6之前为循环链表，JDK1.7取消了循环)

Set

- **HashSet（无序，唯一）:** 基于 HashMap 实现的，底层采用 HashMap 来保存元素
- **LinkedHashSet：** LinkedHashSet 继承于 HashSet，并且其内部是通过 LinkedHashMap 来实现的。有点类似于我们之前说的LinkedHashMap 其内部是基于 HashMap 实现一样，不过还是有一点点区别的
- **TreeSet（有序，唯一）：** 红黑树(自平衡的排序二叉树)

Map

- **HashMap：** JDK1.8之前HashMap由数组+链表组成的，数组是HashMap的主体，链表则是主要为了解决哈希冲突而存在的（“拉链法”解决冲突）。JDK1.8以后在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为8）时，将链表转化为红黑树，以减少搜索时间
- **LinkedHashMap：** LinkedHashMap 继承自  HashMap，所以它的底层仍然是基于拉链式散列结构即由数组和链表或红黑树组成。另外，LinkedHashMap  在上面结构的基础上，增加了一条双向链表，使得上面的结构可以保持键值对的插入顺序。同时通过对链表进行相应的操作，实现了访问顺序相关逻辑。详细可以查看：[《LinkedHashMap 源码详细分析（JDK1.8）》](https://www.imooc.com/article/22931)
- **Hashtable：** 数组+链表组成的，数组是 HashMap 的主体，链表则是主要为了解决哈希冲突而存在的
- **TreeMap：** 红黑树（自平衡的排序二叉树）

来源: JavaGuide文章作者: SnailClimb文章链接: 

## 排序

- comparable接口实际上是出自java.lang包 它有一个 `compareTo(Object obj)`方法用来排序
- comparator接口实际上是出自 java.util 包它有一个`compare(Object obj1, Object obj2)`方法用来排序

Comparable 和 Comparator都可以使用Collections.sort() 和  Arrays.sort()来进行排序

**Comparable 和 Comparator 的对比**

1、Comparable 更像是自然排序

2、Comparator 更像是定制排序

**同时存在时采用 Comparator（定制排序）的规则进行比较。**

对于一些普通的数据类型（比如 String, Integer, Double…），它们默认实现了Comparable 接口，实现了 compareTo 方法，我们可以直接使用。

而对于一些自定义类，它们可能在不同情况下需要实现不同的比较策略，我们可以新创建 Comparator 接口，然后使用特定的 Comparator 实现进行比较。


# 函数

函数传参有两种方式，基本类型是值传递，对象是引用传递。

值传递：基本类型和引用作参数，都是拷贝

子类对象转换为Object类型后，可以通过反射调用子类方法。

获取对当前方法调用方的方法名

```java
StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
String methodName = stackTrace[2].getMethodName();
```



# 反射

JAVA 反射机制是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为 java 语言的反射机制。

应用场景：

1. 我们在使用 JDBC 连接数据库时使用 `Class.forName()`通过反射加载数据库的驱动程序；
2. Spring 框架的 IOC（动态加载管理 Bean）创建对象以及 AOP（动态代理）功能都和反射有联系；
3. Mybatis、logback等配置文件中定义对象信息
4. 动态配置实例的属性；

1. 获取Class对象
2. 获取类成员
3. 操作类成员



## 示例

```java
package cn.javaguide;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, IllegalAccessException, InstantiationException, InvocationTargetException, NoSuchFieldException {
        /**
         * 获取TargetObject类的Class对象并且创建TargetObject类实例
         */
        Class<?> tagetClass = Class.forName("cn.javaguide.TargetObject");
        TargetObject targetObject = (TargetObject) tagetClass.newInstance();
        /**
         * 获取所有类中所有定义的方法
         */
        Method[] methods = tagetClass.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println(method.getName());
        }
        /**
         * 获取指定方法并调用
         */
        Method publicMethod = tagetClass.getDeclaredMethod("publicMethod",
                String.class);

        publicMethod.invoke(targetObject, "JavaGuide");
        /**
         * 获取指定参数并对参数进行修改
         */
        Field field = tagetClass.getDeclaredField("value");
        //为了对类中的参数进行修改我们取消安全检查
        field.setAccessible(true);
        field.set(targetObject, "JavaGuide");
        /**
         * 调用 private 方法
         */
        Method privateMethod = tagetClass.getDeclaredMethod("privateMethod");
        //为了调用private方法我们取消安全检查
        privateMethod.setAccessible(true);
        privateMethod.invoke(targetObject);
    }
}
```

## 获取Class对象

- Class.forName;
- obj.getClass();
- 类名.class
- 数组类型，如int[].class

## 获取类成员

```java
xxClass.newInstance() 使用该类型默认构造函数构造实例
xxClass.isInstance(Object)
Array.newInstance(Class, int) 构造该类型的数组
getFields()/getConstructor/getConstructors()/getMethods() 访问该类成员。带Delared的会返回自身所有的（包括私有），不带Delared的会返回自己和所有父类public成员
```

获取构造器后，可以通过constructor.newInstance构造实例对象

```java
Constructor<?> constructor = classObj.getConstructor(new Class[] { TProtocol.class });
Object obj = constructor.newInstance(new Object[] { protocol });
```
## 操作类成员

- 使用Constructor/Field/Method.setAccessible(true) 绕开限制
- 使用Constructor.newInstance(Object[])来生成该类实例
- 使用Field.get/set(Obj) 
- 使用Method.invoke(Obj, object[])来调用方法

## 获取类上的注解对象

```java
ThriftServer thriftAnnotation = actualClazz.getAnnotation(ThriftServer.class);
```

## 获取实现接口及其外部类

```java
interfaceClazz = actualClazz.getInterfaces()[0];
serviceName = interfaceClazz.getEnclosingClass().getSimpleName();
```



## 获取clazz的类名

非数组一般用getName获取全名。

```shell
getName            
普通类 com.test.TestClass
内部类 com.test.TestClass$TestInnerClass
内部类数组 [Lcom.test.TestClass$TestInnerClass;
getCanonicalName   com.test.TestClass

getCanonicalName   
普通类 com.test.TestClass
内部类 com.test.TestClass.TestInnerClass
内部类数组 com.test.TestClass.TestInnerClass[]

getSimpleName
普通类 TestClass
内部类 TestInnerClass
内部类数组 TestInnerClass[]         

```

## 获得泛型类的真实类型

```java
// 获取当前new的对象的泛型的父类类型
ParameterizedType pt = (ParameterizedType) this.getClass().getGenericSuperclass();
// 获取第一个类型参数的真实类型
Class<T> serviceClazz = (Class<T>) pt.getActualTypeArguments()[0];
```

## 方法名查找Method

```java
Method[] ms = clazz.getDeclaredMethods();
for (Method m : ms) {
    if (methodName.equals(m.getName())) {
        return m;
    }
}

ThriftReturn thriftReturn = (ThriftReturn) method.invoke(proxy, args);
```

# 动态代理

```java
public class Test {
  static interface Subject{
    void sayHi();
    void sayHello();
  }
   
  static class SubjectImpl implements Subject{
 
    @Override
    public void sayHi() {
      System.out.println("hi");
    }
 
    @Override
    public void sayHello() {
      System.out.println("hello");
    }
  }
   
  static class ProxyInvocationHandler implements InvocationHandler{
    private Subject target;
    public ProxyInvocationHandler(Subject target) {
      this.target=target;
    }
 
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
      System.out.print("say:");
      return method.invoke(target, args);
    }
     
  }
   
  public static void main(String[] args) {
    Subject subject=new SubjectImpl();
    Subject subjectProxy=(Subject) Proxy.newProxyInstance(subject.getClass().getClassLoader(), subject.getClass().getInterfaces(), new ProxyInvocationHandler(subject));
    subjectProxy.sayHi();
    subjectProxy.sayHello();
     
  }
}
```

执行结果

```shell
say:hi
say:hello
```



# 泛型

## 模板方法

返回值是泛型，可以自动把object（比如反射调用得到的结果）强制转换为T类型。

```java
  public <T> T readData(String path)
  {
    return readData(path, false);
  }
```



## 模板类

## 泛型擦除

在泛型类被类型擦除的时候，之前泛型类中的类型参数部分如果没有指定上限，如 `<T>`则会被转译成普通的 Object 类型，如果指定了上限如 `<T extends String>`则类型参数就被替换成类型上限。

静态泛型方法不能使用类上定义的泛型T。



举例，mybatis通用Enum转换器：

所有的枚举都继承自java.lang.Enum类。由于Java 不支持多继承，所以枚举对象不能再继承其他类 ，只能实现一个通用接口来定义Enum通用格式。

```java
public interface BaseEnum<E extends Enum<?>, T> {
    public T getCode();
    public String getDisplayName();
}
```
再定义具体的Enum类

```
public enum OrderTypeEnum implements BaseEnum<OrderTypeEnum, Integer> {
 
    /**
     * {@value} 所有类型订单
     */
    ORDER_TYPE_ALL(0, "所有类型订单"),
 
    /**
     * {@value} 机票订单
     */
    ORDER_TYPE_FLIGHT(1, "机票订单"),
    /**
     * {@value} 酒店订单
     */
    ORDER_TYPE_HOTEL(2, "酒店订单");
 
    static Map<Integer,OrderTypeEnum> enumMap=new HashMap<>();
    static{
        for(OrderTypeEnum type:OrderTypeEnum.values()){
            enumMap.put(type.getCode(), type);
        }
    }
 
    private int code;
    private String displayName;
 
    private OrderTypeEnum(int code, String displayName) {
        this.code = code;
        this.displayName = displayName;
    }
 
    public static OrderTypeEnum getEnum(int code) {
        return enumMap.get(code);
    }
 
    public void setCode(int code) {
        this.code = code;
    }
 
    @Override
    public Integer getCode() {
        return this.code;
    }
 
    @Override
    public String getDisplayName() {
        return displayName;
    }
 
    public void setDisplayName(String displayName) {
        this.displayName = displayName;
    }
}
```
定义mybatis通用类型转换器
```java
 
public class UniversalEnumTypeHandler<E extends BaseEnum> extends BaseTypeHandler<E>{
    private Class<E> type;
    private E [] enums;
 
    /**
     * 设置配置文件设置的转换类以及枚举类内容，供其他方法更便捷高效的实现
     * @param type 配置文件中设置的转换类
     */
    public UniversalEnumTypeHandler(Class<E> type) {
        if (type == null) {
            throw new IllegalArgumentException("Type argument cannot be null");
        }
        this.type = type;
        this.enums = type.getEnumConstants();
        if (this.enums == null) {
            throw new IllegalArgumentException(type.getSimpleName()
                    + " does not represent an enum type.");
        }
    }
 
    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, E parameter,
                                    JdbcType jdbcType) throws SQLException {
        //BaseTypeHandler已经帮我们做了parameter的null判断
        ps.setObject(i, parameter.getCode(), jdbcType.TYPE_CODE);
    }
 
    @Override
    public E getNullableResult(ResultSet rs, String columnName)
            throws SQLException {
        // 根据数据库存储类型决定获取类型，本例子中数据库中存放String类型
        Integer i = rs.getInt(columnName);
        if (rs.wasNull()) {
            return null;
        } else {
            // 根据数据库中的value值，定位Enum子类
            return locateEnumStatus(i);
        }
    }
 
    @Override
    public E getNullableResult(ResultSet rs, int columnIndex)
            throws SQLException {
        // 根据数据库存储类型决定获取类型，本例子中数据库中存放int类型
        Integer i = rs.getInt(columnIndex);
        if (rs.wasNull()) {
            return null;
        } else {
            // 根据数据库中的value值，定位PersonType子类
            return locateEnumStatus(i);
        }
    }
 
    @Override
    public E getNullableResult(CallableStatement cs, int columnIndex)
            throws SQLException {
        // 根据数据库存储类型决定获取类型，本例子中数据库中存放String类型
        Integer i = cs.getInt(columnIndex);
        if (cs.wasNull()) {
            return null;
        } else {
            // 根据数据库中的value值，定位PersonType子类
            return locateEnumStatus(i);
        }
    }
 
    /**
     * 枚举类型转换，由于构造函数获取了枚举的子类enums，让遍历更加高效快捷
     * @param value 数据库中存储的自定义value属性
     * @return value对应的枚举类
     */
    private E locateEnumStatus(int value) {
        for(E e : enums) {
            if(e.getCode().equals(value)) {
                return e;
            }
        }
        throw new IllegalArgumentException("未知的枚举类型：" + value + ",请核对" + type.getSimpleName());
    }
}
```

# 日期处理
P99
表示日历的类GregorianCalendar
获得当前日历：` GregorianCalendar d = new GregorianCalendar();`
获得日期中的日:`d.get(Calendar.DAY_OF_MONTH)`
获得日期中的月:`d.get(Calendar.MONTH)`

获得日期中的年:`d.get(Calendar.YEAR)`

设置日:`d.set(Calendar.DAY_OF_MONTH, 1);`
获得日历日期中的星期几对应的int值，1代表星期日，6为周五，7代表周六：


    // 得到的weekday和Calendar.SUNDAY，MONDAY等值相同
     int weekday = d.get(Calendar.DAY_OF_WEEK);
获得当地地区星期的起始日:
`int firstDayOfWeek = d.getFirstDayOWeek()`
获得星期几的名称：


     String[] weekdayNames = new DateFormatSymbols().getShortWeekdays();
     weekdayNames[Calendar.SUNDAY]或 weekdayNames[Calendar.SUNDAY]

 表示时间点的类 Date（UTC时间）
Calendar类的getTime和setTime用来和Date类相互转换

 

# 面向对象

## 构造器

一个类没有定义任何构造器，编译器才会自动添加一个无参构造器。

子类的构造器需要调用父类的构造器：

1. 如果父类存在无参构造器，子类自动添加对它的调用（隐式）
2. 如果父类没有无参构造器，子类必须显式调用父类构造器，否则编译错误

##  静态方法

>1. 不能操作对象，也就是方法中不能有this参数（this参数是非静态方法的隐式参数）
>2. 可以访问自身类中的静态域

##  final域

final 关键字主要用在三个地方：变量、方法、类。

1. 对于一个 final 变量，如果是基本数据类型的变量，则其数值一旦在初始化之后便不能更改；如果是引用类型的变量，则在对其初始化之后便不能再让其指向另一个对象。
2. 当用 final 修饰一个类时，表明这个类不能被继承。final 类中的所有成员方法都会被隐式地指定为 final 方法。
3. 使用 final 方法的原因有两个。第一个原因是把方法锁定，以防任何继承类修改它的含义；第二个原因是效率。在早期的 Java  实现版本中，会将 final 方法转为内嵌调用。但是如果方法过于庞大，可能看不到内嵌调用带来的任何性能提升（现在的 Java 版本已经不需要使用  final 方法进行这些优化了）。类中所有的 private 方法都隐式地指定为 final。

final一般和基本类型、不可变类的域配合使用，如String。

公有常量（final域)

> System.out是system类的final域，
> 而setOut是本地方法，绕过了java来修改out

## 不可变类型

不可变类型包括 String、BigDecimal以及包装器类型。


##  抽象类和子类
P164
抽象类是至少包含一个抽象方法的类。特点：

- 子类如果不定义全部的抽象方法，那么也是抽象类。
- 从设计层面来说，抽象是对类的抽象，是一种模板设计，而接口是对行为的抽象，是一种行为的规范


##  对象判同
P160
Object类的equals方法判断引用是否相等，没实际意义。子类中需要重定义equals函数，详见P170

1. 判同
2. 测other Obj是否为null
3. 测other Obj类型是否和this对象相同
4. 类型转换，判断值是否相同，注意字符串可能为空

##  内部类
成员内部类：
内部类只是类之间的关系，而不是对象的嵌套。

内部类也是外部类的一个成员。

在外部类中初始化内部类对象时，隐含的参数是创建它的外围类对象的this引用。因此内部类可以直接引用外部类对象的数据域（outer.beep)。
明确的构造内部对象：

```java
outerObject.new InnerClass(construction parameters) 
    
    public static void main(String[] args){
  　　 Outer outer = new Outer();
  　　outer.show();
    //实例化内部类
  　　Outer.Inner inner = outer.new Inner();
  　　inner.show();
　　}
```



在实例化成员内部类时，成员内部类会持有一个外部类当前对象的引用，这样在成员内部类中就可以直接访问外部类的成员，即使是private修饰的


查看内部类.class
```
>> javap -private  TalkingClock$TimePrinter
>>output:
public class TalkingClock$TimePrinter implements java.awt.event.ActionListener {
 
 
  final TalkingClock this$0;
  public TalkingClock$TimePrinter(TalkingClock);
  public void actionPerformed(java.awt.event.ActionEvent);
}
查看外围类.class
 
>> javap -private  TalkingClock
Compiled from "TalkingClock.java"
public class TalkingClock {
  private boolean beep;
  private int interval;
  public TalkingClock(int, boolean);
  public void start();
  static boolean access$0(TalkingClock);
}
```

局部类：
局部变量会在局部类中备份为final变量（数据域)，所以局部方法即使释放也能使用该变量。
局部类对象也会构造外围类对象的引用，存储在一个final数据域中。
局部类的方法只能引用final的局部变量（拷贝），所以最好将外围类的方法参数声明为final，和局部类建立的拷贝一致。
静态内部类：内部类不需要访问外围类对象时，使用。接口中的内部类自动为static和public

内部类的应用 对同一个包的其他类隐藏，同时内部可以声明为public。外围类之外Outter.innerClass
内部类可以访问创建它的外围类对象的数据域
局部类完全隐藏，只有该方法能访问 静态内部类不引用外围类对象的数据成员

## 解析包名

在基目录使用javac编译，java执行，这样才能正确解析java文件中的包名

## 工厂方法

工厂方法和构造器的区别：

1. 可以产生不同子类对象
   T a = T.getInstance();

   a对象实际是T的子类

2. 工厂可以是接口或抽象类，面向接口编程

## 重载

不可以实现重载的情况：

- 仅抛出不同类型的异常
- 仅改变方法的返回值类型

## Override

满足重写的条件和规则：

- 不能缩小访问级别。比如public不能变private
- 参数列表、返回类型必须与被重写方法的相同
- 重写方法不能声明新的检查异常或者更广的检查异常。但是可以抛出更少，更有限或者不抛出异常。

# Java-Web

## web.xml

context-param配置key-value键值对，启动前可供配置的listener使用。


# 代码风格
---
## 变量命名
规则的优点：

- 规矩
- 提供额外信息。比如局部数据、类数据、全局数据、类型信息
- 强调变量之间的关系，比如employeeAddress， employeeName
- 任何一项规则都好于没有规则

## 限定词

Total、Sum等限定词放在最后

num放在开头代表总数，但最好用count
num放在结尾代表一个下标

## 长度

长度要正好

太长：numberOfPeopleOnTheUsOlympicTeam  numberOfSeatInTheStadium
长度正好：numTeamMembers numSeatsInStadium
recordCount
eventIndex

 


状态标记用enum、具名常量和全局变量

布尔变量名
典型有用的：done、success、error、found、ok
最好能更具体：processingComplete
只使用肯定的布尔变量名，notFound很难阅读

 

 

# 循环
尽量使用带退出的循环(break)==>减少重复代码，方便以后修改
for循环：无需在循环内部控制它
foreach循环：消除循环控制算术
while：无限循环，或只在某一事件发生才终止的循环
while循环更适用，不要用for循环填充循环头

# 日期时间处理

字符串日期时间转util.Date

```
        String string = "2016-10-24 21:59:06";
 
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
 
        System.out.println(sdf.parse(string));
 
```

Calendar设置时间后转Date、unix时间戳

```
Date date=new Date();//取时间
 
Calendar calendar = new GregorianCalendar();
 
calendar.setTime(date);
 
calendar.add(calendar.DATE,1);//把日期往后增加一天.整数往后推,负数往前移动
 
date=calendar.getTime(); //这个时间就是日期往后推一天的结果
long unixTimestamp = date.getTime()/1000;
```

Date转字符串

```
SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
 
String dateString = formatter.format(date);
System.out.println(dateString);
 
```

# 表驱动

```java
Map<MessageId, MessageFieldDescription> messageMap;
Map<String,AbstractField> fieldTypeMap;           存储field类型与 AbstractField子类的映射
class AbstractField

{
    public void ReadAndPrint（String，File）；//读取变量

}

```





MessageFieldDescription可以是一个记录，表，Map结构
用于存放一种消息的field结构：
field1 float，‘Average Temperature’
field2 integer，‘Number of Samplers’
比如Map<String, Pair<String,String>>

1. 由messageId得到消息结构描述记录（表）messageStructure
2. 遍历 messageStructure中每个field，由field得到fieldType，fieldName
3. fieldTypeMap [ fieldType].  ReadAndPrint(fieldName, file)读取消息文件中的消息

# 


构造查询表键值问题
- 转换键，因为一些数据具有同样的value，比如某个年龄段的人具有相同value


索引访问表
- 构造索引表，由基本数据查出键。可以使用HashMap
- 可以使用多个索引表——一个主查询表。比如：
主查询表 含有员工姓名、雇用日期、薪水的表
索引表1 按员工姓名访问主表
索引表2 按薪水访问主表

- 将借助索引表访问数据的代码提取成单独的子程序


阶梯访问表
- 将每一区间的上限写入一张表里
- 将等级字符串也写入一张表
- 写一个循环按照各区间的上限检查分数。当分数第一次小于某区间上限时，则确定等级
- 当列表很大时，考虑准二分查找来确定等级，替代顺序查找。

 


程序中的0和1不一定代表布尔值
采用true，false做布尔判断，而不是 x==0 x==1

# 异常

## Java异常体系

Throwable 

-- Exception -- RuntimeException

-- Error

​			

**未检查异常**

包括派生于Error和RuntimeException类的所有异常

RumtimeException类的异常也可以被抛出和捕获

**已检查异常**

需要被捕获处理

## 捕获异常

- **try 块：** 用于捕获异常。其后可接零个或多个 catch 块，如果没有 catch 块，则必须跟一个 finally 块。
- **catch 块：** 用于处理 try 捕获到的异常。
- **finally 块：** 无论是否捕获或处理异常，finally 块里的语句都会被执行。当在 try 块或 catch 块中遇到 return 语句时，finally 语句块将在方法返回之前被执行。

**在以下 4 种特殊情况下，finally 块不会被执行：**

1. 在 finally 语句块第一行发生了异常。 因为在其他行，finally 块还是会得到执行
2. 在前面的代码中用了 System.exit(int)已退出程序。 exit 是带参函数 ；若该语句在异常语句之后，finally 会执行
3. 程序所在的线程死亡。
4. 关闭 CPU。

**注意：** 当 try 语句和 finally 语句中都有 return 语句时，在方法返回之前，finally 语句的内容将被执行，并且 finally 语句的返回值将会覆盖原始的返回值。

## 异常转译

异常链也是转译的一种

## 方法的失败原子性

在修改对象状态前，先进行计算、检查参数状态，再修改。比如pop前判断size==0，true则抛出EmptyStack异常。
或者在拷贝上执行操作，完成后用结果代替对象内容。

# IO

## 概述

流是一组有顺序的，有起点和终点的字节集合，是对数据传输的总称或抽象。

- 按照流的流向分，可以分为输入流和输出流
- 按照操作单元划分，可以划分为字节流和字符流；
- 按照流的角色划分为节点流和处理流。按照流是否直接与特定的地方(如磁盘、内存、设备等)相连

 Java I0 流的 40 多个类都是从如下 4 个抽象类基类中派生出来的。

- InputStream/Reader: 所有的输入流的基类，前者是字节输入流，后者是字符输入流。
- OutputStream/Writer: 所有输出流的基类，前者是字节输出流，后者是字符输出流。

字节流与字符流：

字符流的由来： 因为数据编码的不同，而有了对字符进行高效操作的流对象。本质其实就是基于字节流读取时，去查了指定的码表。 字节流和字符流的区别：

读写单位不同：字节流以字节（8bit）为单位，字符流以字符为单位，根据码表映射字符，一次可能读多个字节。

处理对象不同：字节流能处理所有类型的数据（如图片、avi等），而字符流只能处理字符类型的数据。

结论：只要是处理纯文本数据，就优先考虑使用字符流。除此之外都使用字节流。



## 读写文件

```java
// fileClasspath以/开头，类路径
Resource resource = new ClassPathResource(fileClasspath);

//如果是用classLoader读取类路径下文件，不加"/"
```

## 键盘输入

方法 1：通过 Scanner

```java
Scanner input = new Scanner(System.in);
String s  = input.nextLine();
input.close();
```

方法 2：通过 BufferedReader

```java
BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
String s = input.readLine();
```

## 缓存流

字节流，字符流每次read都访问硬盘。

缓存流在读取的时候，会一次性读较多的数据到缓存中，以后每一次的读取，都是在缓存中访问，直到缓存中的数据读取完毕，再到硬盘中读取。



缓存字符输入流 BufferedReader 可以一次读取一行数据

```java
    File f = new File("d:/lol.txt");
    // 创建文件字符流
    // 缓存流必须建立在一个存在的流的基础上
    try (
            FileReader fr = new FileReader(f);
            BufferedReader br = new BufferedReader(fr);
        )
    {
        while (true) {
            // 一次读一行·
            String line = br.readLine();
            if (null == line)
                break;
            System.out.println(line);
        }
    } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }
```
PrintWriter 缓存字符输出流， 可以一次写出一行数据

```java
    File f = new File("d:/lol2.txt");
      
    try (
            // 创建文件字符流
//                FileWriter fw = new FileWriter(f);
                OutputStream fw = new FileOutputStream(f);
                // 缓存流必须建立在一个存在的流的基础上
                PrintWriter pw = new PrintWriter(fw);             
    ) {
        pw.println("garen kill teemo");
        pw.println("teemo revive after 1 minutes");
        pw.println("teemo try to garen, but killed again");
    } catch (IOException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
    }			
```
## 库

commons-io库提供通用读写文件、文本方法

Spring ClassPathResource方便根据类路径获取File、绝对路径

## 文件分割

```java
/**
     * 拆分文件
     * @param fileName 待拆分的完整文件名
     * @param byteSize 按多少字节大小拆分
     * @return 拆分后的文件名列表
     * @throws IOException
     */
    public List<String> splitBySize(String fileName, int byteSize)
            throws IOException {
        List<String> parts = new ArrayList<String>();
        File file = new File(fileName);
        int count = (int) Math.ceil(file.length() / (double) byteSize);
        int countLen = (count + "").length();
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(count,
                count * 3, 1, TimeUnit.SECONDS,
                new ArrayBlockingQueue<Runnable>(count * 2));

        for (int i = 0; i < count; i++) {
            String partFileName = file.getName() + "."
                    + leftPad((i + 1) + "", countLen, '0') + ".part";
            threadPool.execute(new SplitRunnable(byteSize, i * byteSize,
                    partFileName, file));
            parts.add(partFileName);
        }
        return parts;
    }

/**
     * 合并文件
     * 
     * @param dirPath 拆分文件所在目录名
     * @param partFileSuffix 拆分文件后缀名
     * @param partFileSize 拆分文件的字节数大小
     * @param mergeFileName 合并后的文件名
     * @throws IOException
     */
    public void mergePartFiles(String dirPath, String partFileSuffix,
            int partFileSize, String mergeFileName) throws IOException {
        ArrayList<File> partFiles = FileUtil.getDirFiles(dirPath,
                partFileSuffix);
        Collections.sort(partFiles, new FileComparator());

        RandomAccessFile randomAccessFile = new RandomAccessFile(mergeFileName,
                "rw");
        randomAccessFile.setLength(partFileSize * (partFiles.size() - 1)
                + partFiles.get(partFiles.size() - 1).length());
        randomAccessFile.close();

        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(
                partFiles.size(), partFiles.size() * 3, 1, TimeUnit.SECONDS,
                new ArrayBlockingQueue<Runnable>(partFiles.size() * 2));

        for (int i = 0; i < partFiles.size(); i++) {
            threadPool.execute(new MergeRunnable(i * partFileSize,
                    mergeFileName, partFiles.get(i)));
        }

    }
```



/**
     * 拆分文件
     * @param fileName 待拆分的完整文件名
     * @param byteSize 按多少字节大小拆分
     * @return 拆分后的文件名列表
     * @throws IOException
     */
    public List<String> splitBySize(String fileName, int byteSize)
            throws IOException {
        List<String> parts = new ArrayList<String>();
        File file = new File(fileName);
        int count = (int) Math.ceil(file.length() / (double) byteSize);
        int countLen = (count + "").length();
        ThreadPoolExecutor threadPool = new ThreadPoolExecutor(count,
                count * 3, 1, TimeUnit.SECONDS,
                new ArrayBlockingQueue<Runnable>(count * 2));

        for (int i = 0; i < count; i++) {
            String partFileName = file.getName() + "."
                    + leftPad((i + 1) + "", countLen, '0') + ".part";
            threadPool.execute(new SplitRunnable(byteSize, i * byteSize,
                    partFileName, file));
            parts.add(partFileName);
        }
        return parts;
    }
# MVC

## Spring


# 迭代器
Iterator相当于指向两个元素之间。
初始化迭代器list.Iterator()返回的迭代器在第0个元素之前（和指针的概念不同，指针是直接指向元素），此时iterator.next()返回的是 第0个元素

# JNI

 Java Native Interface 提供了若干的[API](https://baike.baidu.com/item/API/10154)实现了Java和其他语言的通信 



java系统属性java.library.path设置了加载库时搜索的路径列表，默认如下

- Windows 10/Oracle JDK 8: `java.library.path=%PATH%;.`
- Linux CentOS 7/Open JDK 8: `java.library.path=$LD_LIBRARY_PATH:/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib`

库文件无法正常加载有几种可能：

- 该库文件依赖的库找不到

 ldd命令查看需要加载的库以及其依赖信息 `ldd xxx.so`

 **ls -l /lib64/libc.so.6** 查看包含软连接，确认库文件版本是否正确。有时无法正常加载库文件

# JVM

## 概述

## 内存结构

对象存在于堆内存，局部变量（引用和基本类型变量）则存在于栈内存

**线程私有的：**

- 程序计数器。
- 虚拟机栈
- 本地方法栈

**线程共享的：**

- 堆
- 方法区
- 直接内存

### 程序计数器

 程序计数器主要有下面两个作用：

1. 字节码解释器通过改变程序计数器来依次读取指令，从而实现代码的流程控制，如：顺序执行、选择、循环、异常处理。
2. 在多线程的情况下，程序计数器用于记录当前线程执行的位置，从而当线程被切换回来的时候能够知道该线程上次运行到哪儿了。

程序计数器私有主要是为了**线程切换后能恢复到正确的执行位置**。

### 虚拟机栈和本地方法栈

区别：虚拟机栈为虚拟机执行 Java 方法 （也就是字节码）服务，而本地方法栈则为虚拟机使用到的 Native 方法服务 

堆，用来动态生成内存，存放new出来的东西。注意创建出来的对象只包含属于各自的成员变量，并不包括成员方法。因为同一个类的对象拥有各自的成员变量，存储在各自的堆中，但是他们共享该类的方法，并不是每创建一个对象就把成员方法复制一次。

### 方法区

在 JDK 1.8中移除整个永久代，取而代之的是一个叫元空间（Metaspace）的区域（永久代使用的是JVM的堆内存空间，而元空间使用的是物理内存，直接受到本机的物理内存限制。

主要用于存放已被加载的类信息、静态变量、即时编译器编译后的代码等数据。

JDK8里的Metaspace，可以通过参数-XX:MetaspaceSize
和-XX:MaxMetaspaceSize设定大小，但如果不指定MaxMetaspaceSize的话，Metaspace的大小仅受限于native memory的剩余大小

类的元数据可以在本地内存(native memory)之外分配,所以其最大可利用空间是整个系统内存的可用空间。这样，你将不再会遇到OOM错误，溢出的内存会涌入到交换空间

### 运行时常量池

JDK1.7及之后版本的 JVM 已经将运行时常量池从方法区中移了出来，在 Java 堆（Heap）中开辟了一块区域存放运行时常量池。

Java 基本类型的包装类的大部分都实现了常量池技术，即Byte,Short,Integer,Long,Character,Boolean；这5种包装类默认创建了数值[-128，127]的相应类型的缓存数据，但是超出此范围仍然会去创建新的对象。

局部变量区

- 存储局部变量、this指针、方法参数。
- long和double占用两个数组单元存储，其他基本类型一个单元。64位HotSpot中，一个单元是8个字节。
- 注意，堆中的字段大小和类型相符，byte一个字节，char两个字节。-1（0xFFFFFFFF）存储到char中，高2个字节会被截取掉，变为0xFFFF。

## 代码运行方式

1. java代码编译为.class字节码
2. 虚拟机加载class文件，java类存放于方法区（线程共享）
3. 运行时，hotSpot虚拟机混合解释编译+即时编译，翻译字节码成机器码后执行
4. 对于热点代码，编译成机器码执行。对于不常用代码，一行行解释执行
5. 变量存储于栈帧的局部变量区和堆中，执行方法时把变量都加载到栈帧的操作数栈。高位会扩展0或1，变成int

也就是java程序启动时才会编译为机器码，因此运行时信息可以被即时编译器利用，相比c++的静态编译可能会提高性能。



约束变量取值范围，靠java静态编译器。字节码修改后可以超出范围。

## class文件

### magic number

每个 Class 文件的前四个字节叫做magic字段，用来告诉JVM这是个class文件

```java
u4             magic; //Class 文件的标志
```

### Class 文件版本

之后的两个字节是minor版本号，再之后的两个字节是major版本号，我们看到是33（0033）,大端存储。

```java
    u2             minor_version;//Class 的小版本号
    u2             major_version;//Class 的大版本号
```


十六进制 

JDK1.5      31

JDK1.6      32

JDK1.7      33

JDK8        34

高版本的 Java 虚拟机可以执行低版本编译器生成的 Class 文件，但是低版本的 Java 虚拟机不能执行高版本编译器生成的 Class 文件。所以，我们在实际开发的时候要确保开发的的 JDK 版本和生产环境的 JDK 版本保持一致。 

## 类加载

![](img\类的生命周期.png)

### 加载

类加载过程的第一步，主要完成下面3件事情：

1. 通过全类名获取定义此类的二进制字节流
2. 将字节流所代表的静态存储结构转换为方法区的运行时数据结构
3. 在内存中生成一个代表该类的 Class 对象,作为方法区这些数据的访问入口

对于非数组类的加载阶段，我们可以去完成还可以自定义类加载器去控制字节流的获取方式（重写一个类加载器的 loadClass() 方法）。

数组类型不通过类加载器创建，它由 Java 虚拟机直接创建。

 加载阶段和连接阶段的部分内容是交叉进行的，加载阶段尚未结束，连接阶段可能就已经开始了。 



### 链接

分为验证、准备、解析三个阶段。

准备：为类的静态字段分配内存，并设置类变量默认值。对于final字段，此阶段完成赋值。

解析：将常量池内的符号引用 引用解析为实际引用（如果类未加载，会触发加载）。

链接过程中不一定完成解析，执行字节码前完成符号解析即可。



### 初始化

初始化是类加载的最后一步，也是真正执行类中定义的 Java 程序代码(字节码)，初始化阶段是执行类构造器 ` ()`方法的过程。

对于 `clinit` 方法的调用，虚拟机会自己确保其在多线程环境中的安全性。因为  `clinit`  方法是带锁线程安全，所以在多线程环境下进行类初始化的话可能会引起死锁，并且这种死锁很难被发现。

类不是启动jvm一次全初始化的，而是用到哪个加载哪个。

其他静态字段的赋值、静态代码块，都会放到clinit方法中执行。

初始化一个类的触发场景：

1. 启动的主类
2. new
3. 子类触发父类
4. 访问静态方法、字段
5. 反射调用某个类
6. methodHandle指向方法所在类

类初始化是线程安全的，并且仅执行一次，可用来延迟初始化单例。

### 卸载

卸载类即该类的Class对象被GC。

卸载类需要满足3个要求:

1. 该类的所有的实例对象都已被GC，也就是说堆不存在该类的实例对象。
2. 该类没有在其他任何地方被引用
3. 该类的类加载器的实例已被GC

 在JVM生命周期类，由jvm自带的类加载器加载的类是不会被卸载的。但是由我们自定义的类加载器加载的类是可能被卸载的。 

### 类加载器

java8：

一个类加载器先将请求转发给父类，父类加载器找不到，子类加载器才会尝试去加载。

![](img\类加载双亲委派.png)

JVM 中内置了三个重要的 ClassLoader，除了 BootstrapClassLoader 其他类加载器均由 Java 实现且全部继承自`java.lang.ClassLoader`：

1. **BootstrapClassLoader(启动类加载器)** ：最顶层的加载类，由C++实现，负责加载 `%JAVA_HOME%/lib`（jre/lib)目录下的jar包和类或者或被 `-Xbootclasspath`参数指定的路径中的所有类。
2. **ExtensionClassLoader(扩展类加载器)** ：主要负责加载目录 `%JRE_HOME%/lib/ext` 目录下的jar包和类，或被 `java.ext.dirs` 系统变量所指定的路径下的jar包。
3. **AppClassLoader(应用程序类加载器)** :面向我们用户的加载器，负责加载当前应用classpath下的所有jar包和类。父类是扩展类加载器

类加载器之间的“父子”关系也不是通过继承来体现的，是由“优先级”来决定。 

java9中，启动类加载器加载少数几个关键模块，平台类加载器加载其他类

### 双亲委派模型

双亲委派模型的实现代码非常简单，逻辑非常清晰，都集中在 `java.lang.ClassLoader` 的 `loadClass()` 中，相关代码如下所示。

```java
private final ClassLoader parent; 
protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
        synchronized (getClassLoadingLock(name)) {
            // 首先，检查请求的类是否已经被加载过
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                long t0 = System.nanoTime();
                try {
                    if (parent != null) {//父加载器不为空，调用父加载器loadClass()方法处理
                        c = parent.loadClass(name, false);
                    } else {//父加载器为空，使用启动类加载器 BootstrapClassLoader 加载
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                   //抛出异常说明父类加载器无法完成加载请求
                }
                
                if (c == null) {
                    long t1 = System.nanoTime();
                    //自己尝试加载
                    c = findClass(name);

                    // this is the defining class loader; record the stats
                    sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                    sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                    sun.misc.PerfCounter.getFindClasses().increment();
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }
```



**双亲委派模型的好处**

双亲委派模型保证了Java程序的稳定运行，可以避免类的重复加载（JVM  区分不同类的方式不仅仅根据类名，相同的类文件被不同的类加载器加载产生的是两个不同的类），也保证了 Java 的核心 API  不被篡改。如果没有使用双亲委派模型，而是每个类加载器加载自己的话就会出现一些问题，比如我们编写一个称为 `java.lang.Object` 类的话，那么程序运行的时候，系统就会出现多个不同的 `Object` 类。

为了避免双亲委托机制，我们可以自己定义一个类加载器，然后重写 `loadClass()` 即可。



### 自定义类加载器

除了 `BootstrapClassLoader` 其他类加载器均由 Java 实现且全部继承自`java.lang.ClassLoader`。如果我们要自定义自己的类加载器，很明显需要继承 `ClassLoader`。

用途：

- 比如可以解密加密后的class文件。

- 不同的类加载器加载同一个字节流（比如class文件），会得到两个不同的类，可以用来运行同一个类的不同版本。

https://www.cnblogs.com/wjtaigwh/p/6635484.html

### 示例

执行main方法的步骤如下:

1. 编译好 App.java 后得到 App.class 后，执行 App.class，系统会启动一个 JVM 进程，从 classpath 路径中找到一个名为 App.class 的二进制文件，将 App 的类信息加载到运行时数据区的方法区内，这个过程叫做 App 类的加载
2. JVM 找到 App 的主程序入口，执行main方法
3. 这个main中的第一条语句为 Student student = new Student("tellUrDream") ，就是让 JVM 创建一个Student对象，但是这个时候方法区中是没有 Student 类的信息的，所以 JVM 马上加载 Student 类，把  Student 类的信息放到方法区中
4. 加载完 Student 类后，JVM 在堆中为一个新的 Student 实例分配内存，然后调用构造函数初始化 Student 实例，这个 Student 实例持有 **指向方法区中的 Student 类的类型信息** 的引用
5. 执行student.sayName();时，JVM 根据 student 的引用找到 student 对象，然后根据 student 对象持有的引用定位到方法区中 student 类的类型信息的方法表，获得 sayName() 的字节码地址。
6. 执行sayName()

其实也不用管太多，只需要知道对象实例初始化时会去方法区中找类信息，完成后再到栈那里去运行方法。找方法就在方法表中找。



## 方法调用

子类静态方法可以隐藏父类静态方法，不能重写，因为可以用类名直接调用。。

静态绑定：解析时直接决定调用的方法

动态绑定：运行时根据调用者的动态类型来识别目标方法

### 逃逸分析

一个方法当中的对象如果不逃逸，那么这个对象可能会被分配在栈内存上。

逃逸的情况：

1. 对象存入堆中（静态字段或者堆中对象的实例字段）
2. 对象被传入未知代码中（代码没有内联）

逃逸分析的结果用于将新建对象操作转换成栈上分配或标量替换（局部变量保存在栈上或寄存器上）。

## 元空间

用于存放静态资源，对垃圾回收没有显著影响。

但是一些框架像cglib,*Spring*,Hibernate会创建大量的动态类,因此对于使用这些框架的应用最好是分配多一点空间。

设置 -XX:MetaspaceSize=8m -XX:MaxMetaspaceSize=80m



# GC

## 算法

https://zhuanlan.zhihu.com/p/73628158

https://zhuanlan.zhihu.com/p/26386634

- 标记-清除。缺点：一是标记清楚的效率不高，二是产生内存碎片
- 复制。将内存划分为相等的两块区域A和B，一次只用其中一块A，当需要垃圾回收时，将A中所有存活的对象复制到B，然后清楚A，使用B。就这样周而复始。但是也有一个明显的问题：可使用的内存大小只有一半。
- 标记-整理。先标记，然后让所有存活对象向另一端移动，然后直接清理端边界以外的内存。

## 分代收集算法

G1算法之前，新生代和老年代算法选择：

- 在新生代中，每次收集都会有大量对象死去，所以可以选择复制算法，只需要付出少量对象的复制成本就可以完成每次垃圾收集。
- 老年代的对象存活几率是比较高的，而且没有额外的空间对它进行分配担保，所以我们必须选择“标记-清除”或“标记-整理”算法进行垃圾收集。



对象优先在 eden 区分配

大对象直接进入老年代，避免为大对象分配内存时由于分配担保机制带来的复制而降低效率。

长期存活的对象将进入老年代

- **新生代 GC（Minor GC/YoungGC）**:指发生新生代的的垃圾收集动作，Minor GC 非常频繁，回收速度一般也比较快。
- **老年代 GC（Major GC/Full GC）**:指发生在老年代的 GC，出现了 Major GC 经常会伴随至少一次的 Minor GC（并非绝对），Major GC 的速度一般会比 Minor GC 的慢 10 倍以上。

判断那些对象已经死亡，通过可达性分析法判断对象的引用链是否可达



**Eden区**

IBM 公司的专业研究表明，有将近98%的对象是朝生夕死，所以针对这一现状，所有新对象创建发生在Eden区

复制的过程：

1. 当 Eden 区没有足够空间进行分配时，虚拟机会发起一次 Minor GC。
2. Eden区和非空闲Survivor区存活对象会被复制到另一个空闲的Survivor区中（（若 这个Survivor区不够，则直接进入 Old 区）。
3. 永远保证一个Survivor是空的，

新生代GC（MinorGC/YoungGC）非常频繁，就是在两个Survivor区之间相互复制存活对象，直到Survivor区满为止。

设置两个 Survivor 区最大的好处就是方便使用复制算法解决内存碎片化。

**老年代**：

Tenured

老年代占据着2/3的堆内存空间，只有在 Major GC 的时候才会进行清理，每次 GC 都会触发“Stop-The-World”。内存越大，STW 的时间也越长，所以内存也不仅仅是越大就越好。

除了上述所说，在内存担保机制下，无法安置的对象会直接进到老年代，以下几种情况也会进入老年代。

1. 需要大量连续内存空间的大对象
2. 长期存活对象

老年代GC(MajorGC/FullGC) 的触发条件有多个，FULL GC 的时候会 STOP THE WORD 。

- 在执行 Young GC 之前，JVM 会进行空间分配担保——如果老年代的连续空间小于新生代对象的总大小（或历次晋升的平均大小），则触发一次 Full GC 。
- 大对象直接进入老年代，从年轻代晋升上来的老对象，尝试在老年代分配内存时，但是老年代内存空间不够。
- 显式调用 `System.gc()` 方法时。

## 对象生命周期

在`Java`中，对象的生命周期包括以下几个阶段：创建阶段(`Created`)

应用阶段(`In Use`)

不可见阶段(`Invisible`)

不可达阶段(`Unreachable`)

收集阶段(`Collected`)

终结阶段(`Finalized`)

对象空间重分配阶段(`De-allocated`)



强引用

一般静态域的map强引用了对象的，即使key=null对象也无法释放，因为hashmap里散列桶里保存的是内存地址而不是key的引用。



软引用是用来描述一些还有用但并非必须的对象。对于软引用关联着的对象，在系统将要发生内存溢出异常之前，将会把这些对象列进回收范围进行第二次回收。如果这次回收还没有足够的内存，才会抛出内存溢出异常。

弱引用

弱引用也是用来描述非必须对象的，他的强度比软引用更弱一些，被弱引用关联的对象，在垃圾回收时，如果这个对象只被弱引用关联（没有任何强引用关联他），那么这个对象就会被回收。个人理解是弱引用声明的是对象的使用权。

```java
/**
 * 弱引用关联对象何时被回收
 * Created by ccr at 2018/7/14.
 */
public class WeakReferenceDemo {
    public static void main(String[] args) throws InterruptedException {
        //100M的缓存数据
        byte[] cacheData = new byte[100 * 1024 * 1024];
        //将缓存数据用软引用持有
        WeakReference<byte[]> cacheRef = new WeakReference<>(cacheData);
        System.out.println("第一次GC前" + cacheData);
        System.out.println("第一次GC前" + cacheRef.get());
        //进行一次GC后查看对象的回收情况
        System.gc();
        //等待GC
        Thread.sleep(500);
        System.out.println("第一次GC后" + cacheData);
        System.out.println("第一次GC后" + cacheRef.get());

        //将缓存数据的强引用去除
        cacheData = null;
        System.gc();
        //等待GC
        Thread.sleep(500);
        System.out.println("第二次GC后" + cacheData);
        System.out.println("第二次GC后" + cacheRef.get());
    }
}
第一次GC前[B@7d4991ad
第一次GC前[B@7d4991ad
第一次GC后[B@7d4991ad
第一次GC后[B@7d4991ad
第二次GC后null
第二次GC后null
```

需要注意弱引用的对象可能被回收会是null，需要判断。比如

tomcat-jdbc连接池中，PoolCleaner持有的是对ConnectionPool的弱引用，如果当web app关闭时如果没有显式的回收/关闭ConnectionPool，此时JVM中唯一指向该ConnectionPool的便是PoolCleaner，使用弱引用便不会妨碍连接池的正常回收，以防止出现内存泄漏。

PoolCleaner会检查弱引用的连接池对象是否为null，如果发现它被回收，自己将会从全局Set中移除自己。

```
@Override
public void run() {
    ConnectionPool pool = this.pool.get();
    if (pool == null) {
        stopRunning();
    }
    //...
}
```



## Serial 收集器

垃圾收集线程在进行垃圾收集工作的时候必须暂停其他所有的工作线程（ **"Stop The World"** ），直到它收集结束。

新生代采用复制算法，老年代采用标记-整理算法。 

Serial Old 收集器是Serial 收集器的老年代版本

## 并行收集器

- ParNew
- Parallel Scavenge
- Parallel Old

并行收集器每发生一次垃圾收集，它会停掉所有应用的线程并用多个线程（Stop the world），执行垃圾回收工作。相比Serial收集器，它只是减少了STW的时间。

年轻代和年老代都可以并行收集。

**并行和并发概念补充：**

- **并行（Parallel）** ：指多条垃圾收集线程并行工作，但此时用户线程仍然处于等待状态。
- **并发（Concurrent）**：指用户线程与垃圾收集线程同时执行（但不一定是并行，可能会交替执行），用户程序在继续运行，而垃圾收集器运行在另一个 CPU 上。

## ParNew

ParNew 收集器除了使用多线程进行垃圾收集外，其余行为（控制参数、收集算法、回收策略等等）和 Serial 收集器完全一样。它是许多运行在 Server 模式下的虚拟机的首要选择。

新生代采用复制算法，老年代采用标记-整理算法。

收集年轻代时暂停很短暂。

## Parallel Scavenge

Parallel Scavenge 收集器也是使用复制算法的多线程收集器，看上去几乎和ParNew都一样。提供了很多参数供用户找到最合适的停顿时间或最大吞吐量。**Parallel Scavenge 收集器关注点是吞吐量（高效率的利用 CPU）**

Parallel Scavenge没有使用原本HotSpot其它GC通用的那个GC框架，所以不能跟使用了那个框架的CMS搭配使用

## Parallel Old 

Parallel Old 收集器是Parallel Scavenge 收集器的老年代版本。

使用多线程和“标记-整理”算法。

在注重吞吐量以及 CPU 资源的场合，都可以优先考虑 Parallel Scavenge 收集器和 Parallel Old 收集器。

jdk1.8 64位使用server模式，Linux或windows上默认jvm参数：

```shell
-XX:InitialHeapSize=131708544 -XX:MaxHeapSize=2107336704 -XX:+PrintCommandLineFlags -XX:+PrintGCDetails -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:-UseLargePagesIndividualAllocation -XX:+UseParallelGC 

```

UseParallelGC 即 Parallel Scavenge + Serial Old

## CMS

CMS（Concurrent Mark Sweep）收集器是 HotSpot 虚拟机第一款真正意义上的**并发收集器**，它第一次实现了让垃圾收集线程与用户线程（基本上）同时工作。

主要保证系统的响应时间，减少垃圾收集的停顿时间。

用户线程和年老代GC同时进行，在年老代保持一直有足够的空间以保证不会发生年轻代晋升失败。

```shell
-XX:+UseParNewGC
-XX:+UseConcMarkSweepGC //新生代使用并行收集器，老年代使用 CMS收集器
```



CMS用于年老代，只有ParNew能和它配合使用（收集年轻代）。

https://segmentfault.com/a/1190000004715667?utm_source=tag-newest

缺点：

**标记-清除”算法会导致收集结束时会有大量空间碎片产生**

## G1收集器

G1 (Garbage-First) 是一款面向服务器的垃圾收集器,主要针对配备多颗处理器及大容量内存的机器. 以极高概率满足 GC 停顿时间要求的同时,还具备高吞吐量性能特征.

被视为 JDK1.7 中 HotSpot 虚拟机的一个重要进化特征。它具备一下特点：

- **并行与并发**：G1 能充分利用 CPU、多核环境下的硬件优势，使用多个 CPU（CPU 或者 CPU  核心）来缩短 Stop-The-World 停顿时间。部分其他收集器原本需要停顿 Java 线程执行的 GC 动作，G1  收集器仍然可以通过并发的方式让 java 程序继续执行。
- **分代收集**：虽然 G1 可以不需要其他收集器配合就能独立管理整个 GC 堆，但是还是保留了分代的概念。
- **标记-整理-复制**：与 CMS 的“标记--清理”算法不同，G1 从整体来看是基于“标记整理”算法实现的收集器；从局部上来看是基于“复制”算法实现的。
- **可预测的停顿**：这是 G1 相对于 CMS 的另一个大优势，降低停顿时间是 G1 和 CMS 共同的关注点，但 G1 除了追求低停顿外，还能建立可预测的停顿时间模型，能让使用者明确指定在一个长度为 M 毫秒的时间片段内。

通过JVM参数 –XX:+UseG1GC 使用G1收集器

原理：

美团 https://zhuanlan.zhihu.com/p/22591838

https://zhuanlan.zhihu.com/p/59861022

## jdk默认算法

Linux服务器上查看java默认收集算法

```shell
java -XX:+PrintCommandLineFlags -version

-XX:InitialHeapSize=266390080 -XX:MaxHeapSize=4262241280 -XX:+PrintCommandLineFlags 
-XX:+UseCompressedClassPointers -XX:+UseCompressedOops 
-XX:-UseLargePagesIndividualAllocation -XX:+UseParallelGC
java version "1.8.0_191"
Java(TM) SE Runtime Environment (build 1.8.0_191-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.191-b12, mixed mode)
```

UseParallelGC 即 Parallel Scavenge + Serial Old

## 堆内存jvm参数
显式指定堆内存–Xms和-Xmx.单位为***“ g”*** (GB) 、***“ m”***（MB）、***“ k”***（KB）

```shell
-Xms2G -Xmx5G
```

指定新生代内存最小和最大：

```shell
-XX:NewSize=<young size>[unit] 
-XX:MaxNewSize=<young size>[unit]
```

为 新生代分配256m的内存（NewSize与MaxNewSize设为一致）

```shell
-Xmn256m 
```

> 将新对象预留在新生代，由于 Full GC 的成本远高于 Minor GC，因此尽可能将对象分配在新生代是明智的做法，实际项目中根据 GC 日志分析新生代空间大小分配是否合理，适当通过“-Xmn”命令调节新生代大小，最大限度降低新对象直接进入老年代的情况。

设置新生代（包括Eden和两个Survivor区）与老年代的比值为1

```shell
-XX:NewRatio=1
```



**元空间**

从Java 8开始，如果我们没有指定 Metaspace 的大小，随着更多类的创建，虚拟机会耗尽所有可用的系统内存

```shell
-XX:MetaspaceSize=N //设置 Metaspace 的初始（和最小大小）
-XX:MaxMetaspaceSize=N //设置 Metaspace 的最大大小
```

## GC 调优策略

**策略 1：**将新对象预留在新生代，由于 Full GC 的成本远高于 Minor  GC，因此尽可能将对象分配在新生代是明智的做法，实际项目中根据 GC  日志分析新生代空间大小分配是否合理，适当通过“-Xmn”命令调节新生代大小，最大限度降低新对象直接进入老年代的情况。

**策略  2：**大对象进入老年代，虽然大部分情况下，将对象分配在新生代是合理的。但是对于大对象这种做法却值得商榷，大对象如果首次在新生代分配可能会出现空间不足导致很多年龄不够的小对象被分配的老年代，破坏新生代的对象结构，可能会出现频繁的 full gc。因此，对于大对象，可以设置直接进入老年代（当然短命的大对象对于垃圾回收来说简直就是噩梦）。`-XX:PretenureSizeThreshold` 可以设置直接进入老年代的对象大小。

**策略 3：**合理设置进入老年代对象的年龄，`-XX:MaxTenuringThreshold` 设置对象进入老年代的年龄大小，减少老年代的内存占用，降低 full gc 发生的频率。

**策略 4：**设置稳定的堆大小，堆大小设置有两个参数：`-Xms` 初始化堆大小，`-Xmx` 最大堆大小。

**策略5：**注意： 如果满足下面的指标，**则一般不需要进行 GC 优化：**

> MinorGC 执行时间不到50ms； Minor GC 执行不频繁，约10秒一次； Full GC 执行时间不到1s； Full GC 执行频率不算频繁，不低于10分钟1次。

## server模式

**两种模式的区别在于，Client模式启动速度较快，Server模式启动较慢；**

- 但是启动进入稳定期长期运行之后Server模式的程序运行速度比Client要快很多。
- 这是因为Server模式启动的JVM采用的是重量级的虚拟机，对程序采用了更多的优化；
- 而Client模式启动的JVM采用的是轻量级的虚拟机

JVM启动时采用何种模式是在名为jvm.cfg的配置文件中配置的。 

```
32位的虚拟机在%JAVA_HOME%/jre/lib/i386/jvm.cfg
64位的虚拟机在%JAVA_HOME%/jre/lib/amd64/jvm.cfg
```

## 系统属性

所谓的“系统属性”其实是jvm的属性，设置方法有两种：

1. java启动时-Dprop1=value1
2. java代码中System.setProperty

Linux环境变量最好是java命令执行前设置，一般不在java代码中设置。

# 监控和故障处理

## 影响应用响应时间的因素

- 初始内存设置。
- 通讯耗时。如http、rpc操作。
- 池技术在获取对象时，如果数量过少但高并发时会等待。如thrift连接池大小提高到400、数据库连接池大小由15提高到80.。
- jvm gc。可以考虑使用G1 gc减少停顿。
- STW
- 分布式服务的节点数量。
- 数据库允许的最大连接数。
- 数据库索引优化。
- 数据库对多核是否利用上。
- k8s对Pod内存的限制。比如取消redis服务器对应的pod内存限制。
- 第三方中间件耗时。如fastjson升级版本来提高效率。

## STW

stop the world


等待所有用户线程进入安全点后并阻塞，做一些全局性操作的行为。

## 耗时分析

分析的几个维度：

- cpu占用。top查看
- gc频繁。jstat、jmap、jvisualvm等工具分析
- 线程状态。jstack查看，涉及到对资源的占用。如数据库连接是否正常释放

一般以上多个维度结合分析性能问题。

比如进程响应慢，并且CPU占用高，如下分析：

1. top -Hp查看线程，pid转16进制后,jstack查看线程栈信息
2. 如果是正常的用户线程，则通过该线程的堆栈信息查看其具体是在哪处用户代码处运行比较消耗CPU 
3.  如果该线程是VM Thread，则通过jstat -gcutil   命令监控当前系统的GC状况，然后通过jmap dump:format=b,file= 导出dump文件并用工具分析。 



此外，对于某个接口偶现的耗时现象，可压测加大阻塞点出现频率， 从而通过jstack查看堆栈信息，找到阻塞点； 

## JVM参数

java jmx启动和远程调试

```shell
#脚本所在的目录 
APP_HOME=$(cd "$(dirname "$0")"; pwd)
CLASS_PATH=$APP_HOME/../lib/*:$APP_HOME/../conf
JAVA_OPTS="-server -Xms512m -Xmx512m -Djava.awt.headless=true"
JAVA_OPTS_JMX="-server -Xms512m -Xmx512m -Djava.awt.headless=true -Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false"

# jmx启动
nohup java $JAVA_OPTS $JAVA_OPTS_JMX -Dlogback.configurationFile=$CLASS_PATH/logback.xml $JVM_RUN_ARGS -classpath $CLASS_PATH <mainClass> >> nohup.out 2>&1 &
# 远程调试启动
DEBUG_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=$debug_port,server=y,suspend=n"
nohup java $JAVA_OPTS -Dlogback.configurationFile=$CLASS_PATH/logback.xml $JVM_RUN_ARGS -classpath $CLASS_PATH $DEBUG_OPTS <mainClass> >> nohup.out 2>&1 &



```



-Xmn200m 新生代设置为200m

-XX:NewRatio=2 设置老年代/新生代比例为2。不能为小数

-XX:+UseG1GC 设置 G1回收器

-classpath $CLASS_PATH



jvm参数自动导出内存堆快照

```java
-XX:+HeapDumpOnOutOfMemoryError	内存溢出时自动导出内存快照
-XX:HeapDumpPath=E:/dumps/	导出内存快照时保存的路径
```



## OOM

OOM可能发生的几种情况：

1. 请求创建一个超大对象，通常是一个大数组。

2. 超出预期的访问量/数据量，通常是上游系统请求流量飙升，常见于各类促销/秒杀活动，可以结合业务流量指标排查是否有尖状峰值。过多的对象来不及垃圾收集。
3. 内存泄漏（Memory Leak），大量对象引用没有释放，JVM 无法对其自动回收，常见于使用了 File 等资源没有回收。
4. 过度使用终结器（Finalizer），该对象没有立即被 GC

一些错误消息

- java.lang.OutOfMemoryError: Java heap space
- java.lang.OutOfMemoryError: PermGen space
- java.lang.OutOfMemoryError: Requested array size exceeds VM limit 尝试分配大于堆大小的数组
- java.lang.OutOfMemoryError: request bytes for . Out of swap space? 本机堆的分配失败并且本机堆可能将被耗尽.比如操作系统配置的交换空间不足;系统上的另一个进程是消耗所有可用的内存资源。
- java.lang.OutOfMemoryError: (Native method)

在大多数情况下，诊断内存泄漏需要非常详细地了解相关应用程序。分析方法：

1. 症状识别，区分正常的内存耗尽和泄漏
2. 查看gc情况。老生代一直在gc，但内存并没有减少。说明存在无法被回收的对象，可能是内存泄漏了 
3. 分析堆
4. 启用详细垃圾收集

**首先要区分正常的内存耗尽和泄漏**

通常，如果Java应用程序请求的存储空间超过运行时堆提供的存储空间，则可能是由于设计不佳导致的。例如，如果应用程序创建映像的多个副本或将文件加载到数组中，则当映像或文件非常大时，它将耗尽存储空间。这是正常的资源耗尽。该应用程序按设计工作（虽然这种设计显然是愚蠢的）。

但是，如果应用程序在处理相同类型的数据时稳定地增加其内存利用率，则可能会发生内存泄漏。

参考https://zhuanlan.zhihu.com/p/80255370

**分析堆**
在堆中找到不应该存在的对象块，并确定这些对象是否累积而不是释放。

最后，解决内存泄漏需要您彻底检查代码

**启用详细垃圾收集**

断言确实存在内存泄漏的最快方法之一是启用详细垃圾回收。通常可以通过检查verbosegc输出中的模式来识别内存约束问题。

-verbosegc参数在每次垃圾收集（GC）过程开始时生成跟踪。当内存被垃圾收集时，摘要报告会打印到标准错误，了解内存的管理方式。

可以查看连续的分配失败节，并查找随着时间的推移而减少的释放内存（字节和百分比），同时总内存正在增加。这些是内存耗尽的典型迹象。

## 内存泄漏

内存泄漏定义：一个不再被程序使用的对象或变量还在内存中占有存储空间 

内存溢出 :指程序申请内存时，没有足够的内存供申请者使用

 内存泄漏的堆积最终会导致内存溢出 



内存泄漏的几种情况：

- 尽管短生命周期的对象不再使用，但是因为被静态对象引用而导致不能被回收 
-  连接没有被关闭释放。只有连接被关闭后，垃圾回收器才会回收对应的对象 
- 内部类持有外部类，内部类对象被长期引用，外部类对象也无法被回收。
-  对象被存储进HashSet集合后，修改了参与计算哈希值的字段，导致无法从HashSet集合中单独删除当前对象，造成内存泄露。



## JDK 命令行工具

这些命令在 JDK 安装目录下的 bin 目录下：

- **jps** (JVM Process Status）: 类似 UNIX 的 `ps` 命令。用户查看所有 Java 进程的启动类、传入参数和 Java 虚拟机参数等信息；
- **jstat**（ JVM Statistics Monitoring Tool）:  用于收集 HotSpot 虚拟机各方面的运行数据;
- **jinfo** (Configuration Info for Java) : Configuration Info forJava,显示虚拟机配置信息;
- **jmap** (Memory Map for Java) :生成堆转储快照;
- **jhat** (JVM Heap Dump Browser ) : 用于分析 heapdump 文件，它会建立一个 HTTP/HTML 服务器，让用户可以在浏览器上查看分析结果;
- **jstack** (Stack Trace for Java):生成虚拟机当前时刻的线程快照，线程快照就是当前虚拟机内每一条线程正在执行的方法堆栈的集合。



### jps

显示虚拟机执行主类名称以及这些进程的本地虚拟机唯一 ID。

`jps -l`:输出主类的全名

`jps -v`：输出虚拟机进程启动时 JVM 参数。



### jmap 

查看垃圾收集策略即 JVM 内存占用情况，也可以生成堆转储快照

```shell
#  查看jvm新生代、老年代内存占用情况
jmap -heap <pid>
# 输出dump文件，给jhat、mat、jvisualvm分析
jmap -dump:format=b,file=文件名 [pid]
# JVM会先触发fgc，然后再统计信息
jmap -histo:live <pid>
```

可以使用jmap生成Heap Dump(jvm的堆的快照), 离线分析堆，以检查内存泄漏，检查一些严重影响性能的大对象的创建、什么对象最多，各种对象所占内存的大小。

示例

```shell
C:\Users\SnailClimb>jmap -dump:format=b,file=C:\Users\SnailClimb\Desktop\heap.hprof 17340
Dumping heap to C:\Users\SnailClimb\Desktop\heap.hprof ...
Heap dump file created
```

不使用 `jmap` 命令，要想获取 Java 堆转储，可以使用 `“-XX:+HeapDumpOnOutOfMemoryError”` 参数，可以让虚拟机在 OOM 异常出现之后自动生成 dump 文件，Linux 命令下可以通过 `kill -3` 发送进程退出信号也能拿到 dump 文件。



### jstack 

查看线程栈的描述信息（不是栈实际保存的全部信息）

```shell
# 保存进程的堆栈日志
jstack -l <pid> > jstack.log
# 查看内存占用较多的进程
top
# 查看进程<pid>的线程情况
ps p <pid> -L -o pcpu,pmem,pid,tid,time,tname,cmd
# 挑选了TID=9720的线程进行分析，首先需要将9731这个id转换为16进制
printf "%x\n" 9731
# 查找TID=9720（对应16进制）
vim jstack.log
```



### jstat 

监视虚拟机各种运行状态信息

```shell
# 间隔5s, 每隔10条输出一次头信息, 打印进程号为xx的JVM进程的堆内存使用情况, 以及各代垃圾回收的次数及时间:
jstat -gcutil -h10 <pid> 5000

jstat -gc <pid> <interval/ms> <count>

stat -gccapacity vmid ：显示各个代的容量及使用情况
# 查看年轻代、老年代、metaspace的容量，单位KB
jstat -gcmetacapacity <pid>
-gcoldcapacity 显示老年代的大小
-gcnewcapacity
```

参数说明

```
S0: Heap上的Survivor Space 0区已使用空间的百分比
S1: Heap上的Survivor Space 1区已使用空间的百分比
E:  Heap上的Eden Space区已使用空间的百分比
O:  Heap上的Old Space区已使用空间的百分比
M:  Meta Space(元数据区)已使用空间的百分比
YGC: 从应用程序启动到采样时发生Young GC的次数
YGCT: 从应用程序启动到采样时Young GC所用的时间(单位: 秒)
FGC:  从应用程序启动到采样时发生Full GC的次数
FGCT: 从应用程序启动到采样时Full GC所用的时间(单位: 秒)
GCT:  从应用程序启动到采样时用于垃圾回收的总时间(单位: 秒)
```

21891 进程号； 250ms 采样interval； 7 count
S0     S1     E      O      P     YGC    YGCT    FGC    FGCT     GCT
12.44   0.00  27.20   9.49  96.70    78    0.176     5    0.495    0.672
12.44   0.00  62.16   9.49  96.70    78    0.176     5    0.495    0.672
12.44   0.00  83.97   9.49  96.70    78    0.176     5    0.495    0.672
0.00    7.74   0.00   9.51  96.70    79    0.177     5    0.495    0.673
0.00    7.74  23.37   9.51  96.70    79    0.177     5    0.495    0.673
0.00    7.74  43.82   9.51  96.70    79    0.177     5    0.495    0.673
0.00    7.74  58.11   9.51  96.71    79    0.177     5    0.495    0.673

以上输出表明：
1. 在第三行与第四行，发生一次新生代gc。 本次gc耗时0.001秒，且有对象从Eden区提升到老生代，老生代使用率从9.49% 上升到9.51%。
2. gc之前，survivor space 使用率12.44%， gc后，降为7.74%。

3s一次ygc的频率，甚至频率更低，5s一次，7s一次，这是正常的；如果超过1s一次ygc，0.5s一次ygc那可能eden不够



### jinfo

实时地查看和调整虚拟机各项参数

使用 jinfo 可以在不重启虚拟机的情况下，可以动态的修改 jvm 的参数。尤其在线上的环境特别有用

`jinfo vmid` :输出当前 jvm 进程的全部参数和系统属性 

`jinfo -flag name vmid` :输出对应名称的参数的具体值

`jinfo -flag [+|-]name vmid` 开启或者关闭对应名称的参数。

```shell
C:\Users\SnailClimb>jinfo  -flag  PrintGC 17340
-XX:-PrintGC

C:\Users\SnailClimb>jinfo  -flag  +PrintGC 17340

C:\Users\SnailClimb>jinfo  -flag  PrintGC 17340
-XX:+PrintGC
```

### jhat

分析 heapdump 文件

jhat 用于分析 heapdump 文件，它会建立一个 HTTP/HTML 服务器，让用户可以在浏览器上查看分析结果。

```shell
C:\Users\SnailClimb>jhat C:\Users\SnailClimb\Desktop\heap.hprof
Reading from C:\Users\SnailClimb\Desktop\heap.hprof...
Dump file created Sat May 04 12:30:31 CST 2019
Snapshot read, resolving...
Resolving 131419 objects...
Chasing references, expect 26 dots..........................
Eliminating duplicate references..........................
Snapshot resolved.
Started HTTP server on port 7000
Server is ready.
```

然后访问 <http://localhost:7000/>

### **jstack** 

**生成虚拟机当前时刻的线程快照**

`jstack`（Stack Trace for Java）命令用于生成虚拟机当前时刻的线程快照。线程快照就是当前虚拟机内每一条线程正在执行的方法堆栈的集合.

生成线程快照的目的主要是定位线程长时间出现停顿的原因，如线程间死锁、死循环、请求外部资源导致的长时间等待等都是导致线程长时间停顿的原因。线程出现停顿的时候通过`jstack`来查看各个线程的调用堆栈，就可以知道没有响应的线程到底在后台做些什么事情，或者在等待些什么资源。

**下面是一个线程死锁的代码。我们下面会通过 jstack 命令进行死锁检查，输出死锁信息，找到发生死锁的线程。**

```java
public class DeadLockDemo {
    private static Object resource1 = new Object();//资源 1
    private static Object resource2 = new Object();//资源 2

    public static void main(String[] args) {
        new Thread(() -> {
            synchronized (resource1) {
                System.out.println(Thread.currentThread() + "get resource1");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread() + "waiting get resource2");
                synchronized (resource2) {
                    System.out.println(Thread.currentThread() + "get resource2");
                }
            }
        }, "线程 1").start();

        new Thread(() -> {
            synchronized (resource2) {
                System.out.println(Thread.currentThread() + "get resource2");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread() + "waiting get resource1");
                synchronized (resource1) {
                    System.out.println(Thread.currentThread() + "get resource1");
                }
            }
        }, "线程 2").start();
    }
}
```

Output

```shell
Thread[线程 1,5,main]get resource1
Thread[线程 2,5,main]get resource2
Thread[线程 1,5,main]waiting get resource2
Thread[线程 2,5,main]waiting get resource1
```

线程 A 通过 synchronized (resource1) 获得 resource1 的监视器锁，然后通过` Thread.sleep(1000);`让线程 A 休眠 1s 为的是让线程 B 得到执行然后获取到 resource2 的监视器锁。线程 A 和线程 B 休眠结束了都开始企图请求获取对方的资源，然后这两个线程就会陷入互相等待的状态，这也就产生了死锁。

**通过 jstack 命令分析：**

```shell
C:\Users\SnailClimb>jps
13792 KotlinCompileDaemon
7360 NettyClient2
17396
7972 Launcher
8932 Launcher
9256 DeadLockDemo
10764 Jps
17340 NettyServer	

C:\Users\SnailClimb>jstack 9256
```

输出的部分内容如下：

```java
Found one Java-level deadlock:
=============================
"线程 2":
  waiting to lock monitor 0x000000000333e668 (object 0x00000000d5efe1c0, a java.lang.Object),
  which is held by "线程 1"
"线程 1":
  waiting to lock monitor 0x000000000333be88 (object 0x00000000d5efe1d0, a java.lang.Object),
  which is held by "线程 2"

Java stack information for the threads listed above:
===================================================
"线程 2":
        at DeadLockDemo.lambda$main$1(DeadLockDemo.java:31)
        - waiting to lock <0x00000000d5efe1c0> (a java.lang.Object)
        - locked <0x00000000d5efe1d0> (a java.lang.Object)
        at DeadLockDemo$$Lambda$2/1078694789.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)
"线程 1":
        at DeadLockDemo.lambda$main$0(DeadLockDemo.java:16)
        - waiting to lock <0x00000000d5efe1d0> (a java.lang.Object)
        - locked <0x00000000d5efe1c0> (a java.lang.Object)
        at DeadLockDemo$$Lambda$1/1324119927.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)

Found 1 deadlock.
```

可以看到 `jstack` 命令已经帮我们找到发生死锁的线程的具体信息。

## 磁盘IO

**系统级IO**

使用time+dd测试硬盘读写速度. 在当前目录下新建一个2G的文件

```shell
time dd if=/dev/zero bs=1M count=2048 of=direct_2G 
```

监控系统IO

```shell
iostat -x 1
```

sar -dp可以看到历史IO情况，默认情况下是10分钟记录一次，可以改成1分钟一次

查看磁盘是否有坏道。坏道可能导致IO很高。

/opt/MegaRAID/MegaCli/MegaCli64 LDPDInfo -Aall

**进程IO**

监控进程IO

```shell
pidstat -d  1                  #只显示IO
pidstat -u -r -d -t 1
iotop							#监控每一秒的进程IO情况
```

**业务IO**

注: ioprofile 仅支持多线程程序,对单线程程序不支持. 对于单线程程序的IO业务级分析,strace足以

strace attach到JVM Thread调试

**文件级IO**

主要针对单个文件，分析,当前哪些进程正在对文件读写操作.

- lsof   或者  ls /proc/pid/fd

-  inodewatch.stp  

## 可视化分析工具

https://visualvm.github.io/plugins.html

https://visualvm.github.io/pluginscenters.html

https://blog.csdn.net/qq_23747821/article/details/79675193

https://www.cnblogs.com/xifengxiaoma/p/9402497.html

https://www.ibm.com/developerworks/cn/java/j-lo-visualvm/index.html

jvisualvm工具-->监视-->堆dump，查看哪些类实例最多， 右键选择类TestMemory，选择“在实例视图中显示” 。点击一个实例，可以查看实例被引用的情况

当前堆可以与之前同一进程的堆做对比分析。

jvisualvm也可以导入dump文件。

## GC日志

可以通过配置JVM的启动参数, 打印类的加载情况及对象的回收信息到指定文件。

JVM的GC日志的主要参数： 

```shell
-XX:+PrintGC 输出GC日志 
-XX:+PrintGCDetails 输出GC的详细日志 
-XX:+PrintGCTimeStamps 输出GC的时间戳（以基准时间的形式） 
-XX:+PrintGCDateStamps 输出GC的时间戳（以日期的形式，如 2013-05-04T21:53:59.234+0800） 
-XX:+PrintHeapAtGC 在进行GC的前后打印出堆的信息 
-XX:+PrintGCApplicationStoppedTime // 输出GC造成应用暂停的时间 
-Xloggc:../logs/gc.log 日志文件的输出路径

-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=< number of log files > 
-XX:GCLogFileSize=< file size >[ unit ]
```



日志格式如下

```shell
293.271: [GC [PSYoungGen: 300865K->6577K(310720K)] 392829K->108873K(417472K), 0.0176464 secs] [Times: user=0.06 sys=0.00, real=0.01 secs] 
```

> 293.271代表了GC发生的时间
>
> PSYoungGen，表示新生代使用的是多线程垃圾收集器Parallel  Scavenge。
>
> 300865K表示垃圾收集之前年轻代对象占用空间
>
> 6577K表示垃圾收集之后年轻代对象占用空间(Suvivor)
>
> 括号里的310720K表示整个年轻代分配的大小。
>
> 392829K->108873K(417472K),表示java堆的大小
>
> 老年代的变化和总大小可以用java堆-年轻代的值。
>
> ParNew收集器使用后，新生代名称就会变为“[ParNew”，意为“Parallel New Generation”
>
> Serial收集器中的新生代名为“Default New Generation”，所以显示的是“[DefNew”



Metaspace独立于堆外设置

查看服务器上jvm虚拟机默认给Metaspace配置的容量（单位字节）：

```
java -XX:+PrintFlagsFinal | grep Meta
```

当GC发生时，每个线程只有进入了SafePoint才算是真正挂起，也就是真正的停顿，这个日志的含义是整个GC过程中STW的时间，配置了 **-XX:+PrintGCApplicationStoppedTime** 这个参数才会打印这个信息。
**重点：** 第一个 2.81 seconds 是JVM启动后的秒数，第二个 2.6 seconds 是 JVM发起STW的开始到结束的时间。特别地，如果是GC引发的STW，这条内容会紧挨着出现在GC log的下面。

## 线程状态

查看商旅线程总数（210个）

```bash
jstack -l pid |grep java.lang.Thread.State|wc -l
```

2.查看商旅线程BLOCKED线程数（198个）

```bash
jstack -l pid |grep "java.lang.Thread.State: BLOCKED"|wc -l
```

3.查看商旅线程WAITING状态线程数（5个）

```bash
jstack -l pid |grep "java.lang.Thread.State: WAITING"|wc -l
```

通过具体的线程栈的打印，发现都在等待同一把锁，而占用此锁的线程做了耗时操作，导致锁迟迟无法释放，最终的结果就是，所有线程被BLOCKED住,同时也导致了出现了大量CLOSE_WAIT连接状态，也导致了商旅服务一直无法提供服务。 



## 查看线程信息

```bash
top -Hp 9
```

该进程下的各个线程运行情况如下

```bash
PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
   10 root      20   0 2557160 289824  15872 R 79.3 14.2   0:41.49 java
   11 root      20   0 2557160 289824  15872 S 13.2 14.2   0:06.78 java
```

转换线程id为16进制

```bash
printf "%x\n" 10
```

这里打印结果说明该线程在jstack中的展现形式为0xa，通过jstack命令搜索我们可以看到如下信息：

```bash
"main" #1 prio=5 os_prio=0 tid=0x00007f8718009800 nid=0xb runnable [0x00007f871fe41000]
   java.lang.Thread.State: RUNNABLE
    at com.sinosun.chapter2.eg2.UserDemo.main(UserDemo.java:9)

"VM Thread" os_prio=0 tid=0x00007f871806e000 nid=0xa runnable
```

这里的VM Thread一行的最后显示nid=0xa，这里nid的意思就是操作系统线程id的意思。而VM Thread指的就是垃圾回收的线程。



## GC调优实例1

给应用配置JVM参数

```shell
-XX:+PrintGCDetails -Xloggc:gc.log
```

发现Full GC(Metaspace Threhold) ，查阅资料后怀疑是Metaspace默认初始20m空间不够

## GC调优实例2

1. 触发一次FGC。jmap -histo:live pid

2. 使用jmap -heap pid 查看heap使用情况,   着重观察FGC之后,old区的使用量,  也就是红框内的最小值 。

3.  调整内存分配。heap区的大小可以设置为 old区used的四倍. (仅参考 不绝对)。

   ```shell
   -XX:MetaspaceSize=128M     meta区最小值,
   -XX:MaxMetaspaceSize=256M  mete区最大值,  此值可以参照thrift接口数量(包括bis和base所有的thrift类的数量)来设置, thrft接口越多,则越大, 目前user设置为256
   
   
   -Xms256m   heap初始值, 可以等于heap最大值
   -Xmx256m    heap最大值, 此值跟微服务的性能压力相关, 以user为标准, user目前设置为256,  此项跟ygc的次数相关.
   ```

   

4. 使用   jstat  -gc pid 3000 命令查看gc次数。目标: 第一列: ygc大概保持在30秒以上,也就是说 log刷新10行以上进行一次ygc, 第二列: FGC 次数一天不超过3次 .

![1561511798273](C:\Users\dufa\AppData\Roaming\Typora\typora-user-images\1561511798273.png)

## HTTP状态

500 Internal Server Error： 服务器内部错误，无法正常响应

502 Bad Gateway：网关或代理从上游服务收到无效的响应。可能是路由配置有问题，比如上游服务的ip配错。

# 技术栈

dfwl技术栈
Spring/Spring boot,MySQL,Mongo,Redis,Kafka,ActiveMQ,多线程
HTML,JavaScript,React,css，JQuery

# 单元测试

好的单元测试必须遵守 AIR 原则。

- A：Automatic（自动化）
- I：Independent（独立性）
-  R：Repeatable（可重复） 

单元测试的粒度足够小，有助于精确定位问题。单测粒度至多是类
级别，一般是方法级别

测试用例通常是被定期执行的，自动化。必须使用 assert 来验证

不能受到外界环境的影响。外部调用使用Mock的Sub类

```java
@RunWith(SpringJUnit4ClassRunner.class) //让测试在Spring容器环境下执行
@ContextConfiguration("classpath:unit-test.xml") //加载所需的配置文件（可以以字符数组的形式加载）
@Transactional //开启事务：已经配置了注解式事务
@Rollback //设置测试后回滚，默认属性为true，即回滚
```

单元测试中H2数据源配置取代MySQL数据源配置,如下

```xml
<bean id="ds" class="org.apache.commons.dbcp.BasicDataSource">
    <property name="driverClassName" value="org.h2.Driver"/>
    <property name="url" value="jdbc:h2:mem:test;DB_CLOSE_DELAY=-1"/>
</bean>

<jdbc:initialize-database data-source="ds">
    <jdbc:script location="classpath:db-initial.sql"/>
</jdbc:initialize-database>
```

db-initial.sql

```sql
SET MODE=MySQL;
SET FOREIGN_KEY_CHECKS=0;
CREATE TABLE `t_chat` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID序列，自增',
  `fquestion` varchar(500) DEFAULT NULL COMMENT '问题',
  `fanswer` varchar(2000) DEFAULT NULL COMMENT '答案',
  `feditState` char(1) DEFAULT NULL COMMENT '0：未编辑，1：已编辑',
  `favailable` smallint(6) DEFAULT '0' COMMENT '审核状态&删除状态(-1:已删除，0：审核中，1：通过，2：退回)',
  `fcreateTime` datetime DEFAULT NULL COMMENT '该问答创建时间',
  `feditTime` datetime DEFAULT NULL COMMENT '更新/编辑时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

# 字符集与编码
## Unicode
Unicode背后的想法非常简单，然而却被普遍的误解了。
- Unicode就像一个电话本，标记着字符和数字之间的映射关系。
- 对支持字符的数量没有限制，也不要求字符必须占两个、三个或者其它任意数量的字节。
- Unicode字符是怎样被编码成内存中的字节这是另外的话题，它是被UTF(Unicode Transformation Formats)定义的。


## JAVA编码

1. **内码** :某种语言运行时，其char和string在内存中的编码方式。java中内码（运行内存）中的char使用UTF16的方式编码，一个char占用两个字节，但是某些字符需要两个char来表示。所以，一个字符会占用2个或4个字节。
2. **外码** :除了内码，皆是外码。源代码编译产生的目标代码文件（可执行文件或class文件）中的编码方式属于外码。java中外码中char使用UTF8的方式编码，一个字符占用1～4个字节。

JAVA采用16位（两个字节）的Unicode编码的char类型表示所有字符。输入输出时都需要和当前环境的编码互转。

代码点：是指一个编码表中的某个字符对应的代码值，也就是Unicode编码表中每个字符对应的数值。Unicode标准中，代码点采用16进制书写，并加上前缀U+ 。

代码单元：Char数据类型是一个采用UTF-16编码表示Unicode码点的代码单元，大多数常用的Unicode字符使用一个代码单元就可以表示，而辅助字符需要一对代码单元表示。



str在java中是unicode存储，打印字符串str用各种编码后的字节值。

```
byte[] bs = str.getBytes(encode);

for (byte b : bs) {
    int i = b&0xff;
    System.out.print(Integer.toHexString(i) + "\t");
}
```

## JAVA读中文文件

为了能够正确的读取中文内容
1. 必须了解文本是以哪种编码方式保存字符的
2. 使用字节流读取了文本后，再使用对应的编码方式去识别这些数字，得到正确的字符
    如本例，一个文件中的内容是字符中，编码方式是GBK，那么读出来的数据一定是D6D0。
    再使用GBK编码方式识别D6D0，就能正确的得到字符中

文本 –> stream --> bytes –>编码后 string

FileReader已经把字节根据某种编码识别成了字符

## 表示数据的字节序

计算机处理字节序的时候，不知道什么是高位字节，什么是低位字节。它只知道按顺序先读取低地址的字节。计算机的内部处理都是小端字节序，也就是低地址存储低位字节。

人类还是习惯读写大端字节序，也就是高位字节在前、低位字节在后。所以文件存储、网络传输都是大端字节序。
0x1234567.


>只有读取的时候，才必须区分字节序，其他情况都不用考虑。
口诀是：小端低低。



### 举例2：读取内存数据
比如处理器读取外部数据的时候，必须知道数据的字节序，将其转成正确的值。下面代码中， buf 是整个数据块在内存中的起始地址， offset 是当前正在读取的位置。
数据是大端字节序

```
x = buf[offset]<<8 | buf[offset+1];
 
```
数据是小端字节序
```
x = buf[offset+1]<<8 | buf[offset];
 
```

java代码检测系统字节序，并查看java内部默认字节序
```
import java.nio.ByteBuffer;
 
import java.nio.ByteOrder;
 
import java.util.Arrays;
 
 
 
public class TestByteOrder {
 
 
 
    public static void main(String[] args) {
 
 
 
        // windows平台的字节序是LITTLE_ENDIAN
 
        System.out.println("ByteOrder.nativeOrder():" + ByteOrder.nativeOrder());
 
 
 
        int x = 0x01020304;
 
 
 
        // By特
 
        ByteBuffer bb = ByteBuffer.wrap(new byte[4]);
 
        bb.asIntBuffer().put(x);
 
 
 
        String ss_before = Arrays.toString(bb.array());
 
 
 
        // 默认字节序 BIG_ENDIAN, 内存数据 [1, 2, 3, 4]
 
        System.out.println("默认字节序 " + bb.order().toString() + "," + " 内存数据 " + ss_before);
 
 
 
        bb.order(ByteOrder.LITTLE_ENDIAN);
 
        bb.asIntBuffer().put(x);
 
        String ss_after = Arrays.toString(bb.array());
 
 
 
        // 修改字节序 LITTLE_ENDIAN, 内存数据 [4, 3, 2, 1]
 
        System.out.println("修改字节序 " + bb.order().toString() + "," + " 内存数据 " + ss_after);
 
    }
 
}
 
 
 
```

参考： http://www.freebuf.com/articles/others-articles/25623.html
##  双字节字符集

GBK GB2312等通称 “ DBCS “（Double Byte Charecter Set 双字节字符集）。
最大的特点是：两字节长的汉字字符和一字节长的英文字符并存于同一套编码方案里。 因此他们写的程序为了支持中文处理，必须要注意字串里的每一个字节的值，如果这个值是大于127的，那么就认为一个双字节字符集里的字符出现了。那时候凡是受过加持，会编程的计算机僧侣们都要每天念下面这个咒语数百遍： “一个汉字算两个英文字符！一个汉字算两个英文字符……”
作者：于洋
链接： https://www.zhihu.com/question/23374078/answer/69732605

### GB2312
- 占用两个字节。
- 把汉字、数学符号、罗马希腊的字母、日文的假名、 ASCII 里本来就有的数字、标点、字母都统统重新编了两个字节长的编码，这就是常说的”全角”字符
- 而原来在127号以下的那些就叫”半角”字符。

### GBK
- 仍是两个字节。
- 把GB2312一些没有用的码位用上

 


作者：于洋

链接：https://www.zhihu.com/question/23374078/answer/69732605

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

 

## emoji


Unicode 只是规定了 Emoji 的码点和含义，并没有规定它的样式。举例来说，码点 U+1F600 表示一张微笑的脸，但是这张脸长什么样，则由各个系统自己实现。

因此，当我们输入这个 Emoji 的时候，并不能保证所有用户看到的都是同一张脸。如果用户的系统没有实现这个 Emoji 符号，用户就会看到一个没有内容的方框，因为系统无法渲染这个码点。

 目前， 苹果系统 、 安卓系统 、 Twitter 、 Github 、 Facebook 都有自己的 Emoji 实现

# 泛型

ArrayList heroList<? extends Hero> 表示这是一个Hero泛型或者其子类泛型。不能插入Hero，只能读

 ArrayList heroList<? super Hero> 表示这是一个Hero泛型或者其父类泛型，可以往里面插入Hero以及Hero的子类，但不确定取出来是Hero还是Object。

如果希望，又能插入，又能取出，就不要用通配符？



子类泛型不可以转换为父类泛型

> 假设可以转型成功
> 引用hs指向了ADHero泛型的容器
> 作为Hero泛型的引用hs, 看上去是可以往里面加一个APHero的。
> 但是hs这个引用，实际上是指向的一个ADHero泛型的容器
> 如果能加进去，就变成了ADHero泛型的容器里放进了APHero，这就矛盾了
>
> 所以子类泛型不可以转换为父类泛型 					  				  



可以从注解或泛型信息中获取服务名：

```java

```







# 多线程

## CAS

CAS是英文单词Compare And Swap的缩写，翻译过来就是比较并替换。

CAS机制当中使用了3个基本操作数：内存地址V，旧的预期值A，要修改的新值B。

更新一个变量的时候，只有当变量的预期值A和内存地址V当中的实际值相同时，才会将内存地址V对应的值修改为B。
链接：https://www.jianshu.com/p/ae25eb3cfb5d

## 概述

多线程的优势：

发挥多处理器的优势。

建模简单

异步的简化处理，线程的阻塞互不影响



缺点，带来以下问题：

安全性问题

活跃性问题

性能问题。线程切换开销大



定义：多个线程之间无论操作顺序，都要保证类的不变性（正确性）。比如不可变条件、后验条件约束仍然满足

Java 程序天生就是多线程程序，我们可以通过 JMX 来看一下一个普通的 Java 程序有哪些线程，代码如下。

```java
public class MultiThread {
	public static void main(String[] args) {
		// 获取 Java 线程管理 MXBean
	ThreadMXBean threadMXBean = ManagementFactory.getThreadMXBean();
		// 不需要获取同步的 monitor 和 synchronizer 信息，仅获取线程和线程堆栈信息
		ThreadInfo[] threadInfos = threadMXBean.dumpAllThreads(false, false);
		// 遍历线程信息，仅打印线程 ID 和线程名称信息
		for (ThreadInfo threadInfo : threadInfos) {
			System.out.println("[" + threadInfo.getThreadId() + "] " + threadInfo.getThreadName());
		}
	}
}
```

上述程序输出如下（输出内容可能不同，不用太纠结下面每个线程的作用，只用知道 main 线程执行 main 方法即可）：

```java
[5] Attach Listener //添加事件
[4] Signal Dispatcher // 分发处理给 JVM 信号的线程
[3] Finalizer //调用对象 finalize 方法的线程
[2] Reference Handler //清除 reference 线程
[1] main //main 线程,程序入口
```

从上面的输出内容可以看出：**一个 Java 程序的运行是 main 线程和多个其他线程同时运行**。

## 性能指标

​        **QPS（TPS）：**每秒钟request/事务 数量

​        **并发数：** 系统同时处理的request/事务数

​        **响应时间：**  一般取平均响应时间



访问一个页面会请求服务器3次，一次放，产生一个“T”，产生3个“Q” 

## 线程安全性

- 原子性
- 有序性
- 可见性
  volatile为变量提供可见性，但没有原子性
  只有变量写入内存中，其他线程才会看到。
  一个线程读取内存的值到缓存中修改后，写入之前线程2无法看到修改的值

**原子性**

多个竞态条件导致错误：

常见的是“先检查后执行”，检查时的观察结果可能立即就被其他线程改变。

读取-修改-写入。如计数器、序列生成器

类中即使所有状态变量都是线程安全的，仍然可能线程不安全。

> 要保持状态的一致性，就需要在单个原子操作中更新所有状态变量。 

**可见性**

加锁能保证可见性和原子性。

volatile：

- 变量不会被缓存在寄存器中。
- 一般用于状态flag。
- 不能保证操作的原子性，仅保证可见性。
- 如果对可见性有很复杂的判断，不要用volatile



**一些线程安全的类**如下

BlockingQueue StringBuffer Hashtable、synchronizedMap、ConcurrentMap Vector、synchronizedSet

其中，StringBuffer 是线程安全的，StringBuilder 是非线程安全的

Vector（继承了ArrayList）是线程安全的类，而ArrayList是非线程安全的

因为不需要同步，非线程安全的比线程安全的 快，因此不需要同步时用StringBuilder 、ArrayList。

把非线程安全的集合转换为线程安全

```java
List<Integer> list1 = ``new` `ArrayList<>();
List<Integer> list2 = Collections.synchronizedList(list1);
private static Collection<BitCoinServer> servers = Collections.synchronizedCollection(new ArrayList<BitCoinServer>());
```

## 线程

### 上下文切换

多线程编程中一般线程的个数都大于 CPU 核心的个数，而一个 CPU  核心在任意时刻只能被一个线程使用，为了让这些线程都能得到有效执行，CPU  采取的策略是为每个线程分配时间片并轮转的形式。当一个线程的时间片用完的时候就会重新处于就绪状态让给其他线程使用，这个过程就属于一次上下文切换。

概括来说就是：当前任务在执行完 CPU 时间片切换到另一个任务之前会先保存自己的状态，以便下次再切换回这个任务时，可以再加载这个任务的状态。**任务从保存到再加载的过程就是一次上下文切换**。

### 守护线程

守护线程的概念是： 当一个进程里，所有的线程都是守护线程的时候，结束当前进程。

守护线程通常会被用来做日志，性能统计、移除过期缓存等“内部” 工作。

主线程和子线程没有区别，主线程结束如果存在其他非守护线程，jvm不退出。

### 线程状态

New: 当线程对象创建时存在的状态，此时线程不可能执行；

Runnable：当调用thread.start()后，线程变成为Runnable状态。只要得到CPU，就可以执行；

Running：线程正在执行；

Waiting：执行thread.join()或在锁对象调用obj.wait()等情况就会进该状态，表明线程正处于等待某个资源或条件发生来唤醒自己；

Time_Waiting：执行Thread.sleep(long)、thread.join(long)或obj.wait(long)等就会进该状态，与Waiting的区别在于Timed_Waiting的等待有时间限制；

Blocked：如果进入同步方法或同步代码块，没有获取到锁，则会进入该状态；

Dead：线程执行完毕，或者抛出了未捕获的异常之后，会进入dead状态，表示该线程结束







![](img\线程状态转换.png)

由上图可以看出：

1. 线程创建之后它将处于 **NEW（新建）** 状态，调用 `start()` 方法后开始运行，线程这时候处于 **READY（可运行）** 状态。可运行状态的线程获得了 CPU 时间片（timeslice）后就处于 **RUNNING（运行）** 状态。

2. 进入等待状态的线程需要依靠其他线程的通知才能够返回到RUNNABLE 状态
3. 而 **TIME_WAITING(超时等待)** 状态相当于在等待状态的基础上增加了超时限制，当超时时间到达后 Java 线程将会返回到 RUNNABLE 
4. 当线程调用同步方法时，在没有获取到锁的情况下，线程将会进入到 **BLOCKED（阻塞）** 状态。
5. 线程在执行 Runnable 的`run()`方法之后将会进入到 **TERMINATED（终止）** 状态。

还有两个图这里未贴出，在java/img目录下。



其次，对于jstack日志，我们要着重关注如下关键信息

Deadlock：表示有死锁

Waiting on condition：等待某个资源或条件发生来唤醒自己。具体需要结合jstacktrace来分析，比如线程正在sleep，网络读写繁忙而等待。可能是WAITING或TIMED_WAITING状态。

Blocked：阻塞

Waiting on monitor entry：在等待获取锁

in Object.wait()：获取锁后又执行obj.wait()放弃锁

> 对于Waiting on monitor entry 和 in Object.wait()的详细描述：Monitor是  Java中用以实现线程之间的互斥与协作的主要手段，它可以看成是对象或者 Class的锁。每一个对象都有，也仅有一个  monitor。从下图中可以看出，每个 Monitor在某个时刻，只能被一个线程拥有，该线程就是 "Active Thread"，而其它线程都是 "Waiting Thread"，分别在两个队列 " Entry Set"和 "Wait Set"里面等候。在 "Entry  Set"中等待的线程状态是 "Waiting for monitor entry"，而在 "Wait Set"中等待的线程状态是 "in  Object.wait()"

 如果说系统慢，那么要特别关注Blocked,Waiting on condition 



join

主线程调用thread1.join()，会让主线程进入TIMED_WAITING状态，直到线程thread1结束，主线程继续；

通常用于在main()主线程内，等待其它线程完成再结束main()主线程。

线程池的awaitTermination类似join，阻塞等待任务都完成。

### 线程方法

t.join，即表明在主线程中加入该线程。主线程会等待该线程结束完毕， 才会往下运行

当线程处于竞争关系的时候，优先级高的线程会有更大的几率获得CPU资源

` t1.setPriority(Thread.MAX_PRIORITY)`



当前线程临时暂停，变为就绪状态，使得其他线程可以有更多的机会占用CPU资源

`Thread.yield()`



Thread.sleep()

1. sleep是帮助其他线程获得运行机会的最好方法，但是如果当前线程获取到的有锁，sleep不会让出锁。
2. 线程睡眠到期自动苏醒，并返回到可运行状态（就绪），不是运行状态。
3. 优先线程的调用，现在苏醒之后，并不会里面执行，所以sleep()中指定的时间是线程不会运行的最短时间，sleep方法不能作为精确的时间控制。
   3、sleep()是静态方法，只能控制当前正在运行的线程（示例就是这样调用的，因为类对象可以调用类的静态方法）。



### 创建线程

1. 继承Thread类，启动线程是start()方法
2. 实现Runnable接口，启动线程是start()方法
3. 匿名类的方式，启动线程是start()方法

## AtomicInteger 

 AtomicInteger 类主要利用 CAS (compare and swap) + volatile 和 native 方法来保证原子操作，从而避免 synchronized 的高开销，执行效率大为提升。 

## 内置锁

特点：

1. 锁保护变量（对象）。每次访问这个变量时都需要获得锁。这样就确保同一时刻仅有一个线程访问这个变量。
2. 多个线程都能看到共享变量的最新值。
3. 可重入
4. 获取锁的操作的粒度是”线程“，而不是”调用“

使用方式：

- 修饰静态方法: 访问静态 synchronized 方法占用的锁是当前类的锁
- 修饰实例方法: 而访问非静态 synchronized 方法占用的锁是当前实例对象锁。
- 修饰代码块
- 任意对象都可以用来作为同步对象.

**可重入**

如果内置锁不可重入，那么以下代码会死锁。

```java
class Widget {
    public synchronized void do1() {
        ...
        do2();
    }
        public synchronized void do2() {
        ...
    }
}
```

**常见的加锁约定**：

所有可变状态都封装在对象内部，对所有访问可变状态的代码都使用对象的内置锁同步。

> 当类的不变性涉及多个状态时，它们都必须由同一个锁来保护。

synchronized仅能保证单个操作的原子性，降低了并发性（活跃性和性能），因此去掉整个方法上的synchronized。可以提取出耗时较长、不需要同步的部分，同步的部分尽可能短

```java
synchronized(this){
    //根据入参判断是否命中缓存
    ++cacheHits;
    result = getResultFromCache(params);
}
if(result == null) {
    result = cal(params);
    synchronized(this){
        //更新缓存
    }
}
```

但加锁、释放锁都有开销，也不能拆的太细。

 Java 6 之后 Java 官方对从 JVM 层面对synchronized 较大优化，所以现在的 synchronized 锁效率也优化得很不错了 



实例，双重校验锁实现对象单例（线程安全）

```java
public class Singleton {
    private volatile static Singleton uniqueInstance;

    private Singleton() {
    }

    public static Singleton getUniqueInstance() {
       //先判断对象是否已经实例过，没有实例化过才进入加锁代码
        if (uniqueInstance == null) {
            //类对象加锁
            synchronized (Singleton.class) {
                if (uniqueInstance == null) {
                    uniqueInstance = new Singleton();
                }
            }
        }
        return uniqueInstance;
    }
}
```

uniqueInstance 采用 volatile 关键字修饰也是很有必要的， uniqueInstance = new Singleton(); 这段代码其实是分为三步执行：

1. 为 uniqueInstance 分配内存空间
2. 初始化 uniqueInstance
3. 将 uniqueInstance 指向分配的内存地址

但是由于 JVM 具有指令重排的特性，执行顺序有可能变成  1->3->2。指令重排在单线程环境下不会出现问题，但是在多线程环境下会导致一个线程获得还没有初始化的实例。例如，线程 T1 执行了 1 和 3，此时 T2 调用 getUniqueInstance() 后发现 uniqueInstance 不为空，因此返回  uniqueInstance，但此时 uniqueInstance 还未被初始化。

使用 volatile 可以禁止 JVM 的指令重排，保证在多线程环境下也能正常运行。



直接加上synchronized ，其所对应的同步对象，就是this

```java
    public synchronized void recover(){
        hp=hp+1;
    }
```

一个对象的两个不同的synchronized方法，也会抢夺对象锁。
给一个类中的方法加上synchronized，必须考虑给该类中所有修改该资源的方法加锁。



**同步对象**

JVM会为一个使用内部锁（synchronized）的对象维护两个集合，**Entry Set**和**Wait Set**。

- 抢夺锁的线程进入Entry Set，并且处于线程的BLOCKED状态。
- await后额线程会临时释放锁，进入WAITING状态（Wait Set）。

 wait方法和notify方法，并不是Thread线程上的方法，它们是Object上的方法。

wait和notify是同步对象上的方法，必须在占用了对象锁之后执行。

wait()

- 让占用了这个同步对象的线程，临时释放当前的占用，使当前线程阻塞。并且等待直到被notify或中断。 
- 调用wait的前提是 必须先获得锁，一定是在synchronized块里，否则就会出错。
- 如果wait后其他线程不notify，它就没有机会继续执行。
- 永远都要把wait()放到循环语句。因为wait()的线程永远不能确定其他线程会在什么状态下notify()

notify()

- 通知一个等待在这个同步对象上的线程，你可以苏醒过来了，有机会重新占用当前对象了。之前调用过wait方法的线程就会解除wait状态，再次占用锁后继续向下运行。
- *notify*并*不*释放锁，只是通知。

notifyAll() 

- 通知所有的等待在这个同步对象上的线程，你们可以苏醒过来了，有机会重新占用当前对象了。 

## 对象共享

### 临界区

临界数据指多个进程（或线程）会竞争修改的数据。

临界区指修改临界数据的代码区域。

原子操作指临界区的代码不会被这个临界数据的其他临界区的代码打断。

### 线程封闭

不共享数据，仅在单线程内访问数据，不需要同步。

常见应用：

jdbc连接池，Connection对象在归还之前，不会被分配给其他线程。 

java支持：局部变量、ThreadLocal

### 不可变对象

不可变对象一定是线程安全的。

- 不可变对象内部可以使用可变对象。

- 不可变对象的状态，通过构造函数初始化。而构造函数是线程安全的。

- 不可变对象状态的更新，通过一个新状态的实例替换原有对象。

不可变对象配合volatile，保证可见性，实现了弱原子性保证线程安全。

```java
BigInteger[] factors = cache.getFactores(i);//cache是使用volatile发布的不可变对象
```

Collections.unmodifiableMap(Map map) . 将为其返回一个不可修改视图的映射, 返回的Map不能put remove 操作, 但可以对里的对象进行操作 。

### 发布对象



安全发布只能确保发布当时状态的可见性。

不可变对象可以任意机制发布。

事实不可变对象、可变对象如果未被正确发布，线程看到的引用最新，状态的值却可能失效（Object的构造函数也会给所有成员创建默认值）

可变对象安全发布的方式：

- 静态初始化函数中初始化
- 引用保存到volatile或AtomicReferance的域中
- 构造对象的final域中
- 引用保存到由锁保护的域中（如线程安全的容器类）

构造内部类的实例时，会引用this。需要避免this溢出。可以使用工厂方法。

### volatile

 变量声明为**volatile**，这就指示 JVM，这个变量是不稳定的，每次使用它都到主存中进行读取。

volatile关键字能保证数据的可见性，但不能保证数据的原子性。synchronized关键字两者都能保证。

## 同步容器类

将状态封装，对每个方法进行同步加锁。
包括Vector Hashtable Collections.synchronizedXxx等。在迭代期间，size和get方法之间如果有线程修改容器使它变小，则索引值不再有效，抛出异常。
容器的hashcode equals containsAll 迭代过程中需要对容器加锁。

Collections.synchronizedMap() 对整个map加锁，类似Hashtable

Collections.unmodifiableMap(Map map) . 将为其返回一个不可修改视图的映射, 返回的Map不能put remove 操作, 但可以对里的对象进行操作 。

## 并发容器

### ConcurrentHashMap

**jdk1.7的ConcurrentHashMap：**

实现更加精细， 把map分为多个Segment独立加锁，性能更好。有些方法需要跨段，比如size()和containsValue()，需要锁定整个表而而不仅仅是某个段，这需要按顺序锁定所有段，操作完毕后，又按顺序释放所有段的锁

**jdk1.8的ConcurrentHashMap：**

ConcurrentHashMap取消了Segment分段锁，采用CAS和synchronized来保证并发安全。数据结构跟HashMap1.8的结构类似，数组+链表/红黑二叉树。Java 8在链表长度超过一定阈值（8）时将链表（寻址时间复杂度为O(N)）转换为红黑树（寻址时间复杂度为O(log(N))）

synchronized只锁定当前链表或红黑二叉树的首节点，这样只要hash不冲突，就不会产生并发，效率又提升N倍。



### CopyOnWriteArrayList

CopyOnWriteArrayList 只在增删改上加锁，读不加锁而是从一个事实不可变的容器副本中读取（写时复制）

`CopyOnWriteArrayList` 类的所有可变操作（add，set  等等）都是通过创建底层数组的新副本来实现的。当 List  需要被修改的时候，我并不修改原有内容，而是对原有数据进行一次复制，将修改的内容写入副本。写完之后，再将修改完的副本替换原来的数据，这样就可以保证写操作不会影响读操作了。

从 `CopyOnWriteArrayList` 的名字就能看出`CopyOnWriteArrayList` 是满足`CopyOnWrite` 的 ArrayList，所谓`CopyOnWrite` 也就是说：在计算机，如果你想要对一块内存进行修改时，我们不在原有内存块中进行写操作，而是将内存拷贝一份，在新的内存中进行写操作，写完之后呢，就将指向原来内存指针指向新的内存，原来的内存就可以被回收掉了。

### 阻塞队列

简化了生产者-消费者模式，促进了线程封闭——只是转移了对象的所有权

如爬虫程序是生产者，索引程序是消费者

如果生产者比消费者快，可以使用有界队列，避免积攒过多任务耗尽内存

BlockingQueue

常用LinkedBlockingQueue

BlockingQueue添加和移除元素的api：

|          | *抛出异常*                                                   | *特殊值*                                                     | *阻塞*                                                       | *超时*                                                       |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **插入** | [`add(e)`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`offer(e)`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`put(e)`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`offer(e, time, unit)`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) |
| **移除** | [`remove()`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`poll()`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`take()`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`poll(time, unit)`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) |
| **检查** | [`element()`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | [`peek()`](https://blog.csdn.net/wei_ya_wen/article/details/19344939) | *不可用*                                                     | *不可用*                                                     |

**ArrayBlockingQueue**

BlockingQueue 接口的有界队列实现类。实现：一个对象数组+一把锁+两个条件

- 底层采用**数组**来实现。ArrayBlockingQueue 一旦创建，容量不能改变
- 入队与出队都用同一把锁
- 在只有入队高并发或出队高并发的情况下，因为操作数组，且不需要扩容，性能很高
- 支持公平锁，让最先等待的线程能够最先访问到 ArrayBlockingQueue



**LinkedBlockingQueue**

基于**单向链表**实现的阻塞队列

实现：一个单向链表+两把锁+两个条件

- 可以当做无界队列也可以当做有界队列来使用，同样满足 FIFO 的特性
- 链表，最大容量为整数最大值，可看做容量无限
- 有效的避免了入队与出队时使用一把锁带来的竞争。
- 入队与出队都高并发的情况下，性能比ArrayBlockingQueue高很多

为了防止 LinkedBlockingQueue  容量迅速增，损耗大量内存。通常在创建 LinkedBlockingQueue 对象时，会指定其大小

**ConcurrentSkipListMap**

高并发的有序map

## 对象组合

### 容器类

非线程安全的对象，可以通过锁来保护它，或者线程封闭实现线程安全。

容器类本身通过加锁可以实现容器本身的线程安全，但如果其中存储的Person对象引用发布出去，还需要额外的同步，比如使Person成为线程安全类。

如果使用线程安全的容器类ConcurrentHashMap，里面存储线程安全的对象Point：

1. Point可变。线程1修改一个PointA之后，线程2可以从容器类中访问PointA也会及时看到。
2. Point不可变。线程1修改了key对应PointA为PointB，线程2读取到的map里也会同步为PointB。





并发容器









### 委托

一个类有多个独立且线程安全的状态变量，可以把线程安全性委托为底层状态变量。

举例，CounterServlet仅保存一个数字状态，可以把线程安全性委托给AtomicLong。但必须使用final AtomicLong，防止线程看到的引用不同和竞态条件。

状态变量不受任何不变性条件约束，且线程安全，发布出去不会破坏线程安全性。

比如记录车辆位置的Point，不变性条件是：x，y只能同时变化，不能是车辆未经过的坐标

### 扩展原子操作

无论以下哪种扩展方式，必须和其他操作使用相同的锁保护数据。

- 继承后扩展原子操作。
- 公有域封装线程安全对象，扩展原子操作。
- 组合。私有域封装对象，所有操作都是原子操作，相当于Java监视器模式。

继承和公有域的组合，两种不推荐，因为同步的代码分布在多个类中，更脆弱难以保证同一把锁。



## 同步工具类

闭锁：
闭锁到达结束状态之后，才允许线程通过。用来确保某些活动直到其他活动都完成后才继续执行。
比如服务或资源都有自己的闭锁，可以用来排依赖的先后顺序。

FutureTask：
- 可以用来提前加载稍后需要的数据

  ```java
  thread = new Thread(futureTask);
  thread.start();
  futureTask.get();//阻塞方法
  ```

  

信号量可以用于：
- 实现资源池。许可的初始数量和资源数量相等，请求一个资源时必须先获取一个许可，归还是释放许可，因此请求时资源为空会阻塞直到池中有资源。
- 实现有界阻塞容器。许可的初始数量设置为最大长度，add操作获取许可，remove操作释放许可。

构建高效和可伸缩的结果缓存。对计算任务类进行包装（装饰器模式)
用ConcurrentHashMap和FutureTask缓存计算任务，避免重复计算

### Condition

ReentrantLock对象上可以生成Conditioin。

- Condition是当前线程在所属锁上的“条件”，如等待临时出让锁、唤醒其他线程。
- 多个线程可以用一个condition对象在同一处进行同步。
- 一个锁可以有多个Condition对象。
- Condition对象一般用业务条件命名，比如notFull表示队列未满，notFull.await()代表当前线程等待队列未满。

`Condition.await`相当于object.wait()。当前线程一直等到

- 直到获取信号（被其他线程当前condition.Signal SignAll）。返回`await`之前重新获得锁
- 其他线程调用了当前线程的中断	
- 当前线程被假唤醒  

  

 **公平锁就是先等待的线程先获得锁** 

### ReentrantLock

synchronized和ReentrantLock 都是可重入锁。也就是 自己可以再次获取自己的内部锁， 锁的计数器都自增1，所以要等到锁的计数器下降为0时才能释放锁。 

https://www.cnblogs.com/takumicx/p/9338983.html

特点：

- 等待可中断。 
- 可实现公平锁。
- 可实现选择性通知（锁可以绑定多个条件）

**公平锁**

大部分情况下我们使用非公平锁，因为其性能比公平锁好很多。但是公平锁能够避免线程饥饿，某些情况下也很有用,可以通过 ReentrantLock类的ReentrantLock(boolean fair)构造方法指定。

```java
ReentrantLock lock = new ReentrantLock(true);
```

**等待中断**

当使用synchronized实现锁时,阻塞在锁上的线程除非获得锁否则将一直等待下去，也就是说这种无限等待获取锁的行为无法被中断。而ReentrantLock给我们提供了一个可以响应中断的获取锁的方法`lockInterruptibly()`。该方法可以用来解决死锁问题。

```java
public class ReentrantLockTest {
    static Lock lock1 = new ReentrantLock();
    static Lock lock2 = new ReentrantLock();
    public static void main(String[] args) throws InterruptedException {

        Thread thread = new Thread(new ThreadDemo(lock1, lock2));//该线程先获取锁1,再获取锁2
        Thread thread1 = new Thread(new ThreadDemo(lock2, lock1));//该线程先获取锁2,再获取锁1
        thread.start();
        thread1.start();
        thread.interrupt();//是第一个线程中断
    }

    static class ThreadDemo implements Runnable {
        Lock firstLock;
        Lock secondLock;
        public ThreadDemo(Lock firstLock, Lock secondLock) {
            this.firstLock = firstLock;
            this.secondLock = secondLock;
        }
        @Override
        public void run() {
            try {
                firstLock.lockInterruptibly();
                TimeUnit.MILLISECONDS.sleep(10);//更好的触发死锁
                secondLock.lockInterruptibly();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                firstLock.unlock();
                secondLock.unlock();
                System.out.println(Thread.currentThread().getName()+"正常结束!");
            }
        }
    }
}
```

上面例子中，主线程使其中一个线程中断，被中断的线程将抛出异常，而另一个线程将能获取锁后正常结束。

`tryLock()`,可以选择传入时间参数,表示等待指定的时间。使用该方法配合失败重试机制可以更好的解决死锁问题

```
while(!lock1.tryLock()){
	TimeUnit.MILLISECONDS.sleep(10);
}
```

**选择性通知**

-  synchronized关键字与wait()和notify()/notifyAll()方法相结合可以实现等待/通知机制，被通知的线程是由 JVM 选择的
- 用ReentrantLock类结合Condition实例可以实现“选择性通知”， Condition实例的signalAll()方法 只会唤醒注册在该Condition实例中的所有等待线程。 

### 示例：线程执行顺序

多块代码在多线程条件下，如果要求有执行顺序，可以构造线程屏障。最后要唤醒其他所有线程，保证所有线程都去检测状态

```java
class Foo {

    public Foo() {
        
    }

    Object lock = this;
    volatile boolean firstFinished = false;
    volatile boolean secondFinished = false;

    public void first(Runnable printFirst) throws InterruptedException {
        
        // printFirst.run() outputs "first". Do not change or remove this line.
        synchronized (lock) {
            printFirst.run();
            firstFinished = true;
            lock.notifyAll();
        }
    }

    public void second(Runnable printSecond) throws InterruptedException {
        
        // printSecond.run() outputs "second". Do not change or remove this line.
        synchronized (lock) {
            while (!firstFinished) {
                lock.wait();
            }
            printSecond.run();
            secondFinished = true;
            lock.notifyAll();
        }
    }

    public void third(Runnable printThird) throws InterruptedException {
        
        // printThird.run() outputs "third". Do not change or remove this line.
        synchronized (lock) {
            while (!firstFinished || !secondFinished) {
                lock.wait();
            }
        }
        printThird.run();
    }

}
```

也可以用一个volatile变量，不需要同步

```
private volatile int nums = 0;

...
while(nums!=1){
continue;
}
// printSecond.run() outputs "second". Do not change or remove this line.
printSecond.run();
nums = nums+1;
```

或者定义两个闭锁，前n-1个方法对应n-1个闭锁，第k个方法等待第k-1个方法上的闭锁

```java
countDownLatchOne = new CountDownLatch(1);
countDownLatchTwo = new CountDownLatch(1);

countDownLatchA.await();
printSecond.run();
countDownLatchB.countDown();
```



## 任务执行

每个请求一个新线程：

- 线程生命周期的开销大，如果请求频率高处理轻量级，代价太大。

- 空闲线程占用系统资源，如内存。

- 线程数量存在限制。
- 高负载性能下降快，直至崩溃

### Callable

 **`Runnable` 接口**不会返回结果或抛出检查异常，但是**`Callable` 接口**可以 

### submit

execute()方法用于提交不需要返回值的任务，所以无法判断任务是否被线程池执行成功与否；

submit()方法用于提交需要返回值的任务。线程池会返回一个 Future 类型的对象，通过这个 Future 对象可以判断任务是否执行成功

### 线程池

https://github.com/Snailclimb/JavaGuide/blob/master/docs/java/Multithread/JavaConcurrencyAdvancedCommonInterviewQuestions.md

**创建线程池**

 《阿里巴巴Java开发手册》中强制线程池不允许使用 Executors 去创建，而是通过 ThreadPoolExecutor 的方式，这样的处理方式让写的同学更加明确线程池的运行规则，规避资源耗尽的风险 

`ThreadPoolExecutor`构造函数重要参数分析

**`ThreadPoolExecutor` 3 个最重要的参数：**

- **`corePoolSize` :** 核心线程数线程数定义了最小可以同时运行的线程数量。
- **`maximumPoolSize` :** 当队列中存放的任务达到队列容量的时候，当前可以同时运行的线程数量变为最大线程数。
- **`workQueue`:** 当新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，新任务就会被存放在队列中。

`ThreadPoolExecutor`其他常见参数:

1. **`keepAliveTime`**:当线程池中的线程数量大于 `corePoolSize` 的时候，如果这时没有新的任务提交，核心线程外的线程不会立即销毁，而是会等待，直到等待的时间超过了 `keepAliveTime`才会被回收销毁；
2. **`unit`** : `keepAliveTime` 参数的时间单位。
3. **`threadFactory`** :executor 创建新线程的时候会用到。
4. **`handler`** :饱和策略

```
最佳线程数目 = （（线程等待时间+线程CPU时间）/线程CPU时间 ）* CPU数目
= （线程等待时间与线程CPU时间之比 + 1）* CPU数目
```

比如平均每个线程CPU运行时间为0.5s，而线程等待时间（非CPU运行时间，比如IO）为1.5s，CPU核心数为8，那么根据上面这个公式估算得到：((0.5+1.5)/0.5)*8=32。这个公式进一步转化为：

| `1`  | `最佳线程数目 = |
| ---- | --------------- |
|      |                 |

可以得出一个结论：

**线程等待时间所占比例越高，需要越多线程。线程CPU时间所占比例越高，需要越少线程。**

提交callableTask

```java
future = executor.submit(callableTask);
//...
future.get(); //返回值。可能抛出一个异常
future.get(timeLeft, NANOSECONDS);//为任务设置时限

completionService.submit()；//示例：并发下载、渲染图片资源.下载完成后立即显示出来，图片资源之间无顺序
futures = executor.invokeAll(callableTasks, time, unit); //批量提交，并设置时限
```

同步关闭线程池

```java
executor.awaitTermination()
executor.shutdown()
```

### 线程停止

持有线程的服务，如果存在时间大于创建线程的方法的存在时间，那么要提供生命周期方法如shutdown().

如果服务需要持有线程，可以把管理线程的工作委托给ExecutorService。举例，多个生产者提交日志，消费者线程写入日志文件。





### shutdown hook

jvm停止时，程序中多个关闭钩子会并发执行。为了避免竞态条件或死锁，应该对所有服务（功能）使用同一个关闭钩子。

```java
Runtime.getRuntime().addShutdownHook(new Thread(){});
```

### 任务取消与关闭

关闭的场景：

- 用户请求取消
- 应用程序其中一个任务完成最终目标。如搜索
- 操作有时间限制。
- 错误。如爬虫磁盘空间满。
- 关闭程序

时也要

中断：

- 实现取消的最合理方式

```java
class Thread {
    interrupt();// 发送请求中断（其他）线程的信号
    isInterrupted(); //判断（当前）线程是否中断
    interrupted();//清除（当前）线程中断状态
}
```

合理的中断策略。在某个取消点捕获中断异常后，有几种做法：

- 线程原本就将要结束，那么捕获后清理工作，结束。只有实现了线程中断策略的代码（自定义的Task）才可以屏蔽中断
- 重新抛出异常或恢复中断状态



超时取消线程的方式：

- 定时任务中断task线程，但任务run方法内部的异常需要先捕获，在明确的位置重新抛出。
- future.get来捕获异常

```java
Future<?> future = taskExec.submit(r);
try{
 	future.get(timeout, unit);   
} catch(TimeoutExecption e) {
    
} catch(Execu.. e){
    throw ...
} finally {
    future.cancel(true);
}


```



### 未捕获异常处理

1. 继承Thread.UncaughtExceptionHandler
2. 为ThreadPoolExecutor设置ThreadFactory
3. 通过execute提交的任务，才能把异常交给UncaughtExceptionHandler处理。submit提交的任务会通过future.get抛出异常。



## 生产消费者模型

```java
 public void produce() {
        synchronized (this) {
            while (mBuf.isFull()) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            mBuf.add();
            notifyAll();
        }
    }

    public void consume() {
        synchronized (this) {
            while (mBuf.isEmpty()) {
                try {
                    wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            mBuf.remove();
            notifyAll();
        }

    }
```



消费者1拿到了锁，判断buffer为空，那么wait()

消费者2拿到了锁，同样buffer为空，wait()

生产者1拿到锁，生产，buffer满，notify --> 可能生产者2被唤醒（也可能消费者1被唤醒）

生产者2拿到锁，buffer是满的，wait()

消费者1拿到了锁，消费，notify –->唤醒消费者2后，如果生产者1退出不再竞争锁，则生产者2和消费者3陷入互相等待中（死锁）。





LinkedBlockingQueue的putLock对入队操作加锁，takeLock对出队操作加锁。

入队操作：

- 获取putLock
- 生产前队列已满，则当前（入队）线程等待，直到队列不满
- 入队
- 入队后如果队列仍然不满，通知其他等待入队的线程
- 释放putLock
- 入队后如果队列由空变非空，通知
- 释放putLock

出队操作：

- 获取takeLock
- 出队前队列为空，则当前出队线程等待，直到队列非空
- 出队
- 出队后队列如果仍然非空，通知其他等待出队的线程
- 释放takeLock
- 如果队列由满变非满，通知等待入队的线程。

实现如LinkedBlockingQueue，notEmpty条件用来（通知）同步出队线程，notFull条件用来同步入队线程。

```java
private final ReentrantLock takeLock = new ReentrantLock();

/** Wait queue for waiting takes */
private final Condition notEmpty = takeLock.newCondition();

/** Lock held by put, offer, etc */
private final ReentrantLock putLock = new ReentrantLock();

/** Wait queue for waiting puts */
private final Condition notFull = putLock.newCondition();
```

## 悲观锁

总是假设最坏的情况，每次去拿数据的时候都认为别人会修改，所以每次在拿数据的时候都会上锁。传统的关系型数据库里边就用到了很多这种锁机制，比如行锁，表锁等，读锁，写锁等，都是在做操作之前先上锁。Java中`synchronized`和`ReentrantLock`等独占锁就是悲观锁思想的实现。

## 乐观锁

总是假设最好的情况，每次去拿数据的时候都认为别人不会修改，所以不会上锁，但是在更新的时候会判断一下在此期间别人有没有去更新这个数据，可以使用版本号机制和CAS算法实现。**乐观锁适用于多读的应用类型，这样可以提高吞吐量**，像数据库提供的类似于**write_condition机制**，其实都是提供的乐观锁。在Java中`java.util.concurrent.atomic`包下面的原子变量类就是使用了乐观锁的一种实现方式**CAS**实现的。

**版本号机制实现**

一般是在数据表中加上一个数据版本号version字段，表示数据被修改的次数，当数据被修改时，version值会加一。当线程A要更新数据值时，在读取数据的同时也会读取version值，在提交更新时，若刚才读取到的version值为当前数据库中的version值相等时才更新，否则重试更新操作，直到更新成功。



## 死锁

A线程占有了资源1不释放，等待占有资源2

B线程占有了资源2不释放，等待占有资源1

下面模拟AB线程死锁：

```java
public class DeadLockDemo {
    private static Object resource1 = new Object();//资源 1
    private static Object resource2 = new Object();//资源 2

    public static void main(String[] args) {
        new Thread(() -> {
            synchronized (resource1) {
                System.out.println(Thread.currentThread() + "get resource1");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread() + "waiting get resource2");
                synchronized (resource2) {
                    System.out.println(Thread.currentThread() + "get resource2");
                }
            }
        }, "线程 1").start();

        new Thread(() -> {
            synchronized (resource2) {
                System.out.println(Thread.currentThread() + "get resource2");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println(Thread.currentThread() + "waiting get resource1");
                synchronized (resource1) {
                    System.out.println(Thread.currentThread() + "get resource1");
                }
            }
        }, "线程 2").start();
    }
}
```

## 活锁 LiveLock

任务或者执行者没有被阻塞，由于某些条件没有满足，导致一直重复尝试、失败、尝试、失败。

活锁和死锁的区别在于，处于活锁的实体是在不断的改变状态，所谓的“活”， 而处于死锁的实体表现为等待；活锁有可能自行解开，死锁则不能。

生活中的典型例子： 两个人在窄路相遇，同时向一个方向避让，然后又向另一个方向避让，如此反复。

计算机中的例子：两个线程发生了某些条件的碰撞后重新执行，那么如果再次尝试后依然发生了碰撞，长此下去就有可能发生活锁。

**活锁的解决方法：**

- 比如引入一些随机性。例如如果检测到冲突，那么就暂停随机的一定时间进行重试。这回大大减少碰撞的可能性。 典型的例子是以太网的CSMA/CD检测机制。
- 加入一定的重试次数也是有效的解决办法。
- 约定重试机制避免再次冲突。 例如自动驾驶的防碰撞系统（假想的例子），可以根据序列号约定检测到相撞风险时，序列号小的飞机朝上飞， 序列号大的飞机朝下飞。

作者：专职跑龙套

链接：https://www.jianshu.com/p/dc179210bc62

来源：简书

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



# JDK版本

查看class文件（16进制），前8个字节：
cafe babe 0000 0033 (jdk编译出来并用sublime打开显示）

前四个字节是Java class的特殊符号，叫做magic字段，用来告诉JVM这是个class文件

之后的两个字节是minor版本号

再之后的两个字节是major版本号，我们看到时33，对应下表我们知道33时JDK1.7编译的版本号。

 

十六进制

JDK1.5      31

JDK1.6      32

JDK1.7      33

JDK8         34

 

因为Java是向后兼容的，所以高版本的兼容低版本的，所以有时候你遇到java报： unsupported major.minor version 51，那就是你用低版本的虚拟机去运行高版本JDK编译的class文件了，所以低版本的虚拟机就抱怨了。这里的51是十进制，也就是十六进制的33，及对应JDK1.7，如果出现这种错误，你肯定是使用低于1.7版本的虚拟机去运行这个了。

 也可以使用命令：

```
javap -v IdentNoVerifyTS.class
 
WINDOWS> javap -verbose MyClass | find "version"
LINUX  > javap -verbose MyClass | grep version
 
```

找到其中的major version。51对应的是十六进制的33，也就是1.7版本

# 自定义注解

@Target({METHOD,TYPE}) 表示这个注解可以用用在类/接口上，还可以用在方法上
@Retention(RetentionPolicy.RUNTIME) 表示这是一个运行时注解，即运行起来之后，才获取注解中的相关信息，而不像基本注解如[@Override ](http://how2j.cn/k/annotation/annotation-system/1060.html#step4028)那种不用运行，在编译时eclipse就可以进行相关工作的编译时注解。
@Inherited 表示这个注解可以被子类继承
@Documented 表示当执行javadoc的时候，本注解会生成相关文档

# Log4j

log4j日志输出格式一览：
%c 输出日志信息所属的类的全名
%d 输出日志时间点的日期或时间，默认格式为ISO8601，也可以在其后指定格式，比如：%d{yyy-MM-dd HH:mm:ss }，输出类似：2002-10-18- 22：10：28
%f 输出日志信息所属的类的类名
%l 输出日志事件的发生位置，即输出日志信息的语句处于它所在的类的第几行
%m 输出代码中指定的信息，如log(message)中的message
%n 输出一个回车换行符，Windows平台为“rn”，Unix平台为“n”
%p 输出优先级，即DEBUG，INFO，WARN，ERROR，FATAL。如果是调用debug()输出的，则为DEBUG，依此类推
%r 输出自应用启动到输出该日志信息所耗费的毫秒数
%t 输出产生该日志事件的线程名

# 计算最后一页

last需要根据总数total和每页有多少条数据count来计算得出。

同时，还要看total是否能够整除count
假设总数是50，是能够被5整除的，那么最后一页的开始就是45

if (0 == total % count)
  last = total - count;


假设总数是51，不能够被5整除的，那么最后一页的开始就是50

last = total - total % count;

# Mybatis

## 配置

属性设置

http://www.mybatis.org/mybatis-3/zh/configuration.html#properties

核心设置

http://www.mybatis.org/mybatis-3/zh/configuration.html#settings

## 参数解析

`#{}`是 sql 的参数占位符，Mybatis 会将 sql 中的`#{}`替换为?号，在 sql 执行前会使用 PreparedStatement 的参数设置方法，按序给 sql 的?号占位符设置参数值，比如 ps.setInt(0, parameterValue)，`#{item.name}` 的取值方式为使用反射从参数对象中获取 item 对象的 name 属性值，相当于 `param.getItem().getName()`

## Mapper绑定

Dao 接口，就是人们常说的 `Mapper`接口，接口的全限名，就是映射文件中的 namespace 的值，接口的方法名，就是映射文件中`MappedStatement`的 id 值，接口方法内的参数，就是传递给 sql 的参数。`Mapper`接口是没有实现类的，当调用接口方法时，接口全限名+方法名拼接字符串作为 key 值，可唯一定位一个`MappedStatement`，举例：`com.mybatis3.mappers.StudentDao.findStudentById`，可以唯一找到 namespace 为`com.mybatis3.mappers.StudentDao`下面`id = findStudentById`的`MappedStatement`。在 Mybatis 中，每一个`<select>`、`<insert>`、`<update>`、`<delete>`标签，都会被解析为一个`MappedStatement`对象。

Dao 接口里的方法，是不能重载的，因为是全限名+方法名的保存和寻找策略。

Dao 接口的工作原理是 JDK 动态代理，Mybatis 运行时会使用 JDK 动态代理为 Dao 接口生成代理 proxy 对象，代理对象 proxy 会拦截接口方法，转而执行`MappedStatement`所代表的 sql，然后将 sql 执行结果返回。



不同的 Xml 映射文件，如果配置了 namespace，那么 id 可以重复。namespace+id 是作为 `Map<String, MappedStatement>`的 key 使用的

## 批量更新

```xml
<update id="updateOrderItem"  parameterType="java.util.List">
  <foreach collection="list" item="item"  separator=";">
    update order_item
    <set>
      <if test="item.orderId != null">
        order_id = #{item.orderId},
      </if>
      <if test="item.productId != null">
        product_id = #{item.productId},
      </if>
      <if test="item.count != null">
        count = #{item.count}
      </if>
    </set>
    where id = #{item.id}
  </foreach>
</update>
```

此方式需要允许[MySQL](https://cloud.tencent.com/product/cdb?from=10680)的一次执行多条SQL

```javascript
url=jdbc:mysql://localhost:3306/ssm?characterEncoding=utf-8&allowMultiQueries=true
```

## PageHelper

基本原理是使用 Mybatis 提供的插件接口，实现自定义插件，在插件的拦截方法内拦截待执行的 sql，然后重写 sql，根据 dialect 方言，添加对应的物理分页语句和物理分页参数。

pageHelper会使用ThreadLocal获取到同一线程中的变量信息，各个线程之间的Threadlocal

不会相互干扰

jar包：

```
<dependency>
	<groupId>com.github.pagehelper</groupId>
	<artifactId>pagehelper</artifactId>
	<version>4.1.6</version>
</dependency>
```

Spring boot下配置：

```java
@Configuration
public class PageHelperConfig {
    @Bean
    public PageHelper pageHelper() {
        PageHelper pageHelper = new PageHelper();
        Properties p = new Properties();
        p.setProperty("offsetAsPageNum", "true");
        p.setProperty("rowBoundsWithCount", "true");
        p.setProperty("reasonable", "true");
        pageHelper.setProperties(p);
        return pageHelper;
    }
}
```



使用

```java
//利用PageHelper分页查询 注意：这个一定要放查询语句的前一行,否则无法进行分页,因为它对紧随其后第一个sql语句有效
Page page = PageHelper.startPage(1, 10, orderStandesc);// orderStandesc 是order by后的参数
List<Course> list = courseMapper.selectCourseBySid(id);
PageInfo<Course> pageInfo = new PageInfo<>(list);
// 方法一，比较怀疑
pageInfo.getTotal();
// 方法二
pageInfo.setPages(page.getPages());//总页数
pageInfo.setTotal(page.getTotal());//总条数
```

## 多种数据库

```xml
<bean id="vendorProperties" class="org.springframework.beans.factory.config.PropertiesFactoryBean">
    <property name="properties">
        <props>
            <prop key="MySQL">mysql</prop>
            <prop key="H2">h2</prop>
        </props>
    </property>
</bean>
<bean id="databaseIdProvider" class="org.apache.ibatis.mapping.VendorDatabaseIdProvider">
    <property name="properties" ref="vendorProperties"/>
</bean>
```

## 拦截器

Mybatis 仅可以编写针对 `ParameterHandler`、`ResultSetHandler`、`StatementHandler`、`Executor` 这 4 种接口的插件，Mybatis 使用 JDK 的动态代理，为需要拦截的接口生成代理对象以实现接口方法拦截功能，每当执行这 4 种接口对象的方法时，就会进入拦截方法，具体就是 `InvocationHandler` 的 `invoke()`方法，当然，只会拦截那些你指定需要拦截的方法。

实现 Mybatis 的 Interceptor 接口并复写` intercept()`方法，然后在给插件编写注解，指定要拦截哪一个接口的哪些方法即可，记住，别忘了在配置文件中配置你编写的插件。

## 结果映射

第一种是使用`<resultMap>`标签，逐一定义列名和对象属性名之间的映射关系。第二种是使用 sql  列的别名功能，将列别名书写为对象属性名，比如 T_NAME AS NAME，对象属性名一般是  name，小写，但是列名不区分大小写，Mybatis 会忽略列名大小写，智能找到与之对应对象属性名，你甚至可以写成 T_NAME AS  NaMe，Mybatis 一样可以正常工作。

有了列名与属性名的映射关系后，Mybatis 通过反射创建对象，同时使用反射给对象的属性逐一赋值并返回，那些找不到映射关系的属性，是无法完成赋值的。

# Hibernate

## 注解

mysql自增主键

```java
 
@Id
 @GeneratedValue(strategy = GenerationType.IDENTITY) 
```

多对一

```java
//把Product的getCategory进行多对一映射
@ManyToOne
@JoinColumn(name="cid") //cid是分类表中的字段
public Category getCategory() {
    return category;
}
```
一对多。为Category再加product集合，并提供getter和setter

```java
@OneToMany(fetch=FetchType.EAGER)
@JoinColumn(name="cid") //cid是分类表中的id字段,cid是Product表的字段
public Set<Product> getProducts() {
    return products;
}
```
一对多关系保存：

```
        Session s = sf.openSession();
        s.beginTransaction();
         
        Category c =new Category();
        c.setName("c1");
        s.save(c);
         
        Product p = (Product) s.get(Product.class, 8);
        p.setCategory(c);
        s.update(p);
```

一对多关系保存后，用来通过一查询多个

```
    Category c = (Category) s.get(Category.class, 1);
    Set<Product> ps = c.getProducts();
    for (Product p : ps) {
        System.out.println(p.getName());
    }
```

多对多关系，需要建立中间表用于维护 User和Product之间的关系.可以用@JoinTable指定中间表。



## 事务

MYSQL 表的类型必须是INNODB才支持事务

## 延迟加载

延迟加载（懒加载）：只有访问了这个对象的属性，hibernate才会到数据库中进行查询。否则不会访问数据库

可以选择开启和关闭



一般属性延迟加载：

@Basic(fetch = FetchType.Lazy)



关系延迟加载：

```java
@OneToMany(fetch=FetchType.)
```



在one-many many-many的时候都可以使用关系的延迟加载

## 分页

使用Criteria进行分页查询



## N+1

参考

https://www.cnblogs.com/ealenxie/p/9800818.html

问题描述：JPA基于Hibernate，fetch策略默认为懒加载(并非联表查询)，由于关联的存在 ，又需要将这个对象关联的集合取出，集合数量是N，则要发出N条SQL，于是本来的1条联表查询SQL可解决的问题变成了N+1条SQL。

解决方法是 : 不修改懒加载策略，JPA也不写native SQL，通过联表查询进行解决。@NamedEntityGraph的使用时为了解决sql查询过多的问题

```java
@Entity
@Table(name="s_person")
@NamedEntityGraph(name="person.all",attributeNodes={@NamedAttributeNode("address"),@NamedAttributeNode("cards")})
public class Person {

    @GeneratedValue(generator = "uuid2")
        @GenericGenerator(name = "uuid2", strategy = "uuid2")
    @Id
    private String id;
    private String username;
    private String age;

    @OneToOne
    @JoinColumn(name="address_id",referencedColumnName="id")
    private Address address;
    
   
    @OneToMany(fetch=FetchType.EAGER)
    //在一对多里面,无论是单向还是双向,映射关系的维护端都是在多的那一方.
    //@JoinColumn中name是另一个表的外键列名
    @JoinTable(name="s_person_card",joinColumns={@JoinColumn(name="p_id")}
    ,inverseJoinColumns={@JoinColumn(name="c_id")})
    private List<Cards> cards;

    public List<Cards> getCards() {
        return cards;
    }
    public void setCards(List<Cards> cards) {
        this.cards = cards;
    }

    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    public String getAge() {
        return age;
    }
    public void setAge(String age) {
        this.age = age;
    }

    public Address getAddress() {
        return address;
    }
    public void setAddress(Address address) {
        this.address = address;
    }
}
```

​	

接口	

	public interface PersonRepository extends JpaRepository<Person, String>{
	 
		@EntityGraph(value = "person.all" , type=EntityGraphType.FETCH)
		Person findById(String id);
	 
	}



## 级联

级联有4种类型：
  all：所有操作都执行级联操作；
  none：所有操作都不执行级联操作；
  delete：删除时执行级联操作； 
  save-update：保存和更新时执行级联操作；
级联通常用在one-many和many-to-many上，几乎不用在many-one上



## 二级缓存

需要在实体类上开启

一级缓存：在事务范围内
二级缓存：sessionFactory级别的缓存，各个事务可以共享。

对于批量更新和批量删除操作，如果不希望启用第一级缓存，可以绕过Hibernate API，直接 通过JDBC API来执行指操作。

## 关系

无论是单向还是双向,映射关系的维护端都是在多的那一方。

### @JoinColumn

 `@JoinColumn(name = "AccountCard", referenceColumnName = "AccountCard",insertable=false, updatable=false)` 

insertable=false, updatable=false指定是否对该列进行插入更新（如果该字段兼职外键，都设为false）

### mappedBy

数据库中一对多（多对一）的关系中，关联关系总是被多方维护的即外键建在多方，我们在单方对象的@OneToMany（mappedby=" "）把关系的维护交给多方对象。

### 单向一对一

比如People和Pet，通过人能找到宠物，但通过宠物找不到人。People是关系维护端，有一个外键。

```java
关系维护端
@OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY) //JPA注释： 一对一 关系
@JoinColumn(name="pet_fk" )// 在pepole中，添加一个外键 "pet_fk"
```

### 双向一对一

比如部门-部门经理（部门来维护关系），丈夫和妻子（双方谁维护关系都可以），公民和身份证

```java
@Entity
@Table(name = "t_person")
public class Person {
  @Id
  @GeneratedValue
  private Long id;
  private String name;
  // mappedBy配置映射关系:当前对象IdCard属于哪个person对象
  @OneToOne(optional = false, mappedBy = "person", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
  private IdCard idCard;
...
}
 
 
@Entity
@Table(name = "t_idcard")
public class IdCard {
  @Id
  @GeneratedValue
  private Long id;
  @Column(length = 18)
  private String cardNo;
  // 默认值optional = true表示idcard_id可以为空;反之。。。
  @OneToOne(optional = false, fetch = FetchType.LAZY)
  @JoinColumn(name = "person_id", unique = true)
  // unique=true确保了一对一关系
  private Person person;
  ...
}
```

### 单向多对一

Person和country（国家）是多对一关系。

Person里注解如下：

```java
@ManyToOne  
@JoinColumn(name="countryID")  //Person是多方，countryID是person表里的外键字段，指向country表    
public Country getCountry() {
          return country;      
} 
```

### 单向一对多

一对多的@JoinColumn注解在“被控方”，即一的一方，指的是外表中指向本表的外键名称。

一般用法：

```
@Entity
@Table(name = "t_idcard")
public class IdCard {
@OneToMany(cascade=CascadeType.ALL)  
@JoinColumn(name="personID")//注释的是另一个表指向本表的外键。  
public List<Phone> getPhones() {
        return phones;     
}
```

### 双向一对多

定义

```
@Entity
@Table(name = "t_product")
public class Product {
  @Id
  @GeneratedValue
  private Long id;
  private String name;
  // 多对一
  // optional=false表示外键type_id不能为空
  @ManyToOne(optional = true)
  @JoinColumn(name = "type_id")
  private ProductType type;
  ...
}
 
@Entity
@Table(name = "t_product_type")
public class ProductType {
  @Id
  @GeneratedValue
  private Long id;
  private String name;
  // 一对多:集合Set
  @OneToMany(mappedBy = "type", orphanRemoval = true)
  private Set<Product> products = new HashSet<Product>();
  ...
}
```



# Servlet

http://how2j.cn/k/cart/cart-tutorials/595.html

## servlet Filter中文问题

request.setCharacterEncoding("UTF-8");

```java
        request.setCharacterEncoding("UTF-8");
        String name = request.getParameter("name");
 
        // byte[] bytes = name.getBytes("ISO-8859-1");
        // name = new String(bytes, "UTF-8");
 
        String password = request.getParameter("password");

// 返回中文的响应 
response.setContentType("text/html; charset=UTF-8");
```

如果有很多servlet都需要获取中文，通过EncodingFilter过滤器进行中文处理 

## 服务端跳转

```java
//在Servlet中进行服务端跳转的方式：
request.getRequestDispatcher("success.html").forward(request, response);
```

服务端跳转可以看到浏览器的地址依然是/login 路径，并不会变成success.html 



## 客户端跳转  		 

在Servlet中进行客户端跳转的方式：

```java
response.sendRedirect("fail.html");
```

## Servlet自启动

在web.xml中，配置Hello Servlet的地方，增加一句:

`<load-on-startup>10</load-on-startup>` 

tomcat启动、重启会调用init方法

web应用重新启动、关闭时都会调用destroy方法





## 添加购物车操作

1. 获取购买数量
2. 获取购买商品的id
3. 根据id获取商品对象
4. 创建一个新的OrderItem对象
5. 从session中取出一个List , 这个List里面存放陆续购买的商品。
   如果是第一次从session中获取该List,那么它会是空的，需要创建一个ArrayList
6. 把新创建的OrderItem对象放入该List 中
7. 跳转到显示购物车的listOrderItem

session cookie保存sessionid，服务器session保存购物车信息。

>通常session 
>cookie是不能跨窗口使用的，当你新开了一个浏览器窗口进入相同页面时，系统会赋予你一个新的sessionid，这样我们信息共享的目的就达不到了，此时我们可以先把sessionid保存在persistent
>cookie中，然后在新窗口中读出来，就可以得到上一个窗口SessionID了，这样通过session cookie和persistent 
>cookie的结合我们就实现了跨窗口的session tracking（会话跟踪）。

如果浏览器把cookie功能关闭，那么服务端就无法获取jsessionid,每一次访问，都会生成一个新的session对象。

为了解决这个问题,页面跳转时可以把jsessionid编码到目标url后。

## 通过对象关联

```java
public class OrderItem {
 
    private int id;
    private Product product;
    private int num;
    private Order order;
}

public class Order {
 
    int id;
    User user;
}
```





# RMI

服务端注册服务

```java
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
public class HelloImpl extends UnicastRemoteObject implements IHello {
    // 这个实现必须有一个显式的构造函数，并且要抛出一个RemoteException异常  
    protected HelloImpl() throws RemoteException {
        super();
    }
    
    private static final long serialVersionUID = 4077329331699640331L;
    public String sayHello(String name) throws RemoteException {
        return "Hello " + name + " ^_^ ";
    }
    public static void main(String[] args) {
        try {
            IHello hello = new HelloImpl();
            LocateRegistry.createRegistry(1099); //加上此程序，就可以不要在控制台上开启RMI的注册程序，1099是RMI服务监视的默认端口
            java.rmi.Naming.rebind("rmi://localhost:1099/hello", hello);
            System.out.print("Ready");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

客户端程序：

```java
import java.rmi.Naming;
public class Hello_RMI_Client {
    public static void main(String[] args) {
        try {
            IHello hello = (IHello) Naming.lookup("rmi://localhost:1099/hello");
                System.out.println(hello.sayHello("zhangxianxin"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

# ActiveMq

## 队列模式

其实就是分食模式。 比如生产方发了 10条消息到 activeMQ 服务器， 而此时有多个 消费方，那么这些消费方就会瓜分这些10条消息，一条消息只会被一个消费方得到。

### 生产者

```java
    //0. 先判断端口是否启动了  Active MQ 服务器
    ActiveMQUtil.checkServer();
   //1.创建ConnectiongFactory,绑定地址
   ConnectionFactory factory=new ActiveMQConnectionFactory(url);
   //2.创建Connection
   Connection connection= factory.createConnection();
   //3.启动连接
   connection.start();
   //4.创建会话
   Session session=connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
   //5.创建一个目标 (队列类型)
   Destination destination=session.createQueue(topicName);
   //6.创建一个生产者
   MessageProducer producer=session.createProducer(destination);


   for (int i = 0; i < 100; i++) {
       //7.创建消息
       TextMessage textMessage=session.createTextMessage("队列消息-"+i);
       //8.发送消息
       producer.send(textMessage);
       System.out.println("发送："+textMessage.getText());
   }
   //7. 关闭连接
   connection.close();
```



### 消费者

```java
        //0. 先判断端口是否启动了 Active MQ 服务器
       ActiveMQUtil.checkServer();
       System.out.printf("%s 消费者启动了。 %n", consumerName);

        //1.创建ConnectiongFactory,绑定地址
        ConnectionFactory factory=new ActiveMQConnectionFactory(url);
        //2.创建Connection
        Connection connection= factory.createConnection();
        //3.启动连接
        connection.start();
        //4.创建会话
        Session session=connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        //5.创建一个目标 （主题类型）
        Destination destination=session.createQueue(topicName);
        //6.创建一个消费者
        MessageConsumer consumer=session.createConsumer(destination);
        //7.创建一个监听器
        consumer.setMessageListener(new MessageListener() {

            public void onMessage(Message arg0) {
                // TODO Auto-generated method stub
                TextMessage textMessage=(TextMessage)arg0;
                try {
                    System.out.println(consumerName +" 接收消息："+textMessage.getText());
                } catch (JMSException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

            }
        });
        
        //8. 因为不知道什么时候有，所以没法主动关闭，就不关闭了，一直处于监听状态
//        connection.close();
```

## 主题模式

就是订阅模式。 比如生产方发了10条消息，而此时有多个消费方，那么多个消费方都能得到这 10条消息，就如同订阅公众号那样。

# RocketMq

Rocketmq如何支持分布式事务消息

场景

A（存在DB操作）、B（存在DB操作）两方需要保证分布式事务一致性，通过引入中间层MQ，A和MQ保持事务一致性（异常情况下通过MQ反查A接口实现check），B和MQ保证事务一致（通过重试），从而达到最终事务一致性。

**原理：大事务 = 小事务 + 异步**

1.  MQ与DB一致性原理（两方事务）

MQ消息、DB操作一致性方案：

1)发送消息到MQ服务器，此时消息状态为SEND_OK。此消息为consumer不可见。

2)执行DB操作；DB执行成功Commit DB操作，DB执行失败Rollback DB操作。

3)如果DB执行成功，回复MQ服务器，将状态为COMMIT_MESSAGE；如果DB执行失败，回复MQ服务器，将状态改为ROLLBACK_MESSAGE。注意此过程有可能失败。

4)MQ内部提供一个名为“事务状态服务”的服务，此服务会检查事务消息的状态，如果发现消息未COMMIT，则通过Producer启动时注册的TransactionCheckListener来回调业务系统，业务系统在checkLocalTransactionState方法中检查DB事务状态，如果成功，则回复COMMIT_MESSAGE，否则回复ROLLBACK_MESSAGE

https://www.jianshu.com/p/2838890f3284

# RabbitMq

rabbitMq有3中模式：

fanout 广播模式，每个队列都能收到相同消息

direct 仅指定队列收到

topic 主题模式。其实就是接收方模糊匹配绑定到消息来源的key。比如想接收美国天气和美国新闻的Eg，绑定usa.*进行监听。



# IDEA

gradle报gc overhead limit错误： complier内存设置从700M提高到1000M

# Tomcat

修改tomcat/bin/catalina.sh，在最顶端加入JAVA_OPTS="$JAVA_OPTS
-XX:+PrintGCDetails 
-Xloggc:/usr/local/java/apache-tomcat-7.0.78/bin/gc.log"



# Elasticsearch

## 配置依赖

 spring-boot整合

```groovy
spring-boot-starter-data-elastisearch
```



application.properties

```java
spring.data.elasticsearch.cluster-nodes = 127.0.0.1:9300
```

## 概念

索引相当于数据库。

分词器决定搜索引擎如何使用关键字进行匹配，是匹配整句“护眼带光源”还是分为 护眼，带，光源 3个关键字去匹配。ElasticSearch 默认是没有中文分词器的，需要额外安装。



## kibana

```java
_index 表示哪个索引
_type 表示哪个表
_id 主键
_version 版本
found 数据存在
_source: 数据内容
```



## 批量导入

可以用curl+kibana批量导入json数据



# 单点登录

https://www.jianshu.com/p/613c615b7ef1

## 系统登录机制

**cookie保存会话id**

单系统登录解决方案的核心是cookie+session：

- cookie携带会话id
- 服务器保存session

但cookie是有限制的，这个限制就是cookie的域（通常对应网站的域名），**浏览器发送http请求时会自动携带与该域匹配的cookie**，而不是所有cookie

多系统下的解决办法可以是同域名共享cookie。缺点：

1. 应用群域名得统一
2. 应用群各系统使用的技术（至少是web服务器）要相同，不然cookie的key值（tomcat为JSESSIONID）不同，无法维持会话，共享cookie的方式是无法实现跨语言技术平台登录的，比如java、php、.net系统之间
3. cookie本身不安全

**session劫持**

只要用户知道JSESSIONID，该用户就可以获取到JSESSIONID对应的session内容。

换个浏览器设置cookie后就可以访问站点

> 并不是没有 Cookie 之后就不能用 Session 了，比如你可以将SessionID放在请求的 url 里面`https://javaguide.cn/?session_id=xxx` 。这种方案的话可行，但是安全性和用户体验感降低。当然，为了你也可以对  SessionID 进行一次加密之后再传入后端。

## 单点登录原理

相比于单系统登录，sso需要一个独立的认证中心，只有认证中心能接受用户的用户名密码等安全信息，其他系统不提供登录入口，只接受认证中心的间接授权。间接授权通过令牌实现，sso认证中心验证用户的用户名密码没问题，创建授权令牌，在接下来的跳转过程中，授权令牌作为参数发送给各个子系统，子系统拿到令牌，即得到了授权，可以借此创建局部会话，局部会话登录方式与单系统的登录方式相同。
链接：https://www.zhihu.com/question/342103776/answer/798611224

![](img\单点登录.jpg)

## 注销

单点登录自然也要单点注销，在一个子系统中注销，所有子系统的会话都将被销毁，用下面的图来说明

![](D:\Cloud\开发\Java\单点登录的注销.jpg)

## sso-client

sso采用客户端/服务端架构，我们先看sso-client与sso-server要实现的功能

1. 拦截子系统未登录用户请求，跳转至sso认证中心
2. 接收并存储sso认证中心发送的令牌
3. 与sso-server通信，校验令牌的有效性
4. 建立局部会话
5. 拦截用户注销请求，向sso认证中心发送注销请求
6. 接收sso认证中心发出的注销请求，销毁局部会话

## sso-server

1. 验证用户的登录信息
2. 创建全局会话
3. 创建授权令牌
4. 与sso-client通信发送令牌
5. 校验sso-client令牌有效性
6. 系统注册
7. 接收sso-client注销请求，注销所有会话

## CAS实现单点登录

下面是CAS实现单点登录的一个例子

1. 用户通过浏览器访问[www.a.com/pageA](http://www.a.com/pageA) ，发现未登录则重定向到认证中心登录页面[www.sso.com/login?redirect=www.a.com/pageA](http://www.sso.com/login?redirect=www.a.com/pageA)，后面跟的redirect_url是为了认证通过后重定向回到a.com
2. 认证中心登录成功后，需要：
   1. 建立一个session(全局会话)
   2. 创建一个ticket（可以认为是个随机字符串）
   3. 然后再重定向到你那里，url 中带着ticket : [www.a.com/pageA?ticket=T123](http://www.a.com/pageA?ticket=T123) 与此同时cookie也会发给浏览器，比如：Set cookie : ssoid=1234, [sso.com](http://sso.com) ”。这个cookie是认证中心的cookie
3. a.com拿ticket=T123到认证中心验证，令牌有效后：
   1. 注册系统a.com
   2. 给用户建立session（局部会话）
   3. 返回pageA这个资源
   4. 给浏览器设置cookie。Set cookie : sessionid=xxxx, a.com
4. 这时候用户浏览器实际上有两个cookie,一个是sso.com的，另外一个是a.com的。
5. 用户再次访问a.com另外一个受保护的页面，[www.a.com/pageA1](http://www.a.com/pageA1)，浏览器带上a.com的cookie就知道已登录。
6. 用户访问[www.b.com/pageB](http://www.b.com/pageB)，会重定向www.sso.com/login?redirect=www.b.com/pageB，并带上cookie：ssoid=1234，认证中心就知道已登录会返回ticket，重定向到www.b.com/pageB?ticket=T5678
7. b.com拿ticket=T5678到认证中心验证，令牌有效注册系统b.com





# 微信

## 网页获取用户openId

静默方式直接获取用户openId

非静默方式( 需要用户去手动点击同意 )：

1. 请求微信服务器（url携带state)获取code，重定向到公众号webServer，携带code和原state
2. webServer验证state，接收code，请求微信服务器获取accessToken和openId
3.  access_token在2小时内有效，过期需要重新获取，但1天内获取次数有限。可以使用refresh_token进行刷新，refresh_token有效期为30天，当refresh_token失效之后，需要用户重新授权。 





## 公众号信息

公众号AppSecret：4b8a640bf91678a6d04ae5180e00e09f

appid： wx237b66d0d88747b6 

兆日外网ip： `117.23.83.234` 

```http

基础支持: 获取access_token接口 /token

请求地址：
    https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx237b66d0d88747b6&secret=4b8a640bf91678a6d04ae5180e00e09f 

返回结果:

        200 OK

        Connection: close
        Date: Wed, 23 Oct 2019 02:58:59 GMT
        Content-Type: application/json; encoding=utf-8
        Content-Length: 194

        {
            "access_token": "26_TSVFnxDGnoEKcFN0m_vBLLluUBYgHygvnLQ_ngI3QpQxXGgmSHwTnoz6MG0QMEdnkQatQ3UM8D4lmVdHQsNLSZPT4LxBGT4Ve2I-hQnrhb0TrQtAf4Qu_Fql-NIVN74s1jECERF4bqnpnEOTZMVeAEAVIR", 
            "expires_in": 7200
        }


```

# ThreadLocal

 ThreadLocal 的使用场景有两种:

- 以线程为作用域，不同线程具有不同的数据副本
- 复杂逻辑下的对象传递。如分布式服务中全局流水号、渠道Id的传递。

**原理**

每个线程有一个ThreadLocalMap对象，ThreadLocalMap是定义在ThreadLocal中的静态内部类。ThreadLocal可以理解为只是ThreadLocalMap的封装，

```java
public class Thread implements Runnable {
 ......
//与此线程有关的ThreadLocal值。由ThreadLocal类维护
ThreadLocal.ThreadLocalMap threadLocals = null;

//与此线程有关的InheritableThreadLocal值。由InheritableThreadLocal类维护
ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;
 ......
}
```

线程所操作的是当前线程的 ThreadLocalMap。 第一次xxThreadLocalObj.set时，会初始化当前线程threadLocalMap：

```java
        ThreadLocalMap(ThreadLocal firstKey, Object firstValue) {
            table = new Entry[INITIAL_CAPACITY];
            int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
            table[i] = new Entry(firstKey, firstValue);
            size = 1;
            setThreshold(INITIAL_CAPACITY);
       }
```

对一个线程，定义的一个到多个threadLocal对象都会加入到当前线程的threadLocalMap中

```java
 public void set(T value) {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null)
            map.set(this, value);
        else
            createMap(t, value);
}
ThreadLocalMap getMap(Thread t) {
    return t.threadLocals;
}
```

实际使用中，threadLocal可以是静态对象，当做全局变量使用，各个线程的数据仍然是隔离的。

各个线程使用的threadLocal引用相同，但get出的value不同。



**ThreadLocalMap内存泄露问题**

内部是数组实现，并把操作的 ThreadLocal 对象作为键存储。

ThreadLocalMap 中使用的 key 为 ThreadLocal 的弱引用,而 value 是强引用。所以，如果 ThreadLocal 没有被外部强引用的情况下，在垃圾回收的时候，key 会被清理掉，而 value 不会被清理掉。这样一来，ThreadLocalMap 中就会出现key为null的Entry。假如我们不做任何措施的话，value 永远无法被GC 回收，这个时候就可能会产生内存泄露。ThreadLocalMap实现中已经考虑了这种情况，在调用 set()、get()、remove() 方法的时候，会清理掉 key 为 null 的记录。使用完 ThreadLocal方法后 最好手动调用remove()方法

```java
  static class Entry extends WeakReference<ThreadLocal<?>> {
        /** The value associated with this ThreadLocal. */
        Object value;

        Entry(ThreadLocal<?> k, Object v) {
            super(k);
            value = v;
        }
    }
```


# 正则表达式

```java
Pattern p = Pattern.compile("验证码.*?(\\d{6})");
Matcher m = p.matcher("<str>");
if(m.find()){
    code = m.group(1);
}
```

# NIO

完整的示例，打开一个Selector，注册一个通道注册到这个Selector上(通道的初始化过程略去),然后持续监控这个Selector的四种事件（接受，连接，读，写）是否就绪。

```java
Selector selector = Selector.open();
channel.configureBlocking(false);
SelectionKey key = channel.register(selector, SelectionKey.OP_READ);
while(true) {
  int readyChannels = selector.select();
  if(readyChannels == 0) continue;
  Set selectedKeys = selector.selectedKeys();
  Iterator keyIterator = selectedKeys.iterator();
  while(keyIterator.hasNext()) {
    SelectionKey key = keyIterator.next();
    if(key.isAcceptable()) {
        // a connection was accepted by a ServerSocketChannel.
    } else if (key.isConnectable()) {
        // a connection was established with a remote server.
    } else if (key.isReadable()) {
        // a channel is ready for reading
    } else if (key.isWritable()) {
        // a channel is ready for writing
    }
    keyIterator.remove();
  }
}
```

如果你有少量的连接使用非常高的带宽，一次发送大量的数据，也许典型的IO服务器实现可能非常契合。下图说明了一个典型的IO服务器设计.

如果需要管理同时打开的成千上万个连接，这些连接每次只是发送少量的数据，例如聊天服务器，实现NIO的服务器可能是一个优势。同样，如果你需要维持许多打开的连接到其他计算机上，如P2P网络中，使用一个单独的线程来管理你所有出站连接，可能是一个优势。

网上例子：

```java
/**
 * 
 * @author 闪电侠
 * @date 2019年2月21日
 * @Description: NIO 改造后的服务端
 */
public class NIOServer {
  public static void main(String[] args) throws IOException {
    // 1. serverSelector负责轮询是否有新的连接，服务端监测到新的连接之后，不再创建一个新的线程，
    // 而是直接将新连接绑定到clientSelector上，这样就不用 IO 模型中 1w 个 while 循环在死等
    Selector serverSelector = Selector.open();
    // 2. clientSelector负责轮询连接是否有数据可读
    Selector clientSelector = Selector.open();

    new Thread(() -> {
      try {
        // 对应IO编程中服务端启动
        ServerSocketChannel listenerChannel = ServerSocketChannel.open();
        listenerChannel.socket().bind(new InetSocketAddress(3333));
        listenerChannel.configureBlocking(false);
        listenerChannel.register(serverSelector, SelectionKey.OP_ACCEPT);

        while (true) {
          // 监测是否有新的连接，这里的1指的是阻塞的时间为 1ms
          if (serverSelector.select(1) > 0) {
            Set<SelectionKey> set = serverSelector.selectedKeys();
            Iterator<SelectionKey> keyIterator = set.iterator();

            while (keyIterator.hasNext()) {
              SelectionKey key = keyIterator.next();

              if (key.isAcceptable()) {
                try {
                  // (1) 每来一个新连接，不需要创建一个线程，而是直接注册到clientSelector
                  SocketChannel clientChannel = ((ServerSocketChannel) key.channel()).accept();
                  clientChannel.configureBlocking(false);
                  clientChannel.register(clientSelector, SelectionKey.OP_READ);
                } finally {
                  keyIterator.remove();
                }
              }

            }
          }
        }
      } catch (IOException ignored) {
      }
    }).start();
    new Thread(() -> {
      try {
        while (true) {
          // (2) 批量轮询是否有哪些连接有数据可读，这里的1指的是阻塞的时间为 1ms
          if (clientSelector.select(1) > 0) {
            Set<SelectionKey> set = clientSelector.selectedKeys();
            Iterator<SelectionKey> keyIterator = set.iterator();

            while (keyIterator.hasNext()) {
              SelectionKey key = keyIterator.next();

              if (key.isReadable()) {
                try {
                  SocketChannel clientChannel = (SocketChannel) key.channel();
                  ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
                  // (3) 面向 Buffer
                  clientChannel.read(byteBuffer);
                  byteBuffer.flip();
                  System.out.println(
                      Charset.defaultCharset().newDecoder().decode(byteBuffer).toString());
                } finally {
                  keyIterator.remove();
                  key.interestOps(SelectionKey.OP_READ);
                }
              }

            }
          }
        }
      } catch (IOException ignored) {
      }
    }).start();

  }
}
```

除了编程复杂、编程模型难之外，它还有以下让人诟病的问题：

- JDK 的 NIO 底层由 epoll 实现，该实现饱受诟病的空轮询 bug 会导致 cpu 飙升 100%
- 项目庞大之后，自行实现的 NIO 很容易出现各类 bug，维护成本较高，上面这一坨代码我都不能保证没有 bug

Netty 的出现很大程度上改善了 JDK 原生 NIO 所存在的一些让人难以忍受的问题。

# Netty

```groovy
compile 'io.netty:netty-all:4.1.13.Final'
```

# 日志

```java
// 如果判断为真，那么可以输出 trace 和 debug 级别的日志
if (logger.isDebugEnabled()) {
    //参数可能会进行字符串拼接运算
logger.debug("Current ID is: {} and name is: {}", id, getName());
}
```

# 安全

用户请求传入的任何参数必须做有效性验证。忽略参数校验可能导致：

- page size 过大导致内存溢出
- 恶意 order by 导致数据库慢查询
- 任意重定向
- SQL 注入
- 反序列化注入
- 正则输入源串拒绝服务 ReDoS

在使用平台资源，譬如短信、邮件、电话、下单、支付，必须实现正确的防重放的
机制，如数量限制、疲劳度控制、验证码校验，避免被滥刷而导致资损。

## SQL注入

 SQL 参数严格使用参数绑定。禁止字符串拼接 SQL 访问数据库

> SQL语句在程序运行前已经进行了预编译,当运行时动态地把参数传给PreprareStatement时，即使参数里有敏感字符如 or '1=1'、数据库也会作为一个参数一个字段的属性值来处理而不会作为一个SQL指令



## CSRF

攻击方式：

- 恶意网站B中包含访问A网站的url，get请求。
- 恶意网站页面中隐藏表单提交post请求，需要单独构造form表单和js。

预防：

- 尽可能使用POST请求，仅解析POST请求参数
- 验证码
- 表单、 AJAX 提交必须执行 CSRF 安全验证

发贴、评论、发送即时消息等用户生成内容的场景必须实现防刷、文本内容违禁词
过滤等风控策略

在使用平台资源，譬如短信、邮件、电话、下单、支付，必须实现正确的防重放的
机制，如数量限制、疲劳度控制、验证码校验，避免被滥刷而导致资损



varchar 是可变长字符串，不预先分配存储空间，长度不要超过 5000



 id 必为主键，类型为 bigint unsigned、单表时自增、步长为 1。create_time, update_time
的类型均为 datetime 类型。

小数类型为 decimal ，禁止使用 float 和 double

MySQL 在 Windows 下不区分大小写，但在 Linux 下默认是区分大小写。因此，数据库名、表
名、字段名，都不允许出现任何大写字母

## AccessController

https://www.jianshu.com/p/81985bc2bfa3

在某一个线程的调用栈中，当 AccessController 的 checkPermission 方法被最近的调用程序（例如 A 类中的方法）调用时，对于程序要求的所有访问权限，ACC 决定是否授权的基本算法如下：
1. 如果调用链中的某个调用程序没有所需的权限，将抛出 AccessControlException；
2. 若是满足以下情况即被授予权限：
    a. 调用程序访问另一个有该权限域里程序的方法，并且此方法标记为有访问“特权”；
    b. 调用程序所调用（直接或间接）的后续对象都有上述权限。
# 索引

规范：

- 业务上具有唯一特性的字段，必须建成唯一索引
- 超过3个表禁止join。被关联的字段要有索引

特性：

- 索引如果存在范围查询，那么索引有序性无法利用
- 最左前缀匹配特性，如果左边的值未确定，那么无法使用此索引

# 数据库连接池

设置检查连接（取前或取后）的情况下，一定要保证检查sql可用，否则可能导致连接无法正常归还。

```sql
# oracle
select 1 from dual
# mysql
select 1
```

# Mysql

mysql-jdbc驱动在把byte[]的字段映射到数据库blob字段时，可能会先转换为16进制字符串，因此长度会翻倍。

解决办法：不要采用byte数据作为blob字段的实体映射，而是采用Blob类型来进行映射 

Spring-data实现：

```java
@Entity
@Table(name = "file_table")
@Setter
@Getter
@ToString
public class FileTable {
    @Id
    private int id;

    @Lob
    @Column(name = "content", columnDefinition = "Blob")
    private Blob content;
}

// 测试一个文件存储
@Test
public void testSaveFile() throws IOException {
    FileTable fileTable = new FileTable();
    File file = new File("/Users/zhiquan/code/demo.txt");
    //利用apache-commons工具可以轻松地将file转换成byte数组
    byte[] content = FileUtils.readFileToByteArray(file);
    //利用Hibernate提供的BlobProxy可以轻松的降byte数组转换成Blob对象
    Blob blob = BlobProxy.generateProxy(content);
    fileTable.setContent(blob);
    this.fileTableService.saveFile(fileTable);
}
```



# 幂等性

 幂等性是系统服务对外一种承诺（而不是实现），承诺只要调用接口成功，外部多次调用对系统的影响是一致的。声明为幂等的服务会认为外部调用失败是常态，并且失败之后必然会有重试。 

https://www.cnblogs.com/javalyy/p/8882144.html





## 保证幂等策略

-  幂等需要通过唯一的业务单号来保证是同一笔业务  
- 并发场景下，先查询后更新操作要加锁，实现原子操作

# Web路径

“/”开头路径代表绝对路径。

html中浏览器解析“/”开头路径，对应实际路径是端口后的路径

web端解析“/“开头路径，相对于web应用上下文路径

# Jdbc

Statement、PreparedStatement和CallableStatement都是接口(interface)。 

Statement继承自Wrapper、PreparedStatement继承自Statement、CallableStatement继承自PreparedStatement。  

Statement: 
    提供了执行语句和获取结果的基本方法;普通的不带参的查询SQL；支持批量更新,批量删除; 

PreparedStatement: 

- 可变参数的SQL,编译一次,执行多次,效率高
- 安全性好，有效防止Sql注入等问题
- 支持批量更新,批量删除; 

CallableStatement: 

- 继承自PreparedStatement,支持带参数的SQL操作; 

- 添加了处理 OUT 参数的方法
- 支持调用存储过程,提供了对输出和输入/输出参数(INOUT)的支持; 

# REST

在SOAP模式把HTTP作为一种通信协议，而不是应用协议。所以http中的表头，错误信息等全部无视。实际上http有 put get post delete等方法。

REST 则不然，HTTP method中的 POST GET PUT DELETE 都是与请求方法对应的。服务器可以通过请求方式直接判断请求动作是要进行什么操作。

# Web MVC

局限于协议和场景，web Mvc框架大部分都是:

- 模型不会Push数据给视图
- 控制器通知模型更新，还要获取模型更新的结果数据 ，然后将更新后的模型数据一并转发给视图 





# 数据库中间件

Gaea 实现读写分离mysql的代码

# 分布式事务

ebay

  1.A、B两个系统服务进行异步数据通信

本场景我们采用Q作为消息中间件。可以借鉴ebay模式。

① 应用A的业务逻辑、写本地消息表、写消息队列放在一个队列里。写消息队列业务逻辑放在最后。

② 所有步骤执行成功，事物提交。

③ 有一步骤执行失败，则进行回滚。

此方案需要在记录服务A发送的完整消息日志，以防Q出现问题进行消息补发，在B端创建接收表，去重，保证消息的幂等性。

版权声明：本文为CSDN博主「longfei1984」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/longfei1984/article/details/77601501

第一阶段：transation表和操作队列在同一实例上，可以通过本地的数据库的事务保证。
第二阶段：message_applied表和user表在同一个实上，可以通过本地的数据的事务保证，当有重试或者重复消息过来时，通过message_applied表可以判断是否是重复数据。 



蘑菇街

我们在交易创建流程中，首先创建一个不可见订单，然后在同步调用锁券和扣减库存时，针对调用异常（失败或者超时），发出废单消息到MQ。如果消息发送失败，本地会做时间阶梯式的异步重试；优惠券系统和库存系统收到消息后，会进行判断是否需要做业务回滚，这样就准实时地保证了多个本地事务的最终一致性。





# 序列化

## 对象流

```java
  ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
  ObjectInputStream ois = new ObjectInputStream(bais);
  return ois.readObject();
```

# 分布式唯一Id

https://www.liaoxuefeng.com/article/1280526512029729

PowerMockito

模拟测试雪花算法

https://github.com/timestatic/snowflake/blob/master/src/test/java/com/timestatic/snowflake/SnowFlakeWorkerTest.java

# 对象拷贝

因为Apache下的BeanUtils性能较差，不建议使用，可以使用 Spring的BeanUtils.

MapStructConverter性能最好

# ShutdownHook

Java 语言提供一种 ShutdownHook（钩子）进制，当 JVM 接受到系统的关闭通知之后，调用 ShutdownHook 内的方法，用以完成清理操作，从而平滑的退出应用。

ShutdownHook代码如下：

```javascript
Copy
 Runtime.getRuntime().addShutdownHook(new Thread(() -> {
 System.out.println("关闭应用，释放资源");
 }));
```

Runtime.getRuntime().addShutdownHook(Thread) 需要传入一个线程对象，后续动作将会在该异步线程内完成。除了主动关闭应用（使用 kill -15 指令）,以下场景也将会触发 ShutdownHook :

- 代码执行结束，JVM 正常退出
- 应用代码中调用 System#exit 方法
- 应用中发生 OOM 错误，导致 JVM 关闭
- 终端中使用 Ctrl+C(非后台运行)



# 分布式事务

## 两阶段提交

在两阶段提交中，主要涉及到两个角色，分别是协调者和参与者。

第一阶段：

1. 分布式事务的发起者首先向协调者发起事务请求，然后协调者会给所有参与者发送 `prepare` 请求，告诉参与者你们需要执行事务的内容
2. 参与者收到 `prepare` 消息后，他们会开始执行事务，但不提交，并将 `Undo` 和 `Redo` 信息记入事务日志中，之后参与者就向协调者反馈是否准备好了。

第二阶段：第二阶段主要是协调者根据参与者反馈的情况来决定，接下来通知各参与者提交事务或者回滚事务。



带来的问题：

- **单点故障问题**，如果协调者挂了那么整个系统都处于不可用的状态了。
- **阻塞问题**，即当协调者发送 `prepare` 请求，参与者收到之后如果能处理那么它将会进行事务的处理但并不提交，这个时候会一直占用着资源不释放，如果此时协调者挂了，那么这些资源都不会再释放了，这会极大影响性能。
- **数据不一致问题**，比如当第二阶段，协调者只发送了一部分的 `commit` 请求就挂了，那么也就意味着，收到消息的参与者会进行事务的提交，而后面没收到的则不会进行事务提交，那么这时候就会产生数据不一致性问题。

# JMX

MBean入门

https://blog.csdn.net/qq_32523587/article/details/94991688

# tomcat-jdbc



Tomcat-jdbc连接池

https://www.jianshu.com/p/26eb4cf39335

遗弃连接移除并且超时时间大于0(默认60)，什么是被遗弃呢?其实就是**被应用长时间占用的连接**，被长时间占用的原因可能是应用忘记关闭了，或者是应用阻塞了，等等。注意，这里的移除会**关闭连接**，而不是对其进行回收，放到idle队列中



PooledConnection 是对java.sql.Connection的封装

borrowConnection 

- 从idle队列取一个
- idle里取不到，则进入循环。
- 首先调用borrowConnection重载方法从连接池拿一个返回。密码变化或连接达到最大存活时间，会重新连接。最后会把连接加入busy队列
- 连接池里没有且连接池大小未达到上限，则调用createConnection创建一个新连接。连接创建、加锁后，才委托驱动获取连接。最后会把连接加入busy队列
- 前面都没获取到连接，这里则在一定超时时间内等待从idle队列里取连接

等待时间计算

```java
private PooledConnection borrowConnection(int wait, String username, String password) {
    //...
    long now = System.currentTimeMillis();
    while (true) {
        //...前面都没拿到连接
        long maxWait = wait;
        //if the passed in wait time is -1, means we should use the pool property value
        if (wait==-1) {
            maxWait = (getPoolProperties().getMaxWait()<=0)?
                Long.MAX_VALUE:getPoolProperties().getMaxWait();
        }
        long timetowait = Math.max(0, maxWait - (System.currentTimeMillis() - now));
```

可以看出，真正在生产环境使用时可以配置maxWait参数

## 拦截器

tomcat-jdbc-pool中所有拦截器均继承自抽象类JdbcInterceptor，其公有的invoke方法实现保证了请求可以沿着拦截器链继续向下执行(如果需要):

```java
@Override
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    if (getNext()!=null) return getNext().invoke(proxy,method,args);
    else throw new NullPointerException();
}
```

ProxyConnection为默认添加，其作用是最后调用java.sql.Connection的相应方法

```java
@Override
public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    PooledConnection poolc = connection;
    if (poolc!=null) {
        return method.invoke(poolc.getConnection(),args);
    }
}
```

连接池中的每一个连接均有自己的拦截器链，换句话说，每个连接持有的是每个拦截器的不同实例。

对于每一个连接，拦截器链只会生成一次，生成之后保存在PooledConnection的handler属性中，注意，这里保存的是拦截器链的第一个拦截器。

# 分布式锁

https://zhuanlan.zhihu.com/p/72896771

## redis

redis分布式锁

https://zhuanlan.zhihu.com/p/111329801



Redisson是一个在Redis的基础上实现的Java驻内存数据网格。它不仅提供了一系列的分布式的Java常用对象，还提供了许多分布式服务。其中包括(`BitSet`, `Set`, `Multimap`, `SortedSet`, `Map`, `List`, `Queue`, `BlockingQueue`, `Deque`, `BlockingDeque`, `Semaphore`, `Lock`, `AtomicLong`, `CountDownLatch`, `Publish / Subscribe`, `Bloom filter`, `Remote service`, `Spring cache`, `Executor service`, `Live Object service`, `Scheduler service`) 

Redisson底层采用的是[Netty](http://netty.io/) 框架。支持[Redis](http://redis.cn) 2.8以上版本，支持Java1.6+以上版本。

https://github.com/redisson/redisson

## zookeeper

Curator 是一个 ZK 的开源客户端，也提供了分布式锁的实现。它的使用方式也比较简单：

```text
InterProcessMutex interProcessMutex = new InterProcessMutex(client,"/anyLock"); 
interProcessMutex.acquire(); 
interProcessMutex.release();
```

一个完整示例如下

```java
import java.util.concurrent.TimeUnit;
import lombok.Cleanup;
import lombok.SneakyThrows;
import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.locks.InterProcessMutex;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.zookeeper.data.Stat;


public class ZkLock {

  @SneakyThrows
  public static void main(String[] args) {

    final String connectString = "localhost:2181,localhost:2182,localhost:2183";

    // 重试策略，初始化每次重试之间需要等待的时间，基准等待时间为1秒。
    RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);

    // 使用默认的会话时间（60秒）和连接超时时间（15秒）来创建 Zookeeper 客户端
    @Cleanup CuratorFramework client = CuratorFrameworkFactory.builder().
        connectString(connectString).
        connectionTimeoutMs(15 * 1000).
        sessionTimeoutMs(60 * 100).
        retryPolicy(retryPolicy).
        build();

    // 启动客户端
    client.start();

    final String lockNode = "/lock_node";
    InterProcessMutex lock = new InterProcessMutex(client, lockNode);
    try {
      // 1. Acquire the mutex - blocking until it's available.
      lock.acquire();

      // OR

      // 2. Acquire the mutex - blocks until it's available or the given time expires.
      if (lock.acquire(60, TimeUnit.MINUTES)) {
        Stat stat = client.checkExists().forPath(lockNode);
        if (null != stat){
          // Dot the transaction
        }
      }
    } finally {
      if (lock.isAcquiredInThisProcess()) {
        lock.release();
      }
    }
  }

}
```



# Mockito

http://static.javadoc.io/org.mockito/mockito-core/2.18.3/org/mockito/Mockito.html#0

依赖

```groovy
testCompile "org.mockito:mockito-core:2.+"
```



## Mock对象注入

示例，Mock一个对象替换SampleService对象中的SampleDependency类型的字段。

绕过访问级别的“黑魔法”，但不太优雅。

```java
SampleDependency dependency = mock(SampleDependency.class);
SampleService service = new SampleService();
//spring-test提供的api
ReflectionTestUtils.setField(service, "dependency", dependency);
```

推荐使用mockito 的InjectMocks注解

```java
//初始化mock对象和进行注入的。相当于MockitoAnnotations.initMocks(this)或@RunWith(MockitoJUnitRunner.class)
@Rule public MockitoRule rule = MockitoJUnit.rule();
@Mock SampleDependency dependency;
@InjectMocks SampleService sampleService;
```

Spring注入替换成Mock的对象

```java
@RunWith(SpringRunner.class)
@DirtiesContext
@SpringBootTest
public class ServiceWithMockTest {
    @Rule public MockitoRule rule = MockitoJUnit.rule();
    @Mock DependencyA dependencyA;
    @Autowired @InjectMocks SampleService sampleService;

    @Test
    public void testDependency() {
        when(dependencyA.getExternalValue(anyString())).thenReturn("mock val: A");
        assertEquals("mock val: A", sampleService.foo());
    }
}
```

SpringBoot提供的@MockBean

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class ServiceWithMockBeanTest {
    @MockBean SampleDependencyA dependencyA;
    @Autowired SampleService sampleService;

    @Test
    public void testDependency() {
        when(dependencyA.getExternalValue(anyString())).thenReturn("mock val: A");
        assertEquals("mock val: A", sampleService.foo());
    }
}
```



## 示例

测试Servlet

```java
package org.gradle.demo;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import javax.servlet.RequestDispatcher;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.PrintWriter;
import java.io.StringWriter;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

public class HelloServletTest {
    @Mock private HttpServletRequest request;
    @Mock private HttpServletResponse response;
    @Mock private RequestDispatcher requestDispatcher;

    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void doGet() throws Exception {
        StringWriter stringWriter = new StringWriter();
        PrintWriter printWriter = new PrintWriter(stringWriter);

        when(response.getWriter()).thenReturn(printWriter);

        new HelloServlet().doGet(request, response);

        assertEquals("Hello, World!", stringWriter.toString());
    }

    @Test
    public void doPostWithoutName() throws Exception {
        when(request.getRequestDispatcher("response.jsp"))
            .thenReturn(requestDispatcher);

        new HelloServlet().doPost(request, response);

        verify(request).setAttribute("user", "World");
        verify(requestDispatcher).forward(request,response);
    }

    @Test
    public void doPostWithName() throws Exception {
        when(request.getParameter("name")).thenReturn("Dolly");
        when(request.getRequestDispatcher("response.jsp"))
            .thenReturn(requestDispatcher);

        new HelloServlet().doPost(request, response);

        verify(request).setAttribute("user", "Dolly");
        verify(requestDispatcher).forward(request,response);
    }
}
```

## 打桩

when(mockedList.get(0)).thenReturn("first");

## verify验证对象是否以特定方式调用方法

也可以使用参数匹配器验证入参

## 自定义匹配器

argThat会返回null，因此如果把argThat作为参数，可能会导致空指针异常。

## 验证调用次数、顺序

verify（xx, times(3)).add 验证调用次数
InOrder和verify一起验证一个或多个对象的调用顺序

## 根据参数动态处理（比如打印）、返回

doAnswer(new xxxAnswer()).when(xxx).xxxMethod(paramxxx);
对无返回void方法，doAnswer返回null

```
            Mockito.doAnswer(t -> {
 
                System.out.println( "close");
 
                return null;
 
            }).when(conn).close();
 
 
 
            Mockito.doAnswer(t->{
 
                Object[] params = t.getArguments();
 
                return currentColumnMap.get( params[0] ) ;
 
            }).when(rs).getObject(Mockito.anyString()) ;
 
```

## 监控对象

使用Spy可以让我们能够监视一个真实对象,既可以对这个对象的某一个函数打桩返回我们期望的值,也可以去调用真实的方法.

调用真实方法示例：

```
List list = new LinkedList();
 
List spy = spy(list);
 
// Will throw java.lang.IndexOutOfBoundsException: Index: 0, Size: 0
 
when(spy.get(0)).thenReturn("java");
 
assertEquals("java", spy.get(0));
 
```

安全的打桩：Using doAnswer we can stub it safely.

```
List list = new LinkedList();
 
List spy = spy(list);
 
doAnswer(invocation -> "java").when(spy).get(0);
 
assertEquals("java", spy.get(0));
 
 
 
//Actually, if you don't want to do additional actions upon method invocation, you can just use doReturn.
 
 
 
List list = new LinkedList();
 
List spy = spy(list);
 
doReturn("java").when(spy).get(0);
 
assertEquals("java", spy.get(0));
 
```

