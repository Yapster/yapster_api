from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import yap.signals as yap_signals
import users.signals as users_signals
from django.db import models
from location.models import *
from django.dispatch import receiver
from operator import attrgetter
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils import timezone
from scoring_functions import listening_score_for_user_based_on_subscribed_user,listening_score_for_library_based_on_subscribed_user,listening_score_for_users,listening_score_for_libraries
import re
import signals
import random
import datetime

class Hashtag(models.Model):
	name = models.CharField(max_length=255,unique=True) #name of tag as string
	date_created = models.DateTimeField(auto_now_add=True)
	is_blocked = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

	def delete(self):
		'''disabling delete'''
		raise NotImplementedError('Tags cannot be deleted.')

class Channel(models.Model):
	name = models.CharField(max_length=255,unique=True) #name of Channel as string
	description = models.CharField(max_length=255) #description of the Channel
	picture_flag = models.BooleanField(default=False)
	picture_path = models.CharField(unique=True,max_length=255,blank=True,null=True)
	is_bonus = models.BooleanField(default=False)
	is_promoted = models.BooleanField(default=False)
	geographic_target_flag = models.BooleanField(default=False)
	geographic_target = models.ForeignKey(GeographicTarget,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	def __unicode__(self):
		return self.name

	def delete(self):
		self.is_active = False
		self.date_deleted = datetime.datetime.now()
		self.save(update_fields=['is_active','date_deleted'])

class WebsiteUrl(models.Model):
	url = models.URLField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.url

	def delete(self):
		raise NotImplementedError('Websites cannot be deleted.')

class Yap(models.Model):
	user = models.ForeignKey(User,related_name="yaps")
	title = models.CharField(max_length=255)
	description = models.CharField(max_length=255,blank=True,null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)
	length = models.BigIntegerField() #time in seconds
	hashtags_flag = models.BooleanField(default=False)
	hashtags = models.ManyToManyField(Hashtag, related_name="yaps",blank=True,null=True) #foreign key to tags
	channel_flag = models.BooleanField(default=False)
	channel = models.ForeignKey(Channel, blank=True, null=True,related_name="yaps")
	libraries_flag = models.BooleanField(default=True)
	audio_path = models.CharField(max_length=255) #location of the audio file
	picture_flag = models.BooleanField(default=False)
	picture_path = models.CharField(max_length=255,blank=True,null=True)
	picture_cropped_flag = models.BooleanField(default=False)
	picture_cropped_path = models.CharField(blank=True,max_length=255)
	listen_count = models.BigIntegerField(default=0)
	website_urls_flag = models.BooleanField(default=False)
	website_urls = models.ManyToManyField(WebsiteUrl, related_name="yaps",blank=True,null=True)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	url = models.URLField(max_length=255,null=True,blank=True)
	color_1 = models.CharField(max_length=255,null=True,blank=True)
	color_2 = models.CharField(max_length=255,null=True,blank=True)
	color_3 = models.CharField(max_length=255,null=True,blank=True)
	facebook_shared_flag = models.BooleanField(default=False)
	facebook_account_id = models.BigIntegerField(blank=True,null=True)
	twitter_shared_flag = models.BooleanField(default=False)
	twitter_account_id = models.BigIntegerField(blank=True,null=True)
	google_plus_shared_flag = models.BooleanField(default=False)
	google_plus_account_id = models.BigIntegerField(blank=True,null=True)
	linkedin_shared_flag = models.BooleanField(default=False)
	linkedin_account_id = models.BigIntegerField(blank=True,null=True)
	deleted_date = models.DateTimeField(blank=True,null=True)
	deleted_latitude = models.FloatField(null=True,blank=True)
	deleted_longitude = models.FloatField(null=True,blank=True)
	deleted_point = models.PointField(srid=4326,null=True,blank=True)
	is_private = models.BooleanField(default=False)
	is_draft = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			is_created = True
		super(Yap, self).save(*args, **kwargs)
		if is_created:
			self.user.profile.yap_count += 1
			self.user.profile.save(update_fields=["yap_count"])
			signals.yap_created.send(sender=self.__class__,yap=self)
			
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
				self.user.profile.yap_count -= 1
				self.user.profile.save(update_fields=["yap_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.deleted_date = datetime.datetime.now()
				self.save(update_fields=['is_active','deleted_date'])
				self.user.profile.yap_count -= 1
				self.user.profile.save(update_fields=["yap_count"])
			signals.yap_deleted.send(sender=self.__class__,yap=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This yap is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'

	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.deleted_date = None
				self.save(update_fields=['is_active','is_user_deleted','deleted_date'])
			elif is_user_activated == False:
				return 'To activate a yap, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This yap is already activated.'

 	def add_hashtags(self, hashtags):
		if isinstance(hashtags,str):
			hashtags = re.split(r'\s*,\s*',hashtags)
		for hashtag in hashtags:
			t = Hashtag.objects.get_or_create(name=hashtag)[0]
			self.hashtags.add(t)

	def add_website_urls(self, urls):
		for url in urls:
			w = WebsiteUrl.objects.get_or_create(url=url)[0]
			self.website_urls.add(w)
			return True

class Library(models.Model):
	user = models.ForeignKey(User,related_name="libraries")
	title = models.CharField(max_length=255) #name of Channel as string
	description = models.CharField(max_length=255,blank=True,null=True) #description of the Channel
	url = models.URLField(max_length=255,null=True,blank=True)
	picture_flag = models.BooleanField(default=False)
	picture_path = models.CharField(max_length=255,blank=True,null=True)
	picture_cropped_flag = models.BooleanField(default=False)
	picture_cropped_path = models.CharField(max_length=255,blank=True,null=True)
	subscriber_users_count = models.BigIntegerField(default=0)
	color_1 = models.CharField(max_length=255,null=True,blank=True)
	color_2 = models.CharField(max_length=255,null=True,blank=True)
	color_3 = models.CharField(max_length=255,null=True,blank=True)
	yaps = models.ManyToManyField(Yap, related_name="libraries")
	is_reverse_chronological_order = models.BooleanField(default=True)
	is_promoted = models.BooleanField(default=True)
	geographic_target_flag = models.BooleanField(default=False)
	geographic_target = models.ForeignKey(GeographicTarget,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	date_edited = models.DateTimeField(null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	class Meta:
		ordering = ['-date_created']

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Library, self).save(*args, **kwargs)


	def delete(self):
		self.is_active = False
		self.date_deleted = datetime.datetime.now()
		self.save(update_fields=['is_active','date_deleted'])

	def add_yap(self, yap):
		self.yaps.add(yap)
		self.date_edited = datetime.datetime.now()
		self.save(update_fields=['date_edited'])


class LibraryOrder(models.Model):
	user = models.ForeignKey(User, related_name="library_order")
	library = models.ForeignKey(Library, related_name="library_order")
	order = models.BigIntegerField(null=True,blank=True)
	is_user_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['-pk']

	def save(self, *args, **kwargs):
		is_created = False
		if self.user.profile.is_reverse_chronological_order_for_libraries == True:
			self.order = LibraryOrder.objects.filter(user=self.user,is_active=True).count() + 1	
		super(LibraryOrder, self).save(*args, **kwargs)


	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active', 'is_user_deleted'])
			else:
				self.is_active = False
				self.save(update_fields=['is_active'])
		else:
			return 'LibraryOrder object\'s is_active is currently False meaning it\'s already deleted.'

	def activate(self):
		if self.is_active == False:
			if is_user_deleted == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
			else:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active', 'is_user_deleted'])
		else:
			return 'LibraryOrder object\'s is_active is currently True meaning it\'s already active.'

class LibraryYapOrder(models.Model):
	library = models.ForeignKey(Library, related_name="library_yap_order")
	yap = models.ForeignKey(Yap, related_name="library_yap_order")
	order = models.BigIntegerField(null=True,blank=True)
	is_user_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['-pk']

	def save(self, *args, **kwargs):
		is_created = False
		if not self.pk:
			self.order = LibraryYapOrder.objects.filter(library=self.library).count() + 1
		super(LibraryYapOrder, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active', 'is_user_deleted'])
			else:
				self.is_active = False
				self.save(update_fields=['is_active'])
		else:
			return 'LibraryYapOrder object\'s is_active is currently False meaning it\'s already deleted.'

	def activate(self):
		if self.is_active == False:
			if is_user_deleted == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
			else:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active', 'is_user_deleted'])
		else:
			return 'LibraryYapOrder object\'s is_active is currently True meaning it\'s already active.'


class Listen(models.Model):
	user = models.ForeignKey(User, related_name='listens',null=True,blank=True)
	anonymous_user_flag = models.BooleanField(default=False)
	yap = models.ForeignKey(Yap, related_name='listens')
	listen_click_count = models.BigIntegerField(default=0)
	time_listened = models.BigIntegerField(blank=True,null=True) #amount of time listened. defaults to 0 seconds and the `set_time` function can be used to edit
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_user_deleted = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "listen"

	def save(self, *args, **kwargs):
		'''overwritten save to increment relevant listen_counts'''
		is_created = False
		if not self.pk:
			if self.anonymous_user_flag == False:
				self.user_listen_id = Listen.objects.filter(user=self.user).count() + 1
				is_created = True
  		super(Listen, self).save(*args, **kwargs)
		if is_created:
			elf.yap.listen_count += 1
			self.yap.save(update_fields=['listen_count'])
			self.user.profile.listen_count += 1
			self.user.profile.save(update_fields=["listen_count"])
			signals.listen_created.send(sender=self.__class__,listen=self)
	
	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.yap.listen_count -= 1
				self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count -= 1
				self.user.profile.save(update_fields=["listen_count"])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.yap.listen_count -= 1
				self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count -= 1
				self.user.profile.save(update_fields=["listen_count"])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This listen object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.yap.listen_count += 1
				self.yap.save(update_fields=['listen_count'])
				self.user.profile.listen_count += 1
				self.user.profile.save(update_fields=["listen_count"])
			elif is_user_activated == False:
				return 'To activate a listen, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This listen is already activated.'

	def set_time_listened(self,time_listened):
		'''change the amount of time listened for'''
		self.time_listened = time_listened
		self.save(update_fields=['time_listened'])
		if self.reyap_flag == True:
			signals.listen_created_on_reyap_time_listened_updated(sender=self.__class__,listen=self)

class ListenClick(models.Model):
	user = models.ForeignKey(User,related_name='user_listen_clicked')
	listen = models.ForeignKey(Listen,related_name='listen_clicked')
	time_clicked = models.BigIntegerField()
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		super(ListenClick, self).save(*args, **kwargs)
		self.listen.listen_click_count += 1
		self.listen.save(update_fields=['listen_click_count'])

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.listen.listen_click_count -= 1
				self.listen.save(update_fields=['listen_click_count'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.listen.listen_click_count -= 1
				self.listen.save(update_fields=['listen_click_count'])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This listen_click object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.listen.listen_click_count += 1
				self.listen.save(update_fields=['listen_click_count'])
			elif is_user_activated == False:
				return 'To activate a listen_click, you must activate a user (is_user_activated=True).'
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This listen_click is already activated.'

class SubscribeUser(models.Model):
	user_subscription_id = models.BigIntegerField(default=1)
	#user is the person asking to listen
	user = models.ForeignKey(User, related_name='subscribe_user_user')
	#user_requested is the person being asked to be listen to
	subscribed_user = models.ForeignKey(User, related_name='subscribe_user_subscribed_user')
	date_created = models.DateTimeField(auto_now_add=True)
	created_latitude = models.FloatField(null=True,blank=True)
	created_longitude = models.FloatField(null=True,blank=True)
	created_point = models.PointField(srid=4326,null=True,blank=True)
	is_unsubscribed = models.BooleanField(default=False)
	date_unsubscribed = models.DateTimeField(blank=True,null=True)
	unsubscribed_latitude = models.FloatField(null=True,blank=True)
	unsubscribed_longitude = models.FloatField(null=True,blank=True)
	unsubscribed_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	@classmethod
	def name(self):
		return "request"

	def __unicode__(self):
			return "%s is subscribed to %s" % (self.user, self.subscribed_user)

	def save(self, *args, **kwargs):
		super(SubscribeUser, self).save(*args, **kwargs)
		self.user.profile.subscribing_users_count += 1
		self.user.profile.save(update_fields=['subscribing_users_count'])
		self.subscribed_user.profile.subscriber_users_count += 1
		self.subscribed_user.profile.save(update_fields=['subscriber_users_count'])


	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
			self.user.profile.subscribing_users_count -= 1
			self.user.profile.save(update_fields=['subscribing_users_count'])
			self.subscribed_user.profile.subscriber_users_count -= 1
			self.subscribed_user.profile.save(update_fields=['subscriber_users_count'])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
			self.user.profile.subscribing_users_count += 1
			self.user.profile.save(update_fields=['subscribing_users_count'])
			self.subscribed_user.profile.subscriber_users_count += 1
			self.subscribed_user.profile.save(update_fields=['subscriber_users_count'])
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

	def unsubscribe(self):
		self.is_unsubscribed = True
		if not self.date_unfollowed:
			self.date_unfollowed = datetime.datetime.now()
			self.is_user_deleted = False
			self.is_active = False
			self.save(update_fields=['date_unfollowed','is_unsubscribed','is_active'])
			self.user.profile.subscribing_users_count -= 1
			self.user.profile.save(update_fields=['subscribing_users_count'])
			self.subscribed_user.profile.subscriber_users_count -= 1
			self.subscribed_user.profile.save(update_fields=['subscriber_users_count'])


class SubscribeLibrary(models.Model):
	user_subscription_id = models.BigIntegerField(default=1)
	#user is the person asking to listen
	user = models.ForeignKey(User, related_name='subscribed_libraries')
	#user_requested is the person being asked to be listen to
	subscribed_library = models.ForeignKey(Library, related_name='subscribed_libraries')
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)
	created_latitude = models.FloatField(null=True,blank=True)
	created_longitude = models.FloatField(null=True,blank=True)
	created_point = models.PointField(srid=4326,null=True,blank=True)
	is_unsubscribed = models.BooleanField(default=False)
	date_unsubscribed = models.DateTimeField(blank=True,null=True)
	unsubscribed_latitude = models.FloatField(null=True,blank=True)
	unsubscribed_longitude = models.FloatField(null=True,blank=True)
	unsubscribed_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def __unicode__(self):
			return "%s is subscribed to %s" % (self.user, self.subscribed_library)

	def save(self, *args, **kwargs):
		super(SubscribeLibrary, self).save(*args, **kwargs)
		self.user.profile.subscribing_libraries_count += 1
		self.user.profile.save(update_fields=['subscribing_libraries_count'])

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
			self.user.profile.subscribing_libraries_count -= 1
			self.user.profile.save(update_fields=['subscribing_libraries_count'])
			self.subscribed_library.subscriber_users_count -= 1
			self.subscribed_library.save(update_fields=['subscriber_users_count'])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_activated.send(sender=self.__class__,follower_request=self)
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

	def unsubscribe(self):
		self.is_unsubscribed = True
		if not self.date_unfollowed:
			self.date_unfollowed = datetime.datetime.now()
			self.is_user_deleted = False
			self.is_active = False
			self.save(update_fields=['date_unfollowed','is_unsubscribed','is_active'])
			self.user.profile.subscribing_libraries_count -= 1
			self.user.profile.save(update_fields=['subscribing_libraries_count'])
			self.subscribed_library.subscriber_users_count -= 1
			self.subscribed_library.save(update_fields=['subscriber_users_count'])

class FacebookShare(models.Model):
	user_facebook_share = models.BigIntegerField(default=1)
	user = models.ForeignKey(User, related_name='user_facebook_shares')
	shared_yap_flag = models.BooleanField(default=False)
	shared_yap = models.ForeignKey(Yap, related_name="facebook_shares")
	shared_user_flag = models.BooleanField(default=False)
	shared_user = models.ForeignKey(User, related_name="facebook_shares")
	shared_library_flag = models.BooleanField(default=False)
	shared_library = models.ForeignKey(Library, related_name="facebook_shares")
	date_created = models.DateTimeField(blank=True,null=True)
	shared_latitude = models.FloatField(null=True,blank=True)
	shared_longitude = models.FloatField(null=True,blank=True)
	shared_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		super(FacebookShare, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_deleted.send(sender=self.__class__,follower_request=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_activated.send(sender=self.__class__,follower_request=self)
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

class TwitterShare(models.Model):
	user_twitter_share = models.BigIntegerField(default=1)
	user = models.ForeignKey(User, related_name='user_twitter_shares')
	shared_yap_flag = models.BooleanField(default=False)
	shared_yap = models.ForeignKey(Yap, related_name="twitter_shares")
	shared_user_flag = models.BooleanField(default=False)
	shared_user = models.ForeignKey(User, related_name="twitter_shares")
	shared_library_flag = models.BooleanField(default=False)
	shared_library = models.ForeignKey(Library, related_name="twitter_shares")
	date_created = models.DateTimeField(blank=True,null=True)
	shared_latitude = models.FloatField(null=True,blank=True)
	shared_longitude = models.FloatField(null=True,blank=True)
	shared_point = models.PointField(srid=4326,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		super(TwitterShare, self).save(*args, **kwargs)

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
				self.user.profile.following_count -= 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count -= 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_deleted.send(sender=self.__class__,follower_request=self)
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
				self.user.profile.following_count += 1
				self.user.profile.save(update_fields=['following_count'])
				self.user_requested.profile.follower_count += 1
				self.user_requested.profile.save(update_fields=['follower_count'])
			signals.follower_request_activated.send(sender=self.__class__,follower_request=self)
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

class Dashboard(models.Model):
	user = models.ForeignKey(User,primary_key=True,related_name='dashboard')
	subscribed_most_listened_users = models.ManyToManyField(User, related_name="dashboard_subscribed_most_listened_users",blank=True,null=True)
	date_calculated_subscribed_most_listened_users = models.DateTimeField(auto_now_add=True)
	subscribed_most_listened_libraries = models.ManyToManyField(Library, related_name="dashboard_most_listened_subscribed",blank=True,null=True)
	date_calculated_subscribed_most_listened_libraries = models.DateTimeField(auto_now_add=True)
	#Explore Stuff
	explore_top_users = models.ManyToManyField(User, related_name="dashboard_explore_top_users",blank=True,null=True)
	date_calculated_explore_top_users = models.DateTimeField(auto_now_add=True)
	explore_top_libraries = models.ManyToManyField(Library, related_name="dashboard_explore_top_users",blank=True,null=True)
	date_calculated_explore_top_libraries = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_user_deleted = models.BooleanField(default=False)
	objects = models.GeoManager()

	def delete(self,is_user_deleted=False):
		if self.is_active == True:
			if is_user_deleted == True:
				self.is_active = False
				self.is_user_deleted = True
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_deleted == False:
				self.is_active = False
				self.save(update_fields=['is_active'])
		elif self.is_active == False and self.is_user_deleted == False:
			return 'This FollowerRequest object is already deleted.'
		elif self.is_active == False and self.is_user_deleted == True:
			return 'This user has already been deleted.'
			
	def activate(self,is_user_activated=False):
		if self.is_active == False:
			if is_user_activated == True:
				self.is_active = True
				self.is_user_deleted = False
				self.save(update_fields=['is_active','is_user_deleted'])
			elif is_user_activated == False:
				self.is_active = True
				self.save(update_fields=['is_active'])
		elif self.is_active == True and self.is_user_deleted == False:
			return 'This FollowerRequest is already activated.'

	def recalculate_subscribed_most_listened_users(self):
		print "here in function"
		self.subscribed_most_listened_users.clear()
		listen_exists = Listen.objects.filter(user=self.user,is_active=True).exists()
		users_subscribed_to = self.user.subscribe_user_user.filter(is_active=True)
		if self.user.listens.filter(is_active=True).exists() == True:
			key = listening_score_for_user_based_on_subscribed_user
			reverse = True
		else:
			key = lambda *args: random.random()
			reverse = False
		users_to_add_into_subscribed_most_listened_users = sorted(set(users_subscribed_to),key=key, reverse=reverse)[:5]
		for user_to_add_into_subscribed_most_listened_users in users_to_add_into_subscribed_most_listened_users:
			self.subscribed_most_listened_users.add(user_to_add_into_subscribed_most_listened_users.subscribed_user)
		self.date_calculated_subscribed_most_listened_users = datetime.datetime.now()
		self.save(update_fields=['date_calculated_subscribed_most_listened_users'])

	def recalculate_subscribed_most_listened_libraries(self):
		self.subscribed_most_listened_libraries.clear()
		listen_exists = Listen.objects.filter(user=self.user,is_active=True).exists()
		libraries_subscribed_to = self.user.subscribed_libraries.filter(is_active=True)
		if self.user.listens.filter(is_active=True).exists() == True:
			key = listening_score_for_library_based_on_subscribed_user
			reverse = True
		else:
			key = lambda *args: random.random()
			reverse = False
		libraries_to_add_into_subscribed_most_listened_libraries = sorted(set(libraries_subscribed_to),key=key, reverse=reverse)[:5]
		for library_to_add_into_subscribed_most_listened_libraries in libraries_to_add_into_subscribed_most_listened_libraries:
			self.subscribed_most_listened_libraries.add(library_to_add_into_subscribed_most_listened_libraries.subscribed_library)
		self.date_calculated_subscribed_most_listened_libraries = datetime.datetime.now()
		self.save(update_fields=['date_calculated_subscribed_most_listened_libraries'])

	def check_date_calculated_subscribed_most_listened_users(self):
		if (timezone.now() - self.date_calculated_subscribed_most_listened_users).days >= 0:
			return False
		else:
			return True

	def check_date_calculated_subscribed_most_listened_libraries(self):
		if (timezone.now() - self.date_calculated_subscribed_most_listened_libraries).days >= 0:
			return False
		else:
			return True

	#Dashboard Explore Screen

	def recalculate_explore_top_users(self):
		self.explore_top_users.clear()
		minutes = 2880
		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
		yaps = Yap.objects.filter(is_active=True,is_private=False,date_created__gte=time)
		users = User.objects.filter(yaps__in=yaps,is_active=True)
		if self.user.listens.filter(is_active=True).exists() == True:
			key = listening_score_for_users
			reverse = True
		else:
			key = lambda *args: random.random()
			reverse = False
		users_to_add_into_explore_top_users = sorted(set(users),key=key, reverse=reverse)[:5]
		for user_to_add_into_explore_top_users in users_to_add_into_explore_top_users:
			self.explore_top_users.add(user_to_add_into_explore_top_users)
		self.date_calculated_explore_top_users = datetime.datetime.now()
		self.save(update_fields=['date_calculated_explore_top_users'])

	def recalculate_subscribed_top_libraries(self):
		self.explore_top_libraries.clear()
		minutes = 2880
		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
		yaps = Yap.objects.filter(is_active=True,is_private=False,date_created__gte=time)
		libraries = Library.objects.filter(yaps__in=yaps,is_active=True)
		if self.user.listens.filter(is_active=True).exists == True:
			key = listening_score_for_libraries
			reverse = True
		else:
			key = lambda *args: random.random()
			reverse = False
		libraries_to_add_into_explore_top_libraries = sorted(set(libraries),key=key,reverse=reverse)[:5]
		for library_to_add_into_explore_top_libraries in libraries_to_add_into_explore_top_libraries:
			self.explore_top_libraries.add(library_to_add_into_explore_top_libraries)
		self.date_calculated_explore_top_libraries = datetime.datetime.now()
		self.save(update_fields=['date_calculated_explore_top_libraries'])

	def check_date_calculated_explore_top_users(self):
		if (timezone.now() - self.date_calculated_explore_top_users).days >= 1:
			return False
		else:
			return True

	def check_date_calculated_explore_top_libraries(self):
		if (timezone.now() - self.date_calculated_explore_top_libraries).days >= 1:
			return False
		else:
			return True


@receiver(yap_signals.yap_deleted)
def yap_deleted(sender, **kwargs):
	yap = kwargs.get("yap")
	#Delete All The Listens With This Yap
	listens_with_this_yap = Listen.objects.filter(yap=yap,is_active=True)
	for listen in listens_with_this_yap:
		listen.delete(is_user_deleted=yap.is_user_deleted)

@receiver(yap_signals.listen_deleted)
def listen_deleted(sender, **kwargs):
	listen = kwargs.get("listen")
	listen_clicks_with_this_listen = ListenClick.objects.filter(is_active=True)
	for listen_click in listen_clicks_with_this_listen:
		listen_click.delete(is_user_deleted=listen.is_user_deleted)

