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

以上发现是问题的关键 -- 90%的操作不会使用JOIN功能，而这一功能却是关系型数据库的核心。

JOIN操作非常消耗资源。当面对大规模的数据时，工程师通常会将数据复原为一个整体(拒绝使用第一范式)来避免使用JOIN操作而导致的高延时。 通过这种方式来降低响应延时的代价是增加了应用的复杂性--此时应用程序需要考虑数据的完整性而不是数据库本身。

Amazon.com的工程师已经采用了以上方法来降低延时。实际上，正是意识到亚马逊工程师所需的并不是关系型数据模型，才使得Dynamo设计师重新评估关系型数据库的其它方面。

**可用性比数据一致性更加重要**

大部分关系型数据库使用strongly consistent model来操作数据。简而言之，这种模式会使得所有客户端在同一时间能够获得相同的数据(想想这个场景:一个用户正在写数据，而多个用户正在读这个写的数据)。

让我们通过Twitter作为例子. 假设2:30PM，Bob在Virginia 发布了一条关于猫的信息。在信息发布之后，有2个用户查看了Bob发布的信息，他们分别是他的邻居Cheryl和住在新加坡的叔叔Jeffrey。如果Twitter使用strongly-consistent model，Cheryl和Jeffrey会看到Bob发布的关于猫的信息。

用这种方式来确保看到一致的信息不是最理想的，原因有以下几点:

首先，考虑地理位置的因素。Twitter选择一台数据库服务来实施strong consistency。该数据库服务位于Virginia，离Bob和Cheryl很近。这使得该服务的响应很快能到达Bob和Cheryl，但是到达Jeffrey所需的时间就变长了，因为猫的信息会跨越大西洋从Virginia到Singapore。从地理上来分析，Bob和Cheryl获取猫的信息所花的时间显然会比Jeffrey所需的时间短。这种只选择一台数据库服务来实施strong consistency model的结果是，一些用户，像Jeffrey，获取信息的时间会变得漫长起来。那么有什么方式能让这些用户获取信息的时间缩短?

抛弃只有一台数据服务的做法，Twitter可以选择2台数据库服务，每台数据库服务上的数据是相同的--其中一台放到Virginia另外一台放到Singapore。此时，如果我们依然需要实施strong consistency model， 那么就意味着同一个用户从以上2台数据库服务在同一时间获取同一份信息，其得到的数据是一样的。这也意味着Twitter需要在数据库服务上实现复杂的同步算法--在Bob发布的关于猫的信息提交到数据库之前，这些信息必须成功地提交到这2台数据服务上。此时，Bob的提交将往返于整个大西洋，最终导致用户的写操作变得更慢。

在Dynamo paper中，Amazon指出strong consistency在其业务场景中并不重要。具体应用到我们的例子中的场景是:Jeffrey与Cheryl在同一时间将看到不同的版本的关于猫的信息。数据库服务可以使用eventual consistency model来同步数据。也就是说最终不同用户会看到相同的信息。Jeffrey最终会看到Bob发布的关于猫的信息，而这条信息于2:32 PM传送到Singapore，即便是这条信息于2:30 PM传送到Virginia。

Strong consistency model对于某些场景相当重要-比如银行账户中的余额-但对于某些场景并不重要，比如Twitter示例或者Amazon的购物车系统。 去掉strong consistency model的使用而换成eventual consistency model大大促进了Dynamo的发展。对于Twitter示例或者Amazon的购物车系统这类业务场景，速度和可用性比同时获取相同数据更加重要。通过减弱关系型数据库的consistency model，Dynamo的工程师能够研发更加适合Amazon.com业务场景的数据库-也就是论文中提到的Dynamo。

注意: 这一节的内容简化了数据的一致性(consistency)，可用性(availability)，以及其它关于数据库和分布式系统的概念。你应该视其为初级知识而不是最终的解释。

**无限伸缩**

最后一个关键点是：Dynamo能够无限扩展，同时不会影响性能。使得Dynamo具有这种特性的原因在于：Dynamo避免使用关系型模型建模（比如剔除JOIN操作）以及避免使用strong consistency model（转而使用eventual consistency model）。

当扩充一个系统的处理能力时，要么通过**垂直扩充**（比如：使用处理能力更强（更多CPUs或内存（RAM））的服务器），要么通过**水平扩充**（比如：将整套数据分割成不同的数据子集，并将每部分数据子集分配到不同的机器上）。垂直扩充会导致高昂的费用，最终这种扩充会达到极限（比如无法添加更多的CPUs）。然而水平扩充不会导致高昂的费用，同时不会受到限制，其缺点是实现起来并不是一件容易的事情。

让我们通过一个例子来理解**水平扩充**。假设：你有一个装满用户信息的数据集，该数据集切割成3部分，并将每一部分存储在不同的机器上。此时，你制定了一个分布策略：根据用户姓氏来分配。比如A到H姓氏的数据存储在机器1，I到Q姓氏的数据存储在机器2，R到Z姓氏的数据存储在机器3。

如果我们只是获取某个用户的信息，这种分配策略是没问题的（因为响应时间很短）--比如：如果我们想获取Linda Duffy的信息，那么我们只需要发送一个请求到机器1。然而，如果你想从多台机器获取不同的数据，那么这种分配策略显然不适合这类查询模式（因为响应时间变长了）--比如：获取所有年龄超过18岁的用户信息。

同样，**水平扩充**也会因strong consistency model而受阻。比如：我将一整套数据复制到不同的机器，那么当我更新某台机器上的数据时，其它机器也需要同步这些修改。这就要求用户写入数据时，需要等待该数据成功同步到所有机器之后才能进行或许的操作，这无疑增加了响应延时。

为了支持水平扩充来提供稳定的性能，需要削弱Dynamo对上述阻力的依赖。为了无限存储数据，DynamoDB使用了[一致性hash算法](https://en.wikipedia.org/wiki/Consistent_hashing)来将数据均匀分布到不同的数据节点上。随着数据量增多，AWS能自动添加新的节点来存储新增的数据，并将部分且少量的数据从老节点挪动到新的节点上。

为了避免处理分布在不同机器上的数据，DynamoDB要求所有的读数据操作都必须通过主键来完成（而不是遍历整个数据集）。再来看看之前提到的关于存储用户数据的例子：该数据集的主键是用户的姓氏，DynamoDB会根据前面提到的一致性hash算法来均匀分布数据。如果想获取年龄超过18岁的用户信息，那么需要建立[附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)来重新映射原来的数据集，使得年龄超过18岁的用户集中在一台机器上，最终使得这类查询只需从一台机器上获取数据。

最后，由于DynamoDB采用了eventual consistency model，这种策略使得同步数据变得更加容易。你可以将数据复制到不同的机器上，然后从任意一台机器上查找数据，这样，获取同一份数据的吞吐量提高了（比如现在有3台机器提供相同的数据）。然后采用这种策略会使得不同时间点，3台机器上的数据会不一样，但在某一个时间点所有机器上的数据最终会保持一致。对于那些对数据一致性不高的应用场景，这种缺点依然可以接受。如果你无法接受这种缺陷，那么你依然可以为DynamoDB指定strongly-consistent model。

在DynamoDB中引入这些改变使得它面对无限（超过100TBs）的数据依然能提供1ms之内的查询延时。

准备好使用DynamoDB来处理100TBs以上的数据，同时期望其依然能够提供稳定的性能？请从[准备环境](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/environment-setup.md)开始，然后[对单条数据进行操作](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)。

## 参考

* [A Decade of Dynamo](http://www.allthingsdistributed.com/2017/10/a-decade-of-dynamo.html) post on Werner Vogel's blog
* [Dynamo: Amazon's Highly Available Key-value Store](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
* [CAP Theorum](https://en.wikipedia.org/wiki/CAP_theorem)
* [Amazon Takes Another Pass at NoSQL with DynamoDB](http://readwrite.com/2012/01/18/amazon-enters-the-nosql-market/)
* [原文链接](https://www.dynamodbguide.com/the-dynamo-paper)