resource "google_storage_bucket" "data-landing" {
 name          = "${var.project_id}-data-landing"
 location      = "EU"
 storage_class = "STANDARD"

 uniform_bucket_level_access = true
 }

 resource "google_storage_bucket" "dataflow_bucket" {
  name          = "${var.project_id}-dataflow-bucket"
  location      = "EU"
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  
}