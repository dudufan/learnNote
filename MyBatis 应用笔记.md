批量加载mapper.xml,  以上配置失败，是因为没有将UserMapper.xml和UserMapper.java 放在同一个目录
<!-- 批量加载映射配置文件,mybatis自动扫描包下面的mapper接口进行加载
        遵循一定的规范：需要将mapper接口类名和mapper.xml映射文件名称保持一致，且在一个目录中；
            上边规范的前提是：使用的是mapper代理方法;
      -->
 <package name="com.mybatis.mapper"/>


 
二级缓存 经测试，MyBatis 不开启二级缓存情况下建立5000个会话执行相同查询情 况下，时间是开启二级缓存的6倍...
不同的SqlSession对象，一级缓存不起作用。



