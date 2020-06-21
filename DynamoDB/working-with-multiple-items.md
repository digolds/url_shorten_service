# 如何在DynamoDB中同时操作多项数据

在过去的章节里，我们一次只能操作一项数据--比如[插入，查找](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)，[更新以及删除单项数据](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items.md)。而在这篇文章里，我们将一次同时操作多项数据。从这章开始，我们将创建一张具有复合主键的表，并在该表中同时操作多项数据。

[复合主键](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)对于DynamoDB而言非常有用。它允许你通过一个查询操作就能获取一组相关的数据项，除此之外，它还有其它强大的用途。

本文将创建一张具有复合主键的表。然后我们将使用BatchWriteItem API来批量生成多项数据。后续的几篇文章将使用[Query](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)和[Scan](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/scans.md) API作用到这些数据。

## 创建表

创建一张具有复合主键的表[与创建一张具有简单主键的表](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)类似，都需要定义属性和key schema。不同的是，你需要指定2个属性构成复合主键，而不是1个。 然后你需要指定其中一个属性是分区键，另外一个属性是排序键。

分区键决定了你的数据是如何划分的，而排序键则决定了具有相同分期键的数据项是有序的。分区键尤其重要-当使用Query操作时，你只能使用分区键。分区键与排序键组合在一起可以建立一对多的数据模型-因为一个相同的分区键下，可以有多个不同的排序键。

每当需要基于复合主键来对数据建模时，可以根据以下句子来填写空格处，最终构建正确的查询模式：

> "Give me all of the ____ from a particular ___."

放入第一个空格的属性应该是排序键，而放到最后一个空格的属性则是分区键。在以下示例中，我们将创建一张即包含User类型数据，同时也会包含Order类型数据的表："UserOrdersTable"，其中每个User可以包含多个Orders。按照以上句子来构建查询模型，其最终的结果是："返回该Username的所有OrderIds"。基于这句话，可以得出：Username是分区键，而OrderId则是排序键。

为了创建"UserOrdersTable"，需要使用CreateTable API：

```bash
$ aws dynamodb create-table \
    --table-name UserOrdersTable \
    --attribute-definitions '[
      {
          "AttributeName": "Username",
          "AttributeType": "S"
      },
      {
          "AttributeName": "OrderId",
          "AttributeType": "S"
      }
    ]' \
    --key-schema '[
      {
          "AttributeName": "Username",
          "KeyType": "HASH"
      },
      {
          "AttributeName": "OrderId",
          "KeyType": "RANGE"
      }
    ]' \
    --provisioned-throughput '{
      "ReadCapacityUnits": 1,
      "WriteCapacityUnits": 1
    }' \
    $LOCAL
```

返回的结果如下所示：

```bash
{
    "TableDescription": {
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/UserOrdersTable",
        "AttributeDefinitions": [
            {
                "AttributeName": "Username",
                "AttributeType": "S"
            },
            {
                "AttributeName": "OrderId",
                "AttributeType": "S"
            }
        ],
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0,
            "WriteCapacityUnits": 1,
            "LastIncreaseDateTime": 0.0,
            "ReadCapacityUnits": 1,
            "LastDecreaseDateTime": 0.0
        },
        "TableSizeBytes": 0,
        "TableName": "UserOrdersTable",
        "TableStatus": "ACTIVE",
        "KeySchema": [
            {
                "KeyType": "HASH",
                "AttributeName": "Username"
            },
            {
                "KeyType": "RANGE",
                "AttributeName": "OrderId"
            }
        ],
        "ItemCount": 0,
        "CreationDateTime": 1514657981.297
    }
}
```

这有点类似我们之前创建的"UsersTable"，只不过，这次我们还添加了分区键"OrderId"。

## 批量写入多项数据

到目前为止，我们已经创建了表"UserOrdersTable"。为了同时操作多项数据，接下来我们将向该表写入多项数据。有一种批量写入多项数据的方式是借助BatchWriteItem API。这个API能让你在一次请求中最多同时插入或者删除25项数据。借助这个API，你甚至能在同一请求中操作不同的表。

然而使用BatchWriteAPI会有一些限制。首先，你无法在其中使用UpdateItem API，因为UpdateItem只能单独使用。其次，你无法使用条件表达式。

当执行批量操作时，失败的结果有2种。其中一种是：非法参数导致整个操作失败的错误。比如试图向一张不存在的表中插入数据，试图写入超过25项数据或者写入的数据量超过了限制。

另外一种：一项或多项数据的插入是失败的。 这是一种比较常见的错误，比如你的操作超出了表的写入限制或AWS内部的错误。如果时这种错误，那么返回的结果将返回那些没有执行成功的数据项，而这些数据项将放置在"UnprocessedItems"字段中。

下面这个示例展示了BatchWriteItem的用法，它将向"UserOrdersTable"中插入25项数据。每项数据不仅有"Username"属性，还有"OrderId"属性。OrderId属性的值是时间戳，格式如：<OrderDate>-<RandomInteger>。除此之外还有Amount属性，该属性描述了订单额度。

在[下一篇文章中](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/querying.md)，我们将基于插入的数据项来实践多项数据的查询操作。

```bash
$ aws dynamodb batch-write-item \
    --request-items '{
        "UserOrdersTable": [
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20160630-12928"},
                        "Amount": {"N": "142.23"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20170608-10171"},
                        "Amount": {"N": "18.95"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20170609-25875"},
                        "Amount": {"N": "116.86"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20160630-28176"},
                        "Amount": {"N": "88.30"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170609-18618"},
                        "Amount": {"N": "122.45"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170609-4177"},
                        "Amount": {"N": "27.89"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170608-24041"},
                        "Amount": {"N": "142.02"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170609-17146"},
                        "Amount": {"N": "114.00"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170609-9476"},
                        "Amount": {"N": "19.41"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20160630-13286"},
                        "Amount": {"N": "146.37"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170609-8718"},
                        "Amount": {"N": "76.19"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "daffyduck"},
                        "OrderId": {"S": "20171129-29970"},
                        "Amount": {"N": "6.98"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170609-10699"},
                        "Amount": {"N": "122.52"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20160630-25621"},
                        "Amount": {"N": "141.78"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170330-29929"},
                        "Amount": {"N": "80.36"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20160630-4350"},
                        "Amount": {"N": "138.93"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170330-20659"},
                        "Amount": {"N": "47.79"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170115-20782"},
                        "Amount": {"N": "80.05"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170330-18781"},
                        "Amount": {"N": "98.40"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170330-1645"},
                        "Amount": {"N": "25.53"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170115-2268"},
                        "Amount": {"N": "37.30"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170609-8267"},
                        "Amount": {"N": "32.13"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20170330-3572"},
                        "Amount": {"N": "126.17"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "alexdebrie"},
                        "OrderId": {"S": "20171129-28042"},
                        "Amount": {"N": "83.12"}
                    }
                }
            },
            {
                "PutRequest": {
                    "Item": {
                        "Username": {"S": "yosemitesam"},
                        "OrderId": {"S": "20170609-481"},
                        "Amount": {"N": "136.68"}
                    }
                }
            }
        ]
    }' \
    $LOCAL
```

其返回结果显示，所有数据项均成功写入DynamoDB，如下所示：

```bash
{
    "UnprocessedItems": {}
}
```

* [原文连接](https://www.dynamodbguide.com/working-with-multiple-items)