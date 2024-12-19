# terraform/dynamodb.tf
resource "aws_dynamodb_table" "bucket_metadata" {
  name           = "${var.project_name}-${var.environment}-bucket-metadata"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "name"
  range_key      = "partition_id"

  attribute {
    name = "name"
    type = "S"
  }

  attribute {
    name = "partition_id"
    type = "N"
  }

  attribute {
    name = "bucket_status"
    type = "S"
  }

  global_secondary_index {
    name               = "status-index"
    hash_key          = "bucket_status"
    projection_type    = "ALL"
  }

  tags = local.common_tags
}

resource "aws_dynamodb_table" "file_metadata" {
  name           = "${var.project_name}-${var.environment}-file-metadata"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "file_id"

  attribute {
    name = "file_id"
    type = "S"
  }

  tags = local.common_tags
}
