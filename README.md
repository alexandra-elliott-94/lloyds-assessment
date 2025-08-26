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



Assumptions:

For the views, the brief was:
```Design a BigQuery schema that enables business users to:
 - View total and average monthly spend per customer.
 - Identify the top 5% of customers by lifetime value. ```
I think there are a number of ways this could be done, but which would be useful to a business user? 
So for `total and average monthly spend per customer` i've gone with a routine that calculates the year, month, total spent that month and average spent per month upto and including that month. 
For `Identify the top 5% of customers by lifetime value. `
lifetime value of banking customers seems like a very complicated metric to calculate, so for the purposes of this demo lifetime value will mean total spend. I have made a simple view that gives the top 5% of customers by spend, but i don't know if thats very useful in a business context and would contain no history for audit purposes. e.g.  a senario in which the crm team would like to see the top 5% of customers once a week to send a promotion. I have included a routine for this 


- transactions data only represents outgoing transactions 



Improvements 
- dedupe data before landing in bucket using hashes
- make customers table a slowly changing dimension table with history 
- change dataflow job to land data in a data lake in the format {data_string, source, ingestion_timestamp}, then use routines or more dataflow jobs to unpack the data. Keep the routines in a seperate repo for each service (customers, transactions) along with any table definitions and views.  
- dynamically create terraform config from a simpler config file, so it can be used by teams with less terraform knowledge
- use dataflow flex templates to launch the job on different sized machines for different sized data
-  