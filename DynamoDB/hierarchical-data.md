# 如何在DynamoDB中查询层级结构的数据

在本文的示例中，我们将展示如何在DynamoDB中建立具有层级结构的数据（比如树状结构）。这个例子使用了大约25000个星巴克实体店的地址信息。你可以到[这里获取源码](https://github.com/alexdebrie/dynamodbguide.com/tree/master/examples/starbucks)来动手实践本文所提到的步骤。

层级结构的数据经常在关系型数据库中使用，将数据以树状结构来表示，比如组织架构图或族谱就是这种类型的数据。在关系型数据库中，为了将这些层级结构的数据连接在一起，通常需要使用多个JOINs来完成。而在本文中，我们仅使用一张DynamoDB的表来建立这种数据结构，并提供了更快的查询性能。

> 这个例子的灵感来自于Rick Houlihan在2017年的AWS reInvent上的研讨会，感兴趣的读者可以到[这里一睹其风采](https://youtu.be/jzeKPKpucS0?t=36m5s)。 

## 一些关于本文示例的基本信息

假设，我们是星巴克，一家跨国公司，门店遍布全球。现在，我们想把全球所有门店的信息存储在DynamoDB中，并希望能够快速查询以下信息：

* 根据门店编号来获取对应的门店信息
* 列举属于某个国家的所有门店信息
* 列举一个州或一个省下的所有门店信息
* 列举一个城市中所有门店信息
* 列举一个区里所有门店信息

第一种查询模式比较简单--就是那种key:value的关系，只需要给出门店编号，那么就能取到该门店的信息。剩余的4种查询模式就不是那么容易实现了。 当然，你可以创建4个[全局附加索引](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/global-secondary-indexes.md)来分别支持这4种查询模式，也可以使用[Filter表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/filtering.md)来过滤出我们想要的数据，但是这2种方法并不高效，同时会消耗更多的读取能力，进而增加费用。

为了解决以上提出的2个问题，我们可以借助该数据的层级信息以及仅使用一个全局附加索引来实现以上4种查询模式！接下来，让我们到[Kaggle获取遍布全球的星巴克门店数据](https://www.kaggle.com/starbucks/store-locations)--大约25000条。获取之后需要将这些数据写入到我们的表中，并验证是否完全倒入！以下提到的代码片段[摘自这里](https://github.com/alexdebrie/dynamodbguide.com/tree/master/examples/starbucks)。

## 准备工作

为了运行以下示例，你需要下载之前提到的数据，并解压它，然后将CVS文件复制到你的工作目录，名称是directory.csv。除此之外，你还要安装Python以及Boto3框架，该框架是Python版本的AWS SDK。你可以运行指令`pip install boto3`来按照该框架。最后，有些例子使用了Click框架，该框架能够帮助你快速制定命令行接口，运行指令`pip install click`来安装它。

## 设计主键和插入数据

一切就绪之后，是时候创建表以及将数据插入到表中。

首先，为表选择合适的主键。主键应该至少体现以下2点：

* 它具有唯一性。也就是它能唯一识别每项数据
* 它具有均匀分布的特性

理想状态下，主键也需要满足至少一条查询模式。

对于我们要处理的问题，将Store Number作为表的简单主键将是不错的选择。如果我们想要更新某个店铺的信息，那么肯定需要提供该店的Store Number。这符合查询模式的第一项：**根据门店编号来获取对应的门店信息**。除此之外，Store Number是均匀分布的。

接着，我们需要考虑其余4种查询数据的模式--如何根据国家，州，城市，区号来获取对应的实体店信息？我们将很快在后面的内容中讨论这个问题，但是现在，我们只需要创建一个全局附加索引"StoreLocationIndex"，这些索引需要满足以下要求：

* 将Country作为分区键（HASH key），用于指定实体店所在的国家
* 排序键（RANGE key）为StateCityPostcode，它是一个由State, City和Postcode构成的字符串，其格式为<STATE>#<CITY>#<POSTCODE>。例如：一家位于Omaha，NE的店铺，该值应该是：NE#OMAHA#68144。

为了创建这个表，则需要运行以下脚本文件。如果执行成功，则会输出以下信息：

```bash
$ python create_table.py
Table created successfully!
```

接下来，将directory.csv文件中的数据加载到DynamoDB中。脚本文件`insert_items.py`将读取这个文件的数据，然后遍历所有数据项，并将每一项数据插入到DynamoDB中。注意：整个过程需要一些时间，因为大约有25000项数据。

```bash
$ python insert_items.py
1000 locations written...
2000 locations written...
... <snip> ...
24000 locations written...
25000 locations written...
```

让我们执行Scan语句来确保插入了25599条数据，如下所示：

```bash
$ aws dynamodb scan \
    --table-name StarbucksLocations \
    --select COUNT \
    $LOCAL
```

以上指令执行之后将返回25599条结果，如下所示：

```bash
{
    "Count": 25599,
    "ScannedCount": 25599,
    "ConsumedCapacity": null
}
```

接下来，让我们查询一些数据！

## 根据Store Number来获取实体店信息

本文的一种获取实体店信息的模式是：给定一个Store Number，返回对应的实体店信息。这里我们将使用"5860-29255"作为Store Number。

因为表的主键是Store Number，所以我们可以使用GetItem API来完成这类查询模式。

运行脚本`get_store_location`，默认情况下，它将获取Store Number为"5860-29255"的实体店信息，如下所示：

```bash
$ python get_store_location.py
Attempting to retrieve store number 5860-29255...

Store number found! Here's your store:

{'City': {'S': 'Pasadena'},
 'Country': {'S': 'US'},
 'Latitude': {'S': '34.16'},
 'Longitude': {'S': '-118.15'},
 'PhoneNumber': {'S': '626-440-9962'},
 'Postcode': {'S': '911033383'},
 'State': {'S': 'CA'},
 'StateCityPostcode': {'S': 'CA#PASADENA#911033383'},
 'StoreName': {'S': 'Fair Oaks & Orange Grove, Pasadena'},
 'StoreNumber': {'S': '5860-29255'},
 'StreetAddress': {'S': '671 N. Fair Oaks Avenue'}}
```

从以上结果可知，返回的实体店信息其对应的Store Number就是"5860-29255"。如果你想获取其它实体店，那么使用选项`--store-number`，根据以下示例来实践：

```bash
$ python get_store_location.py --store-number 3513-125945
Attempting to retrieve store number 3513-125945...

Store number found! Here's your store:

{'City': {'S': 'Anchorage'},
 'Country': {'S': 'US'},
 'Latitude': {'S': '61.21'},
 'Longitude': {'S': '-149.78'},
 'PhoneNumber': {'S': '907-339-0900'},
 'Postcode': {'S': '995042300'},
 'State': {'S': 'AK'},
 'StateCityPostcode': {'S': 'AK#ANCHORAGE#995042300'},
 'StoreName': {'S': 'Safeway-Anchorage #1809'},
 'StoreNumber': {'S': '3513-125945'},
 'StreetAddress': {'S': '5600 Debarr Rd Ste 9'}}
```

## 聚合查询

现在让我们看看如何支持以上剩余的4种查询模式。为了支持这4种查询模式，则需要借助之前创建的全局附加索引-"StoreLocationIndex"。

这里的数据，其层级信息非常关键。在一个州内的所有门店信息肯定属于同一个国家，同一个城市中的所有店铺肯定属于同一个州，同一个区下面的所有店铺肯定属于同一个城市。

由于这种层级关系，我们可以借助分区键以及`begins_with()`函数来实现查找某一层下的所有店铺。

让我们举例说明：有2家店铺，一家位于Pasadena，另外一家位于San Francisco。此时第一家店铺所对应的StateCityPostcode是CA#PASADENA#911033383，而第二家店铺，其StateCityPostcode是CA#SAN FRANCISCO#94158。这2家店铺都开设在同一个州CA，但在不同的城市。

如果我想获取所有加利福尼亚州的所有店铺，那么我将使用以下[关键字表达式](https://github.com/digolds/url_shorten_service/blob/release/DynamoDB/expression-basics.md)：

```bash
Country = "US" AND begins_with(StateCityPostcode, "CA")
```

如果我想查询某个城市的所有门店，应该怎么做？以下给出了答案：

```bash
Country = "US" AND begins_with(StateCityPostcode, "CA#SAN FRANCISCO")
```

最后，如果我想根据区域来获取门店信息，那么可以像下面一样：

```bash
Country = "US" AND begins_with(StateCityPostcode, "CA#SAN FRANCISCO#94158")
```

为了能帮助你快速执行以上指令，你可以使用脚本文件`query_store_locations.py`。

首先，获取属于US内所有的门店信息。为了防止返回的结果填满整个命令行窗口，我在以下示例中使用了--count选项来仅返回门店数量：

```bash
$ python query_store_locations.py --country 'US' --count
Querying locations in country US.
No statecitypostcode specified. Retrieving all results in Country.

Retrieved 4648 locations.
```

注意，以上信息显示了US下一共有4648家星巴克门店。

接下来，让我们把查询范围缩小到州级别。比如，试一下查询Nebraska州内所有星巴克门店：

```bash
$ python query_store_locations.py --country 'US' --state 'NE' --count
Querying locations in country US, state NE.
The key expression includes a begins_with() function with input of 'NE'

Retrieved 58 locations.
```

以上示例显示了我们使用关键字表达式以及begins_with()函数来查找州代号为"NE"的所有店铺信息（总共有58家）。

当然，我们可以再将查询范围缩小到城市Omaha：

```bash
$ python query_store_locations.py --country 'US' --state 'NE' --city 'Omaha' --count
Querying locations in country US, state NE, city Omaha.
The key expression includes a begins_with() function with input of 'NE#OMAHA'

Retrieved 30 locations.
```

此时，我们得到了30家门店。最后，让我们看看查找某一个区下的所有门店。由于返回的结果很少，因此这一次我将去掉--count选项，如下所示：

```bash
$ python query_store_locations.py --country 'US' --state 'NE' --city 'Omaha' --postcode '68144'
Querying locations in country US, state NE, city Omaha, postcode 68144.
The key expression includes a begins_with() function with input of 'NE#OMAHA#68144'

{'Count': 2,
 'Items': [{'City': {'S': 'OMAHA'},
            'Country': {'S': 'US'},
            'Latitude': {'S': '41.23'},
            'Longitude': {'S': '-96.14'},
            'PhoneNumber': {'S': '402-334-1415'},
            'Postcode': {'S': '68144'},
            'State': {'S': 'NE'},
            'StateCityPostcode': {'S': 'NE#OMAHA#68144'},
            'StoreName': {'S': 'Family Fare 3784 Omaha'},
            'StoreNumber': {'S': '48135-261124'},
            'StreetAddress': {'S': '14444 W. CENTER RD., Westwood Plaza'}},
           {'City': {'S': 'Omaha'},
            'Country': {'S': 'US'},
            'Latitude': {'S': '41.23'},
            'Longitude': {'S': '-96.1'},
            'PhoneNumber': {'S': '4027785900'},
            'Postcode': {'S': '681443957'},
            'State': {'S': 'NE'},
            'StateCityPostcode': {'S': 'NE#OMAHA#681443957'},
            'StoreName': {'S': '125th & W. Center Rd.'},
            'StoreNumber': {'S': '2651-53179'},
            'StreetAddress': {'S': '12245 West Center Rd.'}}],
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '738',
                                      'content-type': 'application/x-amz-json-1.0',
                                      'server': 'Jetty(8.1.12.v20130726)',
                                      'x-amz-crc32': '2237738683',
                                      'x-amzn-requestid': '5acf463b-6341-45b7-a485-dd2860845d97'},
                      'HTTPStatusCode': 200,
                      'RequestId': '5acf463b-6341-45b7-a485-dd2860845d97',
                      'RetryAttempts': 0},
 'ScannedCount': 2}
```

我们的关键字表达式使用了NE#OMAHA#68144作为判断依据，其返回结果只有2家门店信息。每家信息都十分全。

你可以继续使用`query_store_locations.py`脚本来实验其他门店。如果不知道如何使用该脚本，那么可以使用`--help`选项来查看使用说明，如下所示：

```bash
$ python query_store_locations.py --help
Usage: query_store_locations.py [OPTIONS]

Options:
  --country TEXT      Country for stores to query. Default is 'US'.
  --state TEXT        State abbreviation for stores to query. E.g.: 'NE'
  --city TEXT         City for stores to query. E.g.: 'Omaha'
  --postcode TEXT     Post code for stores to query. E.g.: '68144'
  --default-state     Use defaults to query at state level.
  --default-city      Use defaults to query at city level.
  --default-postcode  Use defaults to query at post code level.
  --count             Only show counts of items.
  --help              Show this message and exit.
```

> 如果对以上例子还有不明白的地方，那么给我[留言或者发邮件给我](https://twitter.com/alexbdebrie)！

* [原文链接](https://www.dynamodbguide.com/hierarchical-data)