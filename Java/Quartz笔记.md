

# 概述

触发器 Trigger： 什么时候工作。多个Trigger可以用于同一个job。需要关联到组

任务 Job: 做什么工作，是对工作的抽象

JobDetail：job工作的上下文，job需要的配置信息。初始化时JobDataMap、job关联到它上面。需要关联到组上。

JobDataMap: 给 Job 提供参数用的，绑定在了jobDetail上

调度器 Scheduler:使用 Trigger和Jobdetail将任务加入调度器，然后启动。完成后关闭 



# Job

定义job

Job

- 每次scheduler执行job，都会通过反射新创建一个job类（实现了Job接口）的新实例，执行完该实例会被回收。
- Job类必须有默认的无参构造函数
- Job类上不绑定有状态的数据

默认的情况下，无论上一次任务是否结束或者完成，只要规定的时间到了，那么下一次就开始。 

不允许并发执行。如数据库备份工作，并行备份很有可能造成 数据库被锁死 （几个线程同时备份数据库，引发无法预计的混乱） 

```java
@DisallowConcurrentExecution
public class DatabaseBackupJob implements Job {		
```

处理异常:

-  通知所有管理这个 Job 的调度停止运行它 
- 修改参数重新运行

```java
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
public class ExceptionJob1  implements Job {
    public void execute(JobExecutionContext context) throws JobExecutionException {
         int i = 0;
        try {           
        } catch (Exception e) {
            System.out.println("发生了异常，取消这个Job 对应的所有调度");
            JobExecutionException je =new JobExecutionException(e);
            je.setUnscheduleAllTriggers(true);
            throw je;
        }
        
        try {
            //故意发生异常
            System.out.println("运算结果"+100/i);            
        } catch (Exception e) {
            System.out.println("发生了异常，修改一下参数，立即重新执行");
            i = 1;
            JobExecutionException je =new JobExecutionException(e);
            je.setRefireImmediately(true);
            throw je;
        }
    }
}


```

#  SimpleTrigger 

可以方便的实现一系列的触发机制。 

# Spring集成

## 配置

把jobdetail可以注入到TriggerFactoryBean上

triggerFactoryBean可以注入到SchedulerFactoryBean中。

一台定时服务挂了，另一台会接管正在执行的任务



quartz配置

```properties
org.quartz.scheduler.instanceName: FayaQuartzScheduler

#调度器实例编号自动生成
org.quartz.scheduler.instanceId = AUTO

# 持久化配置
org.quartz.jobStore.class = org.quartz.impl.jdbcjobstore.JobStoreTX

#quartz相关数据表前缀名
org.quartz.jobStore.tablePrefix = QRTZ_

#开启分布式部署
org.quartz.jobStore.isClustered = true

#分布式节点有效性检查时间间隔，单位：毫秒
org.quartz.jobStore.clusterCheckinInterval = 20000

org.quartz.scheduler.rmi.export: false
org.quartz.scheduler.rmi.proxy: false
org.quartz.scheduler.wrapJobExecutionInUserTransaction: false

#线程池实现类
org.quartz.threadPool.class: org.quartz.simpl.SimpleThreadPool
org.quartz.threadPool.threadCount: 50
org.quartz.threadPool.threadPriority: 5
org.quartz.threadPool.threadsInheritContextClassLoaderOfInitializingThread: true

org.quartz.jobStore.misfireThreshold: 60000
```

bean定义

```java
/**
 * quartz的配置
 * */
@EnableScheduling
@Configuration
public class QuartzConfiguration {

    @Bean
    public JobFactory jobFactory(ApplicationContext applicationContext)
    {
        AutowiringSpringBeanJobFactory jobFactory = new AutowiringSpringBeanJobFactory();
        jobFactory.setApplicationContext(applicationContext);
        return jobFactory;
    }

    @Bean
    public SchedulerFactoryBean schedulerFactoryBean(JobFactory jobFactory,@Qualifier("dataSource") DataSource dataSource){

        SchedulerFactoryBean schedulerFactoryBean=new SchedulerFactoryBean();
        //将spring管理job自定义工厂交由调度器维护
        schedulerFactoryBean.setJobFactory(jobFactory);
        //设置配置文件位置
        schedulerFactoryBean.setConfigLocation(new ClassPathResource("/quartz.properties"));
        //设置覆盖已存在的任务
        schedulerFactoryBean.setOverwriteExistingJobs(true);
        //项目启动完成后，等待2秒后开始执行调度器初始化
        schedulerFactoryBean.setStartupDelay(2);
        //设置调度器自动运行
        schedulerFactoryBean.setAutoStartup(true);

        //设置数据源，使用与项目统一数据源
        schedulerFactoryBean.setDataSource(dataSource);

        return schedulerFactoryBean;
    }

    /**
     * 继承org.springframework.scheduling.quartz.SpringBeanJobFactory
     * 实现任务实例化方式
     */
    public static class AutowiringSpringBeanJobFactory extends SpringBeanJobFactory implements
            ApplicationContextAware {

        private transient AutowireCapableBeanFactory beanFactory;
        @Override
        public void setApplicationContext(final ApplicationContext context) {
            beanFactory = context.getAutowireCapableBeanFactory();
        }
        /**
         * 将job实例交给spring ioc托管
         * 我们在job实例实现类内可以直接使用spring注入的调用被spring ioc管理的实例
         */
        @Override
        protected Object createJobInstance(final TriggerFiredBundle bundle) throws Exception {
            final Object job = super.createJobInstance(bundle);
            //将job实例交付给spring ioc
            beanFactory.autowireBean(job);
            return job;
        }
    }

}

//配置完成后就可以在service里面引用了
@Autowired
private Scheduler scheduler;
```

链接：http://www.imooc.com/article/272332