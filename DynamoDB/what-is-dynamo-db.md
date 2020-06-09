# 什么是DynamoDB？

[DynamoDB](https://aws.amazon.com/dynamodb/)是一个由AWS提供的NoSQL数据库。它具有以下特点：

* 随着数据量的剧增，它依然能够提供稳定的性能输出
* 它完全由AWS管理。开发人员不需要SSH到其服务器，不需要管理服务器，不需在服务器上更新OS补丁和加密库等
* 它提供了简单的API，这些API能够对数据进行增删改查，除此之外，开发者也能根据获取数据的场景来定义查询模式

DynamoDB适用于以下场景：

**需存储大量数据同时要求低延迟的应用服务**。随着应用服务的数据量增多，JOINs和高级的SQL操作会大大降低关系型数据库的性能，从而导致应用服务的性能变差。如果使用DynamoDB, 对任何数据量（即使超过100 TBs）的查询操作，其延时也能够确定在某个具体的范围。

**AWS Serverless服务**。AWS Lambda服务提供了能自动弹性伸缩，无状态且短暂的计算能力。开发者只需要定义事件就能触发并应用这些计算能力。DynamoDB对外提供了HTTP API，开发者可以通过HTTP API来操作DynamoDB。开发者可以使用IAM roles来为DynamoDB进行认证(你是谁)和授权(你拥有哪些权限，比如读或者读写某张表)。这些特性使得DynamoDB特别适用于Serverless服务。

**对数据具有确定且简单的访问模式(比如根据国家来获取所有星巴克的门店)**。如果你编写了一个推荐系统，并根据用户的偏好来推荐物品，那么把DynamoDB作为数据基础，能够为推荐系统提供更快且性能稳定的key-value访问模式。

## 准备好学习更多关于DynamoDB的知识？

这个系列的文章将以一些[关键的概念](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)开始，学习tables，items以及关于DynamoDB的其它组成部分。如果你急于了解DynamoDB背后所应用的计算机科学理论，那么可以参考[Dynamo Paper](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/the-dynamo-paper.md)。

如果你只是想动手练练，那么可以从[准备环境](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/environment-setup.md)以及[对单条数据进行操作](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)开始。紧接着，你可以通过学习[对多条数据进行操作](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/working-with-multiple-items.md)来掌握DynamoDB的Queries和Scans功能。

以上只是一些基础知识，想要了解更多的高阶知识，可以参考[secondary indexes](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)和[DynamoDB Streams](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/dynamodb-streams.md)。

如果想要获得更多关于DynamoDB的学习资料，那么[这里](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/additional-reading.md)将是一个不错的地方。

[原文链接](https://www.dynamodbguide.com/what-is-dynamo-db)