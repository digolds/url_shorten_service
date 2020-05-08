terraform {
  required_version = "= 0.12.19"
}

data "aws_iam_policy_document" "self_policy" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${var.bucket_name}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}


resource "aws_s3_bucket" "static_web_site" {
  bucket        = var.bucket_name
  acl           = "public-read"
  force_destroy = true
  policy        = data.aws_iam_policy_document.self_policy.json

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  versioning {
    enabled = true
  }
}

output "s3_obj" {
  value = aws_s3_bucket.static_web_site
}

variable "bucket_name" {
  type    = string
  default = "shorten-url-service"
}
