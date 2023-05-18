terraform {
  required_version = ">= 1.0"

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
