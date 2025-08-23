#!/bin/bash

gcloud storage cp ./schemas gs://natural-pipe-469020-h2-dataflow-bucket/schemas --recursive

gcloud storage cp ./data/customers.csv gs://natural-pipe-469020-h2-data-landing/customers.csv