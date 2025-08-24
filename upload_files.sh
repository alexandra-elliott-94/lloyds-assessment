#!/bin/bash

python3 convert_bq_to_json.py

gcloud storage rm gs://natural-pipe-469020-h2-dataflow-bucket/schemas --recursive
gcloud storage rm gs://natural-pipe-469020-h2-data-landing/data --recursive

gcloud storage cp ./schemas gs://natural-pipe-469020-h2-dataflow-bucket/schemas --recursive --cache-control=no-cache

gcloud storage cp ./data gs://natural-pipe-469020-h2-data-landing --recursive --cache-control=no-cache