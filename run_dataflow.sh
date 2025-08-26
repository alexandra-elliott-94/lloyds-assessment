#!/bin/bash
python3 ingest_data.py \
--project=natural-pipe-469020-h2 \
--region=europe-west2  \
--runner=DataflowRunner \
--machine_type=e2-standard-2 \
--staging_location=gs://$natural-pipe-469020-h2-dataflow-bucket/test \
--temp_location=gs://natural-pipe-469020-h2-dataflow-bucket/test \
--save_main_session \
--dataset=data_landing \
--table=customers \
--source_file=gs://natural-pipe-469020-h2-data-landing/data/customers.csv

python3 ingest_data.py \
--project=natural-pipe-469020-h2 \
--region=europe-west2  \
--runner=DataflowRunner \
--machine_type=e2-standard-2 \
--staging_location=gs://$natural-pipe-469020-h2-dataflow-bucket/test \
--temp_location=gs://natural-pipe-469020-h2-dataflow-bucket/test \
--save_main_session \
--dataset=data_landing \
--table=transactions \
--source_file=gs://natural-pipe-469020-h2-data-landing/data/transactions.csv 