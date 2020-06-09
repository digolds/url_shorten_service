# DynamoDB的环境搭建

后续的内容将涉及DynamoDB的API，比如通过AWS CLI来操作DynamoDB。为了操作DynamoDB，我们需要搭建DynamoDB的环境。

## 安装 AWS CLI

[AWS CLI](https://aws.amazon.com/cli/)是AWS提供的命令行工具，开发者通过使用这个工具能够方便地使用AWS所提供的云服务，包括DynamoDB服务。运行以下命令来安装AWS CLI：

```bash
$ pip install awscli
```

如果在安装过程种遇到困难，可以参考这里[进行](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)安装。

## 获取认证和授权

如果你打算使用AWS提供的DynamoDB服务，那么你需要正确地设置认证和授权的权限，具体需要参考[官方文档](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)。

比较简单的一种方式是授予开发者所有关于DynamoDB操作的权限，其策略定义如下：

```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "*"
    }
  ]
}
```

一旦你在AWS上申请了一个账号并得到了能够操作DynamoDB的凭证，那么你还需要将这个凭证通过以下方式设置到本地电脑

```bash
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json
```

## 在本地搭建DynamoDB服务

AWS提供了可在本地运行的DynamoDB，它可以在本地运行，免除了凭证的设置和避免了使用云端DynamoDB所产生的费用。

想要在本地使用DynamoDB，那么根据以下指令下载和安装DynamoDB：

```bash
$ curl -O https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip
$ unzip dynamodb_local_latest.zip
$ rm dynamodb_local_latest.zip
```

下载好之后，通过以下命令在本地启动DynamoDB实例：

```bash
$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

Initializing DynamoDB Local with the following configuration:
Port:	8000
InMemory:	false
DbPath:	null
SharedDb:	true
shouldDelayTransientStatuses:	false
CorsParams:	*
```

如果你看到以上信息，那么说明，DynamoDB已经成功在本地上运行了。接下来便可以操作DynamoDB了。

## 本地 $LOCAL 变量

如果你使用本地的DynamoDB来练习，那么你需要在每一个指令后面追加以下参数：

```bash
--endpoint-url http://localhost:8000
```

当然以上参数可以设置成环境变量，并用较短的环境变量来替代，如下所示：

```bash
$ export LOCAL="--endpoint-url http://localhost:8000"

$ aws dynamodb list-tables $LOCAL
```

如果使用操作本地DynamoDB，那么需要在每一个操作指令后面追加`$LOCAL`，如上所示。如果操作的是云端的DynamoDB，那么无需在每一个指令后面追加`$LOCAL`。

* [原文链接](https://www.dynamodbguide.com/environment-setup)