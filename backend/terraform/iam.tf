# terraform/iam.tf
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-${var.environment}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:CreateBucket",
          "s3:PutBucketEncryption",
          "s3:PutBucketVersioning",
          "s3:PutLifecycleConfiguration"
        ]
        Resource = [
          "arn:aws:s3:::${var.base_bucket_name}-${var.environment}-*",
          "arn:aws:s3:::${var.base_bucket_name}-${var.environment}-*/*"
        ]
      }
    ]
  })
}

# Add these data sources at the top of your iam.tf file
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}