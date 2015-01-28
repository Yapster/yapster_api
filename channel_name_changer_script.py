from yap.models import *
from users.models import *
from notification.models import *
from notification.serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from apns import APNs, Frame, Payload
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import time
import random
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import boto
from django.conf import settings

'''
def change_channels_paths():
	
	channels = Channel.objects.all()
	for channel in channels:
		print channel.channel_name
		channel.icon_explore_path_clicked='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_clicked.png'
		channel.icon_explore_path_unclicked ='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_unclicked.png'
		channel.icon_yap_path_clicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_clicked.png'
		channel.icon_yap_path_unclicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_unclicked.png'
		channel.save(update_fields=['icon_explore_path_clicked','icon_explore_path_unclicked','icon_yap_path_clicked','icon_yap_path_unclicked'])

#change_channels_paths()

def change_channels_path():
	
	channels = Channel.objects.all()
	for channel in channels:
		print channel.channel_name
		channel.icon_explore_path_clicked='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_clicked.png'
		channel.icon_explore_path_unclicked ='yapsterchannels/' + str(channel).lower() + '/explore/' + str(channel).lower() + '_explore_unclicked.png'
		channel.icon_yap_path_clicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_clicked.png'
		channel.icon_yap_path_unclicked='yapsterchannels/' + str(channel).lower() + '/yap/' + str(channel).lower() + '_yap_unclicked.png'
		channel.save(update_fields=['icon_explore_path_clicked','icon_explore_path_unclicked','icon_yap_path_clicked','icon_yap_path_unclicked'])

#change_channels_path()

def delete_channels():

	channels = Channel.objects.all()
	for channel in channels: 
		print channel.channel_name
		channel.delete()

#delete_channels()

channels = [
'Art',
'Beauty',
'Business',
'Celebrity Gossip',
'Comedy',
'Education',
'Family',
'Fashion',
'Finance',
'Food and Drinks',
'Health and Fitness',
'Misc',
'Movies',
'Music',
'News',
'Night Life',
'Organizations',
'Politics',
'Religion',
'Sports',
'Summer',
'Technology',
'TV',

]

def create_channels():

print("starting channels")
#''
total = len(channels)
print total
for i,channel in enumerate(channels):
	channel_string = channel.replace(" ","")
	print(channel + " " + str(i) + "/" + str(total))
	Channel.objects.create(channel_name=channel,
		channel_description=channel,
		icon_explore_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_clicked.png',
		icon_explore_path_unclicked ='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_unclicked.png',
		icon_yap_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_clicked.png',
		icon_yap_path_unclicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_unclicked.png')


#create_channels()


def recalculate_yap_count():

	users = User.objects.all()
	for user in users:
		print user
		total_number_of_yaps_for_this_user = len(Yap.objects.filter(user=user,is_active=True))
		user.profile.yap_count = total_number_of_yaps_for_this_user
		user.profile.save(update_fields=['yap_count'])

recalculate_yap_count()


def delete_useless_users():
	users = User.objects.filter(pk__gte=31)
	for user in users:
		print user
		users_listens = user.listens.all()
		for listen in users_listens:
			print listen.pk
			listen.delete()
		users_likes = user.likes.all()
		for like in users_likes:
			print like.pk
			like.delete()
		users_reyaps = user.reyaps.all()
		for reyap in users_reyaps:
			print reyap.pk
			reyap.delete()
		users_yaps = user.yaps.all()
		for yap in users_yaps:
			print yap.pk
			yap.delete()
		users_notifications = user.notifications.all()
		for notification in users_notifications:
			notification.delete()
		user.delete()

delete_useless_users()
#'''
'''
def change_all_users_to_listen_stream_public():
	users = User.objects.all()
	for user in users:
		print user
		user_info = UserInfo.objects.get(pk=user.pk)
		user_info.modify_account(listen_stream_public=True)

change_all_users_to_listen_stream_public()
#'''
'''
def testing_123_push_notification():
	users = User.objects.filter(is_active=True)
	for user in users:
		sessions = user.sessions.filter(is_active=True)
		for session in sessions:
			if session == '<>':
				continue
			apns = APNs(use_sandbox=settings.APNS_USE_SANDBOX,cert_file=settings.APNS_CERT_FILE,key_file=settings.APNS_KEY_FILE)
			#Send a notification
			token_hex1 = session.session_device_token
			token_hex2 = token_hex1.replace('<','')
			token_hex3 = token_hex2.replace('>','')
			token_hex = token_hex3.replace(' ','')
			badge_number = Notification.objects.filter(is_active=True,user=user,user_read_flag=False).count()
			alert = "Download Yapster's new update, follow our official account @yapsterapp and yap us!"
			payload = Payload(alert=alert,sound="default",badge=badge_number,custom={"user_id":user.pk,"profile_user_id":159})
			apns.gateway_server.send_notification(token_hex,payload)

testing_123_push_notification()
#'''
'''
def investor_email():
	template_html = 'investor_update_email.html'
	template_text = 'investor_update_email.txt'
	from_email = settings.DEFAULT_FROM_EMAIL
	subject = 'Investor Update for Week of 7/14/14 - Yapster,Inc.'
	html = get_template(template_html)
	text = get_template(template_text)
	to = 'jb3991@nyu.edu'
	name = 'Mr. Jonathan Bach'
	d = Context({'name':name})
	text_content = text.render(d)
	html_content = html.render(d)
	msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

#investor_email()
#'''

from boto.s3.key import Key

def change_metadata():
	yaps = Yap.objects.all()
	for yap in yaps:
		yap_path = yap.audio_path
		c = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
		b = c.get_bucket('yapsterapp')
		k = b.get_key(yap_path)
		k.content_type = 'audio/mpeg'
		a = k.content_type
		print yap.pk, a

change_metadata()