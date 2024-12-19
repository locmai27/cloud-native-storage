# terraform/variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "elastic-storage"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "base_bucket_name" {
  description = "Base name for S3 buckets"
  type        = string
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.9"
}
