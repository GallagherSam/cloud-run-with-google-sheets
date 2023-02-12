variable "project_id" {
  type = string
}

variable "apis" {
  type = list(string)
}

variable "cloud_run_service_name" {
  type = string
}

variable "location" {
  type = string
}
