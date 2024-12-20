# terraform/lambda.tf
resource "aws_lambda_function" "upload_handler" {
  filename         = "../upload_function.zip"
  function_name    = "${var.project_name}-${var.environment}-upload-handler"
  role            = aws_iam_role.lambda_role.arn
  handler         = "src.functions.upload.handler.handle"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 256

  environment {
    variables = {
      BASE_BUCKET_NAME = aws_s3_bucket.storage.id
      ENVIRONMENT     = var.environment
    }
  }

  layers = [aws_lambda_layer_version.dependencies.arn]
}

# Lambda Layer for dependencies
resource "aws_lambda_layer_version" "dependencies" {
  filename            = "../lambda_layer.zip"
  layer_name          = "${var.project_name}-${var.environment}-dependencies"
  compatible_runtimes = ["python3.9"]
}

