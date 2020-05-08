terraform {
  required_version = "= 0.12.19"
}

resource "aws_lambda_function" "lambda_function_instance" {
  filename         = "../init_version.zip"
  function_name    = var.function_name
  role             = data.terraform_remote_state.role_for_lambda_state.outputs.role_obj.arn
  handler          = "${var.handler_name}.${var.handler_name}"
  source_code_hash = filebase64sha256("../init_version.zip")
  runtime          = "python3.6"

  environment {
    variables = {
      TABLE_NAME = data.terraform_remote_state.urls_table_state.outputs.table_obj.name
    }
  }
}

data "terraform_remote_state" "vpc_app_state" {
  backend = "local"

  config = {
    path = var.path_vpc_app_state
  }
}

data "terraform_remote_state" "vpc_peering_state" {
  backend = "local"

  config = {
    path = var.path_vpc_peering_state
  }
}

data "terraform_remote_state" "role_for_lambda_state" {
  backend = "local"

  config = {
    path = var.path_role_for_lambda_state
  }
}

data "terraform_remote_state" "urls_table_state" {
  backend = "local"

  config = {
    path = var.path_urls_table_state
  }
}
