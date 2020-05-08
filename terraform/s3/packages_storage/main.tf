terraform {
  required_version = "= 0.12.19"
}

provider "aws" {
  version = "= 2.46"
  region  = "us-east-2"
}

resource "aws_s3_bucket" "packages_storage" {
  bucket = "lambda-packages-url-service"
  acl    = "private"

  force_destroy = true

  versioning {
    enabled = true
  }
  lifecycle {
    prevent_destroy = false
  }
}

output "s3_obj" {
  value = aws_s3_bucket.packages_storage
}
