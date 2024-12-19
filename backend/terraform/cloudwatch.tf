# terraform/cloudwatch.tf
resource "aws_cloudwatch_event_rule" "autoscale_check" {
  name                = "${var.project_name}-${var.environment}-autoscale-check"
  description         = "Trigger storage auto-scaling check"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "autoscale_check" {
  rule      = aws_cloudwatch_event_rule.autoscale_check.name
  target_id = "AutoscaleCheck"
  arn       = aws_lambda_function.autoscale_handler.arn
}

resource "aws_cloudwatch_log_group" "upload_handler" {
  name              = "/aws/lambda/${aws_lambda_function.upload_handler.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "autoscale_handler" {
  name              = "/aws/lambda/${aws_lambda_function.autoscale_handler.function_name}"
  retention_in_days = 14
}
