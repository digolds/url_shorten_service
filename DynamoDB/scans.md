# 在DynamoDB中，谨慎使用Scans操作

本文将介绍DynamoDB的Scans操作。该操作是DynamoDB的重型武器。做一个相似的对比: [GetItem](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)操作就是是一对镊子，可以夹出某个特定的物件。[Query](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)操作像把铁铲，能挖出一大堆物件，但是其作用的范围依旧很小。然而，Scan操作就像一辆拖拉机，把整个修整区域翻个底朝天。

![](https://user-images.githubusercontent.com/6509926/34457385-d95c9ff2-ed74-11e7-86e0-bbf191325502.jpg)

在我们深入到Scan操作之前，请记住以下这句话:

> 不要使用Scan操作，除非你知道自己在做什么。

Scan操作作用于整张表。对数据量庞大的表，该操作将耗尽整张表的读取单元。如果你在应用程序里的关键路径里使用它，那么它会增加响应延时。

只有在以下情况下，才会考虑使用Scan操作:

* 表的数据量不大
* 将数据迁移到另外一个数据库系统 
* you use global secondary indexes in a special way to set up a work queue (very advanced).

带着以上告诫，让我们来探索Scan操作的使用方式。

## Scan操作的基础知识

Scan操作是DynamoDB中最容易使用的功能。开发者只需要在执行该操作时提供表的名字，它就能帮你返回表格中所有数据项（返回的数据量不超过1MB）：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    $LOCAL
```

以下是返回结果（为了方便阅读，其中省略了中间部分）：

```bash
{
    "Count": 25,
    "Items": [
        {
            "OrderId": {
                "S": "20160630-28176"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "88.3"
            }
        },
        ...
        {
            "OrderId": {
                "S": "20171129-28042"
            },
            "Username": {
                "S": "alexdebrie"
            },
            "Amount": {
                "N": "83.12"
            }
        }
    ],
    "ScannedCount": 25,
    "ConsumedCapacity": null
}
```

正如你期待的那样，以上结果显示了表中所有数据项。

与[GetItem](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)和[Query](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)操作类似，你可以在Scan操作时添加`--projection-expression`选项来指定返回特定的属性集。这里将不做演示，留给读者自行完成。

DynamoDB对一次请求所返回的数据量有最多1MB的限制。Scans操作经常会导致返回的数据量超过1MB，这就意味着需要通过分页机制来获取表中所有数据项。而这种分页机制是通过返回结果中"NextToken"来完成的。你只需要在调用Scans操作时添加`--starting-token`选项和"NextToken"来获取下一页的数据。

当然，在试验DynamoDB的Scans操作时，由于数据量并不会很大，因此为了测试这种行为，你可以使用`--max-items`选项来限制其返回数量。例如我们将该选项的值设置为1，如下所示：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    --max-items 1 \
    $LOCAL
```

返回的结果只包含了一项数据，除此之外还包含了"NextToken":

```bash
{
    "Count": 25,
    "Items": [
        {
            "OrderId": {
                "S": "20160630-28176"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "88.3"
            }
        }
    ],
    "NextToken": "eyJFeGNsdXNpdmVTdGFydEtleSI6IG51bGwsICJib3RvX3RydW5jYXRlX2Ftb3VudCI6IDF9",
    "ScannedCount": 25,
    "ConsumedCapacity": null
}
```

## 并发执行Scans

Scan的一种使用场景是将数据导出到冷数据存储系统（冷数据系统是指读操作特别频繁但是写入操作很少的数据库系统）以便分析。然而，如果表中有大量数据（比如超过100TBs），那么执行Scan操作来读取表中的所有数据所需的时间会较长。为了缩短导出时间，DynamoDB的Scan操作有一种Segments的概念，它允许并发执行Scans操作。当你想让Scan操作并发执行，那么你需要指定需要将表分成几段，这个Scan操作作用在哪段。Segments的索引是从0开始的，比如你将表分成了3端，那么0，1，2分别是这3端的编号。开发者可以启动多个线程或进程来并发导出数据。

即便是我们练习的表中数据量不大，但是我们依然可以测试这种行为。例如：我们可以将表分成3段，并启动一个进程来Scan分段编号为1的数据，如下所示：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    --total-segments 3 \
    --segment 1 \
    $LOCAL
```

从以下的结果可知，其返回了11项数据，而不是25项：

```bash
{
    "Count": 11,
    "Items": [
        {
            "OrderId": {
                "S": "20160630-28176"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "88.3"
            }
        },
        ...
        {
            "OrderId": {
                "S": "20170609-9476"
            },
            "Username": {
                "S": "yosemitesam"
            },
            "Amount": {
                "N": "19.41"
            }
        }
    ],
    "ScannedCount": 11,
    "ConsumedCapacity": null
}
```
在下一篇文章里，我们将学习DynamoDB的[Filter](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)功能，以及将其与Query和Scan操作结合在一起使用。

* [原文链接](https://www.dynamodbguide.com/scans)