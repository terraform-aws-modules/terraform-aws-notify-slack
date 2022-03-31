terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.8"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0"
    }
  }
}
