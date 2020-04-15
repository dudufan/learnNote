[TOC]


# 测试驱动开发指南

- 设计。画图示比如UML，但有时不需要
- 编写测试，一小步一小步修改设计


## TDD三定律


- 没有测试之前不要写任何功能代码
- 只编写恰好能够体现一个失败情况的测试代码
- 只编写恰好能通过测试的功能代码


# 敏捷设计
- 设计中的臭味是因为违反一个或多个设计原则。
- 过度遵循设计原则反而会导致臭味
- 源代码就是设计。UML只是描绘设计的一些部分。

# 设计原则
## 单一职责原则（SRP)
### 类的单一职责
>就一个类而言，应该仅有一个引起它变化的原因。

比如：
- 保龄球计分程序，Game类只负责跟踪当前轮frame（返回当前轮总得分），Scorer类负责计算比赛的得分。
- Retangle矩形类中有两个职责，一是包含GUI代码绘制矩形，二是计算矩形面积。那么单纯计算几何学的应用使用Retangle类，会包含多余GUI的代码，浪费链接时间、编译时间以及内存占用。

如果一个类承担的责任过多，一个职责的变化可能会削弱或者抑制这个类完成其他职责的能力。这种耦合会导致脆弱的设计，当变化发生时，设计会遭受破坏。

区分一个类具有单个职责还是多个职责，是在变化实际发生（有征兆）时才有意义。
 ### 函数的单一职责
确保函数只做一件事，函数中的语句都要处在同一个抽象层级上。


## 开放-封闭原则（OCP)
- 开放和封闭都是相对于某种变化而言。
- 不可能完全封闭，只能猜测最有可能发生的变化种类，然后构造抽象来隔离变化。
- 变化发生时，就创建抽象来隔离以后的同类变化。
例子：Shape-Circle-Square的例子只能保证对形状类型变化开发-封闭，也就是drawAllShapes函数对变化做到封闭。但如果drawAllShapes要求先绘制圆，再绘制正方形，那么Shape的抽象反倒成为障碍。

### 如何刺激变化
- 编写测试。因为测试前已经构建了使系统可测试的抽象。
- 短期迭代。
- 开发基础结构前就开发特性并展示给涉众。
- 首先开发最重要的特性。
- 尽早、尽可能频繁的发布软件。

### 使用抽象获得显示封闭
如果drawAllShapes要求先绘制圆，再绘制正方形。可以：
1. 定义排序策略，意味着给两个对象可以推导出绘制哪一个。Shape中增加Precedes(Shape)方法判断先于哪种图形绘制。
2. 在drawAllShapes中先排序，再绘制。
3. 带来问题，每创建一个Shape类，所有Shape类的Precedes方法都要修改。无法对新派生类的添加做到封闭。

### 使用"数据驱动”的方法获取封闭性
为了让Preceds不依赖于具体某种Shape类型:
1. 查表获取Shape参数的order
2. 查表获取自己Shape类的order
3. 比较

## 继承：Liskov替换原则（LSP)
子类型必须能够替换掉他们的基类型。
个人理解：基类型具有的性质，子类型同样具有，这样才能完成同样的行为。

举例：
Square从Rectangle派生，Square的编写者没有违反正方形的不变形，违反的是Rectangle的不变性。

 

继承IS-A关系是就行为方式而言。行为方式可以进行合理假设。

如何明确化合理的假设？

- 契约通过每个方法声明前置条件和后置条件来指定。派生类的方法只能使用相等或更弱的前置条件来替换基类的前置条件，只
  能使用相等或更强的后置条件来替换基类的后置条件。
- 可以在单元测试中指定契约。

违反LSP后采取的解决方案：

- 约定使用范围，不把违反LSP的子类暴露给整个应用程序。一次违反会导致整个结构的失败，这种方案很可能不奏效。
- PersistentSet的Add方法只支持加入PersistentObject对象，所以将PersistentSet和Set统一在一个具有Remove等其他方法的抽象接口MemberContainer下。
- 提取公共部分作为基类。比如，LineSegment需要Line的所有成员变量、方法，可以提取公共部分作为基类LinearObject

## 依赖倒置原则
不同于传统面向过程设计，高层模块不再依赖于底层模块，这样高层模块容易被重用。这是框架设计的核心原则。
不仅倒置依赖关系，接口所有权也倒置。往往是客户（高层模块）拥有抽象接口，服务者（低层模块）则从这些抽象接口派生。

举例：

Button对象控制Lamp对象，不成熟的设计是Lamp依赖于Button。因为button要通知lamp，所以是Lamp依赖于Button。

```java
public class Button
{
    private Lamp itsLamp;
    public void poll(){
        if (/* some condition */) {
            itsLamp.turnOn();
        }
    }
}
```

倒置Lamp的依赖关系，让Lamp依赖于SwitchableDevice接口。SwitchableDevice接口没有所有者，可以被button客户使用，也可以被其他客户使用，所以单独放在一个package中。

 

静态模板方法（静态多态性）可以替代从公共基类继承（动态多态性）。有两个缺点：

- 类型不能运行时修改

- 新类型会迫使重新编译部署。

- 除非严格要求性能，否则优先使用动态多态性。

## 接口隔离原则（ISP)
举个TImedDoor的例子.

TimedDoor是Door的派生类（接口），门开着时间过长，它会发出警报声。为了做到这一点，需要把timedDoor注册到Timer类对象timer的register方法中, 然后timer会通知timedDoor超时。

```
public interface TimedDoor extends Door{
    public void doorTimeout();
}
 
public class Timer {
    public void register(int timeout, TimerClient client) {
        System.out.println("register timedDoor to timer!");
        try {
            sleep(timeout);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        client.timeout();
    }
}
 
public interface TimerClient {
    public void timeout();
}
 
```
TimedDoor需要实现Door接口，也需要实现TimerClient接口让Timer通知它超时。为了分离TimedDoor接口和TimerClient接口，有两种方法：
- 委托。可以理解为
- 多重继承

 

委托实现：

- timedDoor并不需要实现TimerClient接口。
- 当TimedDoor想向Timer对象注册一个超时请求时，它就创建一个DoorTimerAdapter并把它注册给Timer。
- Timer对象发送timeout消息给DoorTimerAdapter对象，DoorTimerAdapter把这个消息委托给TimedDoor。

```java
import isp.TimedDoor;
import isp.Timer;
import isp.TimerClient;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
 
import javax.sql.DataSource;
 
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;
 
public class TestTimerDoor {
 
    @Mock
    TimedDoor timedDoor;
 
    Timer timer = new Timer();
 
    @Mock
    TimerClient doorTimeAdapter;
 
    static DataSource dataSource;
 
    @BeforeClass
    public static void initClass() {
    }
 
    @Before
    public void init() {
        MockitoAnnotations.initMocks(this);
    }
 
    @Test
    public void testTimeout() {
        // timedDoor 实现了TImedDoor接口
        Mockito.doAnswer(t -> {
            System.out.println("door timeout!");
            return null;
        }).when(timedDoor).doorTimeout();
 
        // doorTimeAdapter实现了TimerClient接口，而没有让timedDoor实现TImedDoor接口
        Mockito.doAnswer(t -> {
            timedDoor.doorTimeout();
            return null;
        }).when(doorTimeAdapter).timeout();
 
        timer.register(2000, doorTimeAdapter);
    }
}
```

 

增加新接口代替改变现有接口：

```java
void Client(Service *s) {
    // Service转换为它的子类NewService
    if (NewService* ns = dynamic_cast<NewService *> (s)){
        // use the new service interface
    }
}
```

 

# 设计模式

## 工厂模式
高层组件PizzaStore和底层组件（各种Pizza具体类）都依赖于Pizza抽象：
ChicgoPizza、ChinesePizza实现Pizza“接口”（广义），PizzaStore使用Pizza抽象

设计时倒置思考方式
先从Pizza开始，抽象化一个Pizza

尽量避免违反依赖倒置原则：
1. 变量不持有具体类的引用
2. 不要让类派生自具体类
3. 不要覆盖基类已实现的方法

工厂方法模式：
定义：定义了一个创建对象的接口，但由子类决定要实例化的类是哪一个。工厂方法让类把实例化推迟到子类
例：每个PizzaStore的子类实现createPizza方法（都覆盖了抽象类PizzaStore的createPizza方法）

抽象工厂模式：
提供了一个接口，用于创建相关或依赖对象的家族，而不需要明确指定类
每种Pizza中原料组合不同，使用不同的Pizza原料工厂（都继承自抽象工厂）

抽象工厂的方法经常以工厂方法实现

## 代理模式
问：如何让客户使用代理，而不是真实对象？：常用技巧是提供一个工厂，实例化发生在工厂方法内。可以用代理包装主题再返回。

问：代理和适配器的区别？
答：适配器会改变对象适配的接口，而**代理则实现相同的接口**。

问：代理和装饰者模式的区别？
答：
代理也可能自己取得主题（实例化对象），这和装饰者模式不同。
装饰者模式可能将一个主题包装多次。

## 命令模式
Command接口

    execute() 唯一的方法

LightOnCommand类

    Light light;
    execute();//实现了Command接口，execute()方法中调用light.On()方法

还可以定义其他很多实现Command接口的具体类
SimpleRemoteControl类

    Command cmd;//组合Command接口
    setCommand(Command);//设置命令
    buttonWasPressed();//方法调用Commmand.execute()
实例：

- 数据库事务操作。Transaction接口有validate() execute()方法，分离了从用户获取数据、验证、执行的代码，从而实现了实体上的解耦和时间上的解耦（用户可以先获取数据、凌晨在执行数据库插入更新操作）。
- GUI的do/UNDO操作。
- 设备控制。遥控器例子。
- 多线程核心

总结：COMMAND模式对函数的关注超过了类，但在实际软件开发中很有用。

 

## 模板方法模式 Template Method

示例：

抽象基类是冒泡排序类BubbleSorter，派生类覆写swap、outOfOrder方法，比如IntBubbleSorter。

 

缺点：

- 派生类会和基类绑定在一起。比如，他排序算法没办法重用outOfOrder和swap。

## 策略模式 Strategy

继续BubbleSorter的例子。为了让其他交换排序算法（快速排序）也能重用outOfOrder和swap方法，可以把这几个方法也抽象成SortHandle接口。

```
public interface SortHandle{
    public void swap(int index);
    public boolean outOfOrder(int index);
    public int length();
    public void setArray(Object Array);
}
```

BubbleSorter不需要派生出IntBubbleSorter，只需要把swap操作委托给SortHandle的实现类IntSortHandle。

- SortHandle派生出IntSortHandle、DoubleSortHandle
- BubbleSorter依赖于SortHandle。
- 不仅BubbleSorter可以使用多种SortHandle，QuickBubbleSorter也可以用。这是策略模式比模板方法多的好处。

```
public class BubbleSorter{
    public BubbleSorter(SortHandle handle){
        itsSOrtHandle = handle;
    }
 
    public int sort(Object array){
        ...
    }
}
 
// 策略模式的优点，在于SortHandle可以用于其他算法
public class QuickBubbleSorter{
    public QuickBubbleSorter(SortHandle handle){
        itsSOrtHandle = handle;
    }
 
    public int sort(Object array){
        ...
    }
}
```


# 编程细则
## Switch
如果无法避免Switch，尽量用于创建多态对象（也就是放在抽象工厂中）。
## 对象、数据结构
>对象把数据隐藏于抽象之后，暴露操作数据的函数。数据结构暴露其数据，而没有提供有意义的函数。


面向过程:
- 添加函数时，不需要修改 数据结构。
- 添加数据结构时，必须修改所有函数。  


面向对象:
- 添加函数时，必须修改所有的类
- 添加新类， 不需要修改函数 。

所以系统如果需要经常添加数据类型（类），面向对象比较合适。
## 避免火车代码
>模块不应该通过getter、setter方法暴露其内部结构。


因此ctx.getxxx().get().get（)应当避免。并且这样的代码的抽象层级也不正确，太过细节。
可以包含到一个私有方法中。
## 抽离try/catch
try/catch代码搞乱了代码结构，最好把它单独抽出一个函数：
```
void delete(){
    try{
        deleteItem();

    }catch{
    }
}
void deleteItem(){
        1. xxxx
        2. xxxx

        3. xxxx

}
```