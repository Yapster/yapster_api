import django_facebook
from aws import *
import datetime
from open_facebook import OpenFacebook
from users.models import *
from users.models import Settings
import json

def share_yap_on_facebook(user,facebook_access_token,yap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_connection_flag == True:
		if user.settings.facebook_account_id != None:
			name = str(yap.user.first_name) + ' ' + str(yap.user.last_name) + " (@" + str(user.username) + ") posted a yap on Yapster"
			if user.settings.facebook_page_connection_flag == True:
				api_url = str(user.settings.facebook_page_id) + '/feed'
			elif user.settings.facebook_page_connection_flag == False:
				api_url = str(user.settings.facebook_account_id) + '/feed'
			url = "http://web.yapster.co/yap/" + str(yap.pk)
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			if yap.description != None:
				fb_share_yap_message = "\"" + str(yap.title.encode('utf-8')) + "\" - " + str(yap.description) + " " + "\n" + str(url)
			elif yap.description == None:
				fb_share_yap_message = "\"" + str(yap.title.encode('utf-8')) + "\" " + str(url)
			fb_share_yap_description = "Listen to this yap - and other yaps from " + str(user.first_name) + " " + str(user.last_name) 
			fb_share_yap = facebook.set(api_url, link=url, picture=yap_picture_url, name=name, description=fb_share_yap_description,message=fb_share_yap_message)['id']
			return fb_share_yap
		else:
			return "User has not set up a facebook_account_id."
	else:
		return "User has not connected their account with Facebook."

def share_yap_story_on_facebook(user,facebook_access_token,yap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_connection_flag == True:
		if user.settings.facebook_account_id != None:
			name = str(yap.title.encode('utf-8'))
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:yap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			url = "http://web.yapster.co/yap/" + str(yap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			if yap.description != None:
				fb_yap = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name),"description":json.dumps(yap.description)})['id']
			elif yap.description == None:
				fb_yap = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name)})['id']
			if user.settings.facebook_page_connection_flag == True:
				story_api_url = str(user.settings.facebook_page_id) + '/yapster_fb:yapped'
			elif user.settings.facebook_page_connection_flag == False:
				story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:yapped'
			fb_share_yap = facebook.set(story_api_url,yap=fb_yap)['id']
			return fb_share_yap
		else:
			return "User has not set up a facebook_account_id."
	else:
		return "User has not set up their account with Facebook."

def share_reyap_on_facebook(user,facebook_access_token,reyap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") reyapped a yap on Yapster"
		if user.settings.facebook_page_connection_flag == True:
			api_url = str(user.settings.facebook_page_id) + '/feed'
		elif user.settings.facebook_page_connection_flag == False:
			api_url = str(user.settings.facebook_account_id) + '/feed'
		url = "http://web.yapster.co/reyap/" + str(reyap.pk)
		b = connect_s3(bucket_name="yapsterapp")
		if reyap.yap.picture_flag == True:
			reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		elif reyap.yap.picture_flag == False:
			reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		if reyap.yap.description != None:
			fb_share_reyap_message = "\"" + str(reyap.yap.title.encode('utf-8')) + "\" - " + str(reyap.yap.description) + " " + "\n" + str(url)
		elif reyap.yap.description == None:
			fb_share_reyap_message = "\"" + str(reyap.yap.title.encode('utf-8')) + "\" " + str(url)
		fb_share_reyap_description = "Listen to this reyap - and other reyaps/yaps from " + str(reyap.user.first_name) + " " + str(reyap.user.last_name) 
		fb_share_reyap = facebook.set(api_url, link=url, picture=reyap_picture_url, name=name, description=fb_share_reyap_description,message=fb_share_reyap_message)['id']
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_reyap_story_on_facebook(user,facebook_access_token,reyap):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		if user.settings.facebook_page_connection_flag == True:
			story_api_url = str(user.settings.facebook_page_id) + '/yapster_fb:reyapped'
		elif user.settings.facebook_page_connection_flag == False:
			story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:yapped'
		name = str(reyap.yap.title.encode('utf-8'))
		url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
		b = connect_s3(bucket_name="yapsterapp")
		if reyap.yap.picture_flag == True:
			reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		elif reyap.yap.picture_flag == False:
			reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		if reyap.reyap_flag == True:
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:reyap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name),"description":json.dumps(reyap.yap.description)})['id']
			elif reyap.yap.description == None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,reyap=object_reyapped)['id']
		elif reyap.reyap_flag == False:
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:yap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if reyap.yap.description != None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name),"description":json.dumps(reyap.yap.description)})['id']
			elif reyap.yap.description == None:
				object_reyapped = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,yap=object_reyapped)['id']
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_like_story_on_facebook(user,facebook_access_token,yap=None,reyap=None):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		if user.settings.facebook_page_connection_flag == True:
			story_api_url = str(user.settings.facebook_page_id) + '/yapster_fb:liked'
		elif user.settings.facebook_page_connection_flag == False:
			story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:liked'
		if yap != None and reyap == None:
			name = str(yap.title.encode('utf-8'))
			url = "http://web.yapster.co/yap/" + str(yap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:yap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name),"description":json.dumps(yap.description)})['id']
			elif yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,yap=object_liked)['id']
		elif yap == None and reyap != None:
			name = str(reyap.yap.title.encode('utf-8'))
			url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if reyap.yap.picture_flag == True:
				reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			elif reyap.yap.picture_flag == False:
				reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:reyap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name),"description":json.dumps(reyap.yap.description)})['id']
			elif reyap.yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,reyap=object_liked)['id']
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_listen_story_on_facebook(user,facebook_access_token,yap=None,reyap=None):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		if user.settings.facebook_page_connection_flag == True:
			story_api_url = str(user.settings.facebook_page_id) + '/yapster_fb:listened_to'
		elif user.settings.facebook_page_connection_flag == False:
			story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:listened_to'
		if yap != None and reyap == None:
			name = yap.title.encode('utf-8')
			url = "http://web.yapster.co/yap/" + str(yap.pk)
			b = connect_s3(bucket_name="yapsterapp")
			if yap.picture_flag == True:
				yap_picture_key = b.get_key(yap.picture_cropped_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			elif yap.picture_flag == False:
				yap_picture_key = b.get_key(user.profile.profile_picture_path)
				yap_picture_url = yap_picture_key.generate_url(expires_in=600)
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:yap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:yap'
			if yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name),"description":json.dumps(yap.description)})['id']
			elif yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":yap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,yap=object_liked)['id']
		elif yap == None and reyap != None:
			name = str(reyap.yap.title.encode('utf-8'))
			url = "http://web.yapster.co/reyap/" + str(reyap.pk) + '/'
			b = connect_s3(bucket_name="yapsterapp")
			if reyap.yap.picture_flag == True:
				reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			elif reyap.yap.picture_flag == False:
				reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
				reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
			if user.settings.facebook_page_connection_flag == True:
				object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:reyap'
			elif user.settings.facebook_page_connection_flag == False:
				object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:reyap'
			if reyap.yap.description != None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name),"description":json.dumps(reyap.yap.description)})['id']
			elif reyap.yap.description == None:
				object_liked = facebook.set(object_api_url, object={"url":url,"image":reyap_picture_url,"title":json.dumps(name)})['id']
			fb_share_reyap = facebook.set(story_api_url,reyap=object_liked)['id']
		return fb_share_reyap
	else:
		return "User has not set up a facebook_account_id."

def share_new_following_story_on_facebook(user,user_followed,facebook_access_token):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_account_id != None:
		if user.settings.facebook_page_connection_flag == True:
			story_api_url = str(user.settings.facebook_page_id) + '/yapster_fb:followed'
		elif user.settings.facebook_page_connection_flag == False:
			story_api_url = str(user.settings.facebook_account_id) + '/yapster_fb:followed'
		name = str(user_followed.first_name) + ' ' + str(user_followed.last_name) + ' (@' + str(user_followed.username.encode('utf-8') +')')
		url = "http://yapster.co"
		b = connect_s3(bucket_name="yapsterapp")
		if user_followed.profile.profile_picture_flag == True:
			user_followed_picture_key = b.get_key(user_followed.profile.profile_picture_cropped_path)
			user_followed_picture_url = user_followed_picture_key.generate_url(expires_in=600)
		elif user_followed.profile.profile_picture_flag == False:
			user_followed_picture_url = None
		if user.settings.facebook_page_connection_flag == True:
			object_api_url = str(user.settings.facebook_page_id) + '/objects/yapster_fb:user'
		elif user.settings.facebook_page_connection_flag == False:
			object_api_url = str(user.settings.facebook_account_id) + '/objects/yapster_fb:user'
		description = 'Check out what @' +  str(user.username) + ' and @' + str(user_followed.username) + ' have been yapping about and listening to!'
		user_followed_object = facebook.set(object_api_url, object={"url":url,"image":user_followed_picture_url,"title":name})['id']
		fb_share = facebook.set(story_api_url,user=user_followed_object)['id']
		return fb_share
	else:
		return "User has not set up a facebook_account_id."

def joined_yapster_post_on_facebook(user,facebook_access_token):
	facebook = OpenFacebook(facebook_access_token)
	url = "http://yapster.co"
	name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") just joined Yapster!"
	description = "Click here and download the app to listen to what " + " @" + str(user.username) + " has been yapping about."
	b = connect_s3(bucket_name="yapsterapp")
	fb_share_yapster_picture_key = b.get_key('/yapstersocialmedia/yapster_white_y_green_background')
	fb_share_yapster_picture_url = fb_share_yapster_picture_key.generate_url(expires_in=600)
	if user.settings.facebook_connection_flag == True:
		if user.settings.facebook_page_connection_flag == True:
			api_url = str(user.settings.facebook_page_id) + '/feed'
		elif user.settings.facebook_page_connection_flag == False:
			api_url = str(user.settings.facebook_account_id) + '/feed'
		facebook_post = facebook.set(api_url,link=url,picture=fb_share_yapster_picture_url,name=name,description=description)['id']
		return facebook_post
	else:
		return 'User has not setup Facebook Connection'

def connected_facebook_and_yapster_post_on_facebook(user,facebook_access_token):
	facebook = OpenFacebook(facebook_access_token)
	url = "http://yapster.co"
	name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") just connected Yapster to Facebook!"
	description = "Click here and download the app to listen to what " + " @" + str(user.username) + " has been yapping about."
	b = connect_s3(bucket_name="yapsterapp")
	fb_share_yapster_picture_key = b.get_key('/yapstersocialmedia/yapster_white_y_green_background')
	fb_share_yapster_picture_url = fb_share_yapster_picture_key.generate_url(expires_in=600)
	if user.settings.facebook_connection_flag == True:
		if user.settings.facebook_page_connection_flag == True:
			api_url = str(user.settings.facebook_page_id) + '/feed'
		elif user.settings.facebook_page_connection_flag == False:
			api_url = str(user.settings.facebook_account_id) + '/feed'
		facebook_post = facebook.set(api_url,link=url,picture=fb_share_yapster_picture_url,name=name,description=description)['id']
		return facebook_post
	else:
		return 'User has not setup Facebook Connection'

def get_all_of_users_facebook_friends(user,facebook_access_token):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_connection_flag == True:
		facebook_friends = facebook.get('me/friends',fields="id,name,picture")['data']
		return facebook_friends

def get_all_of_users_facebook_friends_on_yapster(user,facebook_access_token):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_connection_flag == True:
		facebook_friends = facebook.get('me/friends',fields="id")['data']
		this_users_facebook_friends_on_yapster = [friend_facebook_id['id'] for friend_facebook_id in facebook_friends if Settings.objects.filter(is_active=True,facebook_account_id=friend_facebook_id['id']).exists() == True]
		return this_users_facebook_friends_on_yapster

def share_yap_or_reyap_on_facebook(user,facebook_access_token,yap=None,reyap=None):
	facebook = OpenFacebook(facebook_access_token)
	if user.settings.facebook_connection_flag == True:
		if user.settings.facebook_account_id != None:
			if user.settings.facebook_page_connection_flag == True:
				api_url = str(user.settin1gs.facebook_page_id) + '/feed'
			elif user.settings.facebook_page_connection_flag == False:
				api_url = str(user.settings.facebook_account_id) + '/feed'
		else:
			return "User has not set up a facebook_account_id."
	else:
		return "User has not connected their account with Facebook."
	if yap != None and reyap == None:
		name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") shared a yap from Yapster"
		url = "http://web.yapster.co/yap/" + str(yap.pk)
		b = connect_s3(bucket_name="yapsterapp")
		if yap.picture_flag == True:
			yap_picture_key = b.get_key(yap.picture_cropped_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		elif yap.picture_flag == False:
			yap_picture_key = b.get_key(user.profile.profile_picture_path)
			yap_picture_url = yap_picture_key.generate_url(expires_in=600)
		if yap.description != None:
			fb_share_yap_message = "\"" + str(yap.title.encode('utf-8')) + "\" - " + str(yap.description) + " " + "\n" + str(url)
		elif yap.description == None:
			fb_share_yap_message = "\"" + str(yap.title.encode('utf-8')) + "\" " + str(url)
		fb_share_yap_description = "Listen to this yap - and other yaps from " + str(yap.user.first_name) + " " + str(yap.user.last_name)
		fb_share_yap = facebook.set(api_url, link=url, picture=yap_picture_url, name=name, description=fb_share_yap_description,message=fb_share_yap_message)['id']
		return fb_share_yap
	if yap == None and reyap != None:
		name = str(user.first_name) + ' ' + str(user.last_name) + " (@" + str(user.username) + ") shared a reyap from Yapster"
		url = "http://web.yapster.co/reyap/" + str(reyap.pk)
		b = connect_s3(bucket_name="yapsterapp")
		if reyap.yap.picture_flag == True:
			reyap_picture_key = b.get_key(reyap.yap.picture_cropped_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		elif reyap.yap.picture_flag == False:
			reyap_picture_key = b.get_key(reyap.user.profile.profile_picture_path)
			reyap_picture_url = reyap_picture_key.generate_url(expires_in=600)
		if reyap.yap.description != None:
			fb_share_reyap_message = "\"" + str(reyap.yap.title.encode('utf-8')) + "\" - " + str(reyap.yap.description) + " " + "\n" + str(url)
		elif reyap.yap.description == None:
			fb_share_reyap_message = "\"" + str(reyap.yap.title.encode('utf-8')) + "\" " + str(url)
		fb_share_reyap_description = "Listen to this reyap - and other reyaps/yaps from " + str(reyap.user.first_name) + " " + str(reyap.user.last_name) 
		fb_share_reyap = facebook.set(api_url, link=url, picture=reyap_picture_url, name=name, description=fb_share_reyap_description,message=fb_share_reyap_message)['id']
		return fb_share_reyap





