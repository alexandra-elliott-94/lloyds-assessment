#!/bin/bash

python3 convert_bq_to_json.py

gcloud storage cp ./schemas gs://natural-pipe-469020-h2-dataflow-bucket/schemas --recursive --cache-control=no-cache

gcloud storage cp ./data/customers.csv gs://natural-pipe-469020-h2-data-landing/customers.csv --cache-control=no-cache