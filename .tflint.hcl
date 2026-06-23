tflint {
  required_version = ">= 0.60"
}

config {
  format = "compact"
  call_module_type = "local"

  ignore_module = {}
}

plugin "aws" {
  enabled = true
  version = "0.47.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}
