#!/usr/bin/python

import datetime
import time
import subprocess
import boto3
import os
import shutil
import gzip

# config
AWS_KEY = os.environ['LambdaAccessKeyId']
AWS_SECRET = os.environ['LambdaSecretAccessKey']
BUCKET = os.environ['s3Bucket']

#DB array goes host, db, user, password
DATABASES 	= [(os.environ['hostDB1'],os.environ['databaseDB1'], os.environ['userDB1'], os.environ['passDB1'])]

def lambda_handler(event, context):

	# move binary to tmp folder and set as executable
	shutil.copyfile('/var/task/mysqldump', '/tmp/mysqldump')
	os.chmod('/tmp/mysqldump', 0755)

	# get current date and time
	timer = datetime.datetime.utcnow().isoformat()+ "Z"
	timer = str(timer).replace(':', '.')	

	# init s3 client
	s3 = boto3.client('s3')

	# folder & path stuff
	dt = datetime.date.today()
	tf = str(dt.year)+'-'+str(dt.month)
	path_base = '/tmp/dumps/tf'
	
	#create dir to storage dumps
	subprocess.call(['mkdir', '-p', path_base])

	# loops db and make backups
	for i in DATABASES:
		host = i[0]
		database = i[1]
		user = i[2]
		password =  i[3]
		dump_name = 'production-'+database+'-'+timer+'.sql'
		file_name = os.path.join(path_base, dump_name)

		print ''
		print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - '
		print ''
		print 'Dump from: '+database

		#run mysqldump as a subprocess
		p = subprocess.Popen("/tmp/mysqldump -h" + host + " -u" + user + " -p'" + password + "' --all-databases > " + file_name, shell=True)
		p.communicate()

		# sleep while we wait for dump to complete
		time.sleep(20)
		
		# upload to s3
		s3.upload_file(file_name,BUCKET,dump_name)

		# lambda cleanup		
		os.remove('/tmp/mysqldump')
		os.remove(file_name)