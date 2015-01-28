from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from users.models import *
from yap.serializers import *
import facebook as facebook
import twitter as twitter
from operator import attrgetter
from yap.scripts import create_yap,create_library
import dateutil.parser

class CreateYap(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			title = kwargs.get('title')
			description = kwargs.get('description')
			length = kwargs.get('length')
			audio_path = kwargs.get('audio_path')
			library_id = kwargs.get('library_id')
			library = Library.objects.get(pk=library_id)
			picture_flag = kwargs.get('picture_flag')
			if picture_flag == True:
				picture_path = kwargs.get('picture_path')
				picture_cropped_flag = kwargs.get('picture_cropped_flag')
				if picture_cropped_flag == True:
					picture_cropped_path = kwargs.get('picture_cropped_path')
					yap = create_yap(user=user,title=title,description=description,length=length,audio_path=audio_path,library=library,picture_flag=picture_flag,picture_path=picture_path,picture_cropped_flag=picture_cropped_path,picture_cropped_path=picture_cropped_path)
			else:
				yap = create_yap(user=user,title=title,description=description,length=length,audio_path=audio_path,library=library)
			return Response({"valid":True,"message":"Yap has successfully been created.","yap_id":yap.pk})
		else:
			return Response(check[0])

class CreateLibrary(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		print kwargs
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			title = kwargs.get('title')
			description = kwargs.get('description')
			picture_flag = kwargs.get('picture_flag')
			if picture_flag == True:
				picture_path = kwargs.get('picture_path')
				picture_cropped_flag = kwargs.get('picture_cropped_flag')
				if picture_cropped_flag == True:
					picture_cropped_path = kwargs.get('picture_cropped_path')
					library = create_library(user=user,title=title,description=description,picture_flag=picture_flag,picture_path=picture_path,picture_cropped_flag=picture_cropped_path,picture_cropped_path=picture_cropped_path)
			return Response({"valid":True,"message":"Library has successfully been created.","library_id":library.pk})
		else:
			return Response(check[0])

class DeleteYap(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			yap = Yap.objects.get(pk=kwargs['yap_id'])
			response = yap.delete(is_user_deleted=False)
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class DeleteLibrary(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			library = Library.objects.get(pk=kwargs['library_id'])
			response = library.delete(is_user_deleted=False)
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class SubscribeUser(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			subscribing_user_id = kwargs.get('subscribing_user_id')
			response = user.functions.subscribe_user(subscribing_user_id=subscribing_user_id)
			# subscribed_user = User.objects.get(pk=kwargs.get('user_subscribing_id'))
			# subscribe_user = SubscribeUser.objects.get(user=user,subscribed_user=subscribed_user,is_active=True)
			# if follower_request.is_accepted == True:
			# 	if user.settings.facebook_connection_flag == True:
			# 		if 'facebook_shared_flag' in kwargs:
			# 			if kwargs.get('facebook_shared_flag') == True:
			# 				facebook_shared_story = facebook.share_new_following_story_on_facebook(user=user,user_followed=user_requested,facebook_access_token=kwargs.get('facebook_access_token'))
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class SubscribeLibrary(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			subscribing_library_id = kwargs.get('subscribing_library_id')
			response = user.functions.subscribe_library(subscribing_library_id=subscribing_library_id)
			# subscribed_user = User.objects.get(pk=kwargs.get('user_subscribing_id'))
			# subscribe_user = SubscribeUser.objects.get(user=user,subscribed_user=subscribed_user,is_active=True)
			# if follower_request.is_accepted == True:
			# 	if user.settings.facebook_connection_flag == True:
			# 		if 'facebook_shared_flag' in kwargs:
			# 			if kwargs.get('facebook_shared_flag') == True:
			# 				facebook_shared_story = facebook.share_new_following_story_on_facebook(user=user,user_followed=user_requested,facebook_access_token=kwargs.get('facebook_access_token'))
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])

class UnsubscribeUser(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			#print user.functions
			response = user.functions.unsubscribe_user(kwargs['unsubscribing_user_id'])
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])


class UnsubscribeLibrary(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}

		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			#print user.functions
			response = user.functions.follow_accept(kwargs['unsubscribing_library_id'])
			return Response({"valid":True,"message":response})
		else:
			return Response(check[0])


class Listen(APIView):

	def post(self,request):
		"""example json
		"""
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			yap = Yap.objects.get(pk=kwargs['yap_id'])
			if kwargs.get('longitude'):
				longitude = kwargs.pop('longitude')
			if kwargs.get('latitude'):
				latitude = kwargs.pop('latitude')
			if kwargs.get('facebook_shared_flag') == True:
				if kwargs.get('facebook_access_token'):
					if user.settings.facebook_connection_flag == True:
						facebook_access_token = kwargs.pop('facebook_access_token')
					else:
						return Response({"valid":False,"message":"User hasn't connected their account to facebook."})
				else:
					return Response({"valid":False,"message":"Yap cannot be shared to facebook without an facebook_access_token."})
			if kwargs.get('longitude') and kwargs.get('latitude'):
				response = user.functions.listen(yap=yap,longitude=longitude,latitude=latitude)
			else:
				response = user.functions.listen(yap)
			if isinstance(response,dict):
				return Response(response)
			else:
				if kwargs.get('facebook_shared_flag') == True and user.settings.facebook_connection_flag == True:
						f1 = facebook.share_listen_story_on_facebook(user=user,facebook_access_token=facebook_access_token,yap=yap)
				return Response({"valid":True,"message":"success","Listen_id":response.pk})
		else:
			return Response(check[0])

class ListenSetTimeListened(APIView):

	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			response = listen.set_time_listened(time_listened=kwargs['time_listened'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class ListenSkipClicked(APIView):
	def post(self,request):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user=user,session_id=kwargs['session_id'])
		if check[1]:
			listen = Listen.objects.get(pk=kwargs['listen_id'])
			listen_click = ListenClick.objects.create(user=user,listen=listen,skipped_flag=True,time_clicked=kwargs['time_clicked'])
			return Response({"valid":True,"message":"success","listen_id":listen.pk})
		else:
			return Response(check[0])

class PushNotificationObjectCall(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		obj = request['obj']
		obj_type = request['obj_type']
		if check[1]:
			if obj_type == "yap":
				try:
					result = Yap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This yap does not exist.'})
			elif obj_type == "reyap":
				try:
					result = Reyap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This reyap does not exist.'})
			serialized = PushNotificationObjectSerializer(result,data=self.request.DATA,context={'user':user})
			return Response(serialized.data)
		else:
			return Response(check[0])

class ShareToFacebook(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		obj = request['obj']
		obj_type = request['obj_type']
		if check[1]:
			facebook_access_token = request.pop('facebook_access_token')
			if obj_type == "yap":
				try:
					result = Yap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This yap does not exist.'})
				facebook_post = facebook.share_yap_or_reyap_on_facebook(user=user,yap=result,facebook_access_token=facebook_access_token)
				return Response({'valid':True,'message':'Yap has successfully been shared on Facebook.'})
			elif obj_type == "reyap":
				try:
					result = Reyap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This reyap does not exist.'})
				facebook_post = facebook.share_yap_or_reyap_on_facebook(user=user,reyap=result,facebook_access_token=facebook_access_token)
				return Response({'valid':True,'message':'Reyap has successfully been shared on Facebook.'})
		else:
			return Response(check[0])

class ShareToTwitter(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		obj = request['obj']
		obj_type = request['obj_type']
		if check[1]:
			twitter_access_token_key = request.pop('twitter_access_token_key')
			twitter_access_token_secret = request.pop('twitter_access_token_secret')
			if obj_type == "yap":
				try:
					result = Yap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This yap does not exist.'})
				twitter_post = twitter.share_yap_or_reyap_on_twitter(user=user,yap=result,twitter_access_token_key=twitter_access_token_key,twitter_access_token_secret=twitter_access_token_secret)
				return Response({'valid':True,'message':'Yap has successfully been shared on Twitter.'})
			elif obj_type == "reyap":
				try:
					result = Reyap.objects.get(pk=obj,is_active=True)
				except ObjectDoesNotExist:
					return Response({'valid':False,'message':'This reyap does not exist.'})
				twitter_post = twitter.share_yap_or_reyap_on_twitter(user=user,reyap=result,twitter_access_token_key=twitter_access_token_key,twitter_access_token_secret=twitter_access_token_secret)
				return Response({'valid':True,'message':'Reyap has successfully been shared on Twitter.'})
		else:
			return Response(check[0])


