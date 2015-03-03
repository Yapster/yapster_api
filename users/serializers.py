from rest_framework import serializers
from users.models import *
from location.serializers import *
from yap.serializers import *
from django.contrib.auth.models import User


class SettingsSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Settings
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

class ProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	city = serializers.SerializerMethodField("get_city_name")
	country = serializers.SerializerMethodField("get_country_name")
	us_state = serializers.SerializerMethodField("get_us_state_name")
	us_zip_code = serializers.SerializerMethodField("get_us_zip_code")
	viewing_user_subscribed_to_user = serializers.SerializerMethodField("get_viewing_user_subscribed_to_user")
	viewing_user_is_user_flag = serializers.SerializerMethodField("get_viewing_user_is_user_flag")
	viewing_user_is_user_extra_info = serializers.SerializerMethodField("get_viewing_user_is_user_extra_info")

	class Meta:
		model = Profile
		exclude = ['is_active','is_user_deleted','manual_override','manual_override_description']

	def get_city_name(self,obj):
		if obj.city != None:
			return obj.city.name
		else:
			return None

	def get_country_name(self,obj):
		if obj.country != None:
			return obj.country.name
		else:
			return None

	def get_us_state_name(self,obj):
		if obj.us_state != None:
			return obj.us_state.name
		else:
			return None

	def get_us_zip_code(self,obj):
		if obj.us_zip_code != None:
			return obj.us_zip_code.name
		else:
			return None

	def get_viewing_user_subscribed_to_user(self,obj):
		user = self.context['user']
		if obj.user.pk == user.pk:
			return None
		else:
			subscribers = obj.user.functions.list_of_subscriber_users()
			if user in subscribers:
				return True
			else:
				return False

	def get_viewing_user_is_user_flag(self,obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			if obj.user.pk == user.pk:
				return True
			else:
				return False

	def get_viewing_user_is_user_extra_info(self,obj):
		user = self.context['user']
		if user == None:
			return False
		else:
			if obj.user.pk == user.pk:
				return None
			else:
				return {"facebook_connection_flag":obj.user.settings.facebook_connection_flag, "facebook_account_id":obj.user.settings.facebook_account_id,"facebook_page_connection_flag":obj.user.settings.facebook_page_connection_flag,"facebook_page_id":obj.user.settings.facebook_page_id, "twitter_connection_flag":obj.user.settings.twitter_connection_flag, "twitter_account_id":obj.user.settings.twitter_account_id,"last_yap_user_yap_id":user.functions.last_yap_user_yap_id()}


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

# class LibraryPreviewOrderSerializer(serializers.ModelSerializer):
# 	library = serializers.SerializerMethodField("get_library")
# 	class Meta:
# 		model = LibraryOrder
# 		fields = ["library","order"]

# 	def get_library(self,obj):
# 		return LibraryPreviewSerializer(obj.library,context={'user':self.context['user'],'include_library_profile':self.context['include_library_profile']}).data


# class LibraryPreviewSerializer(serializers.ModelSerializer):
# 	user = serializers.SerializerMethodField("get_profile")
# 	library_yap_order = serializers.SerializerMethodField("get_library_yap_order")
# 	viewing_user_subscribed_to_library = serializers.SerializerMethodField("get_viewing_user_subscribed_to_library")

# 	class Meta:
# 		model = Library
# 		exclude = ["is_active","is_user_deleted","date_edited","date_deleted","geographic_target_flag","geographic_target","is_promoted","yaps"]

# 	def get_profile(self,obj):
# 			if self.context['include_library_profile'] == True:
# 				return ProfileSerializer(obj.user, context={'user':self.context['user'], 'include_library_profile':False}).data
# 			else:
# 				return UserSerializer(obj.user, context={'user':self.context['user'], 'include_library_profile':False}).data

# 	def get_library_yap_order(self,obj):
# 		user = self.context['user']
# 		return LibraryYapOrderSerializer(obj.library_yap_order.filter(is_active=True)[:5], context={'user':user}).data

# 	def get_viewing_user_subscribed_to_library(self,obj):
# 		library_id = obj.pk
# 		user = self.context['user']
# 		if user.subscribed_libraries.filter(pk=library_id).exists() == True:
# 			return True
# 		else:
# 			return False



