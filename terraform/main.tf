resource "google_storage_bucket" "data-landing" {
 name          = "${var.project_id}-data-landing"
 location      = "EU"
 storage_class = "STANDARD"
 force_destroy = true

 uniform_bucket_level_access = true
 
 }

 resource "google_storage_bucket" "dataflow_bucket" {
  name          = "${var.project_id}-dataflow-bucket"
  location      = "EU"
  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true
  soft_delete_policy {
    retention_duration_seconds = 0
  }
  

}

resource "google_bigquery_dataset" "data_landing" {
  dataset_id                  = "data_landing"
  friendly_name               = "data_landing"
  description                 = "Dataset for data landing zone"
  location                    = "EU"

  labels = {
    env = "default"
  }
}

resource "google_bigquery_dataset" "invalid_data_landing" {
  dataset_id                  = "invalid_data_landing"
  friendly_name               = "invalid_data_landing"
  description                 = "Dataset for data landing zone"
  location                    = "EU"

  labels = {
    env = "default"
  }
}

resource "google_bigquery_table" "customers" {
  dataset_id = google_bigquery_dataset.data_landing.dataset_id
  table_id   = "customers"
  friendly_name = "Customers Table"
  description   = "Table to hold customer data"

  schema = file("./../schemas/customers/customers_bq.json")
  deletion_protection = false
  labels = {
    env = "default"
  }
}

resource "google_bigquery_table" "customers_invalid" {
  dataset_id = google_bigquery_dataset.invalid_data_landing.dataset_id
  table_id   = "customers"
  friendly_name = "Customers Invalid Table"
  description   = "Table to hold invalid rows from customers data"

  schema = file("./../schemas/invalid.json")
  deletion_protection = false
  labels = {
    env = "default"
  }
}


