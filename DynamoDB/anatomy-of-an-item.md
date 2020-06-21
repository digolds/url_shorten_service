# DynamoDB中，每项数据（item）的构成单元

DynamoDB中的每条数据是构成整个数据集的基础，它对应着关系型数据库中的某一张表中的某一行数据或者对应MongoDB中一个文档，又或者是编程当中的一个对象（比如一个用户对象）。每条数据由主键唯一标识，而主键是在创建表的时候指定的。除了主键之外，每条数据也可以包含其它属性，这些属性与主键组成了一条完整的数据单元（比如：一个用户数据由user_id, name, phone组成，其中user_id是主键）。每个属性（包括主键）都有对应类型，比如string，numbers，lists，sets等，当写入或查询数据的时候，这些类型都需要提供。在这篇文章中，我们将通过以下几个方面来讨论构成每项数据的基础单元：

* 主键
* 属性
* 属性的类型

## 主键

> 表中的每项数据都由主键唯一标识

每当创建一张表的时，你需要为该表指定一个主键。每项数据由主键唯一标识，而且每当向表中插入一项数据时，该项数据必须包含主键信息。

Dynamo支持2种主键。一种是**简单主键**，这种主键只使用了一个属性标识每一项数据，比如用户名或者订单编号。使用简单主键来写入或查询数据时有点类似于key-value数据库，比如Memcached。另外一种是**复合主键**，这种主键使用了2个属性来标识每一项数据。其中一个属性是分区键，它的作用在于将不同的数据划分到对应的分区。另外一个属性是排序键，它的作用是使所有具有相同分区键值的数据依据排序键进行排序。拥有复合主键的表，除了能够支持简单的写入和查询数据操作，还支持更多复杂的数据查询操作。

理解DynamoDB中表的主键对于数据建模至关重要。每当插入和更新数据时，主键都是必不可少的信息。

## 属性

每项数据都由多个属性构成，比如User表中的某一项数据有Name，Age，地址等属性，这些属性类似于关系型数据库中的列。DynamoDB表

DynamoDB表中每一项数据除了必须包含主键属性，其它属性不是必须的。DynamoDB是NoSQL数据库，因此它允许更加灵活的数据模型，而这一点在关系型数据库中是无法办到的。因为这种灵活的数据模型，你能在一张DynamoDB表中存储多种不同类型的数据，比如有一条Car数据，它包含产地，型号和生产年限等属性，同时在相同的表中也包含另外一条Pet数据，它包含类型，血型，年龄，颜色等属性。在DynamoDB中，一张表中同时包含不同类型的数据是常见的做法，这种做法会提高数据查询的效率！

## 属性的类型

当为每一项数据设置属性时，同时需要指定该属性的类型。可指定的类型有简单类型：比如，strings和numbers；也有复合类型：比如：lists，maps和sets。

每当更新或者插入数据时，需要为数据中的每一个属性指定其对应的类型。这些属性的设置需要借助一个map数据结构来完成，其中该map的keys是每一个属性名，而对应的values则是另外一个map，而这个map只有一个元素，其key是对应属性的类型，而value是对应属性的值。比如：你想存储一个用户数据，该数据包含3个属性，分别是姓名，年龄和角色，它们的类型分别是string，number和list，那么你需要为该用户数据设置如下属性信息：

```bash
{
    "Name": { "S": "Alex DeBrie" },
    "Age": { "N": "29" },
    "Roles": { "L": ["Admin", "User"] }
}
```

在以上例子，我们存储了Name属性，其类型是string（通过"S"来代表），值为"Alex DeBrie"。此外，还存储了Age属性，其类型是number（通过"N"来代表），值为"29"。最后，还存储了Roles属性，其类型是list（通过"L"来代表），值为"Admin"和"User"。

同样，每当你从表中获取数据项时，其属性会以map的方式返回。其中，map中的keys是属性名，而values则是另外一个map，这个map的key是对应属性的类型，而value则是对应属性的值。例如，如果你使用GetItem API来获取以上用户数据，那么得到的结果如下所示：

```bash
{
    "Item": {
        "Name": {
            "S": "Alex DeBrie"
        },
        "Age": {
            "N": "29"
        },
        "Roles": {
            "L": ["Admin", "User"]
        }
    }
}
```

> 需要注意的是：Age属性的值"29"是字符串，因此为了得到数值类型29，那么需要在应用程序里将字符串转成数值类型。

对以上属性类型有一些基本了解之后，让我们来看看不同的属性类型。每种属性类型都会以类型标识（比如"S"代表string，而"N"代表number）和用例开始介绍。

**String类型**

**Identifier: "S"**

**用例：**

```bash
"Name": { "S": "Alex DeBrie" }
```

string类型是基础的数据类型，字符集为Unicode，对应的编码方式为UTF-8。DynamoDB允许该类型的属性排序，这种排序十分有用，比如根据姓氏（按照字母次序）或者ISO的时间戳（比如：将"2017-07-01"和"2018-01-01"之间的数据项按照日期来排序）来对多个数据项进行排序。

**Number类型**

**Identifier: "N"**

**用例：**

```bash
"Age": { "N": "29" }
```

数值类型的取值是实数，包括正数（+9.80），负数（-7）和0。它的精度最多是38位（比如9.9999999999999999999999999999999999999E+125）。需要注意的是，你必须以字符串的形式提供数值类型，比如`"29"`而不是`29`，然而，当使用条件表达式时，你却能使用数值操作作用于数值属性。

**Binary类型**

**Identifier: "B"**

**用例：**

```bash
"SecretMessage": { "B": "bXkgc3VwZXIgc2VjcmV0IHRleHQh" }
```

你可以在DynamoDB中存储二进制数据，比如一张图片或压缩过的信息。对于数据量过大的二进制信息，一般会存储在AWS的S3服务上，而不会存储在DynamoDB上，这么做的好处是保持DynamoDB的吞吐量。在使用这种类型的属性时，需要先将二进制信息进行base64编码，然后再设置到该类属性并上传到DynamoDB。

**Boolean类型**

**Identifier: "BOOL"**

**用例：**

```bash
"IsActive": { "BOOL": "false" }
```

布尔类型的值有2个："true"或"false".

**Null类型**

**Identifier: "NULL"**

**用例：**

```bash
"OrderId": { "NULL": "true" }
```

Null类型的值有2个："true"或"false"。一般情况下，不建议使用这种类型。

**List类型**

**Identifier: "L"**

**用例：**

```bash
"Roles": { "L": [ "Admin", "User" ] }
```

列表类型允许在单个属性中存储多个值。列表中每一项数据其类型可以不同，比如同一个列表里包含一个string元素和一个number元素。你可以通过[表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)来操作列表里的元素。

**Map类型**

**Identifier: "M"**

**用例：**

```bash
"FamilyMembers": {
    "M": {
        "Bill Murray": {
            "Relationship": "Spouse",
            "Age": 65
        },
        "Tina Turner": {
            "Relationship": "Daughter",
            "Age": 78,
            "Occupation": "Singer"
        }
    }
}
```

Map和列表一样，允许在单个属性上存储多个元素，与列表不同的是，每个元素都会有一个关联的key，有点类似于大多数编程语言中的字典类型。与列表类型一样，你可以通过表达式来操作Map里的元素。

**String Set类型**

**Identifier: "SS"**

**用例：**

```bash
"Roles": { "SS": [ "Admin", "User" ] }
```

String Set是集合类型，它的特点是所有集合的元素的类型必须统一：都是string类型，其次集合里的所有元素必须是不同的。集合与表达式一起使用能够带来一些实用的效果，比如你可以根据集合里的元素来修改数据，这种修改可以不触发读取数据的操作，从而具有很好的性能。

**Number Set类型**

**Identifier: "NS"**

**用例：**

```bash
"RelatedUsers": { "NS": [ "123", "456", "789" ] }
```

Number Set类型与String Set类型是类似的，唯一的区别是这种集合中的元素类型是number。

**Binary Set类型**

**Identifier: "BS"**

**用例：**

```bash
"SecretCodes": { "BS": [ 
	"c2VjcmV0IG1lc3NhZ2UgMQ==", 
	"YW5vdGhlciBzZWNyZXQ=", 
	"dGhpcmQgc2VjcmV0" 
] }
```

Binary Set类型与String Set类型是类似的，唯一的区别是这种集合中的元素类型是binary。

对以上关于数据项构成单元有一些基础的理解之后，接下来让[我们插入和查询一些数据项](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/inserting-retrieving-items.md)。

* [原文链接](https://www.dynamodbguide.com/anatomy-of-an-item#primary-keys)