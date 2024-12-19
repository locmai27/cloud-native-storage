# terraform/main.tf
provider "aws" {
  region = var.aws_region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket = "${var.base_bucket_name}-${var.environment}-terraform-state"
    key    = "elastic-storage/terraform.tfstate"
    region = "us-east-1"
  }
}
