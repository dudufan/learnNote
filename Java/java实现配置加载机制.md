# 架构
1. 配置加载器。有一个load()方法提供appleConfig
2. 配置方式提供者。有一个provide()方法提供Document对象、或者JSONObject对象...
3. 生产配置方式提供者的工厂。createDocumentProvider(filepath)、 createJSONObjectProvider(filepath)等方法生产各种Provider


## 配置加载器
功能是把某配置文件(比如apple.xml）解析为AppleConfig
实现的接口应该是
```java
public interface IConfigLoader<T> {

   

    /**

     * load the config typed by T

     *

     * @return

     * @throws ConfigException

     */

    public T load() throws ConfigException;

}

```
泛型T告诉提供者应该提供什么，比如Document、JSONObject


## 