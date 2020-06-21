# DynamoDB的本地附加索引

在之前的[文章](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)中，我们学习了附加索引的基础知识。在本文中，我们将深入到本地附加索引。首先，我们将涉及本地附加索引的基础，紧接着通过一个例子来使用本地附加索引。Let's Go!

## 本地附加索引的基础知识

请注意：你只能在具有[**复合主键的表**](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)中添加本地附加索引。本地附加索引的分区键必须和复合主键的分区键一样，然而允许指定不同的排序键。

一些关于本地附加索引的注意事项：

* **本地附加索引的创建必须在创建表的时候添加**。也就是说你无法在已经创建好的表上添加附加索引，而是在创建表的时候添加。这一点与[全局附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/global-secondary-indexes.md)不一样
* **拥有相同分区键，但不同排序键的数据量不允许超过10GB**。注意这10GB数据包括表中的数据量加上本地附加索引中的数据量。如果你使用了本地附加索引，那么你得认真考虑使用[映射表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)
* **Consistency选项**。对于本地附加索引，你可以像表一样选择strong consistency或者eventual consistency。Strong consistency将占用更多的读单元，但是适用于某些场景
* **附加索引与表中的读写单元是共享的**。也就是说向本地索引读写数据时，会占用表中的读写单元

## 创建本地附加索引

现在，让我们动手来实践本地附加索引。还记得创建本地附加索引需要在创建表的时候完成吗！因此之前创建的"Users"表不能使用本地附加索引，所以我们只能考虑在"UserOrdersTable"表中添加附加索引。

还记得之前那个根据订单额度来过滤某个用户订单的例子吗？由于订单额度不是主键的一部分，因此我们不得不先根据主键获取该用户的订单，然后再使用过滤表达式来过滤出超过某个额度的订单。

这种需要根据订单额度来过滤数据的模式对于数据量大的场景显然是不适用的--原因在于，某个用户的订单有很多，比如上万条，而你只需要在这上万条数据中查找几条数据。为了解决这类问题，我们需要建立本地附加索引，并把订单额度作为该索引的排序键。这么一来，根据订单额度来查询订单数据就变快了许多。

虽然本地附加索引能解决以上问题，但不幸的是，创建附加索引必须在创建表的时候指定。不管如何，首先，让我们运行以下指令删除之前的表：

```bash
$ aws dynamodb delete-table \
    --table-name UserOrdersTable \
    $LOCAL
```
紧接着在创建带有本地附加索引的表：

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
      },
      {
          "AttributeName": "Amount",
          "AttributeType": "N"
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
    --local-secondary-indexes '[
      {
          "IndexName": "UserAmountIndex",
          "KeySchema": [
              {
                  "AttributeName": "Username",
                  "KeyType": "HASH"
              },
              {
                  "AttributeName": "Amount",
                  "KeyType": "RANGE"
              }
          ],
          "Projection": {
              "ProjectionType": "KEYS_ONLY"
          }
      }
    ]' \
    --provisioned-throughput '{
      "ReadCapacityUnits": 1,
      "WriteCapacityUnits": 1
    }' \
    $LOCAL
```

以上示例与CreateTable的命令一样。一开始，我们指定了表名，然后增加了2点：(1) 使"Amount"属性作为本地附加索引的排序键；(2) 使用`--local-secondary-indexes`选项。

最后，根据[之前的示例](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/working-with-multiple-items.md)，将25个用户订单插入到刚才创建的表中。这一步留给读者自行完成。

到目前为止，表"UserOrdersTable"将包含25项订单数据。你可以执行以下命令来检验数据的个数：

```bash
$ aws dynamodb scan \
    --table-name UserOrdersTable \
    --select COUNT \
    $LOCAL
```

返回的结果如下所示：

```bash
{
    "Count": 25,
    "ScannedCount": 25,
    "ConsumedCapacity": null
}
```

## 基于本地附加索引来查询数据

到目前为止，我们已经建立了本地附加索引，让我们通过一个具体的例子来使用它。在之前[过滤表达式的例子](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)中，我们查找了客户"daffyduck"订单额度在100美元的所有订单。现在，我们可以直接使用本地附加索引来查询符合以上条件的订单，如下所示：

```bash
$ aws dynamodb query \
    --table-name UserOrdersTable \
    --index-name UserAmountIndex \
    --key-condition-expression "Username = :username AND Amount > :amount" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" },
        ":amount": { "N": "100" }
    }' \
    $LOCAL
```

注意，在以上示例中，我们移除了`--filter-expression`选项，然后将其中的逻辑表达式移到了`--key-condition-expression`选项。我们还使用了`--index-name`来直接从索引中获取订单数据，而不是从表中。

返回结果如下所示：

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
    "ScannedCount": 1,
    "ConsumedCapacity": null
}
```

如同使用过滤条件的例子，以上返回结果正是我们想要的。然而，注意看ScannedCount和Count的返回值。在使用过滤条件的例子里，我们查到了4个属于"daffyduck"的订单，然而满足过滤条件的只有一个并返回给客户端。

当我们使用本地附加索引时ScannedCount的数值是1。这表明DynamoDB只查询到了1项订单额度在100美元以上的订单，而不是4个。这种查询方法与使用使用过滤表达式的方法相比，只作用于一小部分数据，从而最终导致更快的查询速度。如果数据量多的时候，这种速度的提升是非常巨大的。

现在，我们对本地附加索引有了一些了解。接下的一章将介绍[全局附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/global-secondary-indexes.md)。

* [原文链接](https://www.dynamodbguide.com/local-secondary-indexes)