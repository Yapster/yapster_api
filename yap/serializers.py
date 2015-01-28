from rest_framework import serializers
from users.models import Profile
from yap.models import *
from location.serializers import *
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
	user = UserSerializer(partial=True)
	hashtags = HashtagSerializer()
	channel = ChannelSerializer()

	class Meta:
		model = Yap

class AbstractYapSerializer(serializers.ModelSerializer):
	yap_user_subscribed_by_viewer = serializers.SerializerMethodField('get_yap_user_subscribed_by_viewer')
	yap_library_subscribed_by_viewer = serializers.SerializerMethodField('get_yap_library_subscribed_by_viewer')
	yap_info = serializers.SerializerMethodField('get_yap_info')
	date_created = serializers.SerializerMethodField('get_date_created')

	class Meta:
		model = Yap
		fields = ("yap_user_subscribed_by_viewer","yap_library_subscribed_by_viewer","yap_info","date_created")
	
	def get_date_created(self,obj):
		return obj.date_created

	def get_yap_user_subscribed_by_viewer(self, obj):
		user = self.context['user']
		return None #Need to complete

	def get_yap_library_subscribed_by_viewer(self, obj):
		user = self.context['user']
		return Listen.objects.filter(yap=obj,user=user,is_active=True).exists()

	def get_yap_info(self,obj):
		return YapSerializer(obj).data

class LibraryYapOrderSerializer(serializers.ModelSerializer):
	yap = serializers.SerializerMethodField("get_yap")

	class Meta:
		model = LibraryYapOrder
		fields = ["yap", "order"]

	def get_yap(self,obj):
		user = self.context['user']
		print user
		print "here in libraryyaporderSerializer"
		return AbstractYapSerializer(obj.yap,context={'user':self.context['user']}).data


class LibrarySerializer(serializers.ModelSerializer):
	user = UserSerializer()
	library_yap_order = serializers.SerializerMethodField("get_library_yap_order")
	viewing_user_subscribed_to_library = serializers.SerializerMethodField("get_viewing_user_subscribed_to_library")

	class Meta:
		model = Library
		exclude = ["is_active","geographic_target_flag","geographic_target","date_created","date_edited","date_deactivated"]

	def get_library_yap_order(self,obj):
		return LibraryYapOrderSerializer(obj.library_yap_order.filter(is_active=True,order_gt=self.context['after'])[:self.context['amount']]).data

	def get_viewing_user_subscribed_to_library(self,obj):
		library_id = self.context['library_id']
		if self.user.subscribed_libraries.filter(pk=library_id).exists() == True:
			return True
		else:
			return False


class LibraryPreviewSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	library_yap_order = serializers.SerializerMethodField("get_library_yap_order")
	viewing_user_subscribed_to_library = serializers.SerializerMethodField("get_viewing_user_subscribed_to_library")

	class Meta:
		model = Library
		exclude = ["is_active","geographic_target_flag","geographic_target","date_created","date_edited","date_deactivated"]

	def get_library_yap_order(self,obj):
		user = self.context['user']
		print user
		print "here"
		return LibraryYapOrderSerializer(obj.library_yap_order.filter(is_active=True)[:5], context={'user':user}).data

	def get_viewing_user_subscribed_to_library(self,obj):
		library_id = obj.pk
		user = self.context['user']
		if user.subscribed_libraries.filter(pk=library_id).exists() == True:
			return True
		else:
			return False

class LibraryOrderSerializer(serializers.ModelSerializer):
	library = LibrarySerializer()
	class Meta:
		model = LibraryOrder
		fields = ["library","order"]

class LibraryPreviewOrderSerializer(serializers.ModelSerializer):
	library = serializers.SerializerMethodField("get_library")
	class Meta:
		model = LibraryOrder
		fields = ["library","order"]

	def get_library(self,obj):
		return LibraryPreviewSerializer(obj.library,context={'user':self.context['user']}).data

class ListenSerializer(serializers.ModelSerializer):
	user = UserSerializer(partial=True)
	yap = YapSerializer()

	class Meta:
		model = Listen
		exclude = ["is_active","manual_override","manual_override_description"]

class SubscribedLibrarySerializer(serializers.ModelSerializer):
	subscribed_library = serializers.SerializerMethodField("get_subscribed_library")

	class Meta:
		model = Library
		fields = ("subscribed_library",)

	def get_subscribed_library(self,obj):
		return LibraryPreviewSerializer(obj,context={'user':self.context['user']}).data













