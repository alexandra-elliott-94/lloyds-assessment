# lloyds-assessment
  
WIP. 
  
Run to create a landing bucket for your csvs and a bucket to be used by the dataflow job. 
`terraform -chdir=terraform/ init`  
`terraform -chdir=terraform/ plan`  
`terraform -chdir=terraform/ apply`  
  
Run the upload script to upload csv to cloud storage  
`chmod +x ./upload_files.sh`  
`./upload_files.sh`  
  
Run data flow job  
`chmod +x ./run_dataflow.sh`  
`./run_dataflow.sh`  

Improvements 
- change dataflow job to land data in a data lake in the format {data_string, source, ingestion_timestamp}, then use routines or more dataflow jobs to unpack the data. Keep the routines in a seperate repo for each service (customers, transactions) along with any table definitions and views. 
- dynamically create terraform config from a simpler config file, so it can be used by teams with less terraform knowledge
- use dataflow flex templates to launch the job on different sized machines for different sized data
-  