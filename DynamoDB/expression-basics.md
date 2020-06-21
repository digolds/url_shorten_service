# DynamoDB的基础表达式

本文是关于DynamoDB的表达式。表达式是DynamoDB的内置功能，它又细分为以下几类表达式：

* **条件表达式**只能与单项数据的操作配合起来使用，这些操作有PutItem，UpdateItem和DeleteItem。当你为单项数据的操作指定条件表达式时，只有当该表达式的验证结果为`true`时，该操作才能执行，对应的指令选项是`--condition-expression`
* **属性映射表达式**通常会与读取数据项的操作配合起来使用，比如[之前的GetItem例子](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)就使用了属性映射表达式，它的作用在于仅返回该项数据的部分属性，对应的指令选项是`--projection-expression`
* **更新表达式**用于更新已经存在的数据项上的某些属性，对应的指令选项是`--update-expression`
* **主键条件表达式**通常会与查询操作（比如Query）一起使用，这类表达式的条件只能是与主键相关，对应的指令选项是`--key-condition-expression`
* **过滤表达式**通常会与查询操作或遍历操作一起使用，它将作用于查询结果之上，对应的指令选项是`--filter-expression`

只有充分理解了这些表达式，才能更好地使用DynamoDB，进而享受DynamoDB给我们带来的好处。在这篇文章，我们将学习表达式的基础知识，包括使用表达式的属性名和属性值。紧接着，我们将基于上一章关于PutItem的例子来学习如何使用**条件表达式**。

## 表达式的基础知识

DynamoDB中的表达式只是一串字符串，它的内容是特定的逻辑表达式，而这个表达式将用来验证数据是否满足该条件。在这些表达式中，你可以应用一些比较操作符，比如"="（相等），">"（大于）或者">="（大于等于）。例如，以下表达式应用了">="：

```bash
"Age >= 21"
```

该表达式的作用在于：该操作只能作用于年龄在21岁及以上的用户，否则操作结果会出错。

> 注意：以上表达式还无法生效，原因在于该表达式没有指定"21"的类型。为了使以上表达式生效，你需要指定expression attribute values，也就是使用指令属性`--expression-attribute-values`，这一点将在后面提到。

除了可以在表达式中使用比较操作符，还可以在表达式中使用函数。这些函数是DynamoDB提供的，它们有：attribute_exists()，判断某项数据其属性是存在的；attribute_not_exists()，判断某项数据其属性是不存在的；begins_with()，判断某项数据其属性值是以某个子字符串开始的。

我们可以在表达式中使用attribute_not_exists()函数来判断某个订单是否已经发货了，其用法如下所示：

```bash
"attribute_not_exists(DateShipped)"
```

如果该订单有DateShipped属性，那么表明它已经发货了，否则表明它还在仓库中。DynamoDB提供的函数不多，所有的函数如下所示：

* attribute_exists(): 判断某项数据其属性是存在的
* attribute_not_exists(): 判断某项数据其属性是不存在的
* attribute_type(): 判断某项数据其属性的类型是指定的类型
* begins_with(): 判断某项数据其属性值是以某个子字符串开始的
* contains(): 如果该属性是字符串类型，则判断某项数据其属性值是包含某个子字符串的；如果该属性是集合类型（比如List或Map），则判断该属性是包含指定元素的
* size(): 返回属性的大小，不同类型的属性，其大小的计算规则是不一样的。

关于表达式中的比较操作符和函数，读者可以参考[官方文档](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html)。

## 表达式的占位符

之前的内容表明，表达式是一个具有逻辑运算的字符串，DynamoDB通过执行这个表达式来得到一个是或否的结果。然而，有的时候你需要一种更加清晰的方式来编写表达式，比如在表达式中使用变量，然后在其它地方提供变量值。

DynamoDB允许你使用`--expression-attribute-names`和`--expression-attribute-values`选项来编写更加清晰的表达式。通过这种做法，你可以在表达式中指定变量，然后分别使用以上选项来指定变量值，DynamoDB会将这些变量值自动替换掉表达式中的变量。接下来，让我们看看这2个选项的含义。

* `--expression-attribute-names`

有时，你希望针对一个属性编写表达式，但是由于DynamoDB的限制，你无法直接在表达式中使用该属性名，比如：

* 你的属性名称刚好是DynamoDB中预留的关键字。DynamoDB预先保留了大量的关键字，其中包括了："Date"，"Year"和"Name"等。如果你的属性名称恰巧在这些预留的关键字里，那么你需要借助这个选项来提供属性名称的占位符
* 你的属性名称中包含"."。DynamoDB使用"."来获取嵌套类型（比如Map类型）中的子项。如果你的属性名中包含了"."，那么你需要借助这个选项来提供属性名称的占位符
* 你的属性名称开头包含数字。DynamoDB不允许表达式中的属性名称以数字开头，因此如果你的属性名称以数字开头，那么你需要借助这个选项来提供属性名称的占位符

在使用这个选项时，你只需要提供一个Map格式的属性名称集合。这个Map中的key是表达式中的占位符，而value是属性名称。例如，你可以为"Age"属性定义占位符"#a"，而这个占位符可用于表达式，具体示例如下所示：

```bash
  --expression-attribute-names '{
    "#a": "Age"
  }'
```

> 当使用`--expression-attribute-names`时，占位符必须以"**#**"开头。

在之前的[GetItem](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)的例子中，我们使用了`--projection-expression`选项来返回某项数据的部分属性。为了能够在该选项中使用占位符，我们需要将之前的例子改如下：

```bash
$ aws dynamodb get-item \
    --table-name Users \
    --projection-expression "#a, #u" \
    --expression-attribute-names '{
      "#a": "Age",
      "#u": "Username"
    }' \
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

注意，在以上例子中，我们在`--projection-expression`中使用了2个占位符，分别是"#a"和"#u"。而这2个占位符定义在`--expression-attribute-names`选项中，分别对应"Age"和"Username"属性。

最后需要注意的是：如果表达式中的属性是Map类型中的某个键（比如"Address.State"），那么你需要定义对应的占位符。比如，你的数据项中有一个类型为Map的属性"Address"，这个属性包含了3个键，它们分别是："Street"，"City"和"State"。如果你想判断"State"是否是指定的一个值时，你需要在表达式中使用"Address.State"，但是这种表达方式只能通过`--expression-attribute-names`来完成，如下所示：

```bash
--condition-expression "#a.#st = 'Nebraska' " \
    --expression-attribute-names '{
      "#a": "Address",
      "#st": "State"
    }'
```

注意，在以上例子中，"#a.#st"会被替换成"Address.State"。

* `--expression-attribute-values`

`--expression-attribute-values`选项的作用与`--expression-attribute-names`不同，跟在它后面的参数将作用于表达式中的属性值，比如可以定义一个占位符":stn"来替代"#a.#st = 'Nebraska' "中的'Nebraska'。除此之外，在格式上也有些不一样：

* 占位符必须是以":"作为开头，比如上面的":stn"，而不是"#"
* 在设置值的时候，必须提供该值的类型，比如：{":agelimit": {"N": 21} }

关于其用法的例子，可以参考使用[UpdateItem API的文章](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items.md)

## 条件表达式

这一节将通过一个使用条件表达式的例子结束本章的内容。还记得[我们之前使用PutItem](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)来向"User"表中插入数据的例子吗！这个例子有一个问题：如果"Users"表中已经包含了正在插入的数据项，那么这个操作将覆盖已存在的数据项，这种操作将破坏老的数据项，这也许不是我们想要的结果。

好在，我们可以使用条件表达式来避免这种毁灭性操作。下面的示例给出了一种解决方法：我们可以添加--condition-expression "attribute_not_exists(#u)"选项，这个选项的作用在于确保插入的User是不存在的，如果存在，那么这次插入将会失败。

```bash
$ aws dynamodb put-item \
    --table-name Users \
    --item '{
      "Username": {"S": "yosemitesam"},
      "Name": {"S": "Yosemite Sam"},
      "Age": {"N": "73"}
    }' \
    --condition-expression "attribute_not_exists(#u)" \
    --expression-attribute-names '{
      "#u": "Username"
    }' \
    $LOCAL
```

需要注意的是，我们在条件表达式中使用了函数attribute_not_exists()来判断给定的"Username"属性是否存在，并期望它是不存在的，然后期望这次插入操作将会成功。如果你再一次运行以上指令，那么你将得到以下错误：

```bash
An error occurred (ConditionalCheckFailedException) when calling the PutItem operation: The conditional request failed
```

以上错误表明，"Username"为"yosemitesam"的User已经存在，attribute_not_exists(#u)的执行过程是这样的：根据"yosemitesam"获取该User，如果获取成功，那么再判断"Username"属性是否存在于User，如果存在，那么该函数返回的结果是false，如果不存在，该函数返回的结果是true。

本章内容介绍了DynamoDB中表达式的基础知识。表达式是用好DynamoDB的前提，表达式又分为以上5类，而文章的最后通过一个示例来揭示条件表达式的用途，其它表达式的用法将在[后续章节](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/updating-deleting-items.md)中使用到。

* [原文链接](https://www.dynamodbguide.com/expression-basics)