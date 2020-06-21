# DynamoDB的学习指南

如果你在软件行业（尤其是后端服务的研发）里从业几年，你肯定会听说过与存储和处理数据相关的几个时髦的技术词：NoSQL，大数据，云计算，ServerLess，ACID，CAP，分布式等等。驱动这些技术发展的原因是多样的，主要有以下几点：

* 互联网巨头（比如Google，Microsoft，Amazon，Facebook，LinkedIn，Netflix以及Twitter）需要面对体量庞大的数据和流量，这迫使它们创造新的工具来高效处理海量数据
* 需要更短的研发周期和更灵活的数据模型支撑更加敏捷，更加容易测试和及时响应市场的业务场景
* 开源软件的发展变得更加成熟，而且与商业软件相比，提供了更好的功能
* CPU的时钟频率很难提高，多核CPU已经逐渐成为标准，网络变得更快了（从原来的2G转变成为4G，到现在的5G）。这意味着并行计算的能力将会增强
* 得益于云计算服务的出现，即使你在一个小团队，也能打造一个分布式系统，甚至在不同的地理位置的不同机器上运行这套系统
* 许多数字化服务会一直处于7*24小时可用的状态，短暂的停机是无法接受的（比如Amazon短暂地停机会导致其商品买卖交易活动停滞，并引起经济损失）

因此，过去10年，为了应对大规模数据所带来的挑战，相应的工具和技术相继被提出。其中新型数据库系统（"**NoSQL**"）受到了很多关注，但是消息队列（message queues），缓存（caches），搜索引擎，数据流处理框架（Kafka和Samza）和其它分布式技术也相当重要！一个成熟的分布式系统一般会同时应用这些技术和工具。

以上提到的技术和工具都有对应的书籍介绍，而这个系列的文章（其列表如下）将聚焦在NoSQL数据库上，特别是AWS提供的DynamoDB。对于想要从事数据服务研发的工程师们，掌握NoSQL技能是必备的，因为它能够存储大规模数据（超过100TBs）的同时提供稳定的性能（数据操作的时间低于1ms），而要想在SQL数据库中拥有同样的能力，则需要付出巨大的代价，有时甚至无法实现！

NoSQL类型的数据库有很多，包括MongoDB，CouchDB和DynamoDB等。之所以使用DynamoDB的原因之一是它完全托管于AWS，开发者无需准备运行它的机器就能直接创建表。除此之外，DynamoDB还提供了永久的免费套餐。你想成为操作大规模数据的大师吗？如果答案是：Yes，那么你可以使用DynamoDB，并根据以下文章来实现这个目标！

## 介绍

* 1.1  [什么是DynamoDB？](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/what-is-dynamo-db.md)
* 1.2  [DynamoDB的关键概念](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)
* 1.3  [关于Dynamo的论文](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/the-dynamo-paper.md)
* 1.4  [DynamoDB的环境搭建](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/environment-setup.md)

## 单项数据操作

* 2.1  [DynamoDB中，每项数据（item）的构成单元](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)
* 2.2  [在DynamoDB中插入和读取数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)
* 2.3  [基础表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)
* 2.4  [更新和删除数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items.md)

## 多项数据操作

* 3.1  [同时处理多项数据](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/working-with-multiple-items.md)
* 3.2  [查询](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)
* 3.3  [遍历](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/scans.md)
* 3.4  [过滤](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)

## 高级功能

* 4.1  [附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)
* 4.2  [本地附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/local-secondary-indexes)
* 4.3  [全局附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/global-secondary-indexes.md)
* 4.4  [DynamoDB流](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/dynamodb-streams.md)

## 运维相关

* 5.1  Provisioning tables
* 5.2  安全
* 5.3  备份和恢复
* 5.4  自动伸缩
* 5.5  Global Tables

## 数据建模案例

* 6.1  概要
* 6.2  [层级结构的数据](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/hierarchical-data.md)
* 6.3  Leaderboard & Write Sharding

## ADDITIONAL CONCEPTS

* 7.1  如何选择索引类型？

## 数据库对比

* 8.1  MongoDB vs. DynamoDB

## 其它学习资源

* 9.1  [NoSQL的学习资料](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/additional-reading.md)
* 9.2  [原文链接](https://www.dynamodbguide.com)