# DynamoDB的全局附加索引

本文将介绍全局附加索引。与之前[介绍本地附加索引的文章](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/local-secondary-indexes)一样,我们将涉及全局附加索引的基础知识，然后通过一个例子来使用全局附加索引。

## 全局附加索引的基础知识

不像本地附加索引，你可以在具有简单主键或复合主键的表中添加全局附加索引。除此之外，你还可以创建具有简单主键的全局附加索引。

以下是列举了全局附加索引的不同之处：

* **拥有属于自己的读写单元**。当你创建全局附加索引时，你需要单独为该索引分配读写单元。这无疑会增加使用上的复杂程度以及更多的费用，但是同时也给你更加灵活的选择来处理不同模式的读写请求
* **Eventual consistency**。向表中写入一项数据时，这项数据是以异步的方式同步到全局附加索引的。这意味着，当你同时向表和全局附加索引读取同一数据时，其返回结果可能会不一样。而且使用全局附加索引只能选择该选项来同步数据，而无法选择strong consistency来同步数据
* **同一全局附加索引的分区键能够容纳无限数据**。而使用本地附加索引时，这一限制是10GB。
* **适用于任何表**。本地附加索引只能用于具有复合主键的表，而全局附加索引没有这个限制--你可以将其用于具有简单主键或复合主键的表
* **可以创建具有简单主键或者复合主键的全局附加索引**。

## 创建全局附加索引

类似本地附加索引，你可以在创建表的时候创建全局附加索引。然而，你也可以在已有的表上创建全局附加索引。如果在已有的表上创建全局附加索引，那么DynamoDB将自动把表中的数据同步到全局附加索引中。

以下示例展示了如何使用全局附加索引建立稀疏索引。稀疏索引的用途是存放一小部分常用的数据，以便提高更快的查找效率！只有那些包含稀疏索引主键的数据才会被同步到稀疏索引中。

假设有一个场景：跟踪用户退货的订单。我们将在这些订单中添加属性ReturnDate，然后将该属性作为稀疏索引的分区键，OrderId属性作为稀疏索引的排序键。

以下创建了该稀疏索引：

```bash
$ aws dynamodb update-table \
    --table-name UserOrdersTable \
    --attribute-definitions '[
      {
          "AttributeName": "ReturnDate",
          "AttributeType": "S"
      },
      {
          "AttributeName": "OrderId",
          "AttributeType": "S"
      }
    ]' \
    --global-secondary-index-updates '[
        {
            "Create": {
                "IndexName": "ReturnDateOrderIdIndex",
                "KeySchema": [
                    {
                        "AttributeName": "ReturnDate",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "OrderId",
                        "KeyType": "RANGE"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            }
        }
    ]' \
    $LOCAL
```

创建全局附加索引的方式类似于本地附加索引。注意：我只需要在`--attribute-definitions`中添加全局附加索引的属性，以及使用`--global-secondary-index-updates`选项来指定分区键或排序键。

## 基于全局附加索引查找数据

使用全局附加索引来查找数据与本地附加索引类似--你可以使用Query或Scan操作以及指定想要使用的全局附加索引。

在这个例子中，我们创建了一个稀疏索引，但是表中的任何数据都没有包含ReturnDate字段，因此该索引中不会包含任何数据，让我们执行以下Scan操作来验证这一结果：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    --index-name ReturnDateOrderIdIndex \
    $LOCAL
```

从该稀疏索引中返回的结果是空的，如下所示：

```bash
{
    "Count": 0,
    "Items": [],
    "ScannedCount": 0,
    "ConsumedCapacity": null
}
```

让我们使用BatchWriteItem接口来插入几条带有ReturnDate属性的数据，如下所示：

```bash
$ aws dynamodb batch-write-item \
    --request-items '{
        "UserOrdersTable": [
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20160630-12928"},
                        "Amount": {"N": "142.23"},
                        "ReturnDate": {"S": "20160705"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20170608-10171"},
                        "Amount": {"N": "18.95"},
                        "ReturnDate": {"S": "20170628"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20170609-25875"},
                        "Amount": {"N": "116.86"},
                        "ReturnDate": {"S": "20170628"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170609-18618"},
                        "Amount": {"N": "122.45"},
                        "ReturnDate": {"S": "20170615"}
                    }
                }
            }
        ]
    }' \
    $LOCAL
```

以上4条数据将覆盖掉之前的数据，让我们再次执行之前的Scan操作，如下所示：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    --index-name ReturnDateOrderIdIndex \
    $LOCAL
```

现在，我们从稀疏索引中读到了4项数据，如下所示：

```bash
{
    "Count": 4,
    "Items": [
        {
            "OrderId": {
                "S": "20160630-12928"
            },
            "Username": {
                "S": "alexdebrie"
            },
            "Amount": {
                "N": "142.23"
            },
            "ReturnDate": {
                "S": "20160705"
            }
        },
        {
            "OrderId": {
                "S": "20170609-18618"
            },
            "Username": {
                "S": "yosemitesam"
            },
            "Amount": {
                "N": "122.45"
            },
            "ReturnDate": {
                "S": "20170615"
            }
        },
        {
            "OrderId": {
                "S": "20170608-10171"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "18.95"
            },
            "ReturnDate": {
                "S": "20170628"
            }
        },
        {
            "OrderId": {
                "S": "20170609-25875"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "116.86"
            },
            "ReturnDate": {
                "S": "20170628"
            }
        }
    ],
    "ScannedCount": 4,
    "ConsumedCapacity": null
}
```

全局附加索引的用途很多，比如你可以在一小部分退还订单中查找所有昨天返回的订单，而不用在整张表中遍历所有订单。

这一章介绍了全局附加索引的基础知识，下一章的内容将介绍的[DynamoDB流概念](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/dynamodb-streams.md)。

* [原文链接](https://www.dynamodbguide.com/global-secondary-indexes)