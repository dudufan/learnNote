[TOC]
commonpool
redisTemplate, not its type). By default, if commons-pool2 is on the classpath, you get a pooled connection factory.

健康检查

上下文隔离 类隔离

# 文档

Spring整合 https://docs.spring.io/spring/docs/5.2.2.RELEASE/spring-framework-reference/integration.html#spring-integration

# 演进

Spring 2.5引入了基于注解的组件扫描，这消除了大量针对应用程序自身组件的显式XML配置。

Spring 3.0引入了基于Java的配置，这是一种类型安全的可重构配置方式，可以代替XML。

# IOC

IoC（Inverse of Control:控制反转）是一种**设计思想**，就是 **将原本在程序中手动创建对象的控制权，交由Spring框架来管理。**  IoC 在其他语言中也有应用，并非 Spring 特有。

 **IoC 容器是 Spring 用来实现 IoC 的载体，  IoC 容器实际上就是个Map（key，value）,Map 中存放的是各种对象。**

作用：将对象之间的相互依赖关系交给 IoC 容器来管理，并由 IoC 容器完成对象的注入。这样可以很大程度上简化应用的开发，把应用从复杂的依赖关系中解放出来。 

IOC初始化的大致过程：XML --读取–> Resource –解析–> BeanDefinition –注册–> BeanFactory

ioc容器工作流程分为两个阶段：

1. 容器启动。也就是注册BeanDefinition到相应的BeanDefinitionRegistry
2. BeanFactoryPostProcessor修改BeanDefinition
3. Bean实例化。请求方通过容器的 getBean 方法明确地请求某个对象，或者因依赖关系容器
   需要隐式地调用 getBean 方法时，会实例化Bean。
4. BeanPostProcessor 会处理容器内所有符合条件的实例化后的对象实例。同时也会处理Aware 接口注入
5. init destroy

## 控制反转

软件系统在没有引入IOC容器之前，对象A依赖于对象B，那么对象A在初始化或者运行到某一点的时候，自己必须主动去创建对象B或者使用已经创建的对象B。无论是创建还是使用对象B，控制权都在自己手上。
软件系统在引入IOC容器之后，这种情形就完全改变了，由于IOC容器的加入，对象A与对象B之间失去了直接联系，所以，当对象A运行到需要对象B的时候，IOC容器会主动创建一个对象B注入到对象A需要的地方。
通过前后的对比，我们不难看出来：对象A获得依赖对象B的过程,由主动行为变为了被动行为，控制权颠倒过来了，这就是“控制反转”这个名称的由来。

## BeanFactory

工作原理：

1. 不同的外部配置文件格式，给出相应的BeanDefinitionReader实现类，读取并映射为BeanDefinition
2. BeanDefinition 注册到一个 BeanDefinitionRegistry 
3. BeanDefinitionRegistry 完成Bean的注册和加载
4. 每个受管对象的BeanDefinition都存在于容器中
5. 客户端向 BeanFactory 请求相应对象的时候， BeanFactory 会根据BeanDefinition返回对象实例

伪代码

```java
BeanDefinitionRegistry beanRegistry = <某个 BeanDefinitionRegistry 实现类，通常为➥
DefaultListableBeanFactory>;
BeanDefinitionReader beanDefinitionReader = new BeanDefinitionReaderImpl(beanRegistry);
beanDefinitionReader.loadBeanDefinitions("配置文件路径");
// 现在我们就取得了一个可用的BeanDefinitionRegistry实例
```

Spring还在 DefaultListableBeanFactory 的基础上构建了简化XML格式配置加载的 XmlBeanFactory 实现:

```java
beanFactory = new XmlBeanFactory(new ClassPathResource("../news-config.xml"));
//XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(registry);
//reader.loadBeanDefinitions("classpath:../news-config.xml");
```



实现类：

```shell
BeanFactory接口提供最基本的IOC容器管理Bean的功能。好比图书馆

BeanDefinitionRegistry: 在实现中负责注册管理Bean，好比书架

DefaultListableBeanFactory是很重要的一个Ioc实现，其他ioc容器也通过扩展它实现。

DefaultListableBeanFactory实现了BeanFactory接口和BeanDefinitionRegistry接口

BeanDefinitionReader：解析配置文件得到BeanDefinition，如XmlBeanDefinitionReader
```





1. 

## BeanFactoryPostProcessor

BeanFactoryPostProcessor 机制允许我们在容器实
例化相应对象之前，对注册到容器的 BeanDefinition 修改，如修改对象属性信息。

Spring提供的几个BeanFactoryPostProcessor接口的实现类：

- PropertyPlaceholderConfigurer。可以用properties配置的key-value替换占位符
- PropertyOverrideConfigurer。属性覆盖
- CustomEditorConfigurer。自定义字符串和对象之间的转换规则

手动注册的伪代码：

```java
ceConfigurer.postProcessBeanFactory(beanFactory);
```

## BeanPostProcessor

Spring同样可以针对容器中的所有Bean，或者某些Bean定制初始化过程，只需提供一个实现BeanPostProcessor接口的类即可。

ApplicationContext会自动检测在配置文件中实现了BeanPostProcessor接口的所有bean，并把它们注册为后置处理器，然后在容器创建bean的适当时候调用它 



```java
public class PasswordDecodePostProcessor implements BeanPostProcessor {
	public Object postProcessAfterInitialization(Object object, String beanName)
throws BeansException {
        return object;
    }
    public Object postProcessBeforeInitialization(Object object, String beanName)
throws BeansException {
        if(object instanceof PasswordDecodable)
        {
            String encodedPassword = ((PasswordDecodable)object).getEncodedPassword();
            String decodedPassword = decodePassword(encodedPassword);
            ((PasswordDecodable)object).setDecodedPassword(decodedPassword);
        }
        return object;
    }
    
    private String decodePassword(String encodedPassword) {
        // 实现解码逻辑
        return encodedPassword;
    }
    
}
```

 ApplicationContext 容器会自动识别并加载注册到容器的 BeanPostProcessor。

以下xml配置加入了@Autowired、JSR250等注解的：

- AutowiredAnnotationBeanPostProcessor 处理Autowired注解，注入
- CommonAnnotationBeanPostProcessor
- PersistenceAnnotationBeanPostProcessor 
- RequiredAnnotationBeanPostProcessor

```xml
 <context:annotation-config>
```



## Bean生命周期

![](img\Bean生命周期.png)

详细的测试验证输出如下：

```java
Spring容器初始化
=====================================
调用GiraffeService无参构造函数
GiraffeService中利用set方法设置属性值
【BeanNameAware接口】调用setBeanName:: Bean Name defined in context=giraffeService
【BeanClassLoaderAware接口】调用setBeanClassLoader,ClassLoader Name = sun.misc.Launcher$AppClassLoader
【BeanFactoryAware接口】调用setBeanFactory,setBeanFactory:: giraffe bean singleton=true
【XxxAware接口】调用setEnvironment
【XxxAware接口】调用setResourceLoader:: Resource File Name=spring-beans.xml
【XxxAware接口】调用setApplicationEventPublisher
【XxxAware接口】调用setApplicationContext:: Bean Definition Names=[giraffeService, org.springframework.context.annotation.CommonAnnotationBeanPostProcessor#0, com.giraffe.spring.service.GiraffeServicePostProcessor#0]
【BeanPostProcessor接口】执行BeanPostProcessor的postProcessBeforeInitialization方法,beanName=giraffeService
调用PostConstruct注解标注的方法
【InitializingBean接口】执行InitializingBean接口的afterPropertiesSet方法
【init-method】执行配置的init-method
【BeanPostProcessor】执行BeanPostProcessor的postProcessAfterInitialization方法,beanName=giraffeService
Spring容器初始化完毕
=====================================
从容器中获取Bean
giraffe Name=李光洙
=====================================
调用preDestroy注解标注的方法
【DiposableBean接口】执行DisposableBean接口的destroy方法
【destroy-method】执行配置的destroy-method
Spring容器关闭
```

Bean的完整生命周期经历了各种方法调用，这些方法可以划分为以下几类：

1. Bean自身的方法。包括了Bean本身调用的方法和通过配置文件中<bean>的init-method和destroy-method指定的方法
2. Aware接口的方法
3. BeanPostProcessor接口的方法
4. BeanFactoryPostProcessor接口的方法

单例bean默认会在启动容器时实例化

prototype 的bean容器不会持有，容器关闭时，destroy 方法不会被调用

**实例化**

容器在内部实现的时候，采用“策略模式（Strategy Pattern）”来决定采用何种方式初始化bean实例。

1. 根据相应bean定义的 BeanDefintion 取得实例化信息
2. 结合 CglibSubclassingInstantiationStrategy 以及不同的bean定义类型，就可以返回实例化完成的对象实例
3. 以 BeanWrapper 对构造完成的对象实例进行包裹，返回

**构造后初始化**

 `@PostConstruct` 注解的方法将会在依赖注入完成后被自动调用。

**销毁**

 `@PreDestroy`注解的方法将会在容器关闭前被自动调用。

如果处在一个非WBE的应用环境下，为了能让Spring容器优雅的关闭，并调用singleton Bean上的相应析构方法，则需要在JVM里注册一个关闭钩子（shutdown hook）。多例创建后就不被容器管理，无法调用destroy方法

```java
//使用标准的 Runtime 类的 addShutdownHook() 方式来调用相应bean对象的销毁逻辑
((AbstractApplicationContext)container).registerShutdownHook();
```

参考：

https://www.cnblogs.com/zrtqsk/p/3735273.html

https://yemengying.com/2016/07/14/spring-bean-life-cycle/

## Bean加载顺序

**Bean间依赖**

我们可以在bean A上使用`@DependsOn`注解，告诉容器bean B应该先被初始化

**PriorityOrdered接口**

bean实现了PriorityOrdered接口，就会提前实例化

bean实例化之后就不能被beanPostProcessor处理。因此要避免让个别bean意外提前实例化，导致不能被Spring提供的一些beanPostProcessor处理，比如

一般Spring默认的beanPostProcessor都实例化之后，才会实例化自定义的beanPostProcessor。如果自定义的beanPostProcessor实现了PriorityOrdered接口，就会提前实例化

## Bean的作用域

- 单例作用域用于无状态的bean。不需要保存状态。可能会有线程安全化的问题，可以在类中定义一个ThreadLocal成员变量，将需要的可变成员变量保存在 ThreadLocal 中。
- *prototype*用于有状态的bean。每一次请求（从容器中取bean）都会产生一个新的bean实例，相当new.
- request : 每一次HTTP请求都会产生一个新的bean，该bean仅在当前HTTP request内有效。
- session : 每一次HTTP请求都会产生一个新的 bean，该bean仅在当前 HTTP session 内有效。
- global-session：  全局session作用域，仅仅在基于portlet的web应用中才有意义，Spring5已经没有了。Portlet是能够生成语义代码(例如：HTML)片段的小型Java  Web插件。它们基于portlet容器，可以像servlet一样处理HTTP请求。但是，与 servlet 不同，每个 portlet  都有不同的会话

问题：单例bean依赖*prototype* bean的情况：默认只注入一次（第一次new的*prototype* bean）。

解决办法：Spring提供了解决方案如下，每次访问（也就是获取）多例对象字段时，都会为单例对象也生成一个代理子类对象，里面的多例对象是新的。

多例对象的作用域注解如下：

```java
@Scope(value = ConfigurableBeanFactory.SCOPE_PROTOTYPE, proxyMode = ScopedProxyMode.TARGET_CLASS)  
```

其他办法：

- 方法注入
- 注入BeanFactory，每次使用都getBean获取
- 使用ObjectFactoryCreatingFactoryBean返回特定类型的FactoryBean（getObject通过getBean获取），再绑定到单例对象上



### 扫描

```xml
<context:component-scan base-package="org.spring21"/>
```

 支持扫描各类bean。同时将 AutowiredAnnotationBeanPostProcessor 和
CommonAnnotationBeanPostProcessor 一并注册到了容器中

@Component的语义更广 、更宽泛

@Repository 、 @Service 和 @Controller的语义具体

### Bean引用

**自动绑定**

byName

字段用名称查找bean的id（beanName) 

@Qualifier 实际上是 byName 自动绑定的注解版

**内部Bean**

xml中可以声明内部bean，防止被其他bean误引用。

### FactoryBean

sofa不能直接注入ClientFactory，必须让bean实现ClientFactoryAware接口注入。为了方便使用提供了一个FactoryBean，这样就可以在其他地方注入

```java
@Component
public class ClientFactoryBean implements ClientFactoryAware, FactoryBean<ClientFactory> {
    private ClientFactory clientFactory;

    @Override
    public void setClientFactory(ClientFactory clientFactory) {
        this.clientFactory = clientFactory;
    }

    @Override
    public ClientFactory getObject() throws Exception {
        return clientFactory;
    }

    @Override
    public Class<?> getObjectType() {
        return ClientFactory.class;
    }
}

@Component
public class BaseBoltClient{

    @Autowired
    private ClientFactory clientFactory;
}
```

## Bean创建

Bean实例化过程：

（1）ResourceLoader加载配置信息

（2）BeanDefinitionReader读取并解析<bean>标签，并将<bean>标签的属性转换为BeanDefinition对应的属性，并注册到BeanDefinitionRegistry注册表中。

（3）容器扫描BeanDefinitionRegistry注册表，通过反射机制获取BeanFactoryPostProcessor类型的工厂后处理器，并用这个工厂后处理器对BeanDefinition进行加工。

（4）根据处理过的BeanDefinition，实例化bean。然后BeanWrapper结合BeanDefinitionRegistry和PropertyEditorRegistry对Bean的属性赋值。



Spring依赖注入Bean实例默认是单例的，我们由此展开。

AbstractBeanFactory.getBean –> doGetBean –> getSingleton进行bean的创建，双重判断加锁

```java
/**
     * Return the (raw) singleton object registered under the given name.
     * <p>Checks already instantiated singletons and also allows for an early
     * reference to a currently created singleton (resolving a circular reference).
     * @param beanName the name of the bean to look for
     * @param allowEarlyReference whether early references should be created or not
     * @return the registered singleton object, or {@code null} if none found
     */
    protected Object getSingleton(String beanName, boolean allowEarlyReference) {
        Object singletonObject = this.singletonObjects.get(beanName);
        if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
            synchronized (this.singletonObjects) {
                singletonObject = this.earlySingletonObjects.get(beanName);
                if (singletonObject == null && allowEarlyReference) {
                    ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                    if (singletonFactory != null) {
                        //实际上是调用了AbstractAutowireCapableBeanFactory的doCreateBean方法，返回了BeanWrapper包装并创建的bean实例
                        //ObjectFactory主要检查是否有用户定义的BeanPostProcessor后处理内容，并在创建bean时进行处理，如果没有，就直接返回bean本身
                        singletonObject = singletonFactory.getObject();
                        this.earlySingletonObjects.put(beanName, singletonObject);
                        this.singletonFactories.remove(beanName);
                    }
                }
            }
        }
        return (singletonObject != NULL_OBJECT ? singletonObject : null);
    }
```

Spring 通过 `ConcurrentHashMap` 实现单例注册表的特殊方式实现单例模式。Spring 实现单例的核心代码是getSingleton、addSingleton方法

## 注解声明Bean

我们一般使用 `@Autowired` 注解自动装配 bean，要想把类标识成可用于 `@Autowired` 注解自动装配的 bean 的类,采用以下注解可实现：

- `@Component` ：通用的注解，可标注任意类为 `Spring` 组件。如果一个Bean不知道属于哪个层，可以使用`@Component` 注解标注。

- `@Repository` : 对应持久层即 Dao 层，主要用于数据库相关操作。

- `@Service` : 对应服务层，主要涉及一些复杂的逻辑，需要用到 Dao层。

- `@Controller` : 对应 Spring MVC 控制层，主要用户接受用户请求并调用 Service 层返回数据给前端页面。

  

## Aware

为了让Bean可以获取到框架自身的一些对象，Spring提供了一组名为*Aware的接口。
这些接口均继承于`org.springframework.beans.factory.Aware`标记接口

- ApplicationContextAware: 获得ApplicationContext对象,可以用来获取所有Bean definition的名字。
- BeanFactoryAware:获得BeanFactory对象，可以用来检测Bean的作用域。
- BeanNameAware:获得Bean在配置文件中定义的名字。
- ResourceLoaderAware:获得ResourceLoader对象，可以获得classpath中某个文件。
- ServletContextAware:在一个MVC应用中可以获取ServletContext对象，可以读取context中的参数。
- ServletConfigAware在一个MVC应用中可以获取ServletConfig对象，可以读取config中的参数。

# ApplicationContext

`ApplicationContext`接口继承了`BeanFactory`（初始化和注入bean）接口，也可以管理`Bean`。

## 启动

ApplicationContext是ioc容器的高级形式，组合了beanFactory，继承了DefaultResourceLoader。

FileSystemXmlApplicationContext构造器中调用祖先类AbstractApplicationContext.refresh方法

refresh方法有三步：

1. Resource定位。比如FileSystemResource，ClassPathResource
2. 载入BeanDefinition
3. 向ioc容器中注册BeanDefinition

FileSystemXmlApplicationContext -- AbstractApplicationContext -->AbstractXmlApplicationContext –>AbstractRefreshableConfigApplicationContext –>AbstractRefreshableApplicationContext

AbstractApplicationContext.refresh方法实现关键的几步：

1. FileSystemXmlApplicationContext.refresh
2. AbstractRefreshableApplicationContext.refreshBeanFactory。创建了一个DefaultListableBeanFactory，loadBeanDefinitions(beanFactory)。完成Resource定位, beanDefinitions的载入和注册。
3. AbstractRefreshableApplicationContext.loadBeanDefinitions抽象 -> AbstractXmlApplicationContext.loadBeanDefinitions –>XmlBeanDefinitionReader.loadBeanDefinitions 定位Resource。
4. XmlBeanDefinitionReader.loadBeanDefinitions(EncodedResource encodedResource) 加载resource分为几步：a. 得到document对象 b. 得到documentReader c. 处理并注册BeanDefinition

AbstractApplicationContext.refresh源码

```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        // Prepare this context for refreshing.
        prepareRefresh();
        // Tell the subclass to refresh the internal bean factory.
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
        // Prepare the bean factory for use in this context.
        prepareBeanFactory(beanFactory);
        try {
            // Allows post-processing of the bean factory in context subclasses.
            postProcessBeanFactory(beanFactory);
            // Invoke factory processors registered as beans in the context.
            invokeBeanFactoryPostProcessors(beanFactory);
            // Register bean processors that intercept bean creation.
            registerBeanPostProcessors(beanFactory);
            // Initialize message source for this context.
            initMessageSource();
            // Initialize event multicaster for this context.
            initApplicationEventMulticaster();
            // Initialize other special beans in specific context subclasses.
            onRefresh();
            // Check for listener beans and register them.
            registerListeners();
            // Instantiate all remaining (non-lazy-init) singletons.
            finishBeanFactoryInitialization(beanFactory);
            // Last step: publish corresponding event.
            finishRefresh();
        } catch (BeansException ex) {
            // Destroy already created singletons to avoid dangling resources.
            destroyBeans();
            // Reset 'active' flag.
            cancelRefresh(ex);
            // Propagate exception to caller.
            throw ex;
        } finally {
            // Reset common introspection caches in Spring's core, since we
            // might not ever need metadata for singleton beans anymore...
            resetCommonCaches();
        }
    }
}
```

参考：https://github.com/seaswalker/spring-analysis/blob/master/note/Spring.md#%E6%9E%84%E9%80%A0%E5%99%A8

## 获取上下文

获取`ApplicationContext`的方法：

- [`@Autowired`](https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference/core.html#beans-autowired-annotation)也可以用来获取`ApplicationContext`。
- 实现`ApplicationContextAware` 接口

```java
@Component
public class SpringUtils implements ApplicationContextAware {
  private static ApplicationContext ctx;

  /**
   * 服务器启动，Spring容器初始化时，当加载了当前类为bean组件后，
   * 将会调用下面方法注入ApplicationContext实例
   */
  @Override
  public void setApplicationContext(ApplicationContext arg0) {
    System.out.println("setApplicationContext");
    SpringUtils.ctx = arg0;
  }

  public static ApplicationContext getCtx(){
    return ctx;
  }

  /**
   * 外部调用这个getBean方法就可以手动获取到bean
   * 用bean组件的name来获取bean
   * @param beanName
   * @return
   */
  @SuppressWarnings("unchecked")
  public static <T> T getBean(String beanName){
    return (T) ctx.getBean(beanName);
  }

  public static <T> T getBean(Class<T> beanClass)
  {
    return ctx.getBean(beanClass);
  }

  public static Map<String, Object> getBeansWithAnnotation(Class<? extends Annotation> annotation)
  {
    return ctx.getBeansWithAnnotation(annotation);
  }

  public static <T> Map<String, T> getBeansOfType(Class<T> beanClass)
  {
    return ctx.getBeansOfType(beanClass);
  }
}
```



## Resource

统一的资源接口

## ResourceLoader

ApplicationContext接口继承了ResourceLoader

```java
public interface ResourceLoader {
    String CLASSPATH_URL_PREFIX = ResourceUtils.CLASSPATH_URL_PREFIX;
    Resource getResource(String location);
    ClassLoader getClassLoader();
}
```

DefaultResourceLoader可以解析classpath、“/”开头的为ClassPathResource、各种URL（失败后默认构造ClassPathResource）

FileSystemResourceLoader继承自DefaultResourceLoader，覆盖了getResourceByPath方法。getResource方法相同，因此也能解析”classpath:“、各种URL资源，只是”/“开头、默认的为本地文件ResourceResourcePatternResolver是派生自ResourceLoader的接口，支持路径匹配返回多个 Resources。 最常用的一个实现是 PathMatchingResourcePatternResolver。

PathMatchingResourcePatternResolver加载资源的默认行为上会与 DefaultResourceLoader 基本相同，可以通过构造器传入改变默认行为。

AbstractApplicationContext 继承了 DefaultResourceLoader，内部也声明了PathMatchingResourcePatternResolver(this)，因此支持统一资源加载。

各类ApplicationContext和相应的ResourceLoader行为一致。

application contexts都实现了ResourceLoader接口，这样加载资源开发者不需要关注具体的Resource类。

```java
//  ClassPathXmlApplicationContext默认返回 ClassPathResource. 
// FileSystemXmlApplicationContext默认返回 FileSystemResource.
// WebApplicationContext默认返回 ServletContextResource. 
Resource template = ctx.getResource("some/resource/path/myTemplate.txt");
Resource template = ctx.getResource("classpath:some/resource/path/myTemplate.txt");
Resource template = ctx.getResource("file:///some/resource/path/myTemplate.txt");
Resource template = ctx.getResource("http://myhost.com/resource/path/myTemplate.txt");

// 默认的Resource类型也取决于特定上下文类型
ApplicationContext ctx = new ClassPathXmlApplicationContext("conf/appContext.xml");
ApplicationContext ctx =
    new FileSystemXmlApplicationContext("classpath:conf/appContext.xml");
```



 

静态资源可以直接配置为Resource类型的Bean

```
<bean id="myBean" class="...">
    <property name="template" value="some/resource/path/myTemplate.txt"/>
</bean>
```

## 国际化支持

 ApplicationContext 还实现了 MessageSource 接口，可以根据具体的Locale和key获取配置。



## 事件发布

一旦容器内发布 （也就是接收到）ApplicationEvent 及其子类型的事件，注册到容器的 ApplicationListener 就会对这些事件进行处理

```java
public class StartApplicationListener implements ApplicationListener<ContextRefreshedEvent> {
    
    @Override
  	public void onApplicationEvent(ContextRefreshedEvent contextRefreshedEvent) {
        //容器中的beans都初始化后，才会执行这里
    }
}
```

Spring 中默认存在以下事件，他们都是对 `ApplicationContextEvent` 的实现(继承自`ApplicationContextEvent`)：

- `ContextStartedEvent`：`ApplicationContext` 启动后触发的事件;
- `ContextStoppedEvent`：`ApplicationContext` 停止后触发的事件;
- `ContextRefreshedEvent`：`ApplicationContext` 初始化或刷新完成后触发的事件;
- `ContextClosedEvent`：`ApplicationContext` 关闭后触发的事件。

 发布一个事件：`applicationContext.publishEvent()` 

# Spring

Spring提供的基础功能

## 配置类

`@Configuration`指定配置类。

`@ImportResource` 可以导入xml配置。

@Import 可以导入配置类

`@ComponentScan`不指定包名，则扫描当前包下的组件（各类bean)。 组件扫描

## 环境配置



Environmen接口**代表了当前应用所处的环境。**从此接口的方法可以看出，其主要和profile、Property相关。

StandardEnvironment --> Environment --> PropertyResolver



PropertySource接口代表了键值对的Property来源



PropertyResolver接口用来解析PropertyResource。也用来解析占位符，如```new ClassPathXmlApplicationContext("${spring}:config.xml");```

## 依赖注入

bean如果有构造器，可以不写 `@Autowired`



注入配置的属性

```java
@Service
public class ProductService {    
    @Value("${server.port}")    
    String port;
}
```

也可以引用动态生成的属性，如

```java
new SpringApplicationBuilder(EurekaServerApplication.class).properties("server.port=" + port)
```



## 加载配置



[`@PropertySource`](https://docs.spring.io/spring/docs/5.1.4.RELEASE/javadoc-api/org/springframework/context/annotation/PropertySource.html)读取指定的配置文件。

绑定属性的两种方式

- 通过 @value 读取比较简单的配置信息。不推荐
- 通过@ConfigurationProperties读取并与 bean 绑定

 ```java
   // 注意@ConfigurationProperties注入的属性必须要有gettersetter方法
   //BookProperties这个类可以用@Component注册，也可以给其他配置类加上@EnableConfigurationProperties(BookProperties.class)，这样上下文中都可以通过@Autowired注入BookProperties这个bean了
   @Component
   @PropertySource("classpath:book.properties")
   @ConfigurationProperties(prefix = "book")
   public class BookProperties {
       String name;
   
       String author;
   
       public void setName(String name) {
           this.name = name;
       }
   
       public void setAuthor(String author) {
           this.author = author;
       }
   }
   
   //book.properties中配置book.name book.author
 ```



@EnableConfigurationProperties。在需要使用属性的配置类上可以引入配置bean

## Conditional

各种条件判断

```java
public class UserDAOBeanNotPresentsCondition implements Condition {
	@Override
	public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata metadata) {
		UserDAO userDAO = conditionContext.getBeanFactory().getBean(UserDAO.class);
		return (userDAO == null);
	}
}

public class MongoDriverNotPresentsCondition implements Condition {
	@Override
	public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata metadata) {
		try {
			Class.forName("com.mongodb.Server");
			return false;
		} catch (ClassNotFoundException e) {
			return true;
		}
	}
}

public class MongoDbTypePropertyCondition implements Condition {
	@Override
	public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata metadata) {
		String dbType = conditionContext.getEnvironment().getProperty("app.dbType");
		return "MONGO".equalsIgnoreCase(dbType);
	}
}
```

@Profile也是基于Conditional注解来实现的。

类似的实现一个@DatabaseType 

```java
@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Conditional(DatabaseTypeCondition.class)
public @interface DatabaseType {
	String value();
}

public class DatabaseTypeCondition implements Condition {
	@Override
	public boolean matches(ConditionContext conditionContext, AnnotatedTypeMetadata metadata) {
		Map<String, Object> attributes = metadata
											.getAnnotationAttributes(DatabaseType.class.getName());
		String type = (String) attributes.get("value");
		// 默认值为MySql
		String enabledDBType = System.getProperty("dbType", "MySql");
		return (enabledDBType != null && type != null && enabledDBType.equalsIgnoreCase(type));
	}
}
```

在配置类应用该注解：

```java
@Configuration
@ComponentScan
public class AppConfig {
	@Bean
	@DatabaseType("MySql")
	public UserDAO jdbcUserDAO() {
		return new JdbcUserDAO();
	}

	@Bean
	@DatabaseType("mongoDB")
	public UserDAO mongoUserDAO() {
		return new MongoUserDAO();
	}
}
```



@ConditionalOnClass 指定的类必须存在于类路径下

@ConditionalOnBean 容器中是否有指定的Bean

https://sylvanassun.github.io/2018/01/08/2018-01-08-spring_boot_auto_configure/

## FactoryBean

实现了FactoryBean接口的bean可以

# Spring-boot

## 概述

特点：

- 内置了嵌入式的Tomcat、Jetty等Servlet容器，应用可以不用打包成War格式，而是可以直接以Jar格式运行。
- 提供了多个可选择的”starter”以简化Maven的依赖管理（也支持Gradle），让您可以按需加载需要的功能模块。
- 尽可能地进行自动配置，减少了用户需要动手写的各种冗余配置项，Spring Boot提倡无XML配置文件的理念，使用Spring Boot生成的应用完全不会生成任何配置代码与XML配置文件。
- 提供了一整套的对应用状态的监控与管理的功能模块（通过引入spring-boot-starter-actuator），包括应用的线程信息、内存信息、应用是否处于健康状态等，为了满足更多的资源监控需求，Spring Cloud中的很多模块还对其进行了扩展。



## starters

starter的pom文件中定义了需要的所有依赖。

## Gradle

```groovy
apply plugin: 'java'
//检测到java插件后，就配置可执行jar的任务
apply plugin: 'org.springframework.boot'
//统一依赖管理，后面声明依赖时可以忽略版本号
apply plugin: 'io.spring.dependency-management'

sourceCompatibility = 1.8
targetCompatibility = 1.8

buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:2.0.5.RELEASE")
    }
}

bootJar {
    mainClassName = 'cn.how2j.springboot.web.ProductController'
    baseName = 'gs-messaging-redis'
    version = '0.1.0'
}

dependencies {
    //支持web，有内嵌的tomcat。也会包含最基础的组件
    compile("org.springframework.boot:spring-boot-starter-web")
    //spring boot基础核心功能 Core starter, including auto-configuration support, logging and YAML
    compile("org.springframework.boot:spring-boot-starter")
    testCompile('org.springframework.boot:spring-boot-starter-test')
}

```

子模块内如果打包失败，找不到被依赖的子模块代码，需要让被依赖子模块打出jar包，不打bootJar

```groovy
jar.enabled=true
bootJar.enabled=false
```

## 启动类

main方法启动类配置`@SpringApplication`注解，相当于`@Configuration`、`@EnableAutoConfiguration`、`@ComponentScan ` 注解的集合。推荐放在root package下。

- 包含了`@Configuration`。允许在上下文中注册额外的bean或导入其他配置类。
- 扫描被`@Component` (`@Service`,`@Controller`)注解的bean，注解默认会扫描该类所在的包下所有的类。
- 启用 SpringBoot 的自动配置机制。只要classpath依赖了jar包，就会自动配置或使用默认配置。比如应用依赖了redis，默认提供RedisConnectionFactory连接localhost:6379。
- 警告：不要使用默认包，自动扫描会出错。

```java

@SpringBootApplication // same as @Configuration @EnableAutoConfiguration @ComponentScan
public class Application {

    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(MySpringConfiguration.class);
        app.setBannerMode(Banner.Mode.OFF);
        app.run(args);


        new SpringApplicationBuilder()
                .sources(Parent.class)
                .child(Application.class)
                .bannerMode(Banner.Mode.OFF)
                .run(args);
        //动态配置端口
        new SpringApplicationBuilder(ProductDataServiceApplication.class).properties("server.port=" + port).run(args);
    }
}


```



`@EnableAutoConfiguration`激活Auto-configuration。根据依赖自动配置spring。也可以排除某些自动配置类。

```java
@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class, RedisRepositoriesAutoConfiguration.class})
```



## 自动配置

application配置中加入debug=true，打印条件装配的日志。或者 `--debug` 开启

自己显式声明的配置可以代替自动配置，比如自己的DataSource bean可以代替默认的嵌入式数据库。

不使用某些自动配置

```java
import org.springframework.boot.autoconfigure.*;
import org.springframework.boot.autoconfigure.jdbc.*;
import org.springframework.context.annotation.*;

@Configuration(proxyBeanMethods = false)
@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class})
public class MyConfiguration {
}
```

`@EnableAutoConfiguration` 注解通过Spring 提供的 `@Import` 注解导入了`AutoConfigurationImportSelector`类（`@Import` 注解可以导入配置类或者Bean到当前类中）。

`AutoConfigurationImportSelector`类中`getCandidateConfigurations`方法会将所有自动配置类的信息以 List 的形式返回。这些配置信息会被 Spring 容器作 bean 来管理。

```java
	protected List<String> getCandidateConfigurations(AnnotationMetadata metadata, AnnotationAttributes attributes) {
		List<String> configurations = SpringFactoriesLoader.loadFactoryNames(getSpringFactoriesLoaderFactoryClass(),
				getBeanClassLoader());
		Assert.notEmpty(configurations, "No auto configuration classes found in META-INF/spring.factories. If you "
				+ "are using a custom packaging, make sure that file is correct.");
		return configurations;
	}
```

`@Conditional` 注解。`@ConditionalOnClass`(指定的类必须存在于类路径下),`@ConditionalOnBean`(容器中是否有指定的Bean)等等都是对`@Conditional`注解的扩展。

拿 Spring Security 的自动配置举个例子:

`SecurityAutoConfiguration`中导入了`WebSecurityEnablerConfiguration`类，`WebSecurityEnablerConfiguration`源代码如下：

```java
@Configuration
@ConditionalOnBean(WebSecurityConfigurerAdapter.class)
@ConditionalOnMissingBean(name = BeanIds.SPRING_SECURITY_FILTER_CHAIN)
@ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
@EnableWebSecurity
public class WebSecurityEnablerConfiguration {

}
```

`WebSecurityEnablerConfiguration`类中使用`@ConditionalOnBean`指定了容器中必须还有`WebSecurityConfigurerAdapter` 类或其实现类。所以，一般情况下 Spring Security 配置类都会去实现 `WebSecurityConfigurerAdapter`，这样自动将配置就完成了。

## 启动运行

远程调试

```shell
java -Xdebug -Xrunjdwp:server=y,transport=dt_socket,address=8000,suspend=n \
       -jar target/myapplication-0.0.1-SNAPSHOT.jar
```

本地gradle启动

```shell
gradle bootRun
```

  SpringBoot启动的方式是SpringApplication.run(SpringbootConfigApplication.class, args);，它是自动到相应的目录中读取名称为application.properties的配置文件。

   也可以使用SpringApplicationBuilder配置属性：

```java
      new SpringApplicationBuilder(SpringbootConfigApplication.class)
          .properties("spring.config.location=classpath:/springbootconfig.properties").run(args);
```

  这种方式可以定义读取哪一个位置的配置文件进行启动SpringBoot



SpringApplication.run方法中，首先会实例化一个SpringApplication进行初始化

```java
public static ConfigurableApplicationContext run(Class<?>[] primarySources, String[] args) {
   return new SpringApplication(primarySources).run(args);
}
```

初始化过程：

1. 根据classpath里面是否存在某个特征类（org.springframework.web.context.ConfigurableWebApplicationContext）来决定是否应该创建一个为Web应用使用的ApplicationContext类型；
2. 使用SpringFactoriesLoader在应用的classpath中查找并加载所有可用的ApplicationContextInitializer；

3. 使用SpringFactoriesLoader在应用的classpath中查找并加载所有可用的ApplicationListener；
4. 推断并设置main方法的定义类

```java
public SpringApplication(ResourceLoader resourceLoader, Class<?>... primarySources) {
   this.resourceLoader = resourceLoader;
   Assert.notNull(primarySources, "PrimarySources must not be null");
   this.primarySources = new LinkedHashSet<>(Arrays.asList(primarySources));
   this.webApplicationType = WebApplicationType.deduceFromClasspath();
   setInitializers((Collection) getSpringFactoriesInstances(ApplicationContextInitializer.class));
   setListeners((Collection) getSpringFactoriesInstances(ApplicationListener.class));
   this.mainApplicationClass = deduceMainApplicationClass();
}
```

接下来才执行SpringApplication当前实例的run方法

```java
public ConfigurableApplicationContext run(String... args) {
   StopWatch stopWatch = new StopWatch();
    //创建StopWatch实例，并启动，记录任务的运行时间
   stopWatch.start();
   ConfigurableApplicationContext context = null;
   Collection<SpringBootExceptionReporter> exceptionReporters = new ArrayList<>();
    //设置系统属性java.awt.headless
   configureHeadlessProperty();
    //通过SpringFactoriesLoader类loadFactoryNames方法，查找并加载所有spring.factories文件中定义的SpringApplicationRunListener接口的实现，并调用starting方法启动监听器
   //这里才会获取到自定义的SpringApplicationRunListener
   SpringApplicationRunListeners listeners = getRunListeners(args);
   listeners.starting();
   try {
      ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
      ConfigurableEnvironment environment = prepareEnvironment(listeners, applicationArguments);
      configureIgnoreBeanInfo(environment);
      Banner printedBanner = printBanner(environment);
       //创建Spring应用上下文.springboot2.1.0默认web上下文是AnnotationConfigServletWebServerApplicationContext
      context = createApplicationContext();
      exceptionReporters = getSpringFactoriesInstances(SpringBootExceptionReporter.class,
            new Class[] { ConfigurableApplicationContext.class }, context);
       //准备上下文
      prepareContext(context, environment, listeners, applicationArguments, printedBanner);
       //核心方法，容器初始化
      refreshContext(context);
      afterRefresh(context, applicationArguments);
      stopWatch.stop();
      if (this.logStartupInfo) {
         new StartupInfoLogger(this.mainApplicationClass).logStarted(getApplicationLog(), stopWatch);
      }
      listeners.started(context);
      callRunners(context, applicationArguments);
   }
   catch (Throwable ex) {
      handleRunFailure(context, ex, exceptionReporters, listeners);
      throw new IllegalStateException(ex);
   }

   try {
      listeners.running(context);
   }
   catch (Throwable ex) {
      handleRunFailure(context, ex, exceptionReporters, null);
      throw new IllegalStateException(ex);
   }
   return context;
}
```

创建web上下文的过程做了很多事情，后续补充：

```java
public AnnotationConfigServletWebServerApplicationContext() {
	//创建AnnotatedBeanDefinitionReader实例，用来处理含有注解的类。为了处理注解，也注册了所有注解相关的Post Processors
   this.reader = new AnnotatedBeanDefinitionReader(this);
    //创建ClassPathBeanDefinitionScanner实例，用来扫描指定路径下含有注解的类
   this.scanner = new ClassPathBeanDefinitionScanner(this);
}
```

准备Spring应用上下文

```java
private void prepareContext(ConfigurableApplicationContext context, ConfigurableEnvironment environment,
      SpringApplicationRunListeners listeners, ApplicationArguments applicationArguments, Banner printedBanner) {
   context.setEnvironment(environment);
   postProcessApplicationContext(context);
    //依次调用通过SpringFactoriesLoader从spring.factories文件中加载的ApplicationContextInitializer接口的实现的initialize方法，完成Spring应用上下文的初始化工作
    //也会加载sofaBoot的初始化类
   applyInitializers(context);
   listeners.contextPrepared(context);
   if (this.logStartupInfo) {
      logStartupInfo(context.getParent() == null);
      logStartupProfileInfo(context);
   }
   // Add boot specific singleton beans
   ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
   beanFactory.registerSingleton("springApplicationArguments", applicationArguments);
   if (printedBanner != null) {
      beanFactory.registerSingleton("springBootBanner", printedBanner);
   }
   if (beanFactory instanceof DefaultListableBeanFactory) {
      ((DefaultListableBeanFactory) beanFactory)
            .setAllowBeanDefinitionOverriding(this.allowBeanDefinitionOverriding);
   }
   // Load the sources
   Set<Object> sources = getAllSources();
   Assert.notEmpty(sources, "Sources must not be empty");
   load(context, sources.toArray(new Object[0]));
   listeners.contextLoaded(context);
}
```

## 日志

### 日志路径

不指定则输出到控制台

指定日志相对或绝对路径`logging.file` 

or`logging.path` 日志目录，文件名为spring.log

### 日志级别

```properties
logging.level.root=WARN
logging.level.org.springframework.web=DEBUG
logging.level.org.hibernate=ERROR

# group
logging.group.tomcat=org.apache.catalina, org.apache.coyote, org.apache.tomcat
logging.level.tomcat=TRACE
```

### 日志配置

因为日志初始化是在`ApplicationContext` 初始化之前，因此无法通过 `@PropertySources`指定日志配置文件。可以使用logging.properties，logback.xml等配置文件。

其他设置：

```properties
# 默认10MB
logging.file.max-size
# 默认无限期
logging.file.max-history
```



## 调试

打印日志 

```properties
# 多打印一些信息，和debug日志级别无关
debug=true
# enables trace logging
trace=true
```



spring-boot-devtools

默认禁用Spring缓存，方便看到更改。

`spring.http.log-request-details`配置可以记录web请求详情。

## 初始化上下文

ApplicationContextInitializer 接口用于在spring容器refresh之前初始化Spring ConfigurableApplicationContext时的回调。

通常用于需要对应用程序上下文进行编程初始化的web应用程序中。例如，根据上下文环境注册属性源或激活配置文件等。

调用的时机看源码：

```java
private void prepareContext(ConfigurableApplicationContext context,
                            ConfigurableEnvironment environment, SpringApplicationRunListeners listeners,
                            ApplicationArguments applicationArguments, Banner printedBanner) {
    context.setEnvironment(environment);
    postProcessApplicationContext(context);
    applyInitializers(context);
    ...
}
```

用法和SpringApplicationRunListener类似，需要在META-INF/spring.factories文件中注册进去

## 事件

分为框架事件、Bean事件。



Springboot支持三种监听器，ApplicationListener、SpringApplicationRunListeners、SpringApplicationRunListener的关系：

- SpringApplicationRunListeners类和SpringApplicationRunListener类是SpringBoot中新增的类。ApplicationListener是spring中框架的类。
- 在SpringBoot（SpringApplication类）中，使用SpringApplicationRunListeners、SpringApplicationRunListener来间接调用ApplicationListener。
- SpringApplicationRunListeners中包含多个SpringApplicationRunListener，是为了批量执行的封装，它俩生命周期相同，调用每个周期的各个SpringApplicationRunListener。然后广播相应的事件到Spring框架的ApplicationListener。

Spring-boot:2.1.0支持6种事件监听，按顺序分别是：

1. ApplicationStartingEvent：在Spring最开始启动的时候触发
2. ApplicationEnvironmentPreparedEvent：在Spring已经准备好上下文但是上下文尚未创建的时候触发
3. ApplicationPreparedEvent：在Bean定义加载之后、刷新上下文之前触发
4. ApplicationStartedEvent：在刷新上下文之后、调用application命令之前触发
5. ApplicationReadyEvent：在调用applicaiton命令之后触发
6. ApplicationFailedEvent：在启动Spring发生异常时触发
7. ApplicationContextInitializedEvent

使用ApplicationListener监听事件的步骤：

1. 定义一个自己使用的监听器类并实现ApplicationListener接口
2. 通过SpringApplication类中的addListeners方法将自定义的监听器注册进去。也可以通过配置启动监听
3. 需要注意的是，直接用@Component注册监听器的方法只能监听刷新和启动完成（个人理解只有bean都初始化完成后其他事件才能保证监听的到）
4. 拓展，还可以使用通过继承ApplicationEvent添加自定义的事件，供程序监听

```java
@Componen
public class MessageReceiver implements ApplicationListener<ApplicationReadyEvent> {
    private Logger logger = LoggerFactory.getLogger(MessageReceiver.class);
    
    private UserService userService = null;
    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        ConfigurableApplicationContext applicationContext = event.getApplicationContext();
　　　　　//解决userService一直为空
　　　　 userService = applicationContext.getBean(UserService.class); 
　　　　 System.out.println("name"+userService.getName());
    }
}        

public class Application {
    public static void main(String[] args) {
        SpringApplication application = new SpringApplication(Application.class);
        application.addListeners(new MessageReceiver());
        application.run(args);
    
    }
}
```



直接使用SpringApplicationRunListener的场景较少，也能监听事件

```java
public class InitEnvironmentListener implements SpringApplicationRunListener {

    Logger logger = LoggerFactory.getLogger(InitEnvironmentListener.class);
    public InitEnvironmentListener() {
    }

    public InitEnvironmentListener(SpringApplication application, String[]  args){
    }

    @Override
    public void starting() {
    }
    //override all methods
}
```

还要满足SpringFactoriesLoader的约定，在当前SpringBoot项目的classpath下新建META-INF目录，并在该目录下新建spring.fatories文件，文件内容如下:

```properties
#  Listener
org.springframework.boot.SpringApplicationRunListener=\
com.sinosun.thrift.common.InitEnvironmentListener
```





## DB

在 `application.properties`中配置数据源:

```properties
spring.datasource.url=jdbc:mysql://localhost/test
spring.datasource.username=dbuser
spring.datasource.password=dbpass
spring.datasource.driver-class-name=com.mysql.jdbc.Driver

# 配置特定连接池
spring.datasource.hikari.*
spring.datasource.tomcat.*
# For expample:
# Number of ms to wait before throwing an exception if no connection is available.
spring.datasource.tomcat.max-wait=10000

# Maximum number of active connections that can be allocated from this pool at the same time.
spring.datasource.tomcat.max-active=50

# Validate the connection before borrowing it from the pool.
spring.datasource.tomcat.test-on-borrow=true
# 初始化数据库。每次启动都会执行
spring.datasource.initialization-mode=always
spring.datasource.schema=classpath:DDL.sql
```

## Test

`spring-boot-starter-test`会导入`spring-boot-test`、`junit`和其他相关库。

`@SpringBootTest` 创建`ApplicationContext`

- 使用`Junit4`还要加上`@RunWith(SpringRunner.class)`。
- the `webEnvironment`
  attribute of `@SpringBootTest`可以定义server的端口。
- `@*Test`会自动使用`@SpringBootApplication`定义的主配置。

`spring mvc`如果配置了，会生成基于`mvc`的`ApplicationContext`

示例

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes = MyApplication.class)
public class TestJPA {
 
    @Autowired CategoryDAO dao;
 
    @Test
    public void test() {
        List<Category> cs=  dao.findAll();
        for (Category c : cs) {
            System.out.println("c.getName():"+ c.getName());
        }
         
    }
}
```

### Web测试

测试Controller服务

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes = App.class)
@AutoConfigureMockMvc
public class AppTest {

    @Autowired
    private MockMvc mvc;

    @Test
    public void helloGradle() throws Exception {
        mvc.perform(get("/"))
            .andExpect(status().isOk())
            .andExpect(content().string("Hello Gradle!"));
    }

}
```

bootJar bootRun都是spring-boot插件引入的task。

Spring boot默认启动8080端口

```
./gradlew bootRun
```

### Mock

 `@MockBean`



## 热部署

启用spring-boot-devtools：

```groovy
configurations {
    developmentOnly
    runtimeClasspath {
        extendsFrom developmentOnly
    }
}
dependencies {
      developmentOnly("org.springframework.boot:spring-boot-devtools")
}
```

application配置

```
spring.devtools.restart.exclude=static/**,public/**
```

Compiler , 勾选上 Build project automatically。设置autoMake allow when app running

更细微控制

~/.config/spring-boot/spring-boot-devtools.properties

```properties
spring.devtools.restart.trigger-file=.reloadtrigger
```

支持远程调试

### 测试Web服务器端点

使用[`MockMvc`](https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference//testing.html#spring-mvc-test-framework)或[`WebTestClient`](https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference/testing.html#webtestclient-tests)

```java
@RunWith(SpringRunner.class)
@SpringBootTest
@AutoConfigureMockMvc
public class MockMvcExampleTests {

	@Autowired
	private MockMvc mvc;

	@Test
	public void exampleTest() throws Exception {
		this.mvc.perform(get("/")).andExpect(status().isOk())
				.andExpect(content().string("Hello World"));
	}

}
```

## Profile

## Profile使用

假如有开发、测试、生产三个不同的环境，需要定义三个不同环境下的配置。

### 基于properties文件类型

多个环境下的配置文件：

applcation.properties
 application-dev.properties
 application-test.properties
 application-prod.properties

在applcation.properties文件中指定当前的环境： spring.profiles.active=test
 这时候读取的就是application-test.properties文件。

### 基于yml文件类型

只需要一个applcation.yml文件就能搞定，推荐此方式。

```yml
spring:
  profiles: 
    active: prod

---
spring: 
  profiles: dev  
  
server: 
  port: 8080  
  
---
spring: 
  profiles: test  
  
server: 
  port: 8081    
  
---
spring.profiles: prod
spring.profiles.include:
  - proddb
  - prodmq
  
server: 
  port: 8082      
  
---
spring: 
  profiles: proddb  
  
db:
  name: mysql   
  
---
spring: 
  profiles: prodmq   

mq: 
  address: localhost
```

同时激活多个配置

```yml
spring.profiles.active: prod,proddb,prodmq
```

### 基于Java代码

在JAVA配置代码中也可以加不同Profile

@Profile注解只能和@Configuration或@Component一起使用。

```
@Configuration
@Profile("prod")
public class ProductionConfiguration {

    // ...

}
```



# AOP

**Spring AOP就是基于动态代理的**，如果要代理的对象，实现了某个接口，那么Spring AOP会使用**JDK Proxy**，去创建代理对象，而对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候Spring AOP会使用**Cglib** ，这时候Spring AOP会使用 **Cglib** 生成一个被代理对象的子类来作为代理

Spring AOP和AspectJ对比：

- Spring AOP使用了AspectJ的注解
- Spring AOP属于运行时增强，而 AspectJ 是编译时增强。

- Spring AOP 基于代理(Proxying)，而 AspectJ 基于字节码操作(Bytecode Manipulation)。
- Spring AOP 相对来说更简单。当切面太多的话，最好选择 AspectJ ，它比Spring AOP 快很多

### 依赖

配置

```properties
# AOP
spring.aop.auto=true # Add @EnableAspectJAutoProxy.
spring.aop.proxy-target-class=true # Whether subclass-based (CGLIB) proxies are to be created (true), as opposed to standard Java interface-based proxies (false).
```

springboot提供的jar

```gradle
spring-boot-starter-aop
```

### 概述





切面：spring用@Aspect注解的类。切面=切点+Advice

切点（Pointcut）: 表述哪些joinPoint织入

连接点Join Point：需要织入的执行点

Advice：横切关注点逻辑的载体。如果Aspect相当于OOP，那么Advice相当于Method

编织：运行时把切面和advised object连接起来的过程



切面的种类：

- 执行前。BeforeAdvice，资源初始化和其他准备性的工作
- 返回后。AfterReturningAdvice，正常返回后才能执行所以不适合做资源清理工作，也不能修改返回值。
- 抛异常后。ThrowsAdvice，通常用于对系统特定的异常情况监控，统一处理，比如email通知运维。
- finally后。AfterAdvice,资源清理工作。
- 围绕。AroundAdvice，全能。比如用来拦截getPrice打折。

建议尽量使用功能较小的种类，避免出问题。



Introduction类型，也就是给每个目标对象一个单独Advice，加入属性和行为。

IntroductionInterceptor



实现：

默认情况下，如果Spring AOP如果发现目标对象实现了相应Interface，则使用动态代理机制为其生成代理对象实例。

如果目标对象没有实现任何Interface，则使用CGLIB开源的动态字节码生成类库，通过继承为对象生成代理对象实例。因此不支持对final类和方法的复写。



示例

```java
/**
 * Aspect 切面
 * 日志切面
 */
@Aspect
@Component
public class LogAspect {

    /**
     * slf4j日志
     */
    private final static Logger logger = LoggerFactory.getLogger(LogAspect.class);

    /**
     * Pointcut 切入点
     * 匹配cn.controller包下面的所有方法
     */
    @Pointcut("execution(public * cn.controller.*.*(..))")
    public void webLog(){}

    /**
     * 环绕通知
     */
    @Around("webLog()")
    public Object arround(ProceedingJoinPoint pjp) {
        try {
            logger.info("1、Around：方法环绕开始.....");
            Object o =  pjp.proceed();
            logger.info("3、Around：方法环绕结束，结果是 :" + o);
            return o;
        } catch (Throwable e) {
            logger.error(pjp.getSignature() + " 出现异常： ", e);
            return Result.of(null, false, "出现异常：" + e.getMessage());
        }
    }

    /**
     * 方法执行前
     */
    @Before(value = "webLog()")
    public void before(JoinPoint joinPoint){
        logger.info("2、Before：方法执行开始...");
        // 接收到请求，记录请求内容
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        assert attributes != null;
        HttpServletRequest request = attributes.getRequest();
        // 记录下请求内容
        logger.info("URL : " + request.getRequestURL().toString());
        logger.info("HTTP_METHOD : " + request.getMethod());
        logger.info("IP : " + request.getRemoteAddr());
        logger.info("CLASS_METHOD : " + joinPoint.getSignature().getDeclaringTypeName() + "." + joinPoint.getSignature().getName());
        logger.info("ARGS : " + Arrays.toString(joinPoint.getArgs()));

    }

    /**
     * 方法执行结束，不管是抛出异常或者正常退出都会执行
     */
    @After(value = "webLog()")
    public void after(JoinPoint joinPoint){
        logger.info("4、After：方法最后执行.....");
    }

    /**
     * 方法执行结束，增强处理
     */
    @AfterReturning(returning = "ret", pointcut = "webLog()")
    public void doAfterReturning(Object ret){
        // 处理完请求，返回内容
        logger.info("5、AfterReturning：方法的返回值 : " + ret);
    }

    /**
     * 后置异常通知
     */
    @AfterThrowing(value = "webLog()")
    public void throwss(JoinPoint joinPoint){
        logger.error("AfterThrowing：方法异常时执行.....");
    }
}
```



### 切点

StaticMethodMatcherPointcut继承了StaticMethodMatcher。正则匹配

DynamicMethodMatcherPointcut继承了DynamicMethodMatcher



Spring2.0后提供了支持AspectJ语法的切点，AspectJExpressionPointcut。会委托AspectJ类库解析Pointcut表达式，进行匹配。

最常用的切点定义：

- execution(* com.zdy..*(..))：com.zdy包下所有类的所有方法.
- execution(* com.zdy.Dog.*(..)): Dog类下的所有方法.

使用方法:

- Advice上直接定义表达式。如@Around("execution(...)")
- 单独定义切点，被其他Advice引用



单独定义切点，切点只是定义切入的位置，myPointcut方法体内部实际不执行

```java
@Pointcut("execution(public * cn.controller.*.*(..))")
public void myPointcut(){}
@After(value="myPointcut()")
```

注解方式定义的pointcut，可以互相引用，避免重复定义

```java
@Pointcut("execution(public void com.sinosun.dsth(String))")
public void method1Pointcut()
    
@Pointcut("method1Pointcut()")
```

因此可以声明在同一个Aspect，来定义一系列公共的pointcut。



### 切点语法

- execution。*匹配相邻的多个字符，也就是一个word。..。用在匹配类型上，表示多个层次。
- within
- this/target
- args(paramName)。可以绑定参数
- @annotation。检查系统内所有对象的所有方法级别Joinpoint，如果被检测的方法有指定的注解，则当前方法的joinpoint被匹配到。
- @within @target @args

```java
cn.df.*.dosth //cn.df包下这层类的dosth方法
cn.df..*.dosth  //cn.df包下、所有子包里的dosth方法

```

@AroundAdvice第一个参数必须是ProceedJoinPoint类型，用来调用proceed()方法，继续调用链的执行。后续可能还有其他Advice执行。



除了@AroundAdvice，其他Advice都可以可选的声明JoinPoint参数，来获取信息，或者args获取具体参数。

@Before可以引用pointcut方法，也可以直接定义pointcut表达式

```java
public void log(JoinPoint joinpoint)
    
@Before("execution() && args(paramName)")
public void log(String paramName)
    
@AfterThrowing(pointcut=‘xxx“，throwing=“e”)
public void afterThrowing(Jp, RuntimeException e)
```

引用带参数的pointcut

```java
    
@Pointcut("execution(public * cn.controller.*.*(..)) && args(paramName)")
public void pointcut(String paramName)
@Before("pointcut(paramName)")
public void log(String paramName)
```



同一个joinpoint执行多个Advice的顺序：

- beforeAdvice最优先
- 同一个Aspect中多个同类型advice，按声明顺序
- 不同Aspect中，需要定义Order

### 用途

- 异常处理
- 安全检查。也可以用Spring Security、Shiro
- 缓存。可以用Spring Modules、Spring Caching。

```java
if(cache.containsKeys(key)){
    return cache.get(key);
} else {
    Object retVal = jp.proceed();
    cache.put(key, retVal);
    return retVal;
}
```

### 扩展

缺憾：Spring AOP只要调用代理对象的方法，都可以保证目标对象的方法被拦截。但不能保证调用目标对象方法也被拦截。如

```java
proxy.method1{
    //beforeAdvice
    target.method1(){
        //do sth
        target.method2()
    }
}

proxy.method1{
    target.method2()
}
```

执行proxy.method1的过程中，target.method2是无法 被拦截的。

解决办法：让target调用代理对象，这个proxy可以注入

```java
    target.method1(){
        //do sth
        proxy.method2()
    }
```



### 自定义注解

```java
public @interface NeedCheckLogin {
}

@Aspect
@Component
public class LoginAspect
{
    //@Around是在函数运行的之前和之后,value是切点
    //在所有的自定义注解NeedManagetPower方法上切入
    @Around("@annotation(NeedCheckLogin)))")
	public String checklogin(ProceedingJoinPoint joinPoint) throws Throwable {
        HttpSession session= ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest().getSession();
        if (session.getAttribute("username")!=null){
            if(session.getAttribute("power").equals(KeyWord.MANAGER_ROOT)) {
                //通过登录和权限检测
                //正常运行
                return (String)joinPoint.proceed();
            }else{
                return "{\"errno\":\"-2\",\"errmsg\":\"管理员权限不足\"}";
            }
        }else{
            return "{\"errno\":\"-1\",\"errmsg\":\"管理员未登录\"}";
        }
    }
}
```

### Advisor

切面、Aspect也叫Advisor。定义了Pointcut、advice。

比如，如果有统一异常处理的Advisor，需要声明顺序放在最前面，才能拦截到其他Advisor执行时抛出的异常。

### ProxyFactory

织入器



AopProxyFactory用来create AopProxy。Spring仅提供默认实现

```java
public class DefaultAopProxyFactory implements AopProxyFactory, Serializable {

	@Override
	public AopProxy createAopProxy(AdvisedSupport config) throws AopConfigException {
		if (config.isOptimize() || config.isProxyTargetClass() || hasNoUserSuppliedProxyInterfaces(config)) {
			Class<?> targetClass = config.getTargetClass();
			if (targetClass == null) {
				throw new AopConfigException("TargetSource cannot determine target class: " +
						"Either an interface or a target is required for proxy creation.");
			}
			if (targetClass.isInterface() || Proxy.isProxyClass(targetClass)) {
				return new JdkDynamicAopProxy(config);
			}
			return new ObjenesisCglibAopProxy(config);
		}
		else {
			return new JdkDynamicAopProxy(config);
		}
	}
    
public class AdvisedSupport extends ProxyConfig implements Advised {
```

ProxyConfig提供了生成代理对象的控制信息，如是否使用cglib代理（基于类的代理）。

Advised提供提供了生成代理对象的必要信息，如目标类、Advice、Advisor等。

proxyTargetClass设为true，表示基于类的代理。



ProxyFactoryBean继承了AdvisedSupport，也有了DefaultAopProxyFactory的功能。

```java
public class ProxyFactoryBean extends ProxyCreatorSupport
		implements FactoryBean<Object>, BeanClassLoaderAware, BeanFactoryAware {
 }
 
public class ProxyCreatorSupport extends AdvisedSupport {

	private AopProxyFactory aopProxyFactory;
	public ProxyCreatorSupport() {
		this.aopProxyFactory = new DefaultAopProxyFactory();
	}
    
```

xml定义一个ProxyFactoryBean实例，用来产生某种代理对象

```xml
<bean id="taskProxy" class="...ProxyFactoryBean"></bean>
```

### 自动代理

DefaultAdvisorAutoProxyCreator自动搜寻容器内所有Advisor，然后根据各个Advisor提供的拦截信息，为符合条件的容器对象生成相应的代理对象。

### TargetSource

proxy(代理对象)实际代理的不是target,而是targetSource对象。

让proxy代理TargetSource,可以使得每次方法调用的target实例都不同

```java
SingletonTargetSource 默认
PrototypeTargetSource 每次调用target时，target都是新的
HotSwappableTargetSource 热交换功能，可以动态替换target，比如异常时替换数据源
CommonsPool2TargetSource 类似PrototypeTargetSource，池化了
```

### xml方式

配置aop，如果把advice织入到pointcut

```xml
<aop:config></aop:config>
```





# @Schedule

```java
@Configuration //1.主要用于标记配置类，兼备Component的效果。
@EnableScheduling // 2.开启定时任务
@PropertySource("classpath:/bas.properties")
public class TimerTask_bas{
      /** 注入行动Dao类 **/
    @Autowired
    private BasSyndataBusiness basSyndataBusiness;
    
    @Bean
    public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        return new PropertySourcesPlaceholderConfigurer();
    }

    @Scheduled(cron = "${job.schedule}")
    public void sendDataToLibraryPoint() {
        basSyndataBusiness.sendDataToLibraryPoint();
    }

}

```

yaml文件读取

```groovy
compile 'com.github.sanjusoftware:yamlbeans:1.11'
```

### 

## 条件装配

@Conditional可以用在@Bean @Component等组件上

```java
@Configuration
public class MagicConfig {
//只有环境变量magic存在，matches才会返回true，条件才满足，MagicBean才会实例化
  @Bean
  @Conditional(MagicExistsCondition.class)
  public MagicBean magicBean() {
    return new MagicBean();
  }
  
}

@Component
@Conditional(HelloCondition.class)
public class HelloService {
    public void sayHi() {
        LoggerFactory.getLogger(HelloService.class).info("Hello World!");
    }
}

public class UseAliyunCondition implements Condition {

  @Override
  public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
    Environment env = context.getEnvironment();
    return env.containsProperty("magic");
  }
  
}
```

Condition实现类会在Bean加载之前加载，因此它如果依赖其他配置或类加载，必须显式加载。

比如依赖于zk配置加载，可以定义抽象类加载zk配置，让子类继承。

```java
public abstract class ZookeeperCondition implements Condition {
  static {
      ConfigManager.loadZookeeperConfig("message");
  }
}

public class UseAliyunCondition extends ZookeeperCondition {
  ...
}
```

Spring一个对象可以注入到两个不同的接口上。



我们可以在bean A上使用`@DependsOn`注解，告诉容器bean B应该先被初始化

# Spring MVC

SpringMVC几个组件：DispatcherServlet，HandleMapping，Handler，ViewResolver

 



## 概述

![](.\SpringMVC请求处理过程.png)

spring mvc项目：

- web.xml是整个web应用程序（基于Servlet）的部署描述符文件
- ContextLoaderListener加载WebApplicationContext
- DispatcherServlet负责配置Web层组件



DispatcherServlet是控制器，和其他组件交互：

1. MultipartResolver判断
2. HandlerMapping返回给DispatcherServlet一个handler（Object），如Controller
3. DispatcherServlet遍历查找一个可处理当前handler的HandlerAdapter，HandlerAdapter调用handle方法处理
4. Controller处理完毕后返回ModelAndView
5. 委托ViewResolver，根据ModelAndView返回的逻辑视图名称找到具体的view实现
6. 委托view根据模型数据输出视图内容

HandlerMapping负责映射web请求到具体处理的类

ViewResolver映射逻辑视图名和具体的View实例

View接口负责根据模型数据生成视图



> 在 Servlet API 中有一个 ServletContextListener 接口，它能够监听 ServletContext 对象的生命周期，实际上就是监听 Web 应用的生命周期。当Servlet 容器启动或终止Web 应用时，会触发ServletContextEvent 事件，该事件由ServletContextListener 来处理。

Spring提供了 ContextLoaderListener：

- 加载WebApplicationContext，绑定到ServletContext上
- WebApplicationContext中，可以使用自定义scope来注册bean，如request、session。自定义Listener用其他ApplicationContext如ClassPathXmlApplicationContext也可以，但会没有web上下文的一些特性。
- 可指定多个xml配置。默认为/WEB-INF/applicationContext.xml
- 通过WebApplicationContextUtils可获得WebApplicationContext
- Spring和其他Web框架集成的方式，也在此基础上

DispatcherServlet负责配置Web层组件：

- 启动后会加载xxcontroller-servlet.xml（对应web.xml中注册的servlet名称），
- 构建WebApplicationContext（以ContextLoaderListener加载的WebApplicationContext作为父容器）。
- 也可指定多个配置。

Spring支持多种Handler，包括controller

## Controller

> DefaultAnnotationHandlerMapping默认启用，可以获取所有注解的Controller，匹配url。

Spring boot中RequestMappingHandlerMapping和RequestMappingHandlerAdapter配合使用，用来路由请求到Controller的方法

还需要支持注解的HandlerAdaptor，负责：

1. 用来调用handler，它能匹配到一个方法来处理web请求。判断method
2. 把request参数绑定到对象。支持参数注解
3. 支持handler方法返回模型数据

@RequestMapping注解了的方法支持多种类型参数

```java
HttpServletRequest
WebRequest
ModelMap
Map
java.uti.Locale
java.io.InputStream/Reader
java.io.OutputStream/Writer
```

方法支持的返回类型

```java
ModelAndView
String
ModelMap
void
```

默认根据参数名自动绑定参数，也可以用@RequestParam明确指定绑定关系

Controller中，@ModelAttribute标注在方法上，会把返回的数据加入模型数据

@ModelAttribute标注在方法参数上，可以获取模型中的该属性引用。

@SessionAttribute可以将模型对象中的属性加入session管理，一般和@ModelAttribute配置使用。如@SessionAttribute(“loginInfo”)

@RequestParam用来处理 Content-Type 为 application/x-www-form-urlencoded 编码的body内容，绑定参数

@RequestBody接收非 `Content-Type: application/x-www-form-urlencoded`编码格式的数据，比如：`application/json`、`application/xml`等类型的数据。

`@Controller` +`@ResponseBody`= `@RestController`（Spring 4 之后新加的注解）

`@ResponseBody` 注解的作用是将 `Controller` 的方法返回的对象通过适当的转换器转换为指定的格式之后，写入到HTTP 响应(Response)对象的 body 中，通常用来返回 JSON 或者 XML 数据，返回 JSON 数据的情况比较多。

```java
@RestController
public class HelloController {
    @PostMapping("/hello")
    public Person greeting(@RequestBody Person person) {
        return person;
    }

}
```

## MultipartResolver

- Web请求到达DispatcherServlet
- DispatcherServlet在webApplicationContext中查找MultipartResolver
- MultipartResolver的isMultipart方法判断web请求是否为multipart类型
- 如果是则返回一个MultipartHttpServletRequest供后续流程使用

Spring提供了MultipartResolver接口的实现类，如CommonsMultipartResolver

## HandlerMapping

选用HandlerMapping时，如果当前HandlerMapping可以返回合适的Handler(比如Controller），则不再继续询问其他HandlerMapping。

DispatcherServlet调用HandlerMapping的handler方法，返回的HandlerExecutionChain包括了handler和多个HandlerInterceptor

HandlerMapping上可以set多个HandlerInterceptor

优先级：

可以为DispatcherServlet指定多个HandlerMapping。可以指定优先级

SimpleUrlHandlerMapping比BeanNameUrlHandlerMapping优先级高



## HandlerAdapter

DispatcherServlet使用HandlerAdapter来使用handler



自定义的Handler：

1. 能被现有的HandlerMapping找到
2. Spring内置了几种HandlerAdapter，已支持的handler不用提供HandlerAdapter
3. 在内置HandlerAdapter基础上，不满足则额外添加自定义HandlerAdapter，

## HandlerInterceptor

提供3个方法在不同时间点拦截：

- HandlerAdapter调用具体handler处理web请求之前
- HandlerAdapter调用具体handler处理web请求之后
- 框架内整个流程结束，视图渲染完后。无论是否发生异常都拦截

一般继承HandlerInterceptorAdapter实现，注意handler可能实际上RequestMappingHandlerMapping返回的HandlerMethod类型的handler。HandlerMethod提供获取方法上注解的api，可以加权限控制的注解



## Controller

MultiActionController：

- 支持一个Controller里定义多个web请求的方法
- 支持数据绑定和校验
- 需要MethodNameReslover映射web请求到方法。默认提供InternalPathMethodNameReslover
- 提供了delegate属性。可以让自己的controller不继承MultiActionController，直接实例化MultiActionController的bean并配置delegate。MultiActionController会使用反射调用MethodNameReslover返回的方法
- InternalPathMethodNameReslover取出最后一个/后并去除扩展名。可以增加前缀后缀



Controller层功能尽可能少，因为它要继承某种Controller，不方便复用。

redirect:viewName



### SimpleFormController

数据绑定流程在ServletRequestDataBinder中，转换数据到BeanWrapper的工作由PropertyEditor完成。

SimpleFormController可以复写判断是提交的方法，默认根据post判断。

显示表单过程：

1. 创建绑定目标对象（表单参数对象）。可复写，从数据库里读取。
2. 初始化数据绑定类ServletRequestDataBinder
3. 数据绑定
4. 处理表单显示

处理表单提交过程：

1. 从session中获取绑定目标对象。
2. 初始化数据绑定类ServletRequestDataBinder
3. 数据绑定
4. 数据验证
5. 处理表单显示

AbstractWizardFromController可以处理一系列向导表单。

UrlFilenameViewController可以配置静态资源目录，返回视图。

Servlet**Controller可以集成现存Servlet





## View

View负责视图渲染工作，设置返回的Content-Type。实际上就是使用模型数据，输出视图到response中。

可以设置静态属性和RequestContext，View会把它们加入模型，一起公开给模板。

view一般都是通过ViewResolver来实例化的。但自定义场景下也可以直接在controller中构造自定义类型的view返回，比如view会动态的从数据库查询到文件url，读取文件输出到response。

视图输出过程：

```java
view = mv.getView();
view.render(mv.getModelInternal(), request, response)
    
或：
view = resolveViewName(mv.getViewName(), mv.getModelInternal(), request, response)
view.render(mv.getModelInternal(), request, response)
```

FreemakerView使用需要FreeMarkerViewResolver和FreemakerConfigurer支持。

## ViewResolver

ViewResolver大部分都继承自AbstractCachingViewResolver，默认开启view的缓存功能。

单视图的ViewResolver如FreeMarkerViewResolver，根据视图名称查找（模板）文件，构造view实例返回

多视图的ViewResolver都会解析特定配置文件，实例化多个view实例bean。

WebApplicationContext中可以定义多个ViewResolver，根据优先级排序使用，返回null继续，找到view实例则停止。Internal和UrlBased等子类不会返回null，因此优先级设为最低。

## HandlerExceptionReslover

SimpleMappingHandlerExceptionReslover可以配置一组目标Handler，以及异常和错误ModelAndView的映射

可以定义多个指定优先级

## web.xml

springboot之前，传统war包启动需要配置web.xml，加载spring定义beans的文件

```xml
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd" version="3.1">
    <display-name>tomcat-jdbc-notes</display-name>
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>

    <filter>
        <filter-name>EncodeFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <init-param>
            <param-name>forceEncoding</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>EncodeFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>

    <servlet>
        <servlet-name>SpringMVC</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:spring-servlet.xml</param-value>
        </init-param>
    </servlet>
    <servlet-mapping>
        <servlet-name>SpringMVC</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

## XML配置示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans>
    <context:annotation-config/>
 <!-- 扫描Controller,并将其生命周期纳入Spring管理 -->
    <context:component-scan base-package="com.how2java.controller">
          <context:include-filter type="annotation"
          expression="org.springframework.stereotype.Controller"/>
    </context:component-scan>
 
    注解驱动，以使得访问路径与方法的匹配可以通过注解配置
    <mvc:annotation-driven />
     
    静态页面使用容器默认，如html,css,js,images可以访问
    <mvc:default-servlet-handler />
 
    <!-- 视图定位到/WEB/INF/jsp 这个目录下 -->
    <bean
        class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="viewClass"
            value="org.springframework.web.servlet.view.JstlView" />
        <property name="prefix" value="/WEB-INF/jsp/" />
        <property name="suffix" value=".jsp" />
    </bean>
</beans>
```



## 注解配置

Spring 5.0 以后WebMvcConfigurerAdapter会取消掉
WebMvcConfigurerAdapter是实现WebMvcConfigurer接口

```java
@Configuration
public class WebMvcConfg implements WebMvcConfigurer {
	//TODO
}

@Configuration
public class WebMvcConfg extends WebMvcConfigurationSupport {
	//TODO
}
```

## 静态资源

静态资源放在`classpath`或`servletContext`下的`/static`目录。

默认处理静态页面请求的机制如下：

- 加入配置<mvc:default-servlet-handler />。
  我们可以用Web服务器的defaultServlet来处理静态文件，也可用Spring框架来处理静态文件。使用Spring来处理，可以在配置中加入以下代码：
  ​         ```<mvc:default-servlet-handler/> ```
  这样spring会用默认的Servlet来响应静态文件。
- 在webapp目录下创建index.html或index.jsp
- web.xml中将index.html或index.jsp加入welcomfilelist



属性文件配置:

```properties
#http客户端应该以什么样的路径来访问静态资源，默认是/**
spring.mvc.static-path-pattern=/resources/**
# 静态资源映射到的存放位置。可配置列表，依次查找文件
spring.resources.static-locations=classpath:/static,classpath:/public,classpath:/resources,classpath:/META-INF/resources
server.port=8888
server.context-path=/test
```

static-path-pattern与static-locations组合起来演绎了nginx的映射配置。也可以在配置类中配置

```java
@Configuration
@EnableWebMvc
public class WebConfig extends WebMvcConfigurerAdapter {

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/resources/**")
                .addResourceLocations("/public-resources/")
                .setCacheControl(CacheControl.maxAge(1, TimeUnit.HOURS).cachePublic());
    }

}

```



## 内容协商

Content Negotiation

https://docs.spring.io/spring/docs/current/spring-framework-reference/web.html#mvc-config-content-negotiation

可以配置spring mvc如何决定响应的媒体类型。需要配置`ContentNegotiatingViewResolver`、`contentNegotiationManager`（配置url后缀和响应类型的映射）、默认的视图解析（其他）`defalutViewResolver`、

`"GET /projects/spring-boot?format=json"` 被映射到 `@GetMapping("/projects/spring-boot")`。

配置示例如下：

```
spring.mvc.contentnegotiation.favor-parameter=true

# We can change the parameter name, which is "format" by default:
# spring.mvc.contentnegotiation.parameter-name=myparam

# We can also register additional file extensions/media types with:
spring.mvc.contentnegotiation.media-types.markdown=text/markdown
```

## 解析静态资源

```java
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }
}
```

```xml
<mvc:default-servlet-handler/>
```

## 异常处理

方式一：用@ExceptionHandler注解，处理 Controller 内部的异常。

注意两点：

1. 一个Controller下多个@ExceptionHandler上的异常类型不能出现一样的，否则运行时抛异常.
2. @ExceptionHandler下方法返回值类型支持多种，常见的ModelAndView，@ResponseBody注解标注，ResponseEntity等类型都OK.



方式二：使用 `@ControllerAdvice` 和 `@ExceptionHandler` 处理全局异常

```java
@ControllerAdvice
public class DefaultExceptionHandler {
    @ExceptionHandler({UnauthorizedException.class})
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    public ModelAndView processUnauthenticatedException(NativeWebRequest request, UnauthorizedException e) {
        ModelAndView mv = new ModelAndView();
        mv.addObject("ex", e);
        mv.setViewName("unauthorized");
        return mv;
    }

}

@ControllerAdvice(assignableTypes = {ExceptionController.class})
@ResponseBody
public class GlobalExceptionHandler {

    ErrorResponse illegalArgumentResponse = new ErrorResponse(new IllegalArgumentException("参数错误!"));
    ErrorResponse resourseNotFoundResponse = new ErrorResponse(new ResourceNotFoundException("Sorry, the resourse not found!"));
    
    @ExceptionHandler(value = Exception.class)// 拦截所有异常, 这里只是为了演示，一般情况下一个方法特定处理一种异常
    public ResponseEntity<ErrorResponse> exceptionHandler(Exception e) {

        if (e instanceof IllegalArgumentException) {
            return ResponseEntity.status(400).body(illegalArgumentResponse);
        } else if (e instanceof ResourceNotFoundException) {
            return ResponseEntity.status(404).body(resourseNotFoundResponse);
        }
        return null;
    }
}
```

 方式三：抛出ResponseStatusException可以简单返回错误响应

```java
    @GetMapping("/resourceNotFoundException2")
    public void throwException3() {
        throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Sorry, the resourse not found!", new ResourceNotFoundException());
    }
```

**异常处理实例**

```java
import org.springframework.http.HttpStatus;


public enum ErrorCode {
  
    RESOURCE_NOT_FOUND(1001, HttpStatus.NOT_FOUND, "未找到该资源"),
    REQUEST_VALIDATION_FAILED(1002, HttpStatus.BAD_REQUEST, "请求数据格式验证失败");
    private final int code;

    private final HttpStatus status;

    private final String message;

    ErrorCode(int code, HttpStatus status, String message) {
        this.code = code;
        this.status = status;
        this.message = message;
    }

    public int getCode() {
        return code;
    }

    public HttpStatus getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    @Override
    public String toString() {
        return "ErrorCode{" +
                "code=" + code +
                ", status=" + status +
                ", message='" + message + '\'' +
                '}';
    }
}
```

**ErrorReponse.java（返回给客户端具体的异常对象）**

```java
import org.springframework.util.ObjectUtils;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

public class ErrorReponse {
    private int code;
    private int status;
    private String message;
    private String path;
    private Instant timestamp;
    private HashMap<String, Object> data = new HashMap<String, Object>();

    public ErrorReponse() {
    }

    public ErrorReponse(BaseException ex, String path) {
        this(ex.getError().getCode(), ex.getError().getStatus().value(), ex.getError().getMessage(), path, ex.getData());
    }

    public ErrorReponse(int code, int status, String message, String path, Map<String, Object> data) {
        this.code = code;
        this.status = status;
        this.message = message;
        this.path = path;
        this.timestamp = Instant.now();
        if (!ObjectUtils.isEmpty(data)) {
            this.data.putAll(data);
        }
    }

// 省略 getter/setter 方法

    @Override
    public String toString() {
        return "ErrorReponse{" +
                "code=" + code +
                ", status=" + status +
                ", message='" + message + '\'' +
                ", path='" + path + '\'' +
                ", timestamp=" + timestamp +
                ", data=" + data +
                '}';
    }
}
```

**BaseException.java（继承自 RuntimeException 的抽象类，可以看做系统中其他异常类的父类）**

```java
public abstract class BaseException extends RuntimeException {
    private final ErrorCode error;
    private final HashMap<String, Object> data = new HashMap<>();

    public BaseException(ErrorCode error, Map<String, Object> data) {
        super(error.getMessage());
        this.error = error;
        if (!ObjectUtils.isEmpty(data)) {
            this.data.putAll(data);
        }
    }

    protected BaseException(ErrorCode error, Map<String, Object> data, Throwable cause) {
        super(error.getMessage(), cause);
        this.error = error;
        if (!ObjectUtils.isEmpty(data)) {
            this.data.putAll(data);
        }
    }

    public ErrorCode getError() {
        return error;
    }

    public Map<String, Object> getData() {
        return data;
    }

}
```

**GlobalExceptionHandler.java（全局异常捕获）**

遇到异常会优先选取最匹配的方法。`ExceptionHandlerMethodResolver.java`中`getMappedMethod`决定了具体被哪个方法处理。

```java
import com.twuc.webApp.web.ExceptionController;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import javax.servlet.http.HttpServletRequest;

@ControllerAdvice(assignableTypes = {ExceptionController.class})
@ResponseBody
public class GlobalExceptionHandler {
    
    // 也可以将 BaseException 换为 RuntimeException 
    // 因为 RuntimeException 是 BaseException 的父类
    @ExceptionHandler(BaseException.class)
    public ResponseEntity<?> handleAppException(BaseException ex, HttpServletRequest request) {
        ErrorReponse representation = new ErrorReponse(ex, request.getRequestURI());
        return new ResponseEntity<>(representation, new HttpHeaders(), ex.getError().getStatus());
    }

}
```

## 参数绑定

注解都是通过`HttpMessageConverter`转换参数的。

`HttpEntity<B>` For access to request headers and body. 

`@RequestHeader`  For access to request headers. Header values are converted to the declared method argument type. See [`@RequestHeader`](https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference/web.html#mvc-ann-requestheader).

示例详见文档：

  https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference/web.html#mvc-ann-methods

`@PathVariable` :取url地址中的参数。`@RequestParam ` url的查询参数值。

`@RequestBody`:可以**将 HttpRequest body 中的 JSON 类型数据反序列化为合适的 Java 类型。**

`ResponseEntity`: **表示整个HTTP Response：状态码，标头和正文内容**。我们可以使用它来自定义HTTP Response 的内容。

```java
    @GetMapping("/book")
    public ResponseEntity getBookByName(@RequestParam("name") String name) {
        List<Book> results = books.stream().filter(book -> book.getName().equals(name)).collect(Collectors.toList());
        return ResponseEntity.ok(results);
    }
```



**端点映射**

```java
@RestController
@RequestMapping("/persons") //@RequestMapping("/owners/{ownerId}")也可以用uri变量
class PersonController {

    @GetMapping("/{id}")
    public Person getPerson(@PathVariable Long id) {
        // ...
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public void add(@RequestBody Person person) {
        // ...
    }
    
    @GetMapping("/owners/{ownerId}/pets/{petId}")
public Pet findPet(@PathVariable Long ownerId, @PathVariable Long petId) {
    // ...
}
}
```

路径通配符

-  matches one character
- `*` matches zero or more characters within a path segment
- `**` match zero or more path segments

正则表达式定义uri变量：

```java
@GetMapping("/{name:[a-z-]+}-{version:\\d\\.\\d\\.\\d}{ext:\\.[a-z]+}")
public void handle(@PathVariable String version, @PathVariable String ext) {
    // ...
}
```



请求路径`/person.*`携带后缀，请求头就不需要`Accept` header

## 测试

MockMvc 由`org.springframework.boot.test`包提供，实现了对Http请求的模拟，一般用于我们测试  controller 层

```java
@AutoConfigureMockMvc
@SpringBootTest
public class ExceptionTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    void should_return_400_if_param_not_valid() throws Exception {
        mockMvc.perform(get("/api/illegalArgumentException"))
                .andExpect(status().is(400))
                .andExpect(jsonPath("$.message").value("参数错误!"));
    }

    @Test
    void should_return_404_if_resourse_not_found() throws Exception {
        mockMvc.perform(get("/api/resourceNotFoundException"))
                .andExpect(status().is(404))
                .andExpect(jsonPath("$.message").value("Sorry, the resourse not found!"));
    }
}
```

## 生成uri

```java
URI uri = UriComponentsBuilder
        .fromUriString("http://example.com/hotels/{hotel}")
        .queryParam("q", "{q}")
        .encode()
        .buildAndExpand("Westin", "123")
        .toUri();
        
URI uri = UriComponentsBuilder
        .fromUriString("http://example.com/hotels/{hotel}?q={q}")
        .build("Westin", "123");
```



## 异步请求

https://docs.spring.io/spring/docs/5.1.4.RELEASE/spring-framework-reference/web.html#mvc-ann-async-processing

## Servlet 3配置

基于java，代替了web.xml

```java
public class MyWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return null;
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { MyWebConfig.class };
    }

    @Override
    protected String[] getServletMappings() {
        return new String[] { "/" };
    }
    
        // ...

    @Override
    protected Filter[] getServletFilters() {
        return new Filter[] {
            new HiddenHttpMethodFilter(), new CharacterEncodingFilter() };
    }
}
```

## 处理请求的流程

- 搜索匹配的`WebApplicationContext`，绑定请求到controller。
- 给请求绑定多种配置的resolver。`HandlerExceptionResolver`用于在请求处理期间处理异常。
- 找到适合的handler处理，返回model或渲染后的view。

拦截器

`HandlerInterceptor` 

## Context分层

- 一般仅一个root`WebApplicationContext` 。

  ```xml
  <servlet>
          <servlet-name>app</servlet-name>
          <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
          <init-param>
              <param-name>contextConfigLocation</param-name>
              <param-value></param-value>
          </init-param>
          <load-on-startup>1</load-on-startup>
      </servlet>
  
  ```

- 多层次。`ServletContext`和servlet的`WebApplicationContext`绑定。公共services/repositories等基础设施都在root `WebApplicationContext` 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xmlns="http://java.sun.com/xml/ns/javaee" 
         xmlns:web="http://java.sun.com/xml/ns/javaee" 
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" version="2.5">
	
	<!-- spring的配置文件-->
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>
			classpath:applicationContext.xml,
			classpath:applicationContext-shiro.xml
		</param-value>
	</context-param>
	<listener>
		<listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
	</listener>
	
	
	<!-- spring mvc核心：分发servlet -->
	<servlet>
		<servlet-name>mvc-dispatcher</servlet-name>
		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
		<!-- spring mvc的配置文件 -->
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>classpath:springMVC.xml</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
	</servlet>
	<servlet-mapping>
		<servlet-name>mvc-dispatcher</servlet-name>
		<url-pattern>/</url-pattern>
	</servlet-mapping>
	
	<!-- Shiro配置 -->
	<filter>
		<filter-name>shiroFilter</filter-name>
		<filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
		<init-param>
			<param-name>targetFilterLifecycle</param-name>
			<param-value>true</param-value>
		</init-param>
	</filter>
	<filter-mapping>
		<filter-name>shiroFilter</filter-name>
		<url-pattern>/*</url-pattern>
	</filter-mapping>	
	
</web-app>
```

## Filter

在自己的过滤器的类上加上@WebFilter

```java
@WebFilter(filterName = "MyFilterWithAnnotation", urlPatterns = "/api/*")
public class MyFilterWithAnnotation implements Filter {

   ......
}
```

也可以通过FilterRegistrationBean 配置filter，setOrder 方法可以决定 Filter 的执行顺序。

```java
@Configuration
public class MyFilterConfig {
    @Autowired
    MyFilter myFilter;

    @Autowired
    MyFilter2 myFilter2;

    @Bean
    public FilterRegistrationBean<MyFilter> setUpMyFilter() {
        FilterRegistrationBean<MyFilter> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setOrder(2);
        filterRegistrationBean.setFilter(myFilter);
        filterRegistrationBean.setUrlPatterns(new ArrayList<>(Arrays.asList("/api/*")));

        return filterRegistrationBean;
    }

    @Bean
    public FilterRegistrationBean<MyFilter2> setUpMyFilter2() {
        FilterRegistrationBean<MyFilter2> filterRegistrationBean = new FilterRegistrationBean<>();
        filterRegistrationBean.setOrder(1);
        filterRegistrationBean.setFilter(myFilter2);
        filterRegistrationBean.setUrlPatterns(new ArrayList<>(Arrays.asList("/api/*")));
        return filterRegistrationBean;
    }
}
```

## 跨域

概念

https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

- 应用只能向它来源的域发起请求，除非其他域的响应包含正确的CORS头。
- 其他域的response会返回客户端，但是浏览器会把当前网页的源（也就是域）与Access-Control-Allow-Origin里的url进行比较，如果发现有一样的url，就判定允许跨域访问。
- 想让一个web接口允许任何源的跨域访问，可以在response加上`Access-Control-Allow-Origin：*`

**局部配置**

`@CrossOrigin`用在Controller或method上，指定允许跨域访问的origin

```java
@Configuration
public class WebConfig extends WebMvcConfigurerAdapter {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:9000", "null")         .allowedMethods("POST", "GET", "PUT", "OPTIONS", "DELETE")
.maxAge(3600)
.allowCredentials(true);
  }
}
```

## 拦截器

配置拦截器

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // LogInterceptor apply to all URLs.
        registry.addInterceptor(new LogInterceptor());

        // Old Login url, no longer use.
        // Use OldURLInterceptor to redirect to a new URL.
        registry.addInterceptor(new OldLoginInterceptor())//
                .addPathPatterns("/admin/oldLogin");

        // This interceptor apply to URL like /admin/*
        // Exclude /admin/oldLogin
        registry.addInterceptor(new AdminInterceptor())//
                .addPathPatterns("/admin/*")//
                .excludePathPatterns("/admin/oldLogin");
    }

}
```

## 校验参数

spring-boot-starter-web会引入hibernate-validator相关依赖

校验参数

```java
@RestController
@RequestMapping("/api")
@Validated
public class PersonController {

    @GetMapping("/person/{id}")
    public ResponseEntity<Integer> getPersonByID(@Valid @PathVariable("id") @Max(value = 5,message = "超过 id 的范围了") Integer id) {
        return ResponseEntity.ok().body(id);
    }

    @PutMapping("/person")
    public ResponseEntity<String> getPersonByName(@Valid @RequestParam("name") @Size(max = 6,message = "超过 name 的范围了") String name) {
        return ResponseEntity.ok().body(name);
    }
}
//校验Service方法的参数
@Service
@Validated
public class PersonService {

    public void validatePerson(@Valid Person person){
        // do something
    }
}
```

## Web容器

如何使用jetty

```java
compile("org.springframework.boot:spring-boot-starter-web") {
     exclude group: 'org.springframework.boot', module: 'spring-boot-starter-tomcat'
}
compile("org.springframework.boot:spring-boot-starter-jetty")
```

自动配置基础上定制tomcat容器

```java
@Configuration
@EnableWebMvc
@SpringBootConfiguration
public class WebServerConfiguration {

    @Bean
    public TomcatServletWebServerFactory embeddedServletContainerFactory() {
        TomcatConfig.checkConfig();
        //Springboot2.x
        TomcatServletWebServerFactory factory = new TomcatServletWebServerFactory() {
            @Override
            protected void postProcessContext(Context context) {
                ((StandardJarScanner) context.getJarScanner()).setScanManifest(false);
            }
        };
        //Springboot1.x
//        TomcatEmbeddedServletContainerFactory factory = new TomcatEmbeddedServletContainerFactory();
        //设置端口
        factory.setPort(TomcatConfig.getPort());

        ContextConfig contextConfig = new ContextConfig();
        //查找classpath下的web.xml
        ClassPathResource file = new ClassPathResource("/web.xml");
        if (file.exists()) {
            try {
                contextConfig.setDefaultWebXml(file.getFile().getAbsolutePath());
            } catch (IOException e) {
                BaseLog.getSystemLog().warn("Found web.xml exception",e);
                contextConfig.setDefaultWebXml("org/apache/catalin/startup/NO_DEFAULT_XML");
            }
        } else {
            BaseLog.getSystemLog().warn("Not found web.xml in /conf");
            contextConfig.setDefaultWebXml("org/apache/catalin/startup/NO_DEFAULT_XML");
        }
        factory.addContextLifecycleListeners(contextConfig);

        return factory;
    }
 
}
```



项目使用springboot启动一个web项目，在启动阶段看到console中出现了异常“1.10.3-1.4.3\hdf5.jar 系统找不到指定的文件”

## Cookie

**1)设置cookie返回给客户端**

```java
@GetMapping("/change-username")
public String setCookie(HttpServletResponse response) {
    // 创建一个 cookie
    Cookie cookie = new Cookie("username", "Jovan");
    //设置 cookie过期时间
    cookie.setMaxAge(7 * 24 * 60 * 60); // expires in 7 days
    //添加到 response 中
    response.addCookie(cookie);

    return "Username is changed!";
}
```

**2) 使用Spring框架提供的`@CookieValue`注解获取特定的 cookie的值**

```java
@GetMapping("/")
public String readCookie(@CookieValue(value = "username", defaultValue = "Atta") String username) {
    return "Hey! My username is " + username;
}
```

**3) 读取所有的 Cookie 值**

```java
@GetMapping("/all-cookies")
public String readAllCookies(HttpServletRequest request) {

    Cookie[] cookies = request.getCookies();
    if (cookies != null) {
        return Arrays.stream(cookies)
                .map(c -> c.getName() + "=" + c.getValue()).collect(Collectors.joining(", "));
    }

    return "No cookies";
}
```

# 问题

## 动态注入bean
## 获取EntityManager
@Autowired
EntityManager entityManager;



## 获取 sessionFactory
注入bean

```
package cn.xiaojf;



import cn.xiaojf.today.data.rdb.repository.RdbCommonRepositoryImpl;

import org.springframework.boot.SpringApplication;

import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.springframework.context.annotation.Bean;

import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

import org.springframework.orm.jpa.vendor.HibernateJpaSessionFactoryBean;



@SpringBootApplication

@EnableJpaRepositories(repositoryBaseClass = RdbCommonRepositoryImpl.class)

public class Application {

    public static void main(String[] args) {

        SpringApplication.run(Application.class, args);

    }



    @Bean

    public HibernateJpaSessionFactoryBean sessionFactory() {

        return new HibernateJpaSessionFactoryBean();

    }

}

```
复制代码

```
application.properties 中配置



spring.jpa.show-sql = true

spring.jpa.hibernate.ddl-auto=none

spring.jpa.database=mysql

spring.jpa.properties.hibernate.current_session_context_class=org.springframework.orm.hibernate4.SpringSessionContext

```
直接在代码中注入

```
@Autowired

private SessionFactory sessionFactory;

```
# Spring Common
` @Component("specialCustom") the bean name plus Impl` 



## Spring单例模式及线程安全

　　Spring框架中的Bean，或者说组件，获取实例的时候都是默认单例模式，这是在多线程开发的时候需要尤其注意的地方。

　　单例模式的意思是只有一个实例，例如在Spring容器中某一个类只有一个实例，而且自行实例化后并项整个系统提供这个实例，这个类称为单例类。

　　当多个用户同时请求一个服务时，容器会给每一个请求分配一个线程，这时多个线程会并发执行该请求对应的业务逻辑（成员方法），此时就要注意了，如果该处理逻辑中有对单例状态的修改（体现为该单例的成员属性），则必须考虑线程同步问题。

# Spring data JPA

## 依赖

mysql-connector-java

spring-boot-starter-data-jpa


## 配置
基于注解
```
@Configuration
 
@EnableJpaRepositories
 
@Import(InfrastructureConfig.class)
 
public class ApplicationConfig {
 
 
 
}
 
```
一个定制化类更改所有Repository的行为

```java
@Configuration
@EnableJpaRepositories(repositoryBaseClass = MyRepositoryImpl.class)
class ApplicationConfiguration { … }
// 一个定制化类更改所有Repository的行为
class MyRepositoryImpl<T, ID extends Serializable> 
  extends SimpleJpaRepository<T, ID> { 
  private final EntityManager entityManager; 
  MyRepositoryImpl(JpaEntityInformation entityInformation,
                          EntityManager entityManager) {
    super(entityInformation, entityManager);
    // Keep the EntityManager around to used from the newly introduced methods.
    this.entityManager = entityManager;
  }
 
 @Transactional
  public <S extends T> S save(S entity) {
    // implementation goes here
  } 
}
 
 
 
 
 
```
XML
```
// 扫描并排除一些类
<repositories base-package="com.acme.repositories" />
 
<repositories base-package="com.acme.repositories">
 
  <context:exclude-filter type="regex" expression=".*SomeRepository" />
 
</repositories>
```
`spring.jpa.hibernate.ddl-auto=create`属性的值有`create`、`update`等。**一定要不要在生产环境使用 ddl 自动生成表结构**

## 定义实体类

```java
public interface CategoryDAO extends JpaRepository<Category,Integer>{
}
```

继承JpaRepository，并且提供泛型<Category,Integer> 表示这个是针对Category类的DAO,Integer表示主键是Integer类型。
JpaRepository 这个父接口，就提供了CRUD, 分页等等一系列的查询了，直接拿来用，都不需要二次开发的了



@Entity和@Document可以用在同一张表（对象）上
```java
@Entity
@Document //mongodb
class Person {
} 


@DynamicInsert
动态插入，只插入非null值，这样就可以使用数据库默认值

@DynamicUpdate
只更新改变了的值
@Column(unique = true)的unique是用hibernate来给表生成唯一约束的

@Column(nullable = false) 检查参数是否为空，还有@NotNull NotNullApi

@ElementCollection 对象中的嵌套数据结构，比如Map、List

@NotFound(action=NotFoundAction.IGNORE) 内嵌关联的对象如果查询为空，忽略不报异常 
@OneToMany(cascade = CascadeType.ALL) 指定级联操作

```



## 定义接口

查询方法发现策略 Query lookup strategies
>CREATE_IF_NOT_FOUND (default) combines CREATE and USE_DECLARED_QUERY. It looks up a declared query first, and if no declared query is found, it creates a custom method name-based query

Query creation 通过名称定义查询

```java
public interface CategoryDAO extends JpaRepository<Category,Integer>{
 
    public List<Category> findByName(String name);
     
    public List<Category> findByNameLikeAndIdGreaterThanOrderByNameAsc(String name, int id);
} 

@Entity
@Table(name = "category_")
public class Category {
 
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private int id;
     
    @Column(name = "name")
    private String name;
}


// @Test
//根据名称模糊查询，id 大于5, 并且名称正排序查询 
List<Category> cs=  dao.findByNameLikeAndIdGreaterThanOrderByNameAsc("%3%",5);
```
## 懒加载

双向一对多记得一定加上`fetch = FetchType.LAZY `,避免使用`fetch = FetchType.EAGER)`，不然会陷入死循环
双向打印json的时候可能也需要一方忽略关联的对象。

# Spring-Mybatis

## 依赖

mybatis-spring-boot-starter

mysql-connector-java

## 注解方式

```java
@Mapper
public interface CategoryMapper {
    @Select("select * from category_ ")
    List<Category> findAll();
}
```



# Spring-Sqlite

http://how2j.cn/k/springboot/springboot-sqlite/2018.html#nowhere

# Spring test
## 加载Spring配置，包括bean配置
@SpringBootTest指定启动类
@RunWith加载上下文到junit测试类
```
@RunWith(SpringRunner.class)

@SpringBootTest(classes = StartUpApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)

public class HelloControllerTest {



```
## 定义配置
@SpringBootApplication指定启动入口类

```
@SpringBootApplication

public class StartUpApplication {

    public static void main(String[] args) {
      SpringApplication.run(StartUpApplication.class, args);
    }
}

```
## 测试Controller
测试类
```
@RunWith(SpringRunner.class)

@SpringBootTest(classes = StartUpApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)

public class HelloControllerTest {

    /**
     * @LocalServerPort 提供了 @Value("${local.server.port}") 的代替
     */
    @LocalServerPort
    private int port;
    private URL base;

	@Autowired
    private TestRestTemplate restTemplate;

    @Before
    public void setUp() throws Exception {
        String url = String.format("http://localhost:%d/", port);
        System.out.println(String.format("port is : [%d]", port));
        this.base = new URL(url);
    }



    /**
     * 向"/test"地址发送请求，并打印返回结果
     * @throws Exception
     */

    @Test
    public void test1() throws Exception {
        ResponseEntity<String> response = this.restTemplate.getForEntity(
                this.base.toString() + "/test", String.class, "");
        System.out.println(String.format("测试结果为：%s", response.getBody()));
    }
```
Controller类
```
@RunWith(SpringRunner.class)

@SpringBootTest(classes = StartUpApplication.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)

public class HelloControllerTest {
    /**
     * @LocalServerPort 提供了 @Value("${local.server.port}") 的代替
     */
    @LocalServerPort
    private int port;
    private URL base;

    @Autowired
    private TestRestTemplate restTemplate;
	
	@Before
    public void setUp() throws Exception {
        String url = String.format("http://localhost:%d/", port);
        System.out.println(String.format("port is : [%d]", port));
        this.base = new URL(url);
    }

    /**
     * 向"/test"地址发送请求，并打印返回结果
     * @throws Exception
     */
    @Test
    public void test1() throws Exception {
        ResponseEntity<String> response = this.restTemplate.getForEntity(
                this.base.toString() + "/test", String.class, "");
        System.out.println(String.format("测试结果为：%s", response.getBody()));

    }

```
依赖项
```
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.6.RELEASE</version>
    </parent>



    <dependencies>

        <dependency>

            <groupId>org.springframework.boot</groupId>

            <artifactId>spring-boot-starter-web</artifactId>

        </dependency>

        <dependency>

            <groupId>org.springframework.boot</groupId>

            <artifactId>spring-boot-starter-test</artifactId>

        </dependency>

    </dependencies>
```

# Spring orm

## 概述

Spring-orm关注3个方面：

- 数据访问资源管理。包括连接(会话）、连接工厂（Spring提供各种工厂来生成特定连接工厂)
- 数据访问异常的转译
- 事务管理

配置orm一般都需要声明DataSource、连接工厂（多使用Spring提供的FactoryBean）、xxTemplate

模板用于封装除特定业务逻辑以外的模板代码，execute(Callback).

模板方法+Callback接口

## DataSource

相当于连接的工厂，生产上的实现一般是连接缓冲池。

连接池产生connection，是最初Connnection对象的代理对象，实现了java.sql.Connection接口。close后不是真的被关闭，只是被返回给缓冲池。

如果要获得某数据库驱动提供的原始Connection实现类，以便使用特定功能，可以给jdbcTemplate设置`NativeJdbcExtractor` 。NativeJdbcExtractor实现类负责取得真正连接对象。

Spring默认提供了多种NativeJdbcExtractor，如C3P0NativeJdbcExtractor

AbstractDatasource用于实现DataSource

AbstractDatasourceRouting支持多数据源。



## jdbcTemplate

特点：主要解决了statement和conn释放、异常捕获的模板代码。

Spring统一将SQLException转译成了DataAccessException异常体系



DataFieldMaxValueIncrementer接口提供自增序列号，。

MysqlMaxValueIncrementer（以及Hsql的）可以设置cacheSize本地缓存大小。



LobHandler接口封装了各数据库存取Blob、Clob字段的差异性，oracle必须使用OracleLobHandler

## Hibernate

Hibernate特点：

- hibernate的SessionFactory相当于jdbc的DataSource，都需要根据配置初始化。
- getCurrentSession()获取当前线程绑定的session，一般在一个事务结束后关闭。

Spring提供了LocalSessionFactoryBean来配置获取SessionFactory。

为了统一事务管理，LocalSessionFactoryBean构建SessionFactory时，用容器内定义的DataSource而不是Hibernate的ConnectionProvider。实际上Spring会根据传入的DataSource来选择具体的ConnectionProvider。

LocalSessionFactoryBean配置：

- dataSource
- configLocation。一般包括了所有配置，包括映射、hibernate属性配置。
- mappingResources。映射list。
- hibernateProperties。props配置。

有了SessionFactory就可以通过注解注入HibernateDaoSupport，或者xml声明HibernateTemplate

```java
@Repository
public class SysUserDaoImpl extends HibernateDaoSupport implements SysUserDao {
    @Autowired
    public void setSessionFactor(SessionFactory sessionFactory) {
        super.setSessionFactory(sessionFactory);
    }
```

# 事务

## 概述

事务参与者：

- Resource Manager 存储和管理状态，如数据库服务器
- TP Monitor。协调事务处理的中间件，如J2EE的Application Server

- Transaction Manager(TM)  负责多个RM间事务处理的协调工作
- Application。事务边界的触发点

事务按RM多少分类：

- 分布式事务
- 局部事务。应用程序可以直接与RM打交道，使用RM的内置事务支持。

统一事务管理需要关注：

- 隔离数据访问与事务管理的耦合
- 转译事务api抛出异常，屏蔽差异性
- 统一事务编程模型，最好是声明式的。

## 统一事务管理API

Spring提供PlatformTransactionManager接口统一事务管理API。

思考如何实现jdbc的PlatformTransactionManager实现：

1. 事务管理委托给Connection
2. 不同数据访问操作，使用同一个Connection
3. Connection的传递通过ThreadLocal实现。Connection的绑定到线程、解绑、获取操作可以封装到TransactionResourceManager里。

Spring为jdbc提供DataSourceUtils负责获取Connection，提供事务支持。

Spring的事务管理与它提供的数据访问框架紧密结合，比如JdbcTemplate内部就使用



事务的传播行为：

- Required。加入当前事务，不存在则新创建一个事务。默认
- SUPPORTS。加入当前事务，不存在则直接执行。适合查询方法
- Required_NEW。始终会创建新的事务，失败不影响外层事务。
- NESTED。嵌套事务，相当于大事务分成多个小事务，小事务B执行失败可以回滚到B之前并选择执行小事务C。



几个核心类：

- TransactionDefinition。记录事务的控制信息，如隔离级别、传播行为。
- TransactionStatus。记录整个事务状态，包括挂起的事务。一般是DefaultTransactionStatus
- PlatformTransactionManager。事务管理核心组件。
- TransactionSynchronizationManager。为不同的事务线程保存资源、状态，比如DataSourceUtils用它获取当前Connection。Synchronization是回调接口，可以注册到事务处理过程中，事务某些时间点会调用。

>Spring 将 JDBC 的 Connection、Hibernate 的 Session 等访问数据库的连接或者会话对象统称为资源，这些资源在同一时刻是不能多线程共享的 。   为了让 DAO 或 Service 类可以实现单例模式，  Spring 的事务同步管理类 org.springframework.transaction.support.TransactionSynchronizationManager 利用 ThreadLocal 为不同的事务线程提供了独立的资源副本，并同时维护这些事务的配置属性和运行状态信息 。

PlatformTransactionManager:

- getTransaction。开始事务
- commit
- rollback

TransactionTemplate如果要回滚事务，必须把checked异常转为RuntimeException，或者设置事务状态为rollbackOnly

## 事务传播行为

当事务方法被另一个事务方法调用时，必须指定事务应该如何传播。

**TransactionDefinition.PROPAGATION_REQUIRED：** 如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。

PROPAGATION_NESTED 嵌套事务

## 回滚规则

- 默认情况下，事务只有遇到运行期异常时才会回滚，而在遇到检查型异常时不会回滚

- 可以声明事务在遇到特定的检查型异常时像遇到运行期异常那样回滚。

- 可以声明事务遇到特定的异常不回滚，即使这些异常是运行期异常。

## 声明式事务

在TransactionDefinition基础上，TransactionAttribute增加了什么异常需要回滚的信息（rollbackOn方法）。

xml定义元数据，需要声明：

- PlatformTransactionManager的实现类，如DataSourceTransactionManager
- aop advice需要的所有TransactionAttribute信息（事务元数据）

注解声明事务，步骤：

- xml需要开启<tx:annotation-driven>，基础设施
- 定义DataSource
- 定义TransactionManager

## ThreadLocal

ThreadLocal和同步实际上没关系，但目的都是为了线程安全。

ThreadLocal

- 横向上来看，横跨多个线程。可以避免对象的共享，达到线程安全
- 纵向上，线程内传递数据。
- 可以绑定多个线程的资源， 但只会将数据资源给特定线程

应用场景：

- 多线程避免对象的共享，让每个线程持有单独的资源（副本）。如jdbc的Connection非线程安全类，让每个线程单独持有自己的，可以保证事务不混乱。
- 线程内传递数据，避免耦合性很强的参数传递。需要用一组框架类规范并屏蔽对ThreadLocal的直接操作
- 绑定某项全局资源，避免后续多次初始化

实例：

- ThreadLocal保存当前线程使用的数据源标志，实现DataSourceTypeManager
- 访问数据库前需要设定当前线程的类型。DataSourceTypeManager.set

Spring策略模式：

- 事务管理器框架
- 实例化bean对象时，使用反射或cglib
- validation框架的Validator接口

## JTA分布式事务

具体事务资源（RDBMS/MessagesQueue)要加入分布式事务，JTA规范要实现XAResource接口。某数据库（RM）可能提供支持XA的适配器程序（驱动）。然后JTATransactionManager就能与RM通信了。

ApplicationServer负责协调JTATransactionManager与各RM之间的交互，步骤：

1. ApplicationServer通过jndi绑定JTA的UserTransaction或TransactionManager实现类。开始事务时可以调用相应事务管理api
2. ApplicationServer要求JTATransactionManager分配事务号xid，开始事务，绑定事务到当前线程。
3. ApplicationServer和RM适配器要XAResource和Connection。JTATransactionManager用XAResource和RM通信，调用start(xid)通知RM开始记录。
4. ApplicationServer使用Connection访问数据，完成后关闭Connection通知JTATransactionManager。JTATransactionManager调用RM的XAResource.end(xid)
5. 多个RM类似。
6. 结束事务，两阶段提交。JTATransactionManager调用RM的XAResource.prepare(xid)，每一个参与者执行与事务有关的数据更新，所有收到OK后再调用RM的XAResource.commit(xid)

# web session

web服务器创建session后，会给setHeader("set-cookie",sessionkey +"="+id)，设置浏览器cookie中的sessionId

原理

服务器往浏览器中返回cookie信息，一般都是通过HttpServletResponse的addCookie去完成。

代码使用了HTTP Cookie，基本算法很简单：

1. 如果Session没有准备好，那么创建一个Session，得到Session的ID，把此ID通过Set-Cookie发送给浏览器。浏览器会在下一次访问此站点时，发送此ID。
2. 如果Session已经准备好了，也就是说，浏览器通过Cookie发来了ID，并且通过此ID，可以在站点内获取到Session
3. 把创建或者获取的Session赋值给req对象
4. 在请求处理函数生命周期内，可以获取和修改Session对象
5. 在请求处理完后，保存此Session变量


encodeRedirectURL()仅在无法确定浏览器是否支持cookie的时候才会在url后面附加上jsessionid，如果它能找到一个jsessionid的cookie，它就认为浏览器是支持cookie的。因此可以自己创建一个jsessionid的cookie来欺骗encodeRedirectURL()。

# TaskExecutor

Spring提供类似java的Executor接口，封装不同jdk版本之间的

差异，各版本实现有差异。

# 定时

## 注解简单支持

```java
@Configuration
@EnableAsync
@EnableScheduling
public class AppConfig {
}
```

更细微的控制需要实现 `SchedulingConfigurer`   `AsyncConfigurer`  接口

```java
@Scheduled(fixedDelay=5000)
public void doSomething() {
    // something that should execute periodically
}
@Scheduled(fixedRate=5000)
public void doSomething() {
    // something that should execute periodically
}
@Scheduled(cron="*/5 * * * * MON-FRI")
@Async
public void doSomething() {
    // something that should execute on weekdays only
}
```

## Quartz支持

管理jobdetail

```xml
<bean name="exampleJob" class="org.springframework.scheduling.quartz.JobDetailFactoryBean">
    <property name="jobClass" value="example.ExampleJob"/>
    <property name="jobDataAsMap">
        <map>
            <entry key="timeout" value="5"/>
        </map>
    </property>
</bean>
```

job获取jobdetail上下文参数

```java
public class ExampleJob extends QuartzJobBean {

    private int timeout;

    /**
     * Setter called after the ExampleJob is instantiated
     * with the value from the JobDetailFactoryBean (5)
     */
    public void setTimeout(int timeout) {
        this.timeout = timeout;
    }

    protected void executeInternal(JobExecutionContext ctx) throws JobExecutionException {
        // do the actual work
    }

}
```

管理trigger和scheduler

```xml
<bean id="cronTrigger" class="org.springframework.scheduling.quartz.CronTriggerFactoryBean">
    <property name="jobDetail" ref="exampleJob"/>
    <!-- run every morning at 6 AM -->
    <property name="cronExpression" value="0 0 6 * * ?"/>
</bean>

<bean class="org.springframework.scheduling.quartz.SchedulerFactoryBean">
    <property name="triggers">
        <list>
            <ref bean="cronTrigger"/>
            <ref bean="simpleTrigger"/>
        </list>
    </property>
</bean>
```

## Quartz注解配置

Spring给job注入其他bean。需要给

```java
@Component
public class QuartzJobFactory extends AdaptableJobFactory {
    @Autowired
    private AutowireCapableBeanFactory capableBeanFactory;

    @Override
    protected Object createJobInstance(TriggerFiredBundle bundle) throws Exception {
        Object jobInstance = super.createJobInstance(bundle);
        capableBeanFactory.autowireBean(jobInstance);
        return jobInstance;
    }
}
```

scheduler配置

```dart
@Configuration
public class QuartzConfig {

    @Autowired
    DataSource dataSource;

    @Bean
    public SchedulerFactoryBean schedulerFactoryBean (QuartzJobFactory quartzJobFactory) throws Exception {
        SchedulerFactoryBean factoryBean=new SchedulerFactoryBean();
        factoryBean.setJobFactory(quartzJobFactory);
        factoryBean.setConfigLocation(new ClassPathResource("quartz.properties"));
        factoryBean.setDataSource(dataSource);
        factoryBean.afterPropertiesSet();
        return factoryBean;
    }

    @Bean
    public Scheduler scheduler(SchedulerFactoryBean schedulerFactoryBean) throws Exception {
        Scheduler scheduler=schedulerFactoryBean.getScheduler();
        scheduler.start();
        return scheduler;
    }

}
```

https://www.jianshu.com/p/7c6e63c88dc2

# Swagger2

## 依赖

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId> <version>2.9.2</version>
</dependency>
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>    <version>2.9.2</version>
</dependency>
```

## 配置类

最少的配置

```java
@Configuration
@EnableWebMvc
@EnableSwagger2 //引入Swagger相关的几个Configuration配置类
publicclass ApiConfig {
}

@SpringBootApplication
public class Application implements CommandLineRunner, WebMvcConfigurer {
    private static final Logger LOGGER = LoggerFactory.getLogger(Application.class);

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // 解决 SWAGGER 404报错
        registry.addResourceHandler("/swagger-ui.html").addResourceLocations("classpath:/META-INF/resources/");   		     registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");
    }
```

然后就可以访问http://localhost:${port}/swagger-ui.html



自定义，替换自动配置的bean

```java
@Configuration
@EnableSwagger2
public class SwaggerConfig {
    @Bean
    public Docket customDocket() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.any())
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        Contact contact = new Contact("团队名", "www.my.com", "my@my.com");
        return new ApiInfoBuilder()
                .title("文档标题")
                .description("文档描述")
                .contact(contact)   // 联系方式
                .version("1.1.0")  // 版本
                .build();
    }
}
```

# 设计模式

https://mp.weixin.qq.com/s?__biz=Mzg2OTA0Njk0OA==&mid=2247485303&idx=1&sn=9e4626a1e3f001f9b0d84a6fa0cff04a&chksm=cea248bcf9d5c1aaf48b67cc52bac74eb29d6037848d6cf213b0e5466f2d1fda970db700ba41&token=255050878&lang=zh_CN#rd

# Spring Cloud

Spring Cloud可以使用zookeeper作为配置中心和注册中心

https://my.oschina.net/llsydn/blog/1810649

配置中心客户端的配置项只能在bootstrap中配置

## 服务注册中心

服务注册中心也是单独的微服务，需要定义的只有一个启动类和application.yml.

启动类EurekaServerApplication。server.port是动态生成的

```java
package cn.how2j.springcloud;
 
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;
 
import cn.hutool.core.util.NetUtil;
 
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
     
    public static void main(String[] args) {
        //8761 这个端口是默认的，就不要修改了，后面的子项目，都会访问这个端口。
        int port = 8761;
        if(!NetUtil.isUsableLocalPort(port)) {
            System.err.printf("端口%d被占用了，无法启动%n", port );
            System.exit(1);
        }
        new SpringApplicationBuilder(EurekaServerApplication.class).properties("server.port=" + port).run(args);
    }
}
```



application.yml

```yml
eureka:
  instance:
    hostname: localhost
  client:
    registerWithEureka: false
    fetchRegistry: false
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
 
spring:
  application:
    name: eureka-server
```

运行 EurekaServerApplication，并访问：
http://127.0.0.1:8761/

## 客户端负载均衡

一个微服务访问其他某个微服务多个实例，实现负载均衡

build.gradle

```groovy
compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-openfeign'
```

启动类加上@EnableFeignClients ， 表示用于使用 Feign 方式。@EnableDiscoveryClient， 表示用于发现eureka 注册中心的微服务

```java
@SpringBootApplication
@EnableEurekaClient
@EnableDiscoveryClient
@EnableFeignClients
public class ProductViewServiceFeignApplication {
```

根据应用名称在euraka注册中心查找实例

```java
@FeignClient("PRODUCT-DATA-SERVICE")
public interface ProductClientFeign {    
    @GetMapping("/products")    
    public List<Product> listProdcuts();
}
```

## zipkin服务链路追踪

需要追踪的微服务都需要修改。

1. 加入依赖

```groovy
compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-openfeign'
```

2. 在启动类里配置 Sampler 抽样策略： ALWAYS_SAMPLE 表示持续抽样

```java
@Bean
public Sampler defaultSampler() {    return Sampler.ALWAYS_SAMPLE;}
```

3. application.yml都加上zipkin服务的地址。

```yaml
spring:
  zipkin:
    base-url: http://localhost:9411
```

4. 启动zipkin，重启需要被追踪的微服务. java -jar zipkin-server-2.10.1-exec.jar
5. 访问微服务，上http://localhost:9411/zipkin/dependency/查看依赖分析、调用记录

## 配置服务

```java
@SpringBootApplication
@EnableConfigServer
@EnableDiscoveryClient
@EnableEurekaClient
public class ConfigServerApplication {
```

application.yml配置git下配置文件目录。uri是配置目录所在路径, label是分支，searchPaths是目录名

```yaml
spring:
  application:
    name: config-server
  cloud:
    config:
      label: master
      server:
        git:
          uri: https://github.com/how2j/springcloudConfig/
          searchPaths: respo
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
```

## 配置更改后通知

实现配置文件更改后通过Post请求通知其他微服务更新，步骤如下

```groovy
//1. 多了spring-boot-starter-actuator 用于访问路径：/actuator/bus-refresh
//2. 多了spring-cloud-starter-bus-amqp 用于支持 rabbitmq     
compile group: 'org.springframework.boot', name: 'spring-boot-starter-actuator'
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-bus-amqp'
```

bootstrap.yml 新增 bus总线配置总线配置,新增 rabbitMQ 配置

```yaml
spring:
  cloud:
    config:
      label: master
      profile: dev
      discovery:
        enabled:  true
        serviceId:  config-server
    bus:
      enabled: true
      trace:
        enabled: true
  client:
    serviceUrl:
      defaultZone:  http://localhost:8761/eureka/
   
rabbitmq:
  host: localhost
  port: 5672
  username: guest
  password: guest     
```

 application.yml 新增路径访问允许，这样才能访问 /actuator/bus-refresh

```yaml
spring:
  application:
    name:  product-view-service-feign
  thymeleaf:
    cache: false
    prefix: classpath:/templates/
    suffix: .html
    encoding: UTF-8
    content-type: text/html
    mode: HTML5       
  zipkin:
    base-url: http://localhost:9411   
     
management:
  endpoints:
    web:
      exposure:
        include: "*"
      cors:
        allowed-origins: "*"
        allowed-methods: "*"       
```

通过POST请求更新配置中心和客户端配置后，客户端还需要@RefreshScope

```java
@Controller
@RefreshScope
public class ProductController {
 
	@Autowired ProductService productService;
    @Value("${version}")
    String version;
```

因为服务改造后支持了 rabbitMQ, 那么在默认情况下，它的信息就不会进入 Zipkin了。 在启动 Zipkin 的时候 带一个参数就好了

```shell
java -jar zipkin-server-2.10.1-exec.jar --zipkin.collector.rabbitmq.addresses=localhost
```

## 断路器

场景：数据库微服务停止，导致视图服务返回超时，提示信息不友好

思路：改造视图服务，发现数据微服务无法使用后立即使用断路器，给用户提示

视图服务加入依赖

```groovy
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-netflix-hystrix'
```



application.yml或bootstrap.yml中加入

```yaml
feign.hystrix.enabled: true
```

定义断路器

```java
package cn.how2j.springcloud.client;
 
import java.util.ArrayList;
import java.util.List;
 
import org.springframework.stereotype.Component;
 
import cn.how2j.springcloud.pojo.Product;
 
@Component
public class ProductClientFeignHystrix implements ProductClientFeign{
    public List<Product> listProdcuts(){
        List<Product> result = new ArrayList<>();
        result.add(new Product(0,"产品数据微服务不可用",0));
        return result;
    }
 
}
```

如果通过feign访问不通PRODUCT-DATA-SERVICE服务，则使用断路器。

```java
package cn.how2j.springcloud.client;
 
import java.util.List;
 
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
 
import cn.how2j.springcloud.pojo.Product;
 
@FeignClient(value = "PRODUCT-DATA-SERVICE",fallback = ProductClientFeignHystrix.class)
public interface ProductClientFeign {
 
    @GetMapping("/products")
    public List<Product> listProdcuts();
}
```

## 断路器监控

监控也所谓一个微服务，但相对独立，不连接eurka和config-Server。

浏览器上输入url监控具体的服务。



依赖

```groovy
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-netflix-eureka-client'
    compile group: 'org.springframework.boot', name: 'spring-boot-starter-web'
    compile group: 'org.springframework.boot', name: 'spring-boot-starter-actuator'
    compile group: 'org.springframework.boot', name: 'spring-cloud-starter-netflix-hystrix'
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-netflix-hystrix-dashboard'
```

启动类

```java
@SpringBootApplication
@EnableHystrixDashboard
public class ProductServiceHystrixDashboardApplication {
```

配置中指定应用名称

```yaml
spring:
  application:
    name: hystrix-dashboard
```

被监控微服务的启动类增加注解

```java
@EnableCircuitBreaker
public class ProductViewServiceFeignApplication {
```

此外，springCloud 提供了一个 turbine 项目，可以把一个集群里的多个实例汇聚在一个 turbine里，这个然后再在 断路器监控里查看这个 turbine,  这样就能够在集群层面进行监控

http://how2j.cn/k/springcloud/springcloud-turbine/2044.html

## 网关

zuul网关和配置server类似，需要连接eureka。

```groovy
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-netflix-eureka-client'
    compile group: 'org.springframework.cloud', name: 'spring-cloud-starter-netflix-zuul'
    compile group: 'org.springframework.boot', name: 'spring-boot-starter-web'
```

启动类@EnableZuulProxy

```java
@SpringBootApplication
@EnableZuulProxy
@EnableDiscoveryClient
@EnableEurekaClient
public class ProductServiceZuulApplication {
    public static void main(String[] args) {
        int port = 8040;
        if(!NetUtil.isUsableLocalPort(port)) {
            System.err.printf("端口%d被占用了，无法启动%n", port );
            System.exit(1);
        }
        new SpringApplicationBuilder(ProductServiceZuulApplication.class).properties("server.port=" + port).run(args);
     
    }
}
```

配置eureka注册中心地址、路由。

```yaml
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
spring:
  application:
    name: product-service-zuul
zuul:
  routes:
    api-a:
      path: /api-data/**
      serviceId: PRODUCT-DATA-SERVICE
    api-b:
      path: /api-view/**
      serviceId: PRODUCT-VIEW-SERVICE-FEIGN
```



# Spring-kafka

## 创建topic

一种方式是

```java
    /**
     * 通过注入一个 NewTopic 类型的 Bean 来创建 topic，如果 topic 已存在，则会忽略。
     */
    @Bean
    public NewTopic myTopic() {
        return new NewTopic(myTopic, 2, (short) 1);
    }

    @Bean
    public NewTopic myTopic2() {
        return new NewTopic(myTopic2, 1, (short) 1);
    }
```

方式二：通过配置文件注册topic

在 `application.xml` 配置文件中配置 Kafka 连接信息以及我们项目中用到的 topic。

```
server:
  port: 9090
spring:
  kafka:
    bootstrap-servers: localhost:9092
kafka:
  topics:
    - name: topic1
      num-partitions: 3
      replication-factor: 1
    - name: topic2
      num-partitions: 1
      replication-factor: 1
    - name: topic3
      num-partitions: 2
      replication-factor: 1
```

`TopicConfigurations` 类专门用来读取我们的 topic 配置信息：

```
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
@ConfigurationProperties(prefix = "kafka")
@Setter
@Getter
@ToString
class TopicConfigurations {
    private List<Topic> topics;

    @Setter
    @Getter
    @ToString
    static class Topic {
        String name;
        Integer numPartitions = 3;
        Short replicationFactor = 1;

        NewTopic toNewTopic() {
            return new NewTopic(this.name, this.numPartitions, this.replicationFactor);
        }

    }
}
```

在 `TopicAdministrator` 类中我们手动将 topic 对象注册到容器中。

```
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.support.GenericWebApplicationContext;

import javax.annotation.PostConstruct;
import java.util.List;

/**
 * @author shuang.kou
 */
@Configuration
public class TopicAdministrator {
    private final TopicConfigurations configurations;
    private final GenericWebApplicationContext context;

    public TopicAdministrator(TopicConfigurations configurations, GenericWebApplicationContext genericContext) {
        this.configurations = configurations;
        this.context = genericContext;
    }

    @PostConstruct
    public void init() {
        initializeBeans(configurations.getTopics());
    }

    private void initializeBeans(List<TopicConfigurations.Topic> topics) {
        topics.forEach(t -> context.registerBean(t.name, NewTopic.class, t::toNewTopic));
    }


}
```

这样的话，当我们运行项目之后，就会自动创建 3 个名为：topic1、topic2 和 topic3 的主题了。