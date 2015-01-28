import boto
from django.conf import settings

def connect_s3(bucket_name):
	s3 = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
	try:
		b = s3.get_bucket(bucket_name)
	except:
		return 'There is no such bucket.'
	return b
