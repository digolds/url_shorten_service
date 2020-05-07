# 测试微服务的最佳实践-如何测试URL Shortening Service

1. 什么是URL Shortening Service
2. 需求评审和明确URL Shortening Service所要达到的目标
3. URL Shortening Service的性能指标评估
4. URL Shortening Service的拆分
5. 针对URL Shortening Service选择相应的测试工具
6. 为URL Shortening Service制定测试策略
7. 准备测试数据
8. 生成测试报告
9. 参考

## 什么是URL Shortening Service

URL Shortening Service是一个可以将长链接转化成短链接的线上服务。这些短链接与长链接一一对应，用户可以在浏览器里输入短链接，以此来访问长链接，这些长链接就是原始的URL。短链接有这些优点：占用少量的显示空间，可以用于各大线上媒体，软文，报纸或印刷体等；用户在输入短链接时，不容易出错！

例如，以下是一个原始的长链接：

```bash
https://2cloudlabs.com/collection/page/5668639101419520/5649050225344512/5668600916475904/
```

通过URL Shortening Service，我们可以得到以下短链接：

```bash
http://2cl.com/jlg8zpc
```

短链接的长度仅仅是长链接的三分之一。

## 需求评审和明确URL Shortening Service所要达到的目标

URL Shortening Service要实现的基本功能有以下几点：

* 功能性需求

1. 给定一个原始URL（也就是长链接），我们的URL Shorten Service应该生成一个唯一的短链接。这个短链接的长度应该缩减到一定范围，方便复制
2. 当终端用户访问短链接，我们的URL Shorten Service应该自动根据短链接跳转到原始URL

* 非功能性需求

1. 该URL Shortening Service应该高可用，也就是需要满足7*24小时全天候运转
2. 通过短链接访问原始URL所需的时间应该尽可能的短

## URL Shortening Service的性能指标评估

URL Shortening Service的特点是有大量的读操作，同时伴随的少部分的写操作。

## 参考

[Designing a URL Shortening service like TinyURL](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR)