from TwitterAPI import TwitterAPI
from django.conf import settings
from aws import *
import StringIO
import datetime
import json
from users.models import *

def share_yap_on_twitter(user,yap,twitter_access_token_key,twitter_access_token_secret):
	twitter = TwitterAPI(consumer_key=settings.TWITTER_CONSUMER_KEY,consumer_secret=settings.TWITTER_CONSUMER_SECRET,access_token_key=twitter_access_token_key,access_token_secret=twitter_access_token_secret)
	status = "@" + str(yap.user.username) + " yapped \"" + str(yap.title) + '\" -  web.yapster.co/yap/' + str(yap.pk)
	length_of_status = len(status)
	if yap.picture_flag == True:
		if length_of_status >  118:
			extra_length_of_title = length_of_status - 121
			title = yap.title[:(-extra_length_of_title)].upper() + "..." # -3 for three dots ...
		elif length_of_status <= 118:
			title = yap.title
		b = connect_s3(bucket_name="yapsterapp")
		yap_picture_key = b.get_key(yap.picture_path)
		fp = StringIO.StringIO()
		yap_picture_key.get_file(fp)
		yap_picture = fp.getvalue()
		r = twitter.request('statuses/update_with_media',{'status':status}, {'media[]': yap_picture})
	elif yap.picture_flag == False:
		if length_of_status > 140:
			extra_length_of_title = length_of_status - 143
			title = yap.title[:(-extra_length_of_title)].upper() + "..."
		elif length_of_status > 140:
			title = yap.title
		r = twitter.request('statuses/update',{'status':status})
	#print("Success" if r.status_code == 200 else 'Failure')
	if r.status_code == 200:
		return json.loads(r.text)['id']
	else:
		pass

def joined_yapster_post_on_twitter(user,twitter_access_token_key,twitter_access_token_secret):
	twitter = TwitterAPI(consumer_key=settings.TWITTER_CONSUMER_KEY,consumer_secret=settings.TWITTER_CONSUMER_SECRET,access_token_key=twitter_access_token_key,access_token_secret=twitter_access_token_secret)
	status = "@" + str(user.username) + " just joined @Yapsterapp! Click and download to hear some yaps! web.yapster.co/download/ios"
	length_of_status = len(status)
	if length_of_status >  140:
		extra_length_of_title = length_of_status - 140
		status = status[:(-extra_length_of_title)].upper()
	else:
		status = status
	r = twitter.request('statuses/update',{'status':status})
	if r.status_code == 200:
		return json.loads(r.text)['id']
	else:
		pass

def connected_twitter_and_yapster_post_on_twitter(user,twitter_access_token_key,twitter_access_token_secret):
	twitter = TwitterAPI(consumer_key=settings.TWITTER_CONSUMER_KEY,consumer_secret=settings.TWITTER_CONSUMER_SECRET,access_token_key=twitter_access_token_key,access_token_secret=twitter_access_token_secret)
	status = "@" + str(user.username) + " just connected their @Yapsterapp account to Twitter! Click and download to hear some yaps! web.yapster.co/download/ios"
	length_of_status = len(status)
	if length_of_status >  140:
		extra_length_of_title = length_of_status - 140
		status = status[:(-extra_length_of_title)].upper()
	else:
		status = status
	r = twitter.request('statuses/update',{'status':status})
	if r.status_code == 200:
		return json.loads(r.text)['id']
	else:
		pass