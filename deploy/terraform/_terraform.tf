terraform {
  required_version = ">= 1.11.0"

  backend "s3" {
    bucket = "fase4-terraform-state"
    key    = "fase4-auth-service/terraform.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14.1"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.7.2"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.1.0"
    }

    jose = {
      source  = "aiyor-tf/jose"
      version = "0.1.0"
    }

  }
}