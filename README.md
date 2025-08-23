# lloyds-assessment
  
WIP. 
  
Run to create a landing bucket for your csvs and a bucket to be used by the dataflow job. 
`terraform -chdir=terraform/ init`  
`terraform -chdir=terraform/ plan`  
`terraform -chdir=terraform/ apply`  
  
Run the upload script to upload csv to cloud storage  
`chmod +x ./upload_file.sh`  
`./upload_file.sh`  
  
Run data flow job  
`chmod +x ./run_dataflow.sh`  
`./run_dataflow.sh`  