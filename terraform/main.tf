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

  clustering = ["country"]

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
  time_partitioning {
    type          = "DAY"
    field         = "ingestion_timestamp"
  }
}

resource "google_bigquery_table" "transactions" {
  dataset_id = google_bigquery_dataset.data_landing.dataset_id
  table_id   = "transactions"
  friendly_name = "Transactions Table"
  description   = "Table to hold transactions data"

  schema = file("./../schemas/transactions/transactions_bq.json")
  deletion_protection = false
  labels = {
    env = "default"
  }
  time_partitioning {
    type          = "DAY"
    field         = "dt"
  }
  clustering = ["cust_id"]
}

resource "google_bigquery_table" "transactions_invalid" {
  dataset_id = google_bigquery_dataset.invalid_data_landing.dataset_id
  table_id   = "transactions"
  friendly_name = "Transactions Invalid Table"
  description   = "Table to hold invalid rows from transactions data"

  schema = file("./../schemas/invalid.json")
  deletion_protection = false
  labels = {
    env = "default"
  }
  time_partitioning {
    type          = "DAY"
    field         = "ingestion_timestamp"
  }
}
