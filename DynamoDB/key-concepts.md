# DynamoDB的关键概念

在这一章，我们将讨论关于DynamoDB的关键概念。完成这一章的学习之后，你将对以下概念有进一步的认识：

* 表（tables），数据项（items）和每项数据的属性（attributes）
* 主键（primary keys），有简单主键（Partition Key）和复合主键（Partition Key + Sort Key）
* 附加索引（secondary indexes）
* DynamoDB的读写能力


## 表（tables），数据项（items）和每项数据的属性（attributes）

表（tables），数据项（items）和每项数据的属性（attributes）是DynamoDB的基础构建单元。

*表*是数据项的集合，不同类型的数据项都可以放到一张*表*里。例如：有一张*Users*表，该表存储了*每一个用户*的信息；有一张*Orders*表，该表存储了用户的所有订单信息。*表*的概念有点类似于关系型数据库中的*表*或MongoDB中的集合，与它们不同的是，DynamoDB中的表经常会存储不同类型的数据，比如用户信息以及该用户的所有订单信息会存储在**同一张表中**。

An *item* is a single data record in a table. Each item in a table is uniquely identified by the stated primary key of the table. In your Users table, an item would be a particular User. An item is similar to a row in a relational database or a document in MongoDB.

*Attributes* are pieces of data attached to a single item. This could be a simple Age attribute that stores the age of a user. An attribute is comparable to a column in a relational database or a field in MongoDB. DynamoDB does not require attributes on items except for attributes that make up your primary key.

Primary Key
Each item in a table is uniquely identified by a primary key. The primary key definition must be defined at the creation of the table, and the primary key must be provided when inserting a new item.

There are two types of primary key: a simple primary key made up of just a partition key, and a composite primary key made up of a partition key and a sort key.

Using a simple primary key is similar to standard key-value stores like Memcached or accessing rows in a SQL table by a primary key. One example would be a Users table with a Username primary key.

The composite primary key is more complex. With a composite primary key, you specify both a partition key and a sort key. The sort key is used to (wait for it) sort items with the same partition. One example could be an Orders tables for recording customer orders on an e-commerce site. The partition key would be the CustomerId, and the sort key would be the OrderId.

Remember: each item in a table is uniquely identified by a primary key, even with the composite key. When using a table with a composite primary key, you may have multiple items with the same partition key but different sort keys. You can only have one item with a particular combination of partition key and sort key.

The composite primary key enables sophisticated query patterns, including grabbing all items with the given partition key or using the sort key to narrow the relevant items for a particular query.

For more on interacting with items, start with the lesson on the anatomy of an item.

Secondary Indexes
The primary key uniquely identifies an item in a table, and you may make queries against the table using the primary key. However, sometimes you have additional access patterns that would be inefficient with your primary key. DynamoDB has the notion of secondary indexes to enable these additional access patterns.

The first kind of secondary index is a local secondary index. A local secondary index uses the same partition key as the underlying table but a different sort key. To take our Order table example from the previous section, imagine you wanted to quickly access a customer's orders in descending order of the amount they spent on the order. You could add a local secondary index with a partition key of CustomerId and a sort key of Amount, allowing for efficient queries on a customer's orders by amount.

The second kind of secondary index is a global secondary index. A global secondary index can define an entirely different primary key for a table. This could mean setting an index with just a partition key for a table with a composite primary key. It could also mean using completely different attributes to populate a partition key and sort key. With the Order example above, we could have a global secondary index with a partition key of OrderId so we could retrieve a particular order without knowing the CustomerId that placed the order.

Secondary indexes are a complex topic but are extremely useful in getting the most out of DynamoDB. Check out the section on secondary indexes for a deeper dive.

Read and Write Capacity
When you use a database like MySQL, Postgres, or MongoDB, you provision a particular server to run your database. You'll need to choose your instance size -- how many CPUs do you need, how much RAM, how many GBs of storage, etc.

Not so with DynamoDB. Instead, you provision read and write capacity units. These units allow a given number of operations per second. This is a fundamentally different pricing paradigm than the instance-based world -- pricing can more closely reflect actual usage.

DynamoDB also has autoscaling of your read and write capacity units. This makes it much easier to scale your application up during peak times while saving money by scaling down when your users are asleep.

Next steps
If you really want the nitty-gritty fundamentals of DynamoDB, go to the section on the Dynamo Paper. Otherwise, get your environment set up and then start the walkthrough with single-item actions.