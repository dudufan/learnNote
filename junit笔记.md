junit实战中文版


核心：
Assert
测试--@Test
测试类
Suite
Runner




Suite

多个测试类可以组成测试集Suite


Assert
必须使用Assert，否则默认都是绿条
junit提供的assertNotNull，assertEquals等方法配合文本参数，能帮助定位错误，指出错误条件。而不是报出一大段异常


@Test
一个单元测试等于一个@Test方法



把每个单元测试都需要首先执行的代码放到fixture中，@Before,@After