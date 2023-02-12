terraform {
  required_version = ">= 1.2.0"

  backend "gcs" {
    bucket = "YOUR_BUCKET"
    prefix = "YOUR_PREFIX"
  }
}
