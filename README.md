This was for python2.7 on AWS Lambda

You will need to do some fixing for python3+

# rds-s3-backup-lambda
Python script to backup RDS databases to an s3 bucket on AWS

# setup 
Ensure your lamda fucntion has access to the RDS instances VPC
Ensure you created an IAM user / role that can write to the s3 bucket
