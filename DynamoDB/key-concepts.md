# DynamoDB的关键概念

在这一章，我们将讨论关于DynamoDB的关键概念。完成这一章的学习之后，你将对以下概念有进一步的认识：

* 表（tables），数据项（items）和每项数据的属性（attributes）
* 主键（primary keys），有简单主键（Partition Key）和复合主键（Partition Key + Sort Key）
* 附加索引（secondary indexes）
* DynamoDB的读写能力


## 表（tables），数据项（items）和每项数据的属性（attributes）

表（tables），数据项（items）和每项数据的属性（attributes）是DynamoDB的基础构建单元。

*表*是数据项的集合，不同类型的数据项都可以放到一张*表*里。例如：有一张*Users*表，该表存储了*每一个用户*的信息；有一张*Orders*表，该表存储了用户的所有订单信息。*表*的概念有点类似于关系型数据库中的*表*或MongoDB中的集合，与它们不同的是，DynamoDB中的表经常会存储不同类型的数据，比如用户信息以及该用户的所有订单信息会存储在**同一张表中**。

*每条数据*在表里就是一条记录（包含了多个属性（Attributes））。在表里，每条数据由主键（Primary Key）唯一确定。比如在Users表中，一条数据对应一个用户，这条数据包括了用户名，性别和住址等用户相关的信息。每条数据类似于关系型数据库表中的某一行或者MongoDB中的一个文档数据。

*数据的属性*组合成了每条数据，每条数据由多个数据属性构成。比如：一条用户数据包含了年龄属性，该属性存储了该用户的年龄。属性类似于关系型数据库表中的列或MongoDB中的属性。DynamoDB要求每一项数据都至少包含构成该数据主键的属性。

## 主键（Primary Key）

表中的每项数据由主键唯一标识。在创建表的时候，必须定义由哪些属性构成主键，当向表中新添数据的时候，该数据至少需要包含主键信息。

主键的类型有2类：**简单主键**和**复合主键**。前者仅由分区键（Partition Key）构成，而后者由分区键（Partiti Key）和排序键（Sort Key）组成。

简单主键类似于Memcached中的Key和SQL表中的主键。比如：用户名可以作为表*Users*的简单主键。

复合主键则更加复杂。你需要为表中的每一条数据提供分区键和排序键。排序键的作用在于使得同一分区的数据按照排序键的值进行排序。例如：某个用户的所有订单拥有相同的分区键（如：用户名），但每个订单的排序键（如：订单编号）是不相同的。

这里需要提醒的是：表中的每条数据是由主键唯一标识的。当使用复合主键来标识数据时，不同的数据可以拥有相同的分区键，此时，这些数据必须使用不同的排序键。由相同的分区键和不同的排序键构成的主键唯一标识了表中每一条数据。

复合主键可以支持复杂的[数据查询模式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/working-with-multiple-items.md)。这些查询模式有：根据分区键来获取表中的数据；使用排序键来缩小查询范围。

读者可以根据[拆解数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)来理解数据项的基本构成。

## 附加索引（Secondary Index）

主键唯一标识了表中的每一项数据，根据主键可以从表中获取到对应的数据项。然而有的时候，你需要根据其它模式来获取数据，比如你想查询订单金额超过某个范围的订单，而此时该表的Partition Key和Sort Key分别是用户名和订单号。使用该表的复合主键来满足这种查询显然是低效的，因此这个时候需要借助DynamoDB的**附件索引**来满足这一查询模式。附加索引有2种：local secondary index和global secondary index。

**local secondary index**使用了与表相同的分区键但是不同的排序键来构成索引。假设有一张Orders表，你想读取某个用户的所有订单，这些订单需要以订购数量（Amount）进行降序排序。此时，你只需要为Orders表创建一个local secondary index，该索引的分区键是用户ID（CustomerId），排序键是订单的订购数量（Amount）。开发者使用这个索引就能高效地获取某个用户的订单，并按照订单的数量进行排序。

**global secondary index**使用了与表完全不同的分区键和排序键来构成索引。你可以选择其它属性（不包含表的分区键）作为索引的分区键，从而构成该索引的简单主键，当然你也可以选择2个属性来构成索引的主键。假设有一张表，我们可以在这张表上定义一个global secondary index，该索引的分区键是订单号（OrderID），而排序键可以不设置，从而构成一个简单的主键。接着我们可以通过这个索引来根据订单号高效获取某个具体的订单，而无需通过查找用户和用户名下的订单这种低效的方式来查找。

附加索引是一个异常复杂的话题，但是这个功能却非常实用。它是实现不同查询模式的基础，想要深入了解和应用附件索引，读者可以前往[这里](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)。

## 读和写单元

当你使用MySQL，Postgres和MongoDB的时候，你需要启动一个服务器来运行这些数据库实例。你必须为这个服务器配置CPU，内存以及磁盘存储等。

而使用DynamoDB时，你不需要自己启动这些服务器，你只需要为创建的表指定读和写的单元，AWS就能自动地帮你启动服务器，并根据这些读写单元来启动服务器。这些读写单元限制了读写数据的吞吐量（KB/S），越多的读写单元其吞吐量会越大。与自己启动服务器来运行数据库实例的方式相比，这种方式的计费模式更加贴近真实的使用费用。

DynamoDB也能够自动增加和减少表的读写单元。这使得在数据使用的高峰期时，读写单元会自动增多，而在低峰期时，该读写单元会自动减少。通过这种根据实际使用情况来为表动态分配读写单元的方式能够减少支出。

## 下一步学习计划

如果你对DynamoDB的内部实现感兴趣，不妨去看看[Dynamo Paper](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/the-dynamo-paper.md)。如果不感兴趣，那么可以从[搭建DynamoDB的环境](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/environment-setup.md)开始，接着阅读[对单条数据进行操作](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)中的内容来理解数据的基本构成。