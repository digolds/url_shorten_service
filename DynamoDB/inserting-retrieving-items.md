# 在DynamoDB中插入和读取数据项

[数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)是DynamoDB的基础单元，每一张表都会包含多项数据。接下来，在本文中，我们将向DynamoDB中插入和读取数据项。我们将创建Users表，并为该表指定一个[简单键](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)：Username。接着，我们将操作2个基本的接口：PutItem和GetItem。下一篇文章，我们将在这篇文章的基础上[应用表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)来实现更加复杂的查询功能。在这之后，我们将另起一篇文章来讲解[如何更新和删除数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items)。

>为了能顺利操作本文所列举的示例，请确保[DynamoDB的环境](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/environment-setup)已经准备好。注意：如果你使用的是本地版本的DynamoDB，那么请确保`$LOCAL`变量配置正确，如果使用的是AWS上的DynamoDB，那么在每一个命令后面无需追加这个参数。

## 创建表

在演练本文列举的用例之前，首先需要创建一张表。我们将创建一张表"Users"，并为该表定义了一个简单主键："Username"，它的类型是string。

当创建表时，你需要为主键或索引提供属性定义。这些属性定义包含了属性名和属性类型。在Users这张表中，我们使用"Username"作为主键，其类型是string（"S"）。除此之外，你还需要为该表定义KeySchema，其中指定了哪些属性构成主键以及这些属性是HASH键还是RANGE键。在以下示例中，属性"Username"构成了该表的简单主键。最后，你需要指定表名和表的吞吐单元，其中吞吐单元由读和写单元构成。在以下示例中，"Users"表的读写单元都是1，简单来说，越多的读写单元，单位时间内读写数据的速度越快和越多，反之亦然！

有了以上概念, 让我们运行以下指令来创建表"Users":

```bash
$ aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions '[
    {
        "AttributeName": "Username",
        "AttributeType": "S"
    }
  ]' \
  --key-schema '[
    {
        "AttributeName": "Username",
        "KeyType": "HASH"
    }
  ]' \
  --provisioned-throughput '{
    "ReadCapacityUnits": 1,
    "WriteCapacityUnits": 1
  }' \
  $LOCAL
```

如果创建表的操作成功了，你将看到以下返回结果：

```bash
{
    "TableDescription": {
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/Users",
        "AttributeDefinitions": [
            {
                "AttributeName": "Username",
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
        "TableName": "Users",
        "TableStatus": "ACTIVE",
        "KeySchema": [
            {
                "KeyType": "HASH",
                "AttributeName": "Username"
            }
        ],
        "ItemCount": 0,
        "CreationDateTime": 1514562957.925
    }
}
```

为了验证已经成功创建表"Users"，你可以执行`list-tables`命令来获取已创建的表：

```bash
$ aws dynamodb list-tables $LOCAL
{
    "TableNames": [
        "Users"
    ]
}
```

紧接着，你可以通过`describe-table`来查看某张表的详细信息，如下所示：

```bash
$ aws dynamodb describe-table \
  --table-name Users \
  $LOCAL
```

## 插入单项数据

既然我们已经创建了表"Users"，接下来，让我们向该表插入一些数据。为了完成这一操作，我们需要借助DynamoDB的PutItem API。使用PutItem时，开发者需要提供完整的数据项，这项数据除了要包含主键信息，还需要包含其它属性信息。如果新插入的数据项，其主键已经包含在"Users"表中，那么将新插入额度数据项将覆盖老的数据项，否则直接将数据项添加到"Users"表里。

>如果你想避免覆盖原有的数据项，那么可以考虑使用[条件表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)。如果你只是想更新某项数据的某些属性，那么你可以考虑使用DynamoDB的[UpdateItem API](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items.md)。

接下来，让我们插入一个数据项，这项数据只包含了主键信息"alexdebrie"，如下所示：

```bash
$ aws dynamodb put-item \
    --table-name Users \
    --item '{
      "Username": {"S": "alexdebrie"}
    }' \
    $LOCAL
```

如果没有错误发生，那么意味着这次插入是成功的。

让我们向该表中添加更多的数据项，这一次添加的数据项不仅包括主键属性（比如"Username"）还包括其它属性，比如"Name"和"Age"，如下所示：

```bash
$ aws dynamodb put-item \
    --table-name Users \
    --item '{
      "Username": {"S": "daffyduck"},
      "Name": {"S": "Daffy Duck"},
      "Age": {"N": "81"}
    }' \
    $LOCAL
```

注意：在上述操作示例中，我们不仅提供了表"Users"所必须的属性"Username"，我们还提供了其它非必须的属性，比如"Name"和"Age"以及每一个属性[对应的类型]((https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)。与关系型数据库不同的是，DynamoDB允许开发者在添加数据项时决定具体的属性信息（Schema-Less），而不是通过Schema提前定义好数据类型。


DynamoDB的这种数据模型的灵活性（Schema-Less）有好有坏。其好处是，开发者可以将多个不同类型的数据实体放在同一张表里（比如：User和Order可以放在同一张表里），从而提高数据读取的性能。然而，这种灵活性违背了SQL的范式原则，比如可能会导致数据变得不一致，数据冗余等，也会导致分析表中的数据变得更加困难。

## 获取单项数据

在插入单项数据那一节，我们在表"Users"中插入了2项数据。现在让我们来看看如何读取这2项数据。

为了获取单项数据，需要借助GetItem API。为了使用这个API，你需要提供表的名称，如"Users"，除此之外，你还需要提供需要获取这项数据的主键。让我们获取第一个User，如下所示：

```bash
$ aws dynamodb get-item \
    --table-name Users \
    --key '{
      "Username": {"S": "alexdebrie"}
    }' \
    $LOCAL

{
    "Item": {
        "Username": {
            "S": "alexdebrie"
        }
    }
}
```

注意：上述操作示例所获取的User信息被放置在Item中。

接下来让我们获取第二个User的信息，这一次的用户不仅返回了主键信息，而且还将其它属性的信息（如"Name"和"Age"）也返回了。如下所示：

```bash
$ aws dynamodb get-item \
    --table-name Users \
    --key '{
      "Username": {"S": "daffyduck"}
    }' \
    $LOCAL

{
    "Item": {
        "Username": {
            "S": "daffyduck"
        },
        "Age": {
            "N": "81"
        },
        "Name": {
            "S": "Daffy Duck"
        }
    }
}
```

有时，你只想获取某项数据的某些属性信息，比如我只想获取第2个User的"Age"和"Name"信息，那么可以使用`--projection-expression`选项，如下所示：

```bash
$ aws dynamodb get-item \
    --table-name UsersTable \
    --projection-expression "Age, Username" \
    --key '{
      "Username": {"S": "daffyduck"}
    }' \
    $LOCAL

{
    "Item": {
        "Username": {
            "S": "daffyduck"
        },
        "Age": {
            "N": "81"
        }
    }
}
```

在上面的操作示例中，我们使用了`--projection-expression`选项来获取某些属性信息。该选项也可以作用于List和Map属性中的元素。

这篇文章涉及了向DynamoDB中插入和获取单项数据的基础操作示例。在接下来的[一篇文章](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)中，我们将结合表达式来实现更加复杂实用的插入和查询操作。

* [原文链接](https://www.dynamodbguide.com/inserting-retrieving-items)