# Enable APIs
resource "google_project_service" "google_api" {
  for_each = toset(var.apis)

  project = var.project_id
  service = each.key
}

# Create a Service Account
resource "google_service_account" "cloud_run_service_account" {
  project      = var.project_id
  account_id   = "cloud-run-service-account"
  display_name = "Cloud Run Service Account"
}

# Create the Artifac Registry Repository
resource "google_artifact_registry_repository" "repository" {
  location      = var.location
  repository_id = "${var.cloud_run_service_name}-repository"
  format        = "DOCKER"
}

# Create a Cloud Run Service
resource "google_cloud_run_service" "cloud_run_service" {
  project  = var.project_id
  name     = var.cloud_run_service_name
  location = var.location

  template {
    spec {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
      }

      service_account_name = google_service_account.cloud_run_service_account.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  lifecycle {
    ignore_changes = [
      template
    ]
  }
}

# Disable auth for Cloud Run Service
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.cloud_run_service.location
  project  = google_cloud_run_service.cloud_run_service.project
  service  = google_cloud_run_service.cloud_run_service.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
