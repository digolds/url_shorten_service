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

URL Shortening Service的特点是有大量的读操作，同时伴随着少部分的写操作。假设读与写的比例是100:1。接下来需要评估URL Shorten Service各项性能指标。

**流量估计**：假设每个月会生成500 million的短链接，根据读与写的比例来换算，同时期大约会有50 billion的短链接请求操作：

```bash
100 * 500M => 50B
```

根据以上读与写操作的数据，那么可以估算出对应的Queries Per Second（QPS）：

比如，针对写操作（也就是每个月生成500 million的短链接）的QPS，计算如下：

```bash
500 million / (30 days * 24 hours * 3600 seconds) = ~200 URLs/s
```

针对读操作（也就是每个月50 billion的短链接请求操作）的QPS，计算如下：

```bash
100 * 200 URLs/s = 20K/s
```

**存储估计**：假设我们需要存储每一个短链接以及对应的长链接，存储周期为5年。存储每一个短链接以及对应的长链接所需要的存储单元的大小为500 bytes，那么总的存储容量计算如下：

```bash
500 million * 5 years * 12 months * 500 bytes = 15 TB
```

**吞吐量估计**：由于写操作的速度是200 URLs/s，那么每秒向URL Shorten Service写入的数据量是100KB，计算如下：

```bash
200 * 500 bytes = 100 KB/s
```

读操作的速度是20K URLs/s，因此每秒从URL Shorten Service读出的数据量应该是10MB，计算如下：

```bash
20K * 500 bytes = 10 MB/s
```

总的来说，URL Shorten Service的吞吐量分为读取和写入，每秒读取数据的大小与写入数据的大小是不一致的，前者为10 MB/s，后者为100 KB/s。

**内存估计**：如果我们根据80-20原则来缓存数据，也就是我们会缓存20%的数据，那么每天需要缓存的大小是170GB，计算如下：

```bash
20K * 3600 seconds * 24 hours 0.2 * 500 bytes = 170GB
```

**响应时间估计**：URL Shorten Service主要提供2个功能，分别是生成短链接和根据短链接跳转到原始链接。每一个功能都应该有对应的响应时间，确保终端用户能够在有限的时间内得到响应，因此这两个功能的响应时间应该分别设置为2ms和1ms。响应时间的估算，可以通过类似的服务（比如bit.ly, qlink.me）来确定。

通过以上计算，可以列出与URL Shorten Service的性能指标，如下所示：

```bash
New URLs	                  200/s
URL redirections	          20K/s
Incoming data	              100KB/s
Outgoing data	              10MB/s
Storage for 5 years	          15TB
Memory for cache	          170GB
Generating URL response time  2ms
Redirecting URL response time 1ms
```

有了以上指标，接下来就需要围绕以上指标指定测试策略，选择相应的测试工具，准备测试数据，生成测试报告等。在进行日常的测试任务之前，需要对URL Shortening Service的构成有一定的了解。接下来需要对该服务进行拆分。

## URL Shortening Service的拆分
## 针对URL Shortening Service选择相应的测试工具
## 为URL Shortening Service制定测试策略
## 准备测试数据
## 生成测试报告

## 参考

[Designing a URL Shortening service like TinyURL](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR)