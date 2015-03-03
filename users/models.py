from django.db import models
from location.models import *
from yap.models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from users.signals import *
from django.conf import settings
from django.contrib.gis.db import models
import string
import random
import signals
import ast
import datetime
import dateutil.parser

class DeactivatedUserLog(models.Model):
	user_deactivated_user_log_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="deactivate_user_logs")
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		if not self.pk:
			self.user_deactivate_user_log_id = DeactivateUserLog.objects.filter(user=self.user).count() + 1
		super(DeactivateUserLog, self).save(*args, **kwargs)

	def delete(self):
		raise NotImplementedError('ManualOverride objects cannot be deleted.')

class BlackList(models.Model):
	username = models.CharField(max_length=255,unique=True)
	account_created_flag = models.BooleanField(default=False)
	account_created_date = models.DateTimeField(blank=True,null=True)
	blacklisted_date = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	
	def delete(self):
		raise NotImplementedError('BlackList objects cannot be deleted.')


class Profile(models.Model):
	
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)

	user = models.OneToOneField(User,related_name="profile")
	gender_abbreviation = models.CharField(max_length=1, choices=GENDER_CHOICES)
	yap_count = models.BigIntegerField(default=0)
	listen_count = models.BigIntegerField(default=0)
	subscribing_users_count = models.BigIntegerField(default=0)
	subscribing_libraries_count = models.BigIntegerField(default=0)
	subscriber_users_count = models.BigIntegerField(default=0)
	description = models.CharField(blank=True,null=True,max_length=255)
	profile_picture_flag = models.BooleanField(default=False)
	profile_picture_path = models.CharField(blank=True,null=True,max_length=255)
	profile_picture_cropped_flag = models.BooleanField(default=False)
	profile_picture_cropped_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_1_flag = models.BooleanField(default=False)
	web_cover_picture_1_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_2_flag = models.BooleanField(default=False)
	web_cover_picture_2_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_3_flag = models.BooleanField(default=False)
	web_cover_picture_3_path = models.CharField(blank=True,null=True,max_length=255)
	date_of_birth = models.DateField(null=True,blank=True)
	url = models.URLField(max_length=255,null=True,blank=True)
	color_1 = models.CharField(max_length=255,null=True,blank=True)
	color_2 = models.CharField(max_length=255,null=True,blank=True)
	color_3 = models.CharField(max_length=255,null=True,blank=True)
	city = models.ForeignKey(City,related_name="profile_user_city",null=True,blank=True)
	us_state = models.ForeignKey(USState,related_name="profile_user_state",null=True,blank=True)
	us_zip_code = models.ForeignKey(USZIPCode,related_name="profile_user_zip_code",null=True,blank=True)
	country = models.ForeignKey(Country,related_name="profile_user_country",null=True,blank=True)
	phone_number = models.CharField(max_length=20,null=True,blank=True)
	high_security_account_flag = models.BooleanField(default=False)
	verified_account_flag = models.BooleanField(default=False)
	content_provider_approved_date = models.DateField(blank=True,null=True)
	is_reverse_chronological_order_for_libraries = models.BooleanField(default=True)
	is_privileged = models.BooleanField(default=False)
	is_content_provider = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	user_deleted_date = models.DateField(blank=True,null=True)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete a profile, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This profile is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'

	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a profile, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'Profile is already activated.'

	def verify_user(self):
		if not self.verified_account_flag:
			self.verified_account_flag = True
			self.save(update_fields=['verified_account_flag'])
		else:
			return False

	def unverify_user(self):
		if self.verified_account_flag:
			self.verified_account_flag = False
			self.save(update_fields=['verified_account_flag'])
		else:
			return False

	def approve_as_content_provider(self):
		if not self.is_content_provider:
			self.is_content_provider = True
			self.content_provider_approved_date = datetime.datetime.now()
			self.save(update_fields=["is_content_provider","content_provider_approved_date"])


class UserInfo(models.Model):

	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Other'),
	)

	user_id = models.BigIntegerField(primary_key=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	gender_abbreviation = models.CharField(max_length=1,choices=GENDER_CHOICES)
	email = models.EmailField()
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	username = models.CharField(max_length=30,null=True,blank=True)
	date_of_birth = models.DateField()
	description = models.CharField(null=True, blank=True,max_length=255)
	profile_picture_flag = models.BooleanField(default=False)
	profile_picture_path = models.CharField(blank=True,null=True,max_length=255)
	profile_picture_cropped_flag = models.BooleanField(default=False)
	profile_picture_cropped_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_1_flag = models.BooleanField(default=False)
	web_cover_picture_1_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_2_flag = models.BooleanField(default=False)
	web_cover_picture_2_path = models.CharField(blank=True,null=True,max_length=255)
	web_cover_picture_3_flag = models.BooleanField(default=False)
	web_cover_picture_3_path = models.CharField(blank=True,null=True,max_length=255)
	date_of_birth = models.DateField(null=True,blank=True)
	url = models.URLField(max_length=255,null=True,blank=True)
	color_1 = models.CharField(max_length=255,null=True,blank=True)
	color_2 = models.CharField(max_length=255,null=True,blank=True)
	color_3 = models.CharField(max_length=255,null=True,blank=True)
	city = models.ForeignKey(City,related_name="city",blank=True,null=True)
	us_state = models.ForeignKey(USState,related_name="us_state",blank=True,null=True)
	us_zip_code = models.ForeignKey(USZIPCode,related_name="us_zip_code",blank=True,null=True)
	country = models.ForeignKey(Country,related_name="country",blank=True,null=True)
	last_account_modified_date = models.DateTimeField(auto_now_add=True)
	is_privileged = models.BooleanField(default=False)
	is_content_provider = models.BooleanField(default=True)
	high_security_account_flag = models.BooleanField(default=False)
	verified_account_flag = models.BooleanField(default=False)
	facebook_connection_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	facebook_page_connection_flag = models.BooleanField(default=False)
	facebook_page_id = models.BigIntegerField(blank=True,null=True)
	twitter_connection_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_connection_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_connection_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	user_created_latitude = models.FloatField(null=True,blank=True)
	user_created_longitude = models.FloatField(null=True,blank=True)
	user_created_point = models.PointField(srid=4326,null=True,blank=True)
	notify_for_subscribed_libraries = models.BooleanField(default=True)
	notify_for_subscribed_users = models.BooleanField(default=True)
	notify_for_breaking_news = models.BooleanField(default=True)
	notify_for_celebrities = models.BooleanField(default=True)
	notify_for_yapster = models.BooleanField(default=True)
	content_provider_approved_date = models.DateField(blank=True,null=True)
	is_privileged = models.BooleanField(default=False)
	is_content_provider = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	user_deleted_date = models.DateField(blank=True,null=True)
	objects = models.GeoManager()

	def save(self,*args,**kwargs):
		is_created = False
		if not self.pk:
			is_created = True
			self.pk = User.objects.get(username=self.username).pk
		super(UserInfo, self).save(*args, **kwargs)
		if is_created:
			signals.account_created.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username))
				
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete UserInfo, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This UserInfo is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a UserInfo, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'UserInfo is already activated.'

	def modify_account(self,**kwargs):
		'''
		the keyword arguments must be named the names of the models or else a value error is raised

		'''
		if 'facebook_connection_flag' in kwargs:
			if kwargs.get('facebook_connection_flag') == True:
				if 'facebook_access_token' in kwargs:
					facebook_access_token = kwargs.pop('facebook_access_token')
		user = User.objects.get(username=self.username)
		if kwargs.get("current_password"):
			current_password = kwargs.pop("current_password")
			if user.check_password(current_password) == True:
				if kwargs.get("new_password"):
					new_password = kwargs.pop("new_password")
					user.set_password(new_password)
					user.save(update_fields=['password'])
				else:
					return "You must give a new password for this call."
			else:
				return "Your current password was incorrect."

		if kwargs.get("email"):
			email1 = kwargs.pop("email") 
			email2 = email1.replace(' ','')
			email = email2.lower()
			kwargs['email'] = email
			if User.objects.filter(email=email).exists():
				return ("This email has already been used.")
		if kwargs.get("username"):
			username1 = kwargs.pop("username")
			username2 = username1.replace(' ','')
			username = username2.lower()
			kwargs['username'] = username
			if User.objects.filter(username=username).exists() == True:
				return 'This username is unavailable.'
			if BlackList.objects.filter(username=username).exists() == True:
				return 'This username is currently unavailable. Please contact Yapster for more information about creating this account.'

		if kwargs.get("user_country_id") == True and not self.user_country.country_name == "United States":
			kwargs['user_us_state'] = ''
		if kwargs.get("user_us_zip_code") == '':
			user_us_zip_code = None
			kwargs['user_us_zip_code'] = user_us_zip_code
		fields = self._meta.get_all_field_names()
		for item in kwargs.iteritems():
			field = item[0]
			change = item[1]
			if field not in fields:
				raise ValueError("%s is not an option for UserInfo" % (field))
			else:
				setattr(self, field, change) 
		signals.account_modified.send(sender=self.__class__,user_id=self.user_id,**kwargs)
		if 'facebook_connection_flag' in kwargs:
			if User.objects.get(username=self.username).settings.facebook_connection_flag == True:
				signals.facebook_friend_newly_connected_to_facebook.send(sender=self.__class__,user=user,facebook_access_token=facebook_access_token)
		return True

	def edit_profile_picture(self,**kwargs):
		self.profile_picture_flag = kwargs['profile_picture_flag']
		self.profile_picture_path = kwargs['profile_picture_path']
		self.profile_picture_cropped_flag = kwargs['profile_picture_cropped_flag']
		self.profile_picture_cropped_path = kwargs['profile_picture_cropped_path']
		self.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])
		signals.profile_picture_edited.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username),profile_picture_flag=self.profile_picture_flag,profile_picture_path=self.profile_picture_path,profile_picture_cropped_flag=self.profile_picture_cropped_flag,profile_picture_cropped_path=self.profile_picture_cropped_path)
		return 'Profile picture edited.'

	def delete_profile_picture(self,**kwargs):
		self.profile_picture_flag = False
		self.profile_picture_path = None
		self.profile_picture_cropped_flag = False
		self.profile_picture_cropped_path = None
		self.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])
		signals.profile_picture_deleted.send(sender=self.__class__,info=self,user=User.objects.get(username=self.username))
		return 'Profile picture deleted.'

class Settings(models.Model):
	user = models.OneToOneField(User,related_name="settings")
	notify_for_subscribed_libraries = models.BooleanField(default=True)
	notify_for_subscribed_users = models.BooleanField(default=True)
	notify_for_breaking_news = models.BooleanField(default=True)
	notify_for_celebrities = models.BooleanField(default=True)
	notify_for_yapster = models.BooleanField(default=True)
	facebook_connection_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	facebook_page_connection_flag = models.BooleanField(default=False)
	facebook_page_id = models.BigIntegerField(blank=True,null=True)
	facebook_share_reyap = models.BooleanField(default=False)
	twitter_connection_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_share_reyap = models.BooleanField(default=False)
	google_plus_connection_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_share_reyap = models.BooleanField(default=False)
	linkedin_connection_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_share_reyap = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.save(update_fields=['is_active'])
			elif is_user_deleted == False:
				return 'To delete Settings, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This Settings is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a Settings, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'Settings is already activated.'
	
class ForgotPasswordRequest(models.Model):
	user_forgot_password_id = models.BigIntegerField(default=1)
	user = models.ForeignKey(User,related_name="forgot_password_requests")
	user_email = models.EmailField()
	reset_password_security_code = models.CharField(max_length=255,blank=True,null=True)
	reset_password_security_code_used_flag = models.BooleanField(default=False)
	date_used = models.DateTimeField(blank=True,null=True)
	user_signed_in_after_without_using_flag = models.BooleanField(default=False)
	date_signed_in_without_using = models.DateTimeField(blank=True,null=True)
	forgot_password_request_latitude = models.FloatField(null=True,blank=True)
	forgot_password_request_longitude = models.FloatField(null=True,blank=True)
	forgot_password_request_point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self,*args,**kwargs):
		if not self.pk:
			self.user_forgot_password_id = ForgotPasswordRequest.objects.filter(user=self.user).count() + 1
			length = 10
			possible_characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
			randomly_generated_reset_password_security_code = ''.join(random.choice(possible_characters) for _ in range(length))
			self.reset_password_security_code = randomly_generated_reset_password_security_code
			template_html = 'forgot_password_email.html'
			template_text = 'forgot_password_email.txt'
			from_email = settings.DEFAULT_FROM_EMAIL
			subject = 'Yapster Reset Password Security Code'
			html = get_template(template_html)
			text = get_template(template_text)
			user = self.user
			to = user.email
			fgp = self
			d = Context({'user':user,'fgp':fgp})
			text_content = text.render(d)
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
		super(ForgotPasswordRequest, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			self.is_active = False
			self.save(update_fields=['is_active'])
		elif self.is_active == False :
			return 'This object has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
		elif self.is_active == True:
			return 'This object is already activated.'

	def reset_password_security_code_used(self):
		#When a user uses a Forgot password code it gets deleted
		self.reset_password_security_code_used_flag = True
		self.date_used = datetime.datetime.now()
		self.is_active = False
		self.is_user_deleted = True
		self.save(update_fields=['reset_password_security_code_used_flag','date_used','is_active'])
		return True

	def reset_password_security_code_not_used_and_user_signed_in(self):
		#When a user uses a Forgot password code it gets deleted
		self.user_signed_in_after_without_using_flag = True
		self.date_signed_in_without_using = datetime.datetime.now()
		self.is_active = False
		self.is_user_deleted = True
		self.save(update_fields=['user_signed_in_after_without_using_flag','date_signed_in_without_using','is_active','is_user_deleted'])
		return True

class UserFunctions(models.Model):
	user = models.OneToOneField(User,related_name="functions")
	is_user_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	@classmethod
	def create(self,**kwargs):
		# create all user methods to avoid signals
		# return user_id
		device_type = kwargs.pop("device_type")
		if device_type == "computer":
			device_computer_ip = kwargs.pop("device_computer_ip")
		elif device_type == "ios":
			device_ios_token = kwargs.pop("device_ios_token")
		elif device_type == "android":
			device_android_registration_id = kwargs.pop("device_android_registration_id")
		else:
			return (False,"This is not a valid. Please create a new session and use a valid device_type.")
		password = kwargs.pop('password')
		username = kwargs["username"]
		email = kwargs["email"]
		if User.objects.filter(username=username).exists():
			return (False,"This username is unavailable.")
		elif User.objects.filter(email=email).exists():
			return (False,"This email has already been used.")
		elif BlackList.objects.filter(username=username).exists():
			return (False,"This username is currently unavailable. Please contact Yapster for more information about creating this account.")
		first_name = kwargs.get("first_name",None)
		last_name = kwargs.get("last_name",None)
		user = User.objects.create_user(email=email,password=password,username=username,first_name=first_name,last_name=last_name)
		UserInfo.objects.create(**kwargs)
		UserFunctions.objects.create(user=user)
		dashboard = Dashboard.objects.create(user=user)
		dashboard.recalculate_subscribed_most_listened_users()
		dashboard.recalculate_subscribed_most_listened_libraries()
		dashboard.recalculate_explore_top_users()
		dashboard.recalculate_subscribed_top_libraries()
		users_first_library_title = "My Library"
		users_first_library_picture_flag = True
		users_first_library_picture_path = "/misc/twins3"
		users_first_library_picture_cropped_flag = True
		users_first_library_picture_cropped_path = "/misc/twins3"
		users_first_library = Library.objects.get_or_create(user=user,
															title=users_first_library_title,
															picture_flag=users_first_library_picture_flag,
															picture_path=users_first_library_picture_path,
															picture_cropped_flag=users_first_library_picture_cropped_flag,
															picture_cropped_path=users_first_library_picture_cropped_path)
		if device_type == "computer":
			session = Session.objects.get_or_create(user=user,device_computer_flag=True,device_computer_ip=device_computer_ip)[0]
		elif device_type == "android":
			session = Session.objects.get_or_create(user=user,device_android_flag=True,device_android_registration_id=device_android_registration_id)[0]
		elif device_type == "ios":
			session = Session.objects.get_or_create(user=user,device_ios_flag=True,device_ios_token=device_ios_token)[0]
		else:
			return (False,"This is not a valid. Please create a new session and use a valid device_type.")
		# if 'facebook_connection_flag' in kwargs:
		# 	if kwargs.get('facebook_connection_flag') == True:
		# 		signals.new_facebook_friend_joined_yapster.send(sender=self.__class__,user=user,facebook_access_token=facebook_access_token)
		return (user.pk,user.username,user.first_name,user.last_name,session.pk)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				return 'To delete a UserFunctions object, you must delete a user(is_user_deleted=True).'
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This UserFunctions object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				return 'To activate a UserFunctions, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This UserFunctions is already activated.'

	def listen(self, yap,longitude=None,latitude=None):
		'''like the yap if it hasn't been liked by the user. Return the like object.'''
		obj = Listen.objects.create(yap=yap,user=self.user) 
		return obj

	def list_of_subscriber_users(self,amount=None,after=None,queryset=False):
		if after is None:
			subscribers = [subscriber_user.user for subscriber_user in self.user.subscribe_user_subscribed_user.filter(is_unsubscribed=False,is_active=True)[:amount]]
		else:
			subscribers = [subscriber_user.user for subscriber_user in self.user.subscribe_user_subscribed_user.filter(is_unsubscribed=False,is_active=True,date_created__lt=dateutil.parser.parse(after))[:amount]]
		return subscribers


	def list_of_subscribed_users(self,amount=None,after=None):
		if after is None:
			subscribed = [subscribed_user.user for subscribed_user in self.user.subscribe_user_user.filter(is_unsubscribed=False,is_active=True)[:amount]]
		else:
			subscribed = [subscribed_user.user for subscribed_user in self.user.subscribe_user_user.filter(is_unsubscribed=False,is_active=True,date_created__lt=dateutil.parser.parse(after))[:amount]]
		return subscribed

	def list_of_subscribed_libraries(self,amount=None,after=None):
		if after is None:
			subscribed = [subscribed_libraries.subscribed_library for subscribed_libraries in self.user.subscribed_libraries.filter(is_unsubscribed=False,is_active=True)[:amount]]
		else:
			subscribed = [subscribed_libraries.subscribed_library for subscribed_libraries in self.user.subscribed_libraries.filter(is_unsubscribed=False,is_active=True,date_created__lt=dateutil.parser.parse(after))[:amount]]
		return subscribed

	def subscribe_user(self, user_to_subscribe,facebook_share_flag=False,facebook_access_token=None):
		request = SubscribeUser.objects.get_or_create(user=self.user,subscribed_user=user_to_subscribe,is_active=True)
		return request[0]

	def unsubscribe_user(self, user_to_unsubscribe):
		try:
			obj = self.user.subscribe_user_user.get(subscribed_user=user_to_unsubscribe,is_unsubscribed=False,is_active=True)
		except SubscribeUser.DoesNotExist:
			return 'This relationship does not exist.'
		obj.unsubscribe()
		return obj

	def subscribe_library(self, library,facebook_share_flag=False,facebook_access_token=None):
		request = SubscribeLibrary.objects.get_or_create(user=self.user,subscribed_library=library,is_unsubscribed=False,is_active=True)
		return request[0]

	def unsubscribe_library(self, library):
		try:
			obj = self.user.subscribed_libraries.get(user=self.user,subscribed_library=library,is_unsubscribed=False,is_active=True)
		except SubscribeLibrary.DoesNotExist:
			return 'This subscription does not exist.'
		obj.unsubscribe()
		return obj

	def load_libraries(self,amount,after_library=None):
		#after is a datetime
		if after_library is None:
			libraries = Library.objects.filter(user=self.user,is_active=True)
		elif after_library is not None:
			libraries = Library.objects.filter(user=self.user,is_active=True,pk__lt=after_library)
		result_list = sorted(yaps,key=attrgetter('date_created'), reverse=True)
		return result_list[:int(amount)]

	def last_yap_user_yap_id(self):
		user = self.user
		#user.yaps.values('yap_id')[:1]
		return Yap.objects.filter(user=self.user).count()
			
	def verify_user(self):
		user = self.user
		if user.profile.is_active and not user.profile.verified_account_flag:
			user_profile = Profile.objects.get(user=user,is_active=True)
			user_profile.verify_user()
			user_verified.send(sender=self, user=user)
			return 'This user has been verified.'
		elif user.profile.verified_account_flag:
			return 'This user has already been verified.'
		elif not user.profile.is_active:
			return 'This user has been deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'This user is not verified and has also been deactivated.'
		else:
			return False

	def unverify_user(self):
		user = self.user
		if user.profile.is_active and user.profile.verified_account_flag:
			user_profile = Profile.objects.get(user=user,is_active=True)
			user_profile.unverify_user()
			user_unverified.send(sender=self, user=user)
			return 'This user has been unverified.'
		elif not user.profile.verified_account_flag:
			return 'This user has already been unverified.'
		elif not user.profile.is_active:
			return 'This user has been deactivated.'
		elif not user.profile.verified_account_flag and not user.profile.is_active:
			return 'This user is not verified and has also been deactivated.'
		else:
			return False

	def forgot_password(self):
		user = self.user
	 	forgot_password_user_record = ForgotPassword.objects.get_or_create(user=user,is_active=True)
	 	forgot_password_user_record = forgot_password_user_record[0]
	 	response = forgot_password_user_record.forgot_password()
	 	return response

	def delete_or_deactivated_account(self,latitude=None,longitude=None):
		user = self.user
		try:
			d = DeactivatedUserLog.objects.get(user=user,is_active=True)
		except ObjectDoesNotExist:
			d = DeactivateUserLog.objects.create(user=user,latitude=latitude,longitude=longitude,is_active=True)
		self.delete(is_user_deleted=True)
		signals.account_deleted_or_deactivated.send(sender=self.__class__,user=self.user)
		return True

class Session(models.Model):
	user = models.ForeignKey(User,related_name="sessions")
	device_computer_flag = models.BooleanField(default=False)
	device_computer_ip = models.CharField(max_length=255,blank=True,null=True)
	device_ios_flag = models.BooleanField(default=False)
	device_ios_token = models.CharField(max_length=255,blank=True,null=True)
	device_android_flag = models.BooleanField(default=False)
	device_android_registration_id = models.CharField(max_length=255,blank=True,null=True)
	session_manually_closed_flag = models.BooleanField(default=False)
	session_logged_out_flag = models.BooleanField(default=False)
	session_timed_out_flag = models.BooleanField(default=False)
	session_created_latitude = models.FloatField(null=True,blank=True)
	sesssion_created_longitude = models.FloatField(null=True,blank=True)
	session_created_point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	objects = models.GeoManager()

	def save(self,*args,**kwargs):
		super(Session, self).save(*args, **kwargs)

	def check_date(self):
		if (timezone.now() - self.date_created).days >= 1:
			return False
		else:
			return True

	def check_session(self,user,session_id):
		session_id = int(session_id)
		if self.user == user:
			if self.id == session_id:
				return True
			else:
				return 'This session_id is incorrect.'
		else:
			return 'This session and user do not match.'

	def automatic_sign_in_check_session_id_and_device(self,user,identifier):
		if self.check_date() == True:
			if self.user == user:
				if self.device_ios_flag == True:
					if self.device_ios_token == identifier:
						return True
					else:
						return'The session\'s identifier didn\'t match our records.'
				elif self.device_android_flag == True:
					if self.device_android_registration_id == identifier:
						return True
					else:
						return'The session\'s identifier didn\'t match our records.'
				elif self.device_computer_flag == True:
					if self.device_computer_ip == identifier:
						return True
					else:
						return "The session\'s identifier didn\'t match our records."
				else:
					return True
			else:
				return'The session\'s identifier didn\'t match our records.'
		else:
			self.session_timed_out()
			return 'This session has timed out.'


	def sign_in_check_session_id(self):
		if self.check_date() == True:
			return True
		elif self.check_date() == False:
			self.session_timed_out()
			return False

	def close_session(self):
		self.is_active = False
		self.session_manually_closed_flag = True
		self.save(update_fields=['is_active','session_manually_closed_flag'])

	def session_timed_out(self):
		self.is_active = False
		self.session_timed_out_flag = True
		self.save(update_fields=['is_active','session_timed_out_flag'])

	def sign_out_device(self):
		self.is_active = False
		self.session_logged_out_flag = True
		self.save(update_fields=['is_active','session_logged_out_flag'])

from django.dispatch import receiver

@receiver(signals.account_created)
def create_user_sections(sender, **kwargs):
	info = kwargs.get("info")
	user = kwargs.get("user")
	Profile.objects.create(
		user=user,
		gender=info.gender,
		description=info.description,
		city=info.city,
		us_state=info.us_state,
		us_zip_code=info.us_zip_code,
		country=info.country,
		phone_number=info.phone_number,
		date_of_birth=info.date_of_birth,
		profile_picture_flag = info.profile_picture_flag,
		profile_picture_path = info.profile_picture_path,
		profile_picture_cropped_flag = info.profile_picture_cropped_flag,
		profile_picture_cropped_path = info.profile_picture_cropped_path,
	)
	Settings.objects.create(
		user = user,
		facebook_connection_flag = info.facebook_connection_flag,
		facebook_account_id = info.facebook_account_id,
		linkedin_connection_flag = info.linkedin_connection_flag,
		linkedin_account_id = info.linkedin_account_id,
		google_plus_connection_flag = info.google_plus_connection_flag,
		google_plus_account_id = info.google_plus_account_id,
		twitter_connection_flag = info.twitter_connection_flag,
		twitter_account_id = info.twitter_account_id
	)

@receiver(signals.account_modified)
def modify_information(sender,**kwargs):
	user_id = kwargs.get('user_id')
	user_obj = User.objects.get(pk=user_id)
	settings = [
		"notify_for_subscribed_libraries",
		"notify_for_subscribed_users",
		"notify_for_breaking_news",
		"notify_for_celebrities",
		"notify_for_celebrities",
		"notify_for_yapster",
		"facebook_connection_flag",
		"facebook_account_id",
		"facebook_page_connection_flag",
		"facebook_page_id",
		"facebook_share_reyap",
		"twitter_connection_flag",
		"twitter_account_id",
		"twitter_share_reyap",
		"google_plus_connection_flag",
		"google_plus_account_id",
		"google_plus_share_reyap",
		"linkedin_connection_flag",
		"linkedin_account_id",
		"linkedin_share_reyap",
	]
	settings_changes = []
	settings_obj = user_obj.settings
	profile = [
		"gender",
		"description",
		"profile_picture_flag",
		"profile_picture_path",
		"profile_picture_cropped_flag",
		"profile_picture_cropped_path",
		"web_cover_picture_1_flag" 
		"web_cover_picture_1_path"
		"web_cover_picture_2_flag"
		"web_cover_picture_2_path"
		"web_cover_picture_3_flag"
		"web_cover_picture_3_path"
		"date_of_birth",
		"city",
		"us_state",
		"us_zip_code",
		"user_country",
		"phone_number",
		"high_security_account_flag",
		"verified_account_flag",
		"content_provider_approved_date",
		"is_privileged",
		"is_content_provider",
		"is_active",
		"is_user_deleted"
	]
	profile_obj = user_obj.profile
	profile_changes = []
	user = [
		"first_name",
		"last_name",
		"username",
		"email",
	]
	user_changes = []
	password = ["password"]

	for k,v in kwargs.iteritems():
		if k in user:
			user_changes.append(k)
			setattr(user_obj,k,v)
		elif k in profile:
			profile_changes.append(k)
			setattr(profile_obj,k,v)
		if k in settings:
			settings_changes.append(k)
			setattr(settings_obj,k,v)			
	if profile_changes != []:		
		profile_obj.save(update_fields=profile_changes)
	if settings_changes != []:
		settings_obj.save(update_fields=settings_changes)
	print user_changes
	if user_changes !=[]:
		user_obj.save(update_fields=user_changes)

@receiver(signals.profile_picture_edited)
def profile_picture_edited(sender,**kwargs):
	user = kwargs['user']
	profile_picture_flag = kwargs['profile_picture_flag']
	profile_picture_path = kwargs['profile_picture_path']
	profile_picture_cropped_flag = kwargs['profile_picture_cropped_flag']
	profile_picture_cropped_path = kwargs['profile_picture_cropped_path']

	user.profile.profile_picture_flag = profile_picture_flag
	user.profile.profile_picture_path = profile_picture_path
	user.profile.profile_picture_cropped_flag = profile_picture_cropped_flag
	user.profile.profile_picture_cropped_path = profile_picture_cropped_path
	user.profile.save(update_fields=['profile_picture_flag','profile_picture_path','profile_picture_cropped_flag','profile_picture_cropped_path'])

@receiver(signals.account_deleted_or_deactivated)
def account_deleted_or_deactivated(sender,**kwargs):
	user = kwargs.get('user')
	user.profile.delete(is_user_deleted=True)
	recommendations = user.recommended.filter(is_active=True)
	for recommendation in recommendations:
		recommendation.delete(is_user_deleted=True)
	user.settings.delete(is_user_deleted=True)
	user_info = UserInfo.objects.get(pk=user.pk)
	user_info.delete(is_user_deleted=True)
	user.is_active = False
	user.save(update_fields=['is_active'])

