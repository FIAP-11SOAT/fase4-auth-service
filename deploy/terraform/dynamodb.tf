resource "aws_dynamodb_table" "users" {
  name         = "${local.project_name}-users"
  billing_mode = "PAY_PER_REQUEST"

  hash_key = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "tax_id"
    type = "S"
  }

  global_secondary_index {
    name            = "TaxIDIndex"
    hash_key        = "tax_id"
    projection_type = "ALL"
  }

  tags = {
    Name        = "${local.project_name}-users"
    Description = "DynamoDB table to store user information"
  }
}

resource "aws_dynamodb_table_item" "create_anonymous_user" {
  hash_key   = "id"
  table_name = "${local.project_name}-users"

  item = <<ITEM
    {
      "id": {"S": "${uuid()}"},
      "tax_id": {"S": "00000000000"},
      "email": {"S": "anonymous@anonymous.com"},
      "name": {"S": "Anonymous User"},
      "user_type": {"S": "customers"}
    }
  ITEM

  depends_on = [aws_dynamodb_table.users]
}

resource "aws_dynamodb_table_item" "create_employee_user" {
  hash_key   = "id"
  table_name = "${local.project_name}-users"

  item = <<ITEM
    {
      "id": {"S": "${uuid()}"},
      "tax_id": {"S": "11111111111"},
      "email": {"S": "employee@employee.com"},
      "name": {"S": "Default Employee"},
      "user_type": {"S": "employees"}
    }
  ITEM

  depends_on = [aws_dynamodb_table.users]
}
