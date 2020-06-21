# 在DynamoDB中使用Filter表达式

在过去的几篇文章里，我们讨论了[关键字表达式，条件表达式，映射表达式以及更新表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)。本文将讨论最后一类表达式--过滤器表达式。

过滤器表达式用于[Query](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)和[Scan](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/scans.md)操作，它在作用于这些操作所返回的数据集，并过滤出满足条件的数据项，进而返回给客户端。在深入了解Filter之前，我们有必要来了解一下Query或Scan底层的执行过程。

## Query和Scan的执行过程

对于DynamoDB的Query和Scan操作，有3步是需要DynamoDB来完成的：

1. 从表中查找数据。对于这2类操作，查询将从Starting Token开始，如果在Query中提供了关键字表达式，那么查询的过程中将考虑这类关键字
2. （这一步是可选的），如果在查询（Query）或遍历（Query）的过程中使用了Filter，那么这个Filter将作用于第一步返回的数据集。同理，映射表达式也是在这一步作用于第一步返回的数据集。
3. 把数据返回给客户端

有一点需要特别注意的是：DynamoDB对返回数据量的限制是由第一步来决定的。比如，如果你在第一步获取100KB的数据，而在第二步使用过滤器将数据量缩减到10KB，那么DynamoDB依然会按照100KB来计算其最终的返回数据量。还需要注意的是：DynamoDB中的任何操作其处理数据的量不能超过1MB，尽管你正在操作的表有充足的读单元。

过滤表达式和映射表达式不是一个高性能的利器-它们不会使你的查询效率变高，然而，它们能帮助你减少数据量，从而最终减少传输带宽的使用。不仅如此，你可以将这些过滤操作逻辑从业务层转移到数据库层。

> 关于更多Filter以及什么时候使用它的知识可以参考这篇文章[When to use (and when not to use) DynamoDB Filter Expressions](https://www.alexdebrie.com/posts/dynamodb-filter-expressions/)。

## 如何使用Filter

Filter表达式与关键字表达式类似，都可以和Query操作配合--你只需要在过滤表达式中指定想要过滤的属性，查询结果就会更具该表达式来过滤。

让我们基于之前Query来查找用户"daffyduck"的订单。这一次我们想依据订单额度来过滤数据，比如我们只想返回订单量超过100美元的订单，示例如下：

```bash
$ aws dynamodb query \
    --table-name UserOrdersTable \
    --key-condition-expression "Username = :username" \
    --filter-expression "Amount > :amount" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" },
        ":amount": { "N": "100" }
    }' \
    $LOCAL
```

以下的返回结果只返回了一个订单：

```bash
{
    "Count": 1,
    "Items": [
        {
            "OrderId": {
                "S": "20170609-25875"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "116.86"
            }
        }
    ],
    "ScannedCount": 4,
    "ConsumedCapacity": null
}
```

需要注意一点：上面的返回结果包括了"ScannedCount"和"Count"。前者的含义是：DynamoDB帮你查到了一些数据集，数量是4，而后者是指满足过滤条件的数据项有1项，并返回给客户端。

在之前的示例中，你会发现这2者的数值是一样的，那是因为我们没有使用Filter。当加上Filter之后，我们可看到DynamoDB依然会根据主键查找数据，然后在这些数据（4项）的基础上根据过滤表达式来过滤数据（1项）。此时，我们依然消耗4项数据的所对应的读单元，虽然最终返回给客户端的数据量是1项。

最后一点需要注意的是：不能在Filter表达式中使用主键属性。这是合理的，因为你已经可以使用关键字表达式来查询数据了，为什么还需要在Filter表达式中将主键属性指定为过滤条件呢！然而这个限制不适用于Scan操作--也就是说，你依然可以在过滤表达式中使用主键属性。

这篇文章将是最后一篇关于如何同时操作多项数据的。在接下来的章节里，我们将学习更多高级的功能比如[附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)和DynamoDB的流。

* [原文链接](https://www.dynamodbguide.com/filtering)