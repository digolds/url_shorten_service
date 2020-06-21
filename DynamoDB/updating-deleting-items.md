# 更新和删除数据项

在这篇文章中，我们将学习如何向表中更新和删除单项数据。这是最后一篇关于单项数据操作的文章，后续的文章将涉及多个数据项的操作，这些操作主要有Queries和Scans。

## 更新单项数据

在之前的例子中，我们使用PutItem操作来向表中插入单项数据。我们也看到这种操作将会完全覆盖表中已存在的数据。为了不让这个操作覆盖已存在的数据项，我们在这个操作上使用了条件表达式。

有时需要处理这种场景：只更新某项数据的一个或者多个属性，而其它属性保持不变。为了处理这种场景，DynamoDB提供了UpdateItem操作，该操作允许开发者在不读取数据的情况下更新数据。

当使用UpdateItem操作时，你需要指定[**更新表达式**](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)，该表达式由2部分构成，分别是：更新的语义（比如是向数据项中添加属性还是移除属性）和表达式。

当使用更新表达式时，你必须提供以下更新的语义：

* SET: 这个操作用于向数据项中添加新的属性，或者覆盖已有属性
* REMOVE: 该操作用于移除数据项中某一个属性
* ADD: 对于数值类型的属性，该操作代表加或减；对于集合类型的属性，该操作代表向集合中插入元素
* DELETE: 用于从集合中删除元素

让我们通过几个例子来了解更新操作的使用。

* **使用带有SET语义的UpdateItem**

在更新数据项时，最常用的更新操作是SET。比如，如果我想向某项数据添加一个新的属性或者覆盖已有的属性，那么这个SET操作会被用到。

让我们看看最开始的例子：PutItem，假设，我们想让已经添加的用户拥有属性DateOfBirth。 如果不使用UpdateItem操作，我们的做法是首先通过GetItem获取该数据项，然后通过PutItem插入一项包含DateOfBirth属性的数据项。然而通过UpdateItem操作，我们只需要直接插入属性DateOfBirth即可，如下所示：

```bash
$ aws dynamodb update-item \
    --table-name Users \
    --key '{
      "Username": {"S": "daffyduck"}
    }' \
    --update-expression 'SET #dob = :dob' \
    --expression-attribute-names '{
      "#dob": "DateOfBirth"
    }' \
    --expression-attribute-values '{
      ":dob": {"S": "1937-04-17"}
    }' \
    $LOCAL
```

注意我们使用了选项`--expression-attribute-names`和`--expression-attribute-values`。

如果我们再次获取该数据项，那么我们不仅能看到之前的属性，而且还能看到新添的属性，如下所示：

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
        "DateOfBirth": {
            "S": "1937-04-17"
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

* **使用带有REMOVE语义的UpdateItem**

带有REMOVE语义的UpdateItem操作与带有SET语义的UpdateItem操作相反--它用于从一个数据项中删除指定属性。

让我们使用它来移除之前我们添加的属性"DateOfBirth"。我们将使用`--return-values`选项来告诉DynamoDB返回更新之后的结果，以便不需要使用GetItem来获取更新之后的数据项。该选项提供了若干选项，包括返回更新之前的所有属性或部分正在更新的属性。在这里，我们将选择选项"ALL_NEW"，该选项的作用是让DynamoDB在执行UpdateItem成功之后，返回该项数据的已更新过的所有属性。如下所示：

```bash
$ aws dynamodb update-item \
    --table-name Users \
    --key '{
      "Username": {"S": "daffyduck"}
    }' \
    --update-expression 'REMOVE #dob' \
    --expression-attribute-names '{
      "#dob": "DateOfBirth"
    }' \
    --return-values 'ALL_NEW' \
    $LOCAL

{
    "Attributes": {
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

以上的返回结果表明，该数据项已经不包含属性DateOfBirth。

## 删除单项数据

最后一个关于单项数据的操作是删除操作，也就是DeleteItem。在有些场景，你需要删除表中的某项数据，而这个操作则能满足该场景。

DeleteItem操作相当简单--你只需要提供想要删除数据项的主键信息，如下所示：

```bash
$ aws dynamodb delete-item \
    --table-name Users \
    --key '{
      "Username": {"S": "daffyduck"}
    }' \
    $LOCAL
```

以上操作将把"Username"为"daffyduck"的数据项从表中移除。如果你想通过GetItem操作来获取该用户，那么你将得到空的结果。

类似于PutItem操作，你能够使用`--condition-expression`来指定删除的条件。比如我想删除该用户，但是前提条件是该用户的年龄必须是少于21岁，示例如下：

```bash
$ aws dynamodb delete-item \
    --table-name Users \
    --key '{
      "Username": {"S": "yosemitesam"}
    }' \
    --condition-expression "Age < :a" \
    --expression-attribute-values '{
      ":a": {"N": "21"}
    }' \
    $LOCAL

An error occurred (ConditionalCheckFailedException) when calling the DeleteItem operation: The conditional request failed
```

通过以上示例的执行结果可知：由于Yosemite Sam已经73岁了，所以条件表达式将无法通过，最终导致此次删除操作失败。

## 结论

本文将结束单项数据操作的内容。到目前为止，我们已经学习了什么是[数据项以及其基础知识](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/anatomy-of-an-item.md)，这些知识包括了主键，属性和属性类型。然后我们还学习了[如何插入和查询单项数据](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)。在实践这些操作的过程中，我们还介绍了表达式的使用，包括`--expression-attribute-names`和`--expression-attribute-values`的使用。在本文中，我们介绍了更新和删除单项数据，这些操作可以单独使用，也可以配合表达式来使用。

在接下来的章节中，会陆续介绍多项数据的操作，包括查询和遍历操作，除此之外还会使用过滤表达式。这些操作与复合主键结合在一起，能够为开发者带来各种高效数据查询的模式。

* [原文链接](https://www.dynamodbguide.com/updating-deleting-items)