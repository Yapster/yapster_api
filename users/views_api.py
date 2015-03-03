from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from users.serializers import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.models import *
from datetime import datetime
from django.utils import timezone
from yap.serializers import *
from yapster_utils import check_session,automatic_sign_in_check_session_id_and_device,sign_in_check_session_id_and_device
from recommendating_users import recommended_users_to_follow_according_to_questionaire
import facebook as facebook
import twitter as twitter
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['PUT'])
def session_id(request):
	username = request.DATA['username']
	password = request.DATA['password']
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return Response({"message":"Invalid username","valid":False})
	if user.check_password(password):
		session_id = user.session.set_id()
		return Response({"message":"success","valid":True,"session_id":session_id})
	else:
		return Response({"valid":False,"message":"This is the incorrect password."})

class SignUpVerifyEmail(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		email = kwargs.get('email')
		if User.objects.filter(email=email).exists() == True:
			return Response({"valid":False,"message":"This email already exists"})
		else:
			return Response({"valid":True,"message":"This email is available"})

class SignUpVerifyUsername(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		username = kwargs.get('username')
		if User.objects.filter(username=username).exists() == True:
			return Response({"valid":False,"message":"This username already exists"})
		else:
			return Response({"valid":True,"message":"This username is available"})

class SignUp(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		#kwargs = {str(k):str(v[0]) for k,v in dict(request.DATA).iteritems()}
		dob = datetime.datetime.strptime(kwargs['date_of_birth'],"%Y-%m-%d").date()
		age = (datetime.date.today() - dob).days/365.0
		if not age > 13 or not age < 120:
			return Response({"valid":False,"message":"Invalid age."})
		if kwargs.get('country_id'):
			try:
				country = Country.objects.get(pk=kwargs.pop('country_id'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The country you have selected doesn't exist."})
			kwargs['country'] = country
		if kwargs.get('us_state_id') and country.name == "United States":
			try:
				us_state = USState.objects.get(pk=kwargs.pop('us_state_id'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
			kwargs['us_state'] = us_state
		if kwargs.get('us_zip_code'):
			try:
				us_zip_code = USZIPCode.objects.get(name=kwargs.pop('us_zip_code'))
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
			kwargs['us_zip_code'] = us_zip_code
		if kwargs.get('city_name'):
			if country.name == "United States" and kwargs.get('us_state',None) and kwargs.get('us_zip_code',None):
				city = City.objects.get_or_create(name=kwargs.pop('city_name'),us_state=us_state,country=country,us_zip_code=us_zip_code)
			else:
				city = City.objects.get_or_create(name=kwargs.pop('city_name'),country=country)
			kwargs['city'] = city[0]
		if 'facebook_connection_flag' in kwargs:
			if kwargs.get('facebook_connection_flag') == True:
				if 'facebook_account_id' in kwargs:
					if 'facebook_access_token' in kwargs:
						facebook_access_token = kwargs.pop('facebook_access_token')
					else:
						return Response({"valid":False,"message":"You have connected your account with Facebook but not given a Facebook access token."})
				else:
					return Response({"valid":False,"message":"You have connected your account to Facebook but not given your Facebook account id."})
			else:
				pass
		if kwargs.get('twitter_shared_flag') == True:
				if kwargs.get('twitter_access_token_key'):
					if kwargs.get('twitter_access_token_secret'):
						if user.settings.twitter_connection_flag == True:
							twitter_access_token_key = kwargs.pop('twitter_access_token_key')
							twitter_access_token_secret = kwargs.pop('twitter_access_token_secret')
						else:
							return Response({"valid":False,"message":"User hasn't connected their account to Twitter."})
					else:
						return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_secret."})
				else:
					return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_key."})
		ids = UserFunctions.create(**kwargs)			
		if ids[0] == False:
			return Response({"valid":False,"message":ids[1]})
		else:
			template_html = 'welcome_new_user_email.html'
			template_text = 'welcome_new_user_email.txt'
			from_email = settings.DEFAULT_FROM_EMAIL
			subject = 'Welcome to Yapster!'
			html = get_template(template_html)
			text = get_template(template_text)
			user = User.objects.get(pk=ids[0])
			to = user.email
			d = Context({'user':user})
			text_content = text.render(d)
			html_content = html.render(d)
			msg = send_mail(subject,html_content, from_email, [to], fail_silently=False)
			if 'facebook_connection_flag' in kwargs:
				if kwargs.get('facebook_connection_flag') == True:
					if 'facebook_account_id' in kwargs:
						if 'facebook_access_token' in kwargs:
							facebook_post = facebook.joined_yapster_post_on_facebook(user=user,facebook_access_token=facebook_access_token)
						else:
							return Response({"valid":False,"message":"You have connected your account with Facebook but not given a Facebook access token."})
					else:
						return Response({"valid":False,"message":"You have connected your account to Facebook but not given your Facebook account id."})
				else:
					pass
			if kwargs.get('twitter_shared_flag') == True:
				if kwargs.get('twitter_access_token_key'):
					if kwargs.get('twitter_access_token_secret'):
						if user.settings.twitter_connection_flag == True:
							twitter_post = twitter.joined_yapster_post_on_twitter(user=user,twitter_access_token_key=twitter_access_token_key,twitter_access_token_secret=twitter_access_token_secret)
						else:
							return Response({"valid":False,"message":"User hasn't connected their account to Twitter."})
					else:
						return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_secret."})
				else:
					return Response({"valid":False,"message":"Yap cannot be shared without a twitter_access_token_key."})
			return Response({"valid":True,"user_id":ids[0],"session_id":ids[4]})


class SignIn(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		option = request['option']
		option_type = request['option_type']
		password = request['password']
		try:
			if option_type == "email":
				user = User.objects.get(email=option)
			else:
				user = User.objects.get(username=option)
		except User.DoesNotExist:
			return Response({"valid":False,"message":"User does not exist"})
		if user.check_password(password) == True:
			device_type = request.get('device_type')
			identifier = request['identifier']
			check = sign_in_check_session_id_and_device(user=user,device_type=device_type,identifier=identifier)
			if check[1] == True:
				user.last_login = datetime.datetime.now()
				user.save(update_fields=['last_login'])
				if ForgotPasswordRequest.objects.filter(user=user,is_active=True).exists():
					forgot_password_request = ForgotPasswordRequest.objects.get(user=user,is_active=True,is_user_deleted=False)
					forgot_password_request.reset_password_security_code_not_used_and_user_signed_in()
				return Response({"user_id":user.pk,"valid":True,"session_id":check[0]})
			else:
				return Response({"valid":False,"message":"You must send a device identifier to sign in."})
		else:
			return Response({"user_id":user.pk,"valid":False,"message":"invalid password"})

class AutomaticSignIn(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		device_type = request.get('device_type')
		identifier = request.get('identifier')
		session_id = request.get('session_id')
		check = automatic_sign_in_check_session_id_and_device(user=user,session_id=session_id,device_type=device_type,identifier=identifier)
		if check[1]:
			return Response({"valid":True,"user_id":user.pk,"session_id":request['session_id']})
		else:
			return Response({"valid":False,"message":check[0]})


class SignOut(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request['session_id'])

		if check[1]:
			try: 
				session = Session.objects.get(pk=request['session_id'])
			except ObjectDoesNotExist:
				return Response({"valid":False,"message":"This session doesn't exist."})
			session.sign_out_device()
			return Response({"valid":True})
		else:
			return Response(check[0])

class LoadDashboardSubscribedUsers(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			# start = datetime.datetime.now()
			dashboard = Dashboard.objects.get(user=user,is_active=True)
			if 'page' in request:
				page = request.get('page')
				amount = request.get('amount')
				before_for_loop_1 = datetime.datetime.now()
				# print "before for loop_1 " + str(before_for_loop_1 - start)
				subscribed_users = [sub_user.subscribed_user for sub_user in SubscribeUser.objects.filter(user=user,is_active=True)]
				after_subscribed_users = datetime.datetime.now()
				# print "after_for_loop_1 " + str(after_subscribed_users - before_for_loop_1)
				paginator = Paginator(object_list=subscribed_users,per_page=amount,allow_empty_first_page=False)
				try:
					dashboard_users_subscribed = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					return Response({"valid":False,"message":"Page is not an integer."})
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					return Response({"valid":True,"data":None})
			else:
				if dashboard.check_date_calculated_subscribed_most_listened_users() == False:
					dashboard.recalculate_subscribed_most_listened_users()
				after_subscribed_users = datetime.datetime.now()
				# print "after_for_loop_1" + str(after_subscribed_users - start)
				dashboard_users_subscribed = dashboard.subscribed_most_listened_users.all()
			serialized = UserSerializer(dashboard_users_subscribed,many=True,data=self.request.DATA,context={'user':user})
			end = datetime.datetime.now()
			# print "After serializerd " + str(end-after_subscribed_users)
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadDashboardSubscribedLibraries(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			dashboard = Dashboard.objects.get(user=user,is_active=True)
			if 'page' in request:
				page = request.get('page')
				amount = request.get('amount')
				subscribed_libraries = [sub_library.subscribed_library for sub_library in SubscribeLibrary.objects.filter(user=user,is_active=True)]
				paginator = Paginator(object_list=subscribed_libraries,per_page=amount,allow_empty_first_page=False)
				try:
					dashboard_libraries_subscribed = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					return Response({"valid":False,"message":"Page is not an integer."})
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					return Response({"valid":True,"data":None})
			else:
				if dashboard.check_date_calculated_subscribed_most_listened_libraries() == False:
					dashboard.recalculate_subscribed_most_listened_libraries()
				dashboard_libraries_subscribed = dashboard.subscribed_most_listened_libraries.all()
			serialized = LibraryPreviewSerializer(dashboard_libraries_subscribed,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadDashboardExploreUsers(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			dashboard = Dashboard.objects.get(user=user,is_active=True)
			if 'page' in request:
				page = request.get('page')
				amount = request.get('amount')
				minutes = 2880
				time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
				yaps = Yap.objects.filter(is_active=True,date_created__gte=time)
				users = User.objects.filter(yaps__in=yaps,is_active=True)
				if user.listens.filter(is_active=True).exists() == True:
					key = listening_score_for_users
					reverse = True
				else:
					key = lambda *args: random.random()
					reverse = False
				explore_users = sorted(set(users),key=key, reverse=reverse)[:30]
				paginator = Paginator(object_list=explore_users,per_page=amount,allow_empty_first_page=False)
				try:
					dashboard_users_explored = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					return Response({"valid":False,"message":"Page is not an integer."})
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					return Response({"valid":True,"data":None})
			else:
				if dashboard.check_date_calculated_explore_top_users() == False:
					dashboard.recalculate_explore_top_users()
				dashboard_users_explored = dashboard.explore_top_users.all()
			serialized = UserSerializer(dashboard_users_explored,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadDashboardExploreLibraries(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			dashboard = Dashboard.objects.get(user=user,is_active=True)
			if 'page' in request:
				page = request.get('page')
				amount = request.get('amount')
				minutes = 2880
				time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
				yaps = Yap.objects.filter(is_active=True,date_created__gte=time)
				libraries = Library.objects.filter(yaps__in=yaps,is_active=True)
				if self.user.listens.filter(is_active=True).exists() == True:
					key = listening_score_for_libraries
					reverse = True
				else:
					key = lambda *args: random.random()
					reverse = False
				explore_top_libraries = sorted(set(libraries),key=key,reverse=reverse)[:30]
				paginator = Paginator(object_list=explore_top_libraries,per_page=amount,allow_empty_first_page=False)
				try:
					dashboard_libraries_explored = paginator.page(page)
				except PageNotAnInteger:
					# If page is not an integer, deliver first page.
					return Response({"valid":False,"message":"Page is not an integer."})
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					return Response({"valid":True,"data":None})
			else:
				if dashboard.check_date_calculated_explore_top_libraries() == False:
					dashboard.recalculate_subscribed_top_libraries()
				dashboard_libraries_explored = dashboard.explore_top_libraries.all()
			serialized = LibraryPreviewSerializer(dashboard_libraries_subscribed,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadProfileInfo(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			profile_user = User.objects.get(pk=request['profile_user_id'])
			serialized = UserSerializer(profile_user,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadProfileLibraries(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			profile_user = User.objects.get(pk=request['profile_user_id'])
			page = request.get('page',1)
			amount = request.get('amount',5)
			libraries = [lib_order.library for lib_order in profile_user.library_order.filter(is_active=True).order_by('-order')][:amount]
			paginator = Paginator(object_list=libraries,per_page=amount,allow_empty_first_page=False)
			try:
				profile_libraries = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				return Response({"valid":False,"message":"Page is not an integer."})
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				return Response({"valid":True,"data":None})
			serialized = LibraryPreviewSerializer(profile_libraries,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadLibraryInfo(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			profile_user = User.objects.get(pk=request['profile_user_id'])
			page = request.get('page',1)
			amount = request.get('amount',5)
			libraries = [lib_order.library for lib_order in profile_user.library_order.filter(is_active=True).order_by('-order')][:amount]
			paginator = Paginator(object_list=libraries,per_page=amount,allow_empty_first_page=False)
			try:
				profile_libraries = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				return Response({"valid":False,"message":"Page is not an integer."})
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				return Response({"valid":True,"data":None})
			serialized = LibraryPreviewSerializer(profile_libraries,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadLibraryYaps(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user,request.pop('session_id'))
		if check[1]:
			library = User.objects.get(pk=request['library_id'])
			page = request.get('page',1)
			amount = request.get('amount',5)
			yaps_list = [yp_order.yap for yp_order in library.library_yap_order.filter(is_active=True).order_by('-order')][:amount]
			paginator = Paginator(object_list=yaps_list,per_page=amount,allow_empty_first_page=False)
			try:
				yaps = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				return Response({"valid":False,"message":"Page is not an integer."})
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				return Response({"valid":True,"data":None})
			serialized = AbstractYapSerializer(yaps,many=True,data=self.request.DATA,context={'user':user})
			return Response({"valid":True,"data":serialized.data})
		else:
			return Response({"valid":False,"message":check[0]})

class LoadSettings(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			settings = user.settings
			return Response(SettingsSerializer(settings).data)
		else:
			return Response(check[0])

class EditProfilePicture(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			info = UserInfo.objects.get(username=user.username)
			profile_picture_edited = info.edit_profile_picture(**request)
			return Response(profile_picture_edited)
		else:
			return Response(check[0])

class DeleteProfilePicture(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request.pop('user_id'))
		check = check_session(user=user,session_id=request.pop('session_id'))
		if check[1]:
			info = UserInfo.objects.get(username=user.username)
			profile_picture_deleted = info.delete_profile_picture()
			return Response(profile_picture_deleted)
		else:
			return Response(check[0])

class EditProfile(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if kwargs.get('country_id'):
				try:
					country = Country.objects.get(pk=kwargs.pop('country_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The country you have selected doesn't exist."})
				kwargs['country'] = country
			if kwargs.get('us_state_id') and country.country_name == "United States":
				try:
					us_state = USState.objects.get(pk=kwargs.pop('us_state_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
				kwargs['us_state'] = us_state
			if kwargs.get('us_zip_code'):
				try:
					us_zip_code = USZIPCode.objects.get(us_zip_code=kwargs.pop('us_zip_code'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
				kwargs['us_zip_code'] = us_zip_code
			if kwargs.get('city_name') or kwargs.get('city_name') == '':
				if country.country_name == "United States" and kwargs.get('us_state',None) and kwargs.get('us_zip_code',None):
					city = City.objects.get_or_create(city_name=kwargs.pop('city_name'),us_state=us_state,country=country,us_zip_code=us_zip_code,is_active=True)
				else:
					city = City.objects.get_or_create(city_name=kwargs.pop('city_name'),country=country,is_active=True)
				kwargs['city'] = city[0]
			info1 = UserInfo.objects.get(username=user.username)
			info2 = info1.modify_account(**kwargs)
			if isinstance(info2,str):
				return Response({"valid":False,"message":info2})
			else:
				if 'facebook_connection_flag' in kwargs:
					if User.objects.get(username=self.username).settings.facebook_connection_flag == True:
						facebook_post = facebook.connected_facebook_and_yapster_post_on_facebook(user=user,facebook_access_token=facebook_access_token)
				if 'twitter_connection_flag' in kwargs:
					if User.objects.get(username=self.username).settings.twitter_connection_flag == True:
						facebook_post = twitter.connected_twitter_and_yapster_post_on_twitter(user=user,facebook_access_token=facebook_access_token)
				return Response({"valid":True,"message":"Your profile has successfully been edited."})
		else:
			return Response(check[0])

class EditSettings(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if kwargs.get('country_id'):
				try:
					country = Country.objects.get(pk=kwargs.pop('country_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The country you have selected doesn't exist."})
				kwargs['country'] = country
			if kwargs.get('us_state_id') and country.country_name == "United States":
				try:
					us_state = USState.objects.get(pk=kwargs.pop('us_state_id'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The US State you have selected doesn't exist."})
				kwargs['us_state'] = us_state
			if kwargs.get('us_zip_code'):
				try:
					us_zip_code = USZIPCode.objects.get(us_zip_code=kwargs.pop('us_zip_code'))
				except ObjectDoesNotExist:
					return Response({"valid":False,"message":"The ZIP Code you have selected doesn't exist."})
				kwargs['us_zip_code'] = us_zip_code
			if kwargs.get('city_name'):
				if country.country_name == "United States" and kwargs.get('us_state',None) and kwargs.get('us_zip_code',None):
					city = City.objects.get_or_create(city_name=kwargs.pop('city_name'),us_state=us_state,country=country,us_zip_code=us_zip_code)
				else:
					city = City.objects.get_or_create(city_name=kwargs.pop('city_name'),country=country)
				kwargs['city'] = city[0]
			if 'facebook_connection_flag' in kwargs:
				if kwargs.get('facebook_connection_flag') == True:
					if 'facebook_access_token' in kwargs:
						facebook_access_token = kwargs.get('facebook_access_token')
					else:
						kwargs['facebook_connection_flag'] = False
						kwargs['facebook_account_id'] = None
					if "facebook_page_connection_flag" not in kwargs:
						kwargs['facebook_page_connection_flag'] = False
						kwargs['facebook_page_id'] = None
				else:
					kwargs['facebook_connection_flag'] = False
					kwargs['facebook_account_id'] = None
					kwargs['facebook_page_connection_flag'] = False
					kwargs['facebook_page_id'] = None
			if 'twitter_connection_flag' in kwargs:
				if kwargs.get('twitter_connection_flag') == True:
					if 'twitter_access_token_key' in kwargs:
						if 'twitter_access_token_secret' in kwargs:
							twitter_access_token_key = kwargs.pop('twitter_access_token_key')
							twitter_access_token_secret = kwargs.pop('twitter_access_tHoken_secret')
						else:
							return Response({"valid":False,"message":"There must be both twitter_access_token_key and twitter_access_token_secret to connect and share to Twitter. "})
					else:
						return Response({"valid":False,"message":"There must be both twitter_access_token_key and twitter_access_token_secret to connect and share to Twitter. "})
				else:
					kwargs['twitter_connection_flag'] = False
					kwargs['twitter_account_id'] = None
			info1 = UserInfo.objects.get(username=user.username)
			info2 = info1.modify_account(**kwargs)
			new_settings = user.settings
			serialized = SettingsSerializer(new_settings,data=self.request.DATA)
			return Response(serialized.data)
		else:
			return Response(check[0])

class DisconnectFacebookAccount(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if 'facebook_connection_flag' in kwargs:
				if kwargs.get('facebook_connection_flag') == False:
					facebook_changes = {}
					facebook_changes['facebook_connection_flag'] = False
					facebook_changes['facebook_account_id'] = None
					facebook_changes['facebook_page_connection_flag'] = False
					facebook_changes['facebook_page_id'] = None
					facebook_changes['facebook_share_reyap'] = False
					info1 = UserInfo.objects.get(username=user.username)
					info2 = info1.modify_account(**facebook_changes)
					new_settings = user.settings
					serialized = SettingsSerializer(new_settings,data=self.request.DATA)
					return Response(serialized.data)
				else:
					return Response({"valid":False,"message":"The facebook_connection_flag must be false to disconnect the Facebook Account."})
			else:
				return Response({"valid":False,"message":"There must be a facebook_connection_flag sent which must be false to disconnect the Facebook Account."})
		else:
			return Response(check[0])

class DisconnectTwitterAccount(APIView):

	def post(self,request,**kwargs):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs.pop('user_id'))
		check = check_session(user=user,session_id=kwargs.pop('session_id'))
		if check[1]:
			if 'twitter_connection_flag' in kwargs:
				if kwargs.get('twitter_connection_flag') == False:
					twitter_changes = {}
					twitter_changes['twitter_connection_flag'] = False
					twitter_changes['twitter_account_id'] = None
					twitter_changes['twitter_share_reyap'] = False
					info1 = UserInfo.objects.get(username=user.username)
					info2 = info1.modify_account(**twitter_changes)
					new_settings = user.settings
					serialized = SettingsSerializer(new_settings,data=self.request.DATA)
					return Response(serialized.data)
				else:
					return Response({"valid":False,"message":"The twitter_connection_flag must be false to disconnect the Twitter Account."})
			else:
				return Response({"valid":False,"message":"There must be a twitter_connection_flag sent which must be false to disconnect the Twitter Account."})
		else:
			return Response(check[0])

class ForgotPasswordRequestForEmail(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		if User.objects.filter(is_active=True,email=request['email']).exists():
			user = User.objects.get(is_active=True,email=request['email'])
			forgot_password_request = ForgotPasswordRequest.objects.get_or_create(is_active=True,user=user,user_email=user.email)
			forgot_password_request = forgot_password_request[0]
			return Response({"valid":True,"message":"Please check your email for your security code to reset your password."})
		else:
			return Response({"valid":False,"message":"There is no active user with this email."})

class ForgotPasswordRequestForResetPassword(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		option = request['option']
		option_type = request['option_type']
		try:
			if option_type == "email":
				user = User.objects.get(email=option)
			else:
				user = User.objects.get(username=option)
		except User.DoesNotExist:
			return Response({"valid":False,"message":"User does not exist"})
		if ForgotPasswordRequest.objects.filter(is_active=True,user=user,user_email=user.email).exists():
			forgot_password_request = ForgotPasswordRequest.objects.get(is_active=True,user=user,user_email=user.email)
			if forgot_password_request.reset_password_security_code == request['reset_password_security_code']:
				forgot_password_request.reset_password_security_code_used()
				user.set_password(request['new_password'])
				user.save(update_fields=['password'])
				return Response({"valid":True,"message":"Your password has been successfully changed."})
			else:
				return Response({"valid":False,"message":"The security code doesn't match what was sent to your email."})
		else:
			return Response({"valid":False,"message":"You have not requested for a security code. Please click the forgot password button on the sign up screen and request for a security code."})







