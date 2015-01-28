from rest_framework import serializers
from users.models import *
from location.serializers import *
from yap.serializers import YapSerializer, LibrarySerializer,LibraryOrderSerializer,LibraryPreviewOrderSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

	profile_picture_path = serializers.SerializerMethodField('get_profile_picture_path')
	profile_cropped_picture_path = serializers.SerializerMethodField('get_profile_cropped_picture_path')

	class Meta:
		model = User
		fields = ("username","first_name","last_name","id","profile_picture_path","profile_cropped_picture_path")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_path

	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

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


class SettingsSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Settings
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class ProfileInfoSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True) #not return all info in this
	viewing_user_subscribed_to_profile_viewed = serializers.SerializerMethodField("get_viewing_user_subscribed_to_profile_viewed")
	city = CitySerializer()
	country = CountrySerializer()
	us_state = USStateSerializer()
	us_zip_code = USZIPCodeSerializer()
	facebook_connection_flag = serializers.SerializerMethodField("get_facebook_connection_flag")
	facebook_account_id = serializers.SerializerMethodField("get_facebook_account_id")
	facebook_page_connection_flag = serializers.SerializerMethodField("get_facebook_page_connection_flag")
	facebook_page_id = serializers.SerializerMethodField("get_facebook_page_id")
	twitter_connection_flag = serializers.SerializerMethodField("get_twitter_connection_flag")
	twitter_account_id = serializers.SerializerMethodField("get_twitter_account_id")
	last_yap_user_yap_id = serializers.SerializerMethodField("get_last_yap_user_yap_id")

	class Meta:
		model = Profile
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

	def get_viewing_user_subscribed_to_profile_viewed(self,obj):
		user = self.context['user']
		if obj.user.pk == user.pk:
			return None
		else:
			subscribers = obj.user.functions.list_of_subscriber_users()
			if user in subscribers:
				return True
			else:
				return False

	def get_facebook_connection_flag(self,obj):
		return obj.user.settings.facebook_connection_flag
	def get_facebook_account_id(self,obj):
		if obj.user.settings.facebook_connection_flag == True:
			return obj.user.settings.facebook_account_id
		else:
			return None
	def get_facebook_page_connection_flag(self,obj):
		return obj.user.settings.facebook_page_connection_flag
	def get_facebook_page_id(self,obj):
		if obj.user.settings.facebook_page_connection_flag == True:
			return obj.user.settings.facebook_page_id
		else:
			return None
	def get_twitter_connection_flag(self,obj):
		return obj.user.settings.twitter_connection_flag
	def get_twitter_account_id(self,obj):
		if obj.user.settings.twitter_connection_flag == True:
			return obj.user.settings.twitter_account_id
		else:
			return None
	def get_last_yap_user_yap_id(self,obj):
		user = self.context['user']
		if obj.user.pk == user.pk:
			return user.functions.last_yap_user_yap_id()
		else:
			return None


class EditProfileInfoSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True) #not return all info in this
	user_city = CitySerializer()
	user_country = CountrySerializer()
	user_us_state = USStateSerializer()
	user_us_zip_code = USZIPCodeSerializer()

	class Meta:
		model = Profile
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class UserAccountInfo(serializers.ModelSerializer):
	profile = serializers.SerializerMethodField("get_profile")
	settings = serializers.SerializerMethodField("get_settings")

	class Meta:
		model = User

	def get_profile(self,obj):
		return ProfileInfoSerializer(obj.profile).data
	def get_settings(self,obj):
		return SettingsSerializer(obj.settings).data


class ProfileSerializer(serializers.ModelSerializer):
	profile_info = serializers.SerializerMethodField("get_profile_info")
	library_order = serializers.SerializerMethodField("get_library_order")

	class Meta:
		model = User
		fields = ("profile_info","library_order")

	def get_profile_info(self,obj):
		return ProfileInfoSerializer(obj.profile,context={'user':self.context['user']}).data

	def get_library_order(self,obj):
		return LibraryPreviewOrderSerializer((obj.library_order.filter(is_active=True,order__lt=5)[:5]),context={'user':self.context['user']}).data


class SubscribedUserSerializer(serializers.ModelSerializer):
	subscribed_user = serializers.SerializerMethodField("get_subscribed_user_profile")

	class Meta:
		model = User
		fields = ("subscribed_user",)

	def get_subscribed_user_profile(self,obj):
		return ProfileSerializer(obj,context={'user':self.context['user']}).data



