from diagrams import Diagram
from diagrams.gcp.storage import Storage
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.analytics import Dataflow

with Diagram("Data Ingestion", show=False):
    storage = Storage("Data Landing Bucket")
    dataflow = Dataflow("Dataflow Job")
    biqquery = BigQuery("BigQuery")

    storage >> dataflow >> biqquery