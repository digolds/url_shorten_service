terraform {
  required_version = "= 0.12.19"
}

provider "aws" {
  version = "= 2.46"
  region  = "us-east-2"
}

data "aws_iam_policy_document" "self_policy" {
  statement {
    sid    = "Stmt1529862213126"
    effect = "Allow"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${local.bucket_name}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

locals {
  bucket_name = "static-web-for-prod"
}


resource "aws_s3_bucket" "static_web_site" {
  bucket = local.bucket_name
  acl    = "public-read"

  policy = data.aws_iam_policy_document.self_policy.json

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  force_destroy = true

  versioning {
    enabled = true
  }
}

output "s3_obj" {
  value = aws_s3_bucket.static_web_site
}
