# 如何在DynamoDB高效查询多项数据

在DynamoDB中，查找操作的功能十分强大。它允许开发者根据相同的分区键来查询拥有不同[排序键](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/key-concepts.md)的数据项。本文将介绍查询操作的基础知识，分为以下几部分：

* 根据某个分区键查找多项数据
* 基于排序键和使用关键字表达式来查询多项数据
* 使用映射表达式来选择要返回的属性信息

当继续后续的学习之前，你需要理解什么是DynamoDB的表达式。

## 根据某个分区键查找多项数据

在之前的章节里，我们实践了如何[一次操作一项数据](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)。这种操作适合于一些场景，比如：一次操作一个用户信息，这些信息可能是该用户的简介或姓名。

然而，在某些场景，这样的数据操作就不适用了，比如操作用户的订单。有时你可能只需要获取某个订单数据，但是，有的时候我们想获取某个用户的所有订单信息。如果每个订单的信息由不同的分区键识别，那么查找这些订单的效率会很慢。

接下来，让我们看看有什么更好的办法能够快速查找某个用户的所有订单。答案是使用Query操作，首先，我们的场景是获取用户为"daffyduck"的所有订单信息。注意：`--key-condition-expression`选项是非常关键的参数，这个参数定义了我们如何选择要返回的订单。如下所示：

```bash
$ aws dynamodb query \
    --table-name UserOrdersTable \
    --key-condition-expression "Username = :username" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" }
    }' \
    $LOCAL
```

运行以上指令将得到4个属于"daffyduck"的订单，如下所示：

```bash
{
    "Count": 4,
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
        {
            "OrderId": {
                "S": "20170608-10171"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "18.95"
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
            }
        },
        {
            "OrderId": {
                "S": "20171129-29970"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "6.98"
            }
        }
    ],
    "ScannedCount": 4,
    "ConsumedCapacity": null
}
```

这非常管用。你只需要将返回的订单信息显示在订单页面上，然后任由用户选择某个订单进行详细查看。

## 使用关键字表达式

每当你根据分区键来查找数据的时候，这时返回的数据项会很多。然而，有时你需要根据某些条件来获取部分数据项。

例如：在我们设计表的时候，我们要满足以下查询模式：

> Give me all of the OrderIds for a particular Username.

以上查询模式很有用，但是我们想在这个查询模式上再加一些限制条件，比如：

> Give me all of the OrderIds for a particular Username where the Order was placed in the last 6 months.

或者

> Give me all of the OrderIds for a particular Username where the Amount was greater than $50.

有2种方法可以解决以上问题。然而，最为理想的做法是使用排序键和Query操作来确定最终的返回结果。这使得开发者能够使用关键字表达式来快速找到想要的数据。还有一种可行但是却低效的办法：[使用Filter](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)，并将Filter作用于非关键字主键上。

在这一节，我们将看到如何使用关键字表达式来缩小查询结果。之前，我们已经使用了`--key-condition-expression`选项来指定分区键，不仅如此，我们还可以指定排序键，而Query操作将查找满足这些键的多项数据。

还记得之前使用OrderId属性的例子吗？它的格式是<OrderDate>-<RandomInteger>。在表达式中使用OrderId能够使我们根据日期来查找订单。

比如：我们想获取某个用户在2017-2018年的所有订单，那么可以在关键字表达式中引入OrderId，并判断其在"20170101"到"20180101"之间，如下所示：

```bash
aws dynamodb query \
    --table-name UserOrdersTable \
    --key-condition-expression "Username = :username AND OrderId BETWEEN :startdate AND :enddate" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" },
        ":startdate": { "S": "20170101" },
        ":enddate": { "S": "20180101" }
    }' \
    $LOCAL
```

以上示例返回了3个项数据，而不是4项，如下所示：

```bash
{
    "Count": 3,
    "Items": [
        {
            "OrderId": {
                "S": "20170608-10171"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "18.95"
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
            }
        },
        {
            "OrderId": {
                "S": "20171129-29970"
            },
            "Username": {
                "S": "daffyduck"
            },
            "Amount": {
                "N": "6.98"
            }
        }
    ],
    "ScannedCount": 3,
    "ConsumedCapacity": null
}
```

"daffyduck"的第四个订单发生在2016年，由于它不满足条件，所以返回结果不会包含它。

关键字表达式很有用，因为它能支持很多种查询模式，但是它是有限制的。由于只能在关键字表达式使用分区键和排序键，因此在建立数据的查询模式时，你通常需要将数据信息反映到这些键上。不仅如此，它直接影响了你的查询模式的数量，比如选择OrderDate作为排序键以为着你无法根据订单总量来查找订单。

在以后的章节里，我们将看看摆脱以上限制的其它查询方式，它们有Filter或者[附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/secondary-indexes.md)。

## 缩减查询结果的属性

在上述的返回结果中，每项数据都包含了完整的属性。对于数据量不多的情况下，以上例子并没有毛病，但是随着返回的数据量增多，那么就有必要将不需要的属性剔除，以免减少数据量，从而降低响应时间。

为了剔除不必要的属性，那么可以在Query中使用`--projection-expression`，就像在GetItem中一样，它能帮助你只返回想用的属性，而不是所有属性。

例如，我们只想返回用户"daffyduck"的所有订单，但是这一次只需要Amounts属性，如下所示：

```bash
$ aws dynamodb query \
    --table-name UserOrdersTable \
    --key-condition-expression "Username = :username" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" }
    }' \
    --projection-expression 'Amount' \
    $LOCAL
```

执行以上示例，将得到以下仅仅包含Amount属性的数据项：

```bash
{
    "Count": 4,
    "Items": [
        {
            "Amount": {
                "N": "88.3"
            }
        },
        {
            "Amount": {
                "N": "18.95"
            }
        },
        {
            "Amount": {
                "N": "116.86"
            }
        },
        {
            "Amount": {
                "N": "6.98"
            }
        }
    ],
    "ScannedCount": 4,
    "ConsumedCapacity": null
}
```

注意，以上2个示例的返回结果均包含了"Count"，该值的含义是当前请求返回的数据项的数量。如果你仅仅想知道有多少项数据满足查询条件，那么你可以添加选项`--select`，如下所示：

```bash
$ aws dynamodb query \
    --table-name UserOrdersTable \
    --key-condition-expression "Username = :username" \
    --expression-attribute-values '{
        ":username": { "S": "daffyduck" }
    }' \
    --select COUNT \
    $LOCAL
```

以下是返回结果：

```bash
{
    "Count": 4,
    "ScannedCount": 4,
    "ConsumedCapacity": null
}
```

以上，我们涉及了Query API的基础知识。Query是DynamoDB众多功能中最为强大的功能，但是，为了高效使用它，你在数据建模时需要认真想想数据查询模式。在[下一篇文章里](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/scans.md)，我们将了解更加耗时的Scan操作。

* [原文链接](https://www.dynamodbguide.com/querying)