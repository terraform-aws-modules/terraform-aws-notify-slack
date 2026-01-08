terraform {
  required_version = ">= 1.5.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.28"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.0"
    }
  }
}
