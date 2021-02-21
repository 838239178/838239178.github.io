---
layout: post
cover: 'assets/images/tree.png'
title: 关于Spring事务管理失效问题
comments: true
date: 2021-02-21
tags: java web
author: sjh
description: spring事务管理与AOP中的神坑
---

# 关于Spring事务管理失效问题

## 前言

学习 [Java Web](https://blog.pressed.top/javaweb)学到了Spring的事务管理，在实际使用过程中发现，`@Transcational`与 `@EnableTranscationManagement` 组合使用时，出现了事务管理失效、无法回滚的问题，在网上搜索一番依然无法得到答案，后来在自己的冥思苦想下联想起Spring事务管理本质时AOP的结论时恍然大悟，于是通过逐个注释来测试其他切面的方法终于得到答案——环绕通知导致了无法进行事务回滚！

## 原因分析

得知无法进行事务管理的原因是环绕通知时，我开始思考原因，通过查阅网上资料，得知Spring执行AOP切面遵循着一定的顺序，而这个顺序是由 `Order` 属性决定的！然后我就通过更改`Order`的方式对环绕通知的切面和事务管理切面进行测试，最终得出原因为**事务切面的优先级高于环绕通知切面的优先级时，事务管理无法执行（回滚）**

## 解决办法

### 快速解决办法

解决办法由上文非常容易得知，需要通过以下方法修改`Order`的值，需要注意的是该值越大，优先级越低，而事务切面默认值为`Integer.MAX_VALUE`，默认是优先级最低的，但是同样的其他Aspect默认值也是`Integral.MAX_VALAUE`，具体原因本人愚昧未知。所以说以下配置可以忽略事务管理切面的优先级Order的配置，只更改其他Aspect的Order。

#### XML式配置

在以下两个标签中添加配置order属性值

```xml
<aop:advisor order="" />
<aop:around order="" />
```

#### 注解式配置

普通切面类通过`@Order` 注释传入一个`int`值即可

```java
@Component
@Aspect
@Order(10086)
public class MyAspect {}
```

事务管理切面需要在`@EnableTranscationManagement`中配置`order`参数

```java
@EnableTransactionManagement(order = 1008611)
@Configuration
public class SpringConfiguration {}
```

### 优雅的解决办法

如果按照以上方法配置Order难免会在项目越来越大的情况变得难以管理，因为是耦合在代码上的所以不利于管理，所以我们最优雅的解决办法是使用.`properties`配置文件。

#### XML配置

这个就是引用properties罢了，没什么好讲的，学过Spring XML配置都应该知道如何引入properties文件然后通过`${keyName}`访问。

#### 注解配置

因为注解配置使用的是`Java`代码，且本人暂未发现Spring框架本身对Order批量管理的支持，所以只好自己想一套简单但又良好的方法，从贴合框架啊本身的角度来讲，使用XML配置更符合:leaves:Spring框架的生态。

1. 创建properties文件，并在**配置类**中使用`@PropertySource`加载

2. 让你的Aspect类继承`org.springframework.core.Ordered`接口并按照如下来实现接口方法

   ```java
   @Component
   @Aspect
   public class MyAspect implements Ordered {
       @Value("${keyName}")
       private int order;
   
       @Override
       public int getOrder() {
           return this.order;
       }
   }
   ```

#### 关于解决方法

注解配置的解决方法可能不够完美，但是也很好的进行解耦了，还有一些比较方便的方法但是实现难度较大，比如动态代理注解，用类名代替注解内的参数，来避免每次创建类都要用`@Value`注入order，然后就可以再配置文件中直接使用类名作为`key`配置Order了，目前动态代理注释的方法仍不清楚，所以暂时放弃这种方案。