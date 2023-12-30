data "aws_caller_identity" "current" {}

data "archive_file" "example" {
  type        = "zip"
  source_file = "${local.functions_path}/${local.source_filename}"
  output_path = "./${local.source_filename}.zip"
}
