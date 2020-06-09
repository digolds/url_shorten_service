# 关于Dynamo的论文

在2004这一年，Amazon.com的增长速度很快，最终其Oracle上的数据规模达到极限，限制了其业务的发展。为了摆脱这种限制，Amazon开始考虑建立他们自己的数据库（注意：在公司内部搭建一个数据库系统是非常糟糕的想法）。在研发自家的数据库之后，亚马逊的工程师创建了创造了**Amazon Dynamo**数据库，这个数据库支撑了大部分Amazon.com业务，包括其购物车。

那些研发Amazon Dynamo数据库背后的工程师于2007年发布了关于[Dynamo的论文](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)。这篇论文描述了这群工程师在搭建高可用，key-value存储过程中为了满足Amazon.com业务场景所学到的经验。

这篇论文影响深远，并催生一大批NoSQL的解决方案，这些解决方案包括Apache Cassandra(最初由Facebook研发)和AWS提供的 SimpleDB以及DynamoDB（注意AWS团队和Amazon团队是2拨不同的团队，2者互不关联）。2012年，Amazon Web Services对外发布了DynamoDB，该服务借鉴了Dynamo的经验和原则，且完全托管在AWS上。


> 想要了解为何DynamoDB存储100 TBs以上的数据，却依然能保持稳定的性能? 请参考这篇文章 [SQL, NoSQL, and Scale: How DynamoDB scales where relational databases don't](https://www.alexdebrie.com/posts/dynamodb-no-bad-queries/)。

## Dynamo的几个关键点

**非关系型数据模型**

关系型数据模型可以用来为不同类型的数据建模（比如针对一个电商的用户和订单来建模）。通常，使用关系型数据建模的方式为数据建模，需要将关联的数据拆分成更小的数据单元，以便这些数据是不重复的，这就是关系型数据库中著名的**第一范式**。其做法是，如果某类实体数据想要使用另外一类实体数据（比如将订单和用户关联），那么只需要将2类不同的实体数据存储在不同的表格，然后通过外键的方式来关联这2类数据以及通过**JOIN**操作来拼接和获取这2类数据。此时，你只需要修改某个实体（比如某个用户的用户名），那么另一个数据实体（比如订单所属的用户名也发生了变化）所引用的数据也会因此而变化。

然而，Amazon.com工程师在收集数据库需求时发现了一个非常有趣的结果：

>大约70%对数据库的操作是key-value类型，这些操作仅仅使用主键来获取单条数据。大约20%的操作会返回一个数据集，但是这些数据集均来自于同一张表。
>
>-- Werner Vogels, [A Decade of Dynamo](http://www.allthingsdistributed.com/2017/10/a-decade-of-dynamo.html)

This is a huge deal -- 90% of operations weren't using the JOIN functionality that is core to a relational database!

The JOIN operation is expensive. At a large enough scale, engineers often denormalize their data to avoid making expensive joins and slowing down response times. This decrease in response time comes with a trade-off of increased application complexity -- now you need to manage more of your data integrity issues in your code rather than your database.

Amazon.com engineers were already making that trade-off of denormalization to improve response times. The realization that the relational model wasn't needed by Amazon engineers allowed the Dynamo designers to re-evaluate other aspects of a relational database.

**可用性比数据一致性更加重要**

Most relational databases use a strongly consistent model for their data. Briefly, this means all clients of the server will see the same data if querying at the same time.

Let's use Twitter as an example. Imagine that Bob in Virginia tweets a cat picture at 2:30 PM. There are two users that view Bob's profile after he tweets his picture: his neighbor, Cheryl, and his uncle, Jeffrey, who lives in Singapore. If Twitter were using a strongly-consistent model, both Cheryl and Jeffrey should see Bob's most recent tweet as soon as it's committed to the database from Bob's action.

This might not be ideal, for a few reasons. First, think of the geography involved in this scenario. Twitter could choose to have a single database instance to enable this strong consistency. This database instance may be located in Virginia, close to Bob and Cheryl. This results in fast responses to Bob and Cheryl, but very slow responses to Jeffrey as each request must cross an ocean from Singapore to Virginia to request the data, then return from Virginia to Singapore to return it to Jeffrey. This results in slower read times to some users.

Instead of maintaining a single database instance, perhaps Twitter wants to have two instances that are exact replicas -- one in Virginia and one in Singapore. If we still want to maintain strong consistency, this means a user must get the same answer if she queries the Virginia instance or the Singapore instance at the same time. This could be implemented by a more complex system on database writes -- before Bob's tweet is committed to the database, it has to be submitted to both the Virginia instance and the Singapore instance. Now Bob's request needs to make the hop across the ocean and back. This results in slower write times to some users.

In the Dynamo paper, Amazon noted that strong consistency isn't important in all scenarios. In our example, it would be fine if Jeffrey and Cheryl saw slightly different versions of my profile even if they queried at the same time. Sometimes you can settle for eventual consistency, meaning different users will eventually see the same view of the data. Jeffrey will eventually see Bob's tweet in Singapore, but it may be at 2:32 PM rather than 2:30.

Strong consistency is important for certain use cases - think bank account balances - but less important for others, such as our Twitter example or the Amazon shopping cart, which was the impetus for Dynamo. For these use cases, speed and availability are more important than a consistent view of the world. By weakening the consistency model of a relational database, the Dynamo engineers were able to provide a database that better fit the needs of Amazon.com.

Note: This section is a massive simplification of consistency, availability, and other concepts around databases and distributed systems. You should really look at this as a very simple primer rather than a definitive text.

**无限伸缩**

The final key aspect of Dynamo is that it is infinitely scalable without any negative performance impacts. This aspect is a result of the relaxing of relational and consistency constraints from prior databases.

When scaling out a system, you can either vertically scale (use a larger server instance with more CPUs or RAM) or you can horizontally scale by splitting your data across multiple machines, each of which has a subset of your full dataset. Vertical scaling gets expensive and eventually hits limits based on available technology. Horizontal scaling is cheaper but more difficult to achieve.

To think about horizontal scaling, imagine you have a dataset of Users that you want to distribute across three machines. You could choose to split them across machines based on the last name of the Users -- A through H go on machine 1, I through Q go on machine 2, and R through Z go on machine 3.

This is nice if you're getting a single User -- a call to retrieve Linda Duffy can go directly to machine 1 -- but can be slow if your query spans multiple machines. A query to get all users older than 18 will have to hit all three machines, resulting in slower responses.

Similarly, we saw in the previous section how strong consistency requirements can make it difficult to scale out. We would introduce latency during writes to make sure the write is committed to all nodes before returning to the writing user.

Relaxing these requirements makes it much easier for Dynamo to scale horizontally without sacrificing performance. DynamoDB uses consistent hashing to spread items across a number of nodes. As the amount of data in your DynamoDB table increases, AWS can add additional nodes behind the scenes to handle this data.

DynamoDB avoids the multiple-machine problem by essentially requiring that all read operations use the primary key (other than Scans). From our Users example before, our primary key could be LastName, and Amazon would distribute the data accordingly. If you do need to query via Age, you would use a secondary index to apply the same distribution strategy via a different key.

Finally, because DynamoDB allows for eventual consistency, it allows for easier replication strategies of your data. You can have your item copied onto three different machines and query any of them for increased throughput. It's possible one of the machines has a slightly different view of the item at different times due to the eventual consistency model, but this is a trade-off worth accepting for many use cases. Also, you may explicitly specify a strongly-consistent read if it is required for your application.

These changes make it possible for DynamoDB to provide query latencies in single-digit milliseconds for virtually unlimited amounts of data -- 100TB+.

Ready to dig in? Set up your environment then get started with some operations.

## 参考

* [A Decade of Dynamo](http://www.allthingsdistributed.com/2017/10/a-decade-of-dynamo.html) post on Werner Vogel's blog
* [Dynamo: Amazon's Highly Available Key-value Store](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
* [CAP Theorum](https://en.wikipedia.org/wiki/CAP_theorem)
* [Amazon Takes Another Pass at NoSQL with DynamoDB](http://readwrite.com/2012/01/18/amazon-enters-the-nosql-market/)