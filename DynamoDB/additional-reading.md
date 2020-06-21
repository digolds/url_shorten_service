# NoSQL的学习资料

这篇文章收录了一些关于NoSQL的英文资料。有的解释NoSQL为何能规模化而SQL却受到限制；有的涉及NoSQL的单表设计原则，以及解释为何需要使用单表；其中有一篇文章是关于如何将SQL中多张有关联的表转化成DynamoDB中的单张表。还有一些关于DynamoDB的视频资料，其中的内容讲述了NoSQL的设计原则，以及如何高效使用DynamoDB。读者可以通过这些学习资料来掌握NoSQL的理论知识，通过这些知识来设计既能支持100TBs以上数据又能输出稳定性能的数据应用方案。

## 文章:

* [SQL, NoSQL, and Scale: How DynamoDB scales where relational databases don't](https://www.alexdebrie.com/posts/dynamodb-no-bad-queries/) - This is a post of mine explaining the core architectural decisions that allow NoSQL databases to scale further than their SQL brethren.
* [The What, Why, and When of Single-Table Design with DynamoDB](https://www.alexdebrie.com/posts/dynamodb-single-table/) - A deep look at what it means to do single-table design in DynamoDB and why you would want to. It also includes a few situations where you may want to avoid single-table design.
* [Faux-SQL or NoSQL? Examining four DynamoDB Patterns in Serverless Applications](https://www.alexdebrie.com/posts/dynamodb-patterns-serverless/) - This is a post I wrote on the common data modeling patterns I see with DynamoDB in serverless applications.
* [Why Amazon DynamoDB isn't for everyone]() - My favorite post on this topic. Forrest Brazeal does a great job breaking down the pros and cons of DynamoDB.
* [From relational DB to single DynamoDB table: a step-by-step exploration](https://www.trek10.com/blog/dynamodb-single-table-relational-modeling/) - Another great post by Forrest Brazeal. It's a detailed walkthrough of how to use the single-table DynamoDB pattern in a complex use case.
* [Why the PIE theorem is more relevant than the CAP theorem](https://www.alexdebrie.com/posts/choosing-a-database-with-pie/) - Another post I wrote about choosing a database that includes consideration of DynamoDB.

## 视频:

* [Advanced Design Patterns for DynamoDB (reInvent 2017)](https://www.youtube.com/watch?v=jzeKPKpucS0). Rick Houlihan is a master of DynamoDB and has some great tips.
* [Advanced Design Pattens for DynamoDB (reInvent 2018)](https://www.youtube.com/watch?v=HaEPXoXVf2k). Rick Houlihan is back with more tips. The first half is similar to 2017, but the second half has different examples. Highly recommended. Get the slides here.
* [Advanced Design Patterns for DynamoDB (reInvent 2019)](https://t.co/fRtp2X3Vgg?amp=1). The most recent edition of Rick Houlihan's DynamoDB talk.
* [Data Modeling with DynamoDB (reInvent 2019)](https://www.youtube.com/watch?v=DIQVJqiSUkE). A gentler introduction to DynamoDB single-table concepts. Watch this video if Rick's is too advanced.
* [Using (and ignoring) DynamoDB Best Practices in Serverless (ServerlessConf NYC 2019)](https://acloud.guru/series/serverlessconf-nyc-2019/view/dynamodb-best-practices). This talk focuses on using DynamoDB in Serverless applications.

## 参考资料:

* [Awesome DynamoDB](https://github.com/alexdebrie/awesome-dynamodb) -- A GitHub repo with DynamoDB links and resources
* [DynamoDB landing page](https://aws.amazon.com/dynamodb/)
* [AWS Developer Guide Docs](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
* [AWS CLI reference for DynamoDB](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html)
* [Boto3 (Python client library for AWS) docs](http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html)
* [Javascript client library for AWS](https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/DynamoDB.html)
* [Document Client cheat sheet (Javascript)](https://github.com/dabit3/dynamodb-documentclient-cheat-sheet).Created by [Nader Dabit](https://twitter.com/dabit3)
* [原文链接](https://www.dynamodbguide.com/additional-reading)