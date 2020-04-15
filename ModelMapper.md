# 配置gradle
```

sourceCompatibility = 
1.7


repositories {

    maven { url 
"http://maven.aliyun.com/nexus/content/groups/public/" 
}

}


dependencies {

    compile 
group
: 
'com.alibaba'
, 
name
: 
'fastjson'
, 
version
: 
'1.2.46'

    
compile 
group
: 
'org.modelmapper'
, 
name
: 
'modelmapper'
, 
version
: 
'2.1.0'

    
testCompile 
group
: 
'junit'
, 
name
: 
'junit'
, 
version
: 
'4.12'

}

```
## 映射规则语法
### 同类型的字段转换（包括常量-变量）
```

map().setName(source.getFirstName());
map(source.address, destination.streetAddress);
```
### 不同类型强转
```java
map(source.getAge()).setAgeString(null);
map(source.getAgeString()).setAge((short) 0);
map(21).setAgeString(null);
```
注意：其中最右边括号的值完全没用。
### 不同层次间转换（deep mapping）
```
map().getCustomer().setName(source.person.getFirstName());
``` ### 跳过不转换某些值
```
skip().setName(null);

skip(source.name);
```
## 定义具体类型的转换器
### 同类型转换
```
Converter<String, String> toUppercase = new AbstractConverter<String, String>() {

    protected String convert(String source) {
        return source == null ? null : source.toUppercase();
    }
};
// Using the toUppercase Converter to map from a source property to a destination property is simple:
using(toUppercase).map().setName(source.getName());
```

### 不同类型转换
```java
Converter<Person, String> toUppercase = new AbstractConverter<Person, String>() {
    protected String convert(Person person) {
        return person == null ? null : person.getFirstName();
    }
};
// When defining a mapping to use this converter, we simply pass the source object, which is of type Person, to the map method:

using(personToNameConverter).map(source).setName(null);

``` ## 映射泛型
```java
Type listType = new TypeToken<List<String>>() {}.getType();
List<String> characters = modelMapper.map(numbers, listType);
```

