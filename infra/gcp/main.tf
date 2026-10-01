terraform {
  required_version = ">= 1.6.0, < 2.0.0"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 6.0" }
  }
}
variable "project_id" { type = string }
variable "region" { type = string }
variable "bucket_name" { type = string }
provider "google" {
  project = var.project_id
  region  = var.region
}
resource "google_storage_bucket" "source" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  versioning { enabled = true }
}
resource "google_pubsub_topic" "telemetry" { name = "fabric-telemetry" }
resource "google_pubsub_subscription" "fabric" {
  name                       = "fabric-telemetry-consumer"
  topic                      = google_pubsub_topic.telemetry.id
  ack_deadline_seconds       = 60
  message_retention_duration = "86400s"
}
output "bucket" { value = google_storage_bucket.source.name }
output "subscription" { value = google_pubsub_subscription.fabric.id }
