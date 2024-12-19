# terraform/s3.tf
# Initial storage bucket
resource "aws_s3_bucket" "storage" {
  bucket = "${var.base_bucket_name}-${var.environment}-001"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "storage" {
  bucket = aws_s3_bucket.storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER"
    }
  }
}

# Bucket for Lambda deployment packages
resource "aws_s3_bucket" "lambda_storage" {
  bucket = "${var.project_name}-${var.environment}-lambda"
  tags   = local.common_tags
}
