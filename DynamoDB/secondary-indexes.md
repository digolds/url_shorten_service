# DynamoDB的附加索引

到目前为止，大部分的读操作主要是基于表的主键来执行的，要么通过[GetItem](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)或者[Query](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)完成。使用表的主键来查找数据项是非常高效的一种做法，同时也避免了使用[Scan](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/scans.md)来遍历整张表。

然而，使用主键会限制数据的查询模式。比如，在之前的查询示例中，我们将订单日期作为排序键，使得我们可以根据订单的日期来快速获取某个客户的所有订单。这就意味着我们无法根据订单量来快速获取某个客户的所有订单，因为订单量并不是主键属性。为了解决这个问题，我们可以使用[Filter](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)表达式来解决，但是这种办法并不高效，因为Filter是作用在返回的数据集上。那么有什么办法能让返回的数据集就是根据订单数量的大小来决定的？

幸运的是，DynamoDB有一个附加索引的功能，它允许开发者定义其它附加主键，而这些主键可以用于Query（查询）或Scan（遍历）操作。

本文将讨论2种类型的索引，以及使用附加索引的基本规则。

## 附加索引的类型有几种？

DynamoDB支持2类附加索引，它们分别是：[本地索引（local secondary indexs）](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/local-secondary-indexes.md)和[全局索引（global secondary indexes）](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/global-secondary-indexes.md)。

本地索引只能创建在具有[复合主键](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)的表之上，它的分区键与复合主键的分区键是一样的，但是却使用了不同的排序键。使用本地索引的一种场景是之前根据订单量来获取某客户的所有订单的示例。

全局索引能够创建与[表的主键](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)完全不一样的附加主键。比如：你可以在一张具有附加主键的表上使用全局索引来创建简单键，或者你也可以选择与主键完全不同的属性来创建附加的复合主键。当然，如果一张表只有一个简单主键，那么你依然可以使用全局索引来创建附加的复合主键。

附加索引是一个相当有用的功能，它能够衍生出更加高效且灵活的查询模式。

## 附加索引的基础知识

下面有一些关于附加索引的基础知识是需要知道的：

* **附加索引可以不唯一**。还记得吗？当我们插入数据时要求该数据的主键是必须唯一的，但是这一条限制不适用于附加索引。因此你可以创建2个具有相同附加索引的数据项（前提是其主键必须不一样）。
* **附加索引的不一定要提供**。当向表中插入数据时，你必须指定主键，而可以不需要提供附加索引的信息--如果你插入一项新的数据，该数据没有包含索引信息，那么该数据不会添加到索引里，这样的特性使索引变得更加稀疏，常常被称为稀疏索引。稀疏索引有其用武之地，比如建立一个索引搜集所有退货的商品。
* 每张表的**索引数量是有限制**的. 每张表最多能创建20个全局索引和5个本地索引

## 向附加索引中映射属性

当你创建附加索引的时候，你需要指定那些属性是需要映射到即将创建的附加索引。这么做的好处是：当一个基于附加索引的查询执行时，映射好的属性将直接返回，从而避免再次从主表中读取属性信息。

而映射的选项有：

* KEYS_ONLY: 仅映射表的主键信息，比如分区键和排序键以及对应的值
* ALL: 将表中完整的数据项映射到该索引
* INCLUDE: 选择若干属性映射到该索引

当你建立索引时，要结合查询模式来考虑。DynamoDB会根据索引所存储的数据量来收费，因此将完整的数据项映射将会使你的存储费用变成2倍。而另一方面，你还需要避免查询一次数据需要读取2次表格的情况（一次索引，另外一次是表）。

接下来，让我们进一步了解什么是本地索引。

* [原文链接](https://www.dynamodbguide.com/secondary-indexes)