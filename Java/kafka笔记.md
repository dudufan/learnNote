[TOC]

http://kafka.apache.org/documentation.html

# 概述



结合了文件系统和消息队列的优点

特点：

发布-订阅

可靠存储

实时处理



用途：

存储海量历史数据作批处理

构建消息驱动的应用程序。

重视存储，消费者可以控制消费的位置，可以当作特殊分布式文件系统。特点：高性能低延时的提交日志存储/复制/传播。

可靠的消息管道

网站行为追踪

统计信息监控收集

[Event sourcing](http://martinfowler.com/eaaDev/EventSourcing.html)

提交日志存储 [log compaction](http://kafka.apache.org/documentation.html#compaction) 



特性：

日志分区

支持多个数据中心复制和备份

记录用topic分类

每条记录有key/value/timestamp

Kafka实例

每一台kafka实例都有一个brokerId



提供API:

[Consumer API](http://kafka.apache.org/documentation.html#consumerapi) 

- [Producer API](http://kafka.apache.org/documentation.html#producerapi) 

[Streams API](http://kafka.apache.org/documentation/streams)可以对流数据做复杂的转换

[Connector API](http://kafka.apache.org/documentation.html#connect) 

```java
public class Message implements Serializable {
    private String topic;
    // 消息的键值，kafka支持
    private String key;
    // 消息属性
    private Map<String, String> properties;
    private String value;
    // 多条消息可以区分事务
    private String transactionId;
    // 指定分区
    private Integer partition;
}

public interface Producer {
    sendMessage(ProducerRecord);
}
```



# 查看版本

```shell
find / -name \*kafka_\* | head -1 | grep -o ``'\kafka[^\n]*'
```

 你应该看到像kafka_2.11-0.9.0.1-site-docs.tgz这样的文件，其中2.11是Scala版本，0.9.0.1是Kafka版本。 

# 存储机制

## 日志分区

存储数据的文件叫日志，日志分区。

日志三个维度

topic 1-n partition 

partition n-1 server

partition 1-n replicas

分区日志的特点：

- 分区是一个结构化的提交日志
- 给一个topic可以指定创建0-多个partition。一个分区只能在一台server上，不同分区可以在一台或多台上
- 一个分区内保证消息有序，每条记录有一个唯一的序列号叫offset
- 会把多个分区动态分配到group中的多个消费者，一个分区只能被一个consumer消费，一个consumer可以消费多个分区。因此consumer group内consumer实例数不能超过分区数。当只有一个broker时，所有的分区就只分配到该Broker上
- 设置日志保留的时间
- 性能相对数据大小不变
- kafka允许生产者等待反馈，保证数据写并且复制成功
- kafka是根据key的hash值与分区数取模来决定数据存储到那个分区



作用：

- 方便水平扩展
- 作为并行单元，负载均衡，提供单台吞吐量

缺点：

如果分区过多，那么日志分段也会很多，写的时候由于是批量写，其实就会变成随机写了，随机 I/O 这个时候对性能影响很大。所以一般来说 Kafka 不能有太多的 Partition。

## 分区备份

- 每个分区有一个leader，有0到多个副本作为followers，每个副本都在不同的server上。副本数量不超过broker数量。
- 分区的leader负责读写，其他副本只是备份
- 每个kafka server是部分分区的leader，也是其他分区的follower



举例：

一个分区，3个副本

```shell
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
 Topic: my-replicated-topic  Partition: 0    Leader: 1   Replicas: 1,2,0 Isr: 1,2,0
```

replicas显示分区的所有副本，无论是leader还是followers，无论所在node是否存活。

isr显示该分区活跃的副本。

leader所在kafka server(node 1)进程关闭后，leader自动切换到node 2

```shell
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
 Topic: my-replicated-topic  Partition: 0    Leader: 2   Replicas: 1,2,0 Isr: 2,0
```



## 保证消息顺序

两种方法：

1. topic内有序。一般分区内有序就足够了，为保证一个topic下都有序，那就只能用一个分区。
2. 分区内有序。发送消息的时候指定 key/Partition，这样同一个 Key 的所有消息都进入到相同的分区里面



## 可靠存储

 Kafka 为分区（Partition）引入了多副本（Replica）机制。

- 一个分区有多个副本，一个leader多个follower

- 生产者和消费者只与 leader 副本交互。发送被发送到leader，然后 follower 副本才能从 leader 副本中拉取消息进行同步

- followers只是为保证消息存储的安全性

问题：假如 leader 副本所在的 broker 突然挂掉，那么就要从 follower 副本重新选出一个 leader ，但是 leader 的数据还有一些没有被 follower 副本的同步的话，就会造成消息丢失。

**设置 acks = all**

解决办法就是我们设置  **acks = all**。acks 是 Kafka 生产者(Producer)  很重要的一个参数。

acks 的默认值即为1，代表我们的消息被leader副本接收之后就算被成功发送。当我们配置 **acks = all** 代表则所有副本都要接收到该消息之后该消息才算真正成功被发送。

**设置 replication.factor >= 3**

为了保证 leader 副本能有 follower 副本能同步消息，我们一般会为 topic 设置 **replication.factor >= 3**。这样就可以保证每个 分区(partition) 至少有 3 个副本。虽然造成了数据冗余，但是带来了数据的安全性。

**设置 min.insync.replicas > 1**

一般情况下我们还需要设置 **min.insync.replicas> 1** ，这样配置代表消息至少要被写入到 2 个副本才算是被成功发送。**min.insync.replicas** 的默认值为 1 ，在实际生产中应尽量避免默认值 1。

但是，为了保证整个 Kafka 服务的高可用性，你需要确保 **replication.factor > min.insync.replicas** 。为什么呢？设想一下加入两者相等的话，只要是有一个副本挂掉，整个分区就无法正常工作了。这明显违反高可用性！一般推荐设置成 **replication.factor = min.insync.replicas + 1**。

**设置 unclean.leader.election.enable = false**

> **Kafka 0.11.0.0版本开始 unclean.leader.election.enable 参数的默认值由原来的true 改为false**

我们最开始也说了我们发送的消息会被发送到 leader 副本，然后 follower 副本才能从 leader 副本中拉取消息进行同步。多个 follower 副本之间的消息同步情况不一样，当我们配置了 **unclean.leader.election.enable = false**  的话，当 leader 副本发生故障时就不会从  follower 副本中和 leader 同步程度达不到要求的副本中选择出  leader ，这样降低了消息丢失的可能性。

# Rebalance

当新的消费者加入消费组，它会消费一个或多个分区，而这些分区之前是由其他消费者负责的；另外，当消费者离开消费组（比如重启、宕机等）时，它所消费的分区会分配给其他分区。这种现象称为**重平衡（rebalance）**。重平衡是
Kafka 
一个很重要的性质，这个性质保证了高可用和水平扩展。**不过也需要注意到，在重平衡期间，所有消费者都不能消费消息，因此会造成整个消费组短暂的不可用。**而且，将分区进行重平衡也会导致原来的消费者状态过期，从而导致消费者需要重新更新状态，这段期间也会降低消费性能

# 多数据中心

分区复制冗余机制只适用于同一个 Kafka 集群内部，对于多个 Kafka 集群消息同步可以使用 Kafka 提供的 MirrorMaker 
工具。本质上来说，MirrorMaker 只是一个 Kafka 
消费者和生产者，并使用一个队列连接起来而已。它从一个集群中消费消息，然后往另一个集群生产消息。




# 生产者

producer负责选择把记录放入topic下某个partition。可以使用轮询的方式或者对key值计算的函数，来选择partition

```java
./kafka-console-producer.sh --broker-list 192.168.16.100:9092 --topic gonst </root/WordsList.txt
```

## Ack机制

Producer在发送生产出的数据给Broker时，可以选择三种模式，称为acks，它是Acknowledgment的缩写。意思是Broker对Producer即将发送来的数据采用何种确认方式。

**acks=0**

在该模式下，Producer不会等待Broker的确认反馈，即不关心Broker是否正确的将发送来的数据持久化，所以在这种模式下，很有可能会丢失数据。因为如果Broker挂了，Producer不会被通知到，所以还会不停的发送数据导致数据丢失。在对数据完整性需求不强烈的场景下，这种模式可以提高性能。

**acks=1**

默认采用的模式，该模式下Producer会等待Leader Broker的确认反馈，当Broker确实将数据持久化到至少一个Partition中后，给予Producer确认反馈，Producer才会继续发送数据。该模式下有几点需要注意：

- 不保证Replicas也持久化了数据。
- 当Producer没有收到Broker的确认反馈时，Producer会尝试重新发送数据。
- 当Leader Broker挂了，但是Replicas又没有持久化数据时，还是会丢失数据。
- 该模式只能说是可以有效防止数据丢失。

**acks=all**

该模式下，Producer同样需要等待Broker的确认，但是确认更为严格，需要所有的Partition（Leader + Replicas）都持久化数据后才返回确认信息。这种模式下，只要Replicas足够多，数据基本不会丢失。

在该模式下，还有一个重要的参数`min.insync.replicas`需要配置。该参数的意思是当`acks=all`时，至少有多少个Replicas需要确认已成功持久化数据，这个Replicas数量也包括Leader。

举个例子，假设有三个Broker，参数为`min.insync.replicas=2`、`replication.factor=3`、`acks=all`，那么Producer每次发送Message时，都需要至少2个Broker给予确认反馈，换句话说，在这个Kafka集群中，只能允许一个Broker挂掉。如果`min.insync.replicas=3`，那么一个Broker都不能挂，否则Producer在发送Message时会收到`NOT_ENOUGH_REPLICAS`的异常。



作者：大猪小猪在菜盘
链接：https://www.jianshu.com/p/78df43dc603f
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

## Producer Api

```
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>2.4.0</version>
</dependency>
```

producer：

- 线程安全，一个应用中多个线程使用一个会更快。
- 发送消息时可以指定 Partition 
- sender方法是异步的，调用后立即返回。用一个缓冲池保存未发送到server的records，后台线程负责发送，支持批量发送
- 幂等开启后，send失败返回错误后会无限重试，要关掉producer检查上一条消息确保不重复发送。

示例。异步发送

```java
 Properties props = new Properties();
 props.put("bootstrap.servers", "localhost:9092");
// The acks config controls the criteria under which requests are considered complete. The "all" setting we have specified will result in blocking on the full commit of the record, the slowest but most durable setting. 
 props.put("acks", "all");
 props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
 props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

 Producer<String, String> producer = new KafkaProducer<>(props);
 for (int i = 0; i < 100; i++)
     producer.send(new ProducerRecord<String, String>("my-topic", Integer.toString(i), Integer.toString(i)));

 producer.close();
```

同步发送，get方法阻塞直到发送结果返回。当get方法抛出一个错误时，说明数据没有被正确写入，此时需要处理这个错误。 

```java
public void send2Kafka(Producer<Integer, String> kafkaProducer, String topic, List<String> lines) throws InterruptedException, ExecutionException{
    for(String line : lines) {
        ProducerRecord<Integer, String> message = new ProducerRecord<Integer, String>(topic, line);
        this.kafkaProducer.send(message).get();
    }
}
```

更推荐异步回调的方式处理消息发送失败的情况：

```java
        ListenableFuture<SendResult<String, Object>> future = kafkaTemplate.send(topic, o);
        future.addCallback(result -> logger.info("生产者成功发送消息到topic:{} partition:{}的消息", result.getRecordMetadata().topic(), result.getRecordMetadata().partition()),
                ex -> logger.error("生产者发送消失败，原因：{}", ex.getMessage()));
```

部分其他配置

```
bootstrap.servers 一个或多个kafkaServer的监听地址，就算只配一个也会发送到集群所有server上
retries 消息发送失败后自动重试。0不重试
batch.size 缓冲池大小
linger.ms 等待多久从缓冲池批量发送一次。0表示默认立即发送消息，多条时间相近的消息也会批量发送（高负载情况下很有用）。举例，设置为1，等待1ms可能会有100个记录填入缓冲池。
buffer.memory 缓冲池内存大小
enable.idempotence 保证当前会话内生产者最终发送成功一次，不会重复发送。ack=all retries=MAx
```

事务api需要0.11.0以上版本。send后不需要get，如果发送一条消息失败会抛出KafkaException。

```java
 Properties props = new Properties();
 props.put("bootstrap.servers", "localhost:9092");
 props.put("transactional.id", "my-transactional-id");
 Producer<String, String> producer = new KafkaProducer<>(props, new StringSerializer(), new StringSerializer());

 producer.initTransactions();

 try {
     producer.beginTransaction();
     for (int i = 0; i < 100; i++)
         producer.send(new ProducerRecord<>("my-topic", Integer.toString(i), Integer.toString(i)));
     producer.commitTransaction();
 } catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
     // We can't recover from these exceptions, so our only option is to close the producer and exit.
     producer.close();
 } catch (KafkaException e) {
     // For all other exceptions, just abort the transaction and try again.
     // 之前成功的写入都被标记aborted
     producer.abortTransaction();
 }
 producer.close();
```

## 重试

有时消息发送失败是因为网络问题，这种问题可能在很短暂的时间内就会自动修复，那么在这种情况下，我们希望Producer在发送失败后能重新尝试发送。

解决办法：

- 在异步发送添加回调函数的前提下，失败情况的回调函数检查失败原因后重新发送

- retries （重试次数）设置一个比较合理的值，一般是 3 ，但是为了保证消息不丢失的话一般会设置比较大一点。
- 建议还要设置重试间隔，因为间隔太小的话重试的效果就不明显了，网络波动一次你3次一下子就重试完了

问题：当设置了`retries`参数大于0后，假如我们需要相同Key的Message进入特定的Partition保证顺序。那么此时如果：

1. 第一条Message发送失败
2. 第二条Message发送成功了
3. 第一条通过重试发送成功了

那么Message的顺序就发生了变化。

解决办法：参数`max.in.flight.requests.per.connection`是未通过acks确认的发送请求最大数，默认是5。作用类似TCP的发送窗口

如果想在设置了`retries`还要严格控制Message顺序，可以把`max.in.flight.requests.per.connection`设置为1



作者：大猪小猪在菜盘
链接：https://www.jianshu.com/p/78df43dc603f
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

# 消费者



## Consumer Api

```
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>2.4.0</version>
</dependency>
```

offset不仅是分区内记录的唯一标识，也记录了（一个逻辑）消费者在分区内的位置。

对于一个消费者，有两个相关的值：

- [`position`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#position-org.apache.kafka.common.TopicPartition-)。消费者每次poll之后自动更新。
- [`committed position`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#commitSync--)。消费者进程失败或重启后恢复到的position，可以自动周期性的提交offset，或者用api(e.g. [`commitSync`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#commitSync--) and [`commitAsync`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#commitAsync-org.apache.kafka.clients.consumer.OffsetCommitCallback-)).显示指定。

消费者group中每个consumer都可以订阅多个topic。 [`subscribe`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#subscribe-java.util.Collection-org.apache.kafka.clients.consumer.ConsumerRebalanceListener-) APIs.

partition、consumer数量的变化，都会引发rebalancing。[`ConsumerRebalanceListener`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/ConsumerRebalanceListener.html)监听变化。

> In addition, when group reassignment happens automatically, consumers can be notified through a [`ConsumerRebalanceListener`](http://kafka.apache.org/24/javadoc/org/apache/kafka/clients/consumer/ConsumerRebalanceListener.html),

订阅topics后，consumer调用poll就会加入group。consumerd的poll方法内部会在`session.timeout.ms`内给server发送heartbeats，不发送consumer会被认为死掉，partition也会被重新分配。

 poll方法：

- 默认阻塞，可以指定timeout。
- 内部会给kafka server发送心跳。

**Automatic Offset Committing**

 This example demonstrates a simple usage of Kafka's consumer api that relies on automatic offset committing. 

topic可以是操作名，groupid可以是服务名称。

```java
     Properties props = new Properties();
     props.setProperty("bootstrap.servers", "localhost:9092");
     props.setProperty("group.id", "test");
     props.setProperty("enable.auto.commit", "true");
     props.setProperty("auto.commit.interval.ms", "1000");
     props.setProperty("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
     props.setProperty("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
     KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
     consumer.subscribe(Arrays.asList("foo", "bar"));
     while (true) {
         ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
         for (ConsumerRecord<String, String> record : records)
             System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());
     }
 
```

## 消费者丢失消息

问题：当消费者拉取到了分区的某个消息之后，消费者会自动提交了 offset。自动提交的话会有一个问题，试想一下，当消费者刚拿到这个消息准备进行真正消费的时候，突然挂掉了，消息实际上并没有被消费，但是 offset 却被自动提交了。

解决办法：简单粗暴，我们手动关闭闭自动提交 offset，每次在真正消费完消息之后之后再自己手动提交 offset 

# Broker 配置



```properties
zookeeper.connect: hostname1:port1,hostname2:port2,hostname3:port3/chroot/path
broker.id 不设置会自动生成
delete.topic.enable
log.dir 存放日志数据的目录。不是错误日志
```



**listeners**

```properties
listeners: INSIDE://172.17.0.10:9092,OUTSIDE://172.17.0.10:9094
advertised_listeners: INSIDE://172.17.0.10:9092,OUTSIDE://<公网 ip>:端口
kafka_listener_security_protocol_map: "INSIDE:SASL_PLAINTEXT,OUTSIDE:SASL_PLAINTEXT"
kafka_inter_broker_listener_name: "INSIDE"
```

`advertised_listeners` 监听器会注册在 `zookeeper` 中；

当我们对 `172.17.0.10:9092`  请求建立连接，`kafka` 服务器会通过 `zookeeper` 中注册的监听器，找到 `INSIDE` 监听器，然后通过 `listeners` 中找到对应的 通讯 `ip` 和 端口；

同理，当我们对 `<公网 ip>:端口`  请求建立连接，`kafka` 服务器会通过 `zookeeper` 中注册的监听器，找到 `OUTSIDE` 监听器，然后通过 `listeners` 中找到对应的 通讯 `ip` 和 端口 `172.17.0.10:9094`；

总结：

- 程序中使用的ip必须在listeners或advertised_listeners中包含。比如程序中要使用10.1.6.201连接kafka服务器，服务器配置必须是listeners=PLAINTEXT://10.1.6.201:9092,不能是PLAINTEXT://:9092(只能localhost连接)
- `advertised_listeners` 是对外暴露的服务端口，真正建立连接用的是 `listeners`。



只有内网

比如在公司搭建的 `kafka` 集群，只有内网中的服务可以用，这种情况下，只需要用 `listeners` 就行

```
listeners: <协议名称>://<内网ip>:<端口>
```

内外网

在 `docker` 中或者 在类似阿里云主机上部署 `kafka` 集群，这种情况下是 需要用到 `advertised_listeners`。

以 `docker` 为例：

```properties
listeners: INSIDE://0.0.0.0:9092,OUTSIDE://0.0.0.0:9094
advertised_listeners: INSIDE://localhost:9092,OUTSIDE://<宿主机ip>:<宿主机暴露的端口>
kafka_listener_security_protocol_map: "INSIDE:SASL_PLAINTEXT,OUTSIDE:SASL_PLAINTEXT"
kafka_inter_broker_listener_name: "INSIDE"
```

# Consumers

传统消息队列可以由多个消费者实例消费，一条消息仅能消费一次。

发布订阅广播到每个订阅者，因此对单个订阅者难以扩展为一个集群（需要单独做负载均衡）。

consumer group结合了传统消息队列和发布订阅的优点。

- 一个consumer group就是一个逻辑订阅者，比如user服务的多个实例。发送到Topic的消息,只会被订阅此Topic的每个group中的一个consumer消费。

消费者维护的元数据只有分区日志中自己消费到了哪个offset，消费者可以自己控制，可以重置到之前的offset，也可以

kafka会自动把多个分区动态均匀分配到一个consumer group的多个consumer实例上。



[Multi-tenancy](http://kafka.apache.org/intro#intro_multi-tenancy)



# 流处理

# Connectors

可以用来捕获数据库表的改变到kafka的topic，或者从topic导出到db

Stream api。可以消费或生产topic

# shell命令

启动

```shell
# 简单内置zookeeper
> bin/zookeeper-server-start.sh config/zookeeper.properties
#
> bin/kafka-server-start.sh config/server.properties
```

创建topic

```shell
> bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
> bin/kafka-topics.sh --create --zookeeper 10.1.6.201:2181 --replication-factor 1 --partitions 1 --topic test
> bin/kafka-topics.sh --list --bootstrap-server localhost:9092
test
```

0.9.0.1版本不支持bootstrap-server选项直连kafka server，以下命令都需要连接zookeeper

创建topic

```
bin/kafka-topics.sh --create --zookeeper 10.1.6.201:2181 --topic sms_log --replication-factor 1 --partitions 2
```

查看topic的分区、分片信息。

每个分区都有一个leader，零或多个follower

isr是当下存活的副本节点

```
> bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
Topic:my-replicated-topic   PartitionCount:1    ReplicationFactor:3 Configs:
    ``Topic: my-replicated-topic  Partition: 0    Leader: 1   Replicas: 1,2,0 Isr: 1,2,0
    
>bin/kafka-topics.sh --describe --zookeeper 10.1.6.201:2181 --topic sms_log
```

该topic仅有一个topic，Partition0的副本中，节点1是Leader，负责读写。

发送消息

```
> bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
This is a message
This is another message
> bin/kafka-console-producer.sh --broker-list 10.1.6.201:9092,10.1.6.202:9092 --topic sms_log
```

消费

```
> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message
> bin/kafka-console-consumer.sh --zookeeper 10.1.6.201:2181 --from-beginning --topic sms_log
```

# 测试

创建topic

```shell
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic yqt_test
```

# 高可用



## 可靠发送

