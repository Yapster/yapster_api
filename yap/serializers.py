from rest_framework import serializers
from users.models import Profile
from yap.models import *
from location.serializers import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
	profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')
	web_cover_picture_1_path = serializers.SerializerMethodField('get_web_cover_picture_1_path')
	description = serializers.SerializerMethodField('get_description')
	city_name = serializers.SerializerMethodField('get_city_name')
	us_state_name = serializers.SerializerMethodField('get_us_state_name')
	us_zip_code_name = serializers.SerializerMethodField('get_us_zip_code_name')
	country_name = serializers.SerializerMethodField('get_country_name')
	subscriber_users_count = serializers.SerializerMethodField('get_subscriber_users_count')
	subscribing_users_count = serializers.SerializerMethodField('get_subscribing_users_count')
	subscribing_libraries_count = serializers.SerializerMethodField('get_subscribing_libraries_count')
	libraries_count = serializers.SerializerMethodField('get_libraries_count')
	viewing_user_subscribed_to_user = serializers.SerializerMethodField('get_viewing_user_subscribed_to_user')
	viewing_user_is_user_extra_info = serializers.SerializerMethodField('get_viewing_user_is_user_extra_info')

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","web_cover_picture_1_path","description","city_name","us_state_name","us_zip_code_name","country_name","subscriber_users_count","subscribing_users_count","subscribing_users_count","subscribing_libraries_count","libraries_count","viewing_user_subscribed_to_user","viewing_user_is_user_extra_info")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_web_cover_picture_1_path(self,obj):
		return obj.profile.web_cover_picture_1_path

	def get_description(self,obj):
		return obj.profile.description

	def get_city_name(self,obj):
		if obj.profile.city != None:
			return obj.profile.city.name
		else:
			return None

	def get_country_name(self,obj):
		if obj.profile.country != None:
			return obj.profile.country.name
		else:
			return None

	def get_us_state_name(self,obj):
		if obj.profile.us_state != None:
			return obj.profile.us_state.name
		else:
			return None

	def get_us_zip_code_name(self,obj):
		if obj.profile.us_zip_code != None:
			return obj.profile.us_zip_code.name
		else:
			return None

	def get_subscriber_users_count(self,obj):
		return obj.profile.subscriber_users_count

	def get_subscribing_users_count(self,obj):
		return obj.profile.subscribing_users_count

	def get_subscribing_libraries_count(self,obj):
		return obj.profile.subscribing_libraries_count

	def get_libraries_count(self,obj):
		return Library.objects.filter(user=obj,is_active=True).count()

	def get_viewing_user_subscribed_to_user(self,obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			if obj.pk == user.pk:
				return None
			else:
				subscribers = obj.functions.list_of_subscriber_users()
				if user in subscribers:
					return True
				else:
					return False

	def get_viewing_user_is_user_extra_info(self,obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			if obj.pk == user.pk:
				return {"facebook_connection_flag":obj.settings.facebook_connection_flag, "facebook_account_id":obj.settings.facebook_account_id,"facebook_page_connection_flag":obj.settings.facebook_page_connection_flag,"facebook_page_id":obj.settings.facebook_page_id, "twitter_connection_flag":obj.settings.twitter_connection_flag, "twitter_account_id":obj.settings.twitter_account_id,"last_yap_user_yap_id":obj.functions.last_yap_user_yap_id()}
			else:
				return None

class ListUserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	profile_description = serializers.SerializerMethodField("get_profile_description")

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path","profile_description")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path
	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_profile_description(self,obj):
		return obj.profile.description

class ChannelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Channel
		exclude = ["date_created","date_deactivated","is_active","manual_override","manual_override_description"]

class ChannelListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Channel
		exclude = ["date_created","date_deactivated","is_active","manual_override","manual_override_description"]

class HashtagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Hashtag
		exclude = ["is_active","is_blocked"]

class YapSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField("get_user")
	hashtags = HashtagSerializer()
	channel = ChannelSerializer()

	class Meta:
		model = Yap
		exclude = ["is_user_deleted","is_active","is_draft","is_private","deleted_point","deleted_longitude","deleted_latitude","deleted_date","linkedin_account_id","linkedin_shared_flag","google_plus_account_id","google_plus_shared_flag","twitter_account_id","twitter_shared_flag","facebook_account_id","facebook_shared_flag","point","longitude","latitude","website_urls","website_urls_flag","libraries_flag","channel_flag","channel","hashtags","hashtags_flag","date_created","date_deleted"]

	def get_user(self,obj):
		return UserSerializer(obj.user,context=self.context).data

class AbstractYapSerializer(serializers.ModelSerializer):
	yap_user_subscribed_by_viewer = serializers.SerializerMethodField('get_yap_user_subscribed_by_viewer')
	yap_info = serializers.SerializerMethodField('get_yap_info')
	date_created = serializers.SerializerMethodField('get_date_created')

	class Meta:
		model = Yap
		fields = ("yap_user_subscribed_by_viewer","yap_info","date_created")
	
	def get_date_created(self,obj):
		return obj.date_created

	def get_yap_user_subscribed_by_viewer(self, obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			return SubscribeUser.objects.filter(user=user,subscribed_user=obj.user,is_active=True).exists()
	def get_yap_info(self,obj):
		return YapSerializer(obj,context=self.context).data

class LibraryYapOrderSerializer(serializers.ModelSerializer):
	yap = serializers.SerializerMethodField("get_yap")

	class Meta:
		model = LibraryYapOrder
		fields = ["yap", "order"]

	def get_yap(self,obj):
		user = self.context['user']
		return AbstractYapSerializer(obj.yap,context=self.context).data


class LibraryPreviewOrderSerializer(serializers.ModelSerializer):
	library = serializers.SerializerMethodField("get_library")
	class Meta:
		model = LibraryOrder
		fields = ["library","order"]

	def get_library(self,obj):
		return LibraryPreviewSerializer(obj.library,context=self.context).data

class LibraryPreviewSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField("get_user")
	yaps = serializers.SerializerMethodField("get_yaps")
	viewing_user_subscribed_to_library = serializers.SerializerMethodField("get_viewing_user_subscribed_to_library")


	class Meta:
		model = Library
		exclude = ["date_deleted","date_edited","is_user_deleted","is_active","geographic_target","geographic_target_flag","is_promoted"]

	def get_user(self,obj):
		return UserSerializer(obj.user,context={'user':self.context['user']}).data

	def get_yaps(self,obj):
		yaps = [yap_order.yap for yap_order in obj.library_yap_order.filter(is_active=True).order_by('-order')][:3]
		return AbstractYapSerializer(yaps,context=self.context).data

	def get_viewing_user_subscribed_to_library(self,obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			return user.subscribed_libraries.filter(subscribed_library=obj).exists()










