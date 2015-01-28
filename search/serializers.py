from rest_framework import serializers
from users.models import Profile,Settings,Recommended
from users.serializers import *
from search.models import *
from location.serializers import *
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
from django.db.models import Sum

class ExploreSearchResultsSerializer(serializers.Serializer):
	yap_id = serializers.SerializerMethodField("get_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_post_id(self, obj):
		return obj.yap_id

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':None,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data

class ExplorePeopleSearchSerializer(serializers.ModelSerializer):
	following_info = serializers.SerializerMethodField("get_user_following_info")
	profile_picture_path = serializers.SerializerMethodField("get_profile_picture_path")
	profile_cropped_picture_path = serializers.SerializerMethodField("get_profile_cropped_picture_path")
	user_following_listed_user = serializers.SerializerMethodField("get_user_following_listed_user")

	class Meta:
		model = User
		fields = ("id","username","first_name","last_name","profile_picture_path","profile_cropped_picture_path","user_following_listed_user")

	def get_profile_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path
	def get_profile_cropped_picture_path(self,obj):
		return obj.profile.profile_picture_cropped_path

	def get_user_following_listed_user(self,obj):
		user = self.context['user']
		if obj.pk == user.pk:
			return None
		else:
			if obj.pk in user.functions.list_of_following():
				user_following_listed_user = True
			else:
				user_following_listed_user = False
			return user_following_listed_user


class ProfileSearchResultsSerializer(serializers.Serializer):
	date_created = serializers.SerializerMethodField("get_date_created")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_date_created(self, obj):
		return obj.date_created

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name != "yap" and name != "reyap":
			if obj.reyap_flag == True:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
			else:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.user,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data
		else:
			return YapSerializer(obj.yap).data

class StreamSearchResultsSerializer(serializers.Serializer):
	user_post_id = serializers.SerializerMethodField("get_user_post_id")
	post_info = serializers.SerializerMethodField("get_post_info")
	yap_info = serializers.SerializerMethodField("get_yap_info")

	def get_user_post_id(self, obj):
		return obj.pk

	def get_post_info(self,obj):
		name = obj.__class__.name()
		if name != "yap" and name != "reyap":
			if obj.reyap_flag == True:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.reyap.user,"user":self.context['user'],"date_action_done":obj.date_created}).data
			else:
				return AbstractPostSerializer(obj.yap,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		elif name == "yap":
			return AbstractPostSerializer(obj,context={'reyap_flag':False,'reyap_user':None,"user":self.context['user'],"date_action_done":obj.date_created}).data
		else:
			return AbstractPostSerializer(obj.yap,context={'reyap_flag':True,'reyap_user':obj.user,"user":self.context['user'],"date_action_done":obj.date_created}).data

	def get_yap_info(self,obj):
		name = obj.__class__.name()
		if name == "yap":
			return YapSerializer(obj).data
		else:
			return YapSerializer(obj.yap).data


class ExploreScreenStatisticsSerializer(serializers.Serializer):

	user_yapster_number = serializers.SerializerMethodField("get_user_yapster_number")
	total_number_of_users = serializers.SerializerMethodField("get_total_number_of_users")
	user_time_listened_in_the_last_24hrs = serializers.SerializerMethodField("get_user_time_listened_in_the_last_24hrs")
	total_time_listened_in_the_last_24hrs = serializers.SerializerMethodField("get_total_time_listened_in_the_last_24hrs")


	def get_user_yapster_number(self,obj):
		user = obj
		number_of_users_before_user = User.objects.filter(pk__lt=user.pk).count()
		user_yapster_number = number_of_users_before_user + 1
		return user_yapster_number

	def get_total_number_of_users(self,obj):
		total_number_of_users = User.objects.count()
		return total_number_of_users

	def get_user_time_listened_in_the_last_24hrs(self,obj):
		user = obj
		print user
		days = 1
		time = datetime.datetime.now() - datetime.timedelta(days=days)
		user_time_listened_in_the_last_24hrs = Listen.objects.filter(is_active=True,user=user,date_created__gte=time).aggregate(Sum('time_listened'))
		print user_time_listened_in_the_last_24hrs
		user_time_listened_in_the_last_24hrs = user_time_listened_in_the_last_24hrs['time_listened__sum']
		if user_time_listened_in_the_last_24hrs == None:
			return "0 secs"
		else:
			if user_time_listened_in_the_last_24hrs < 60:
				if user_time_listened_in_the_last_24hrs == 1:
					return str(user_time_listened_in_the_last_24hrs) + " sec"
				else:
					return str(user_time_listened_in_the_last_24hrs) + " secs"
			if user_time_listened_in_the_last_24hrs >= 60 and user_time_listened_in_the_last_24hrs < 3600:
				minutes = user_time_listened_in_the_last_24hrs / 60
				seconds = (user_time_listened_in_the_last_24hrs % 60)
				if minutes == 1:
					if seconds == 1:
						return str(minutes) + " min " + str(seconds) + " sec"
					else:
						return str(minutes) + " min " + str(seconds) + " secs"
				else:
					if seconds == 1:
						return str(minutes) + " mins " + str(seconds) + " sec"
					else:
						return str(minutes) + " mins " + str(seconds) + " secs"
			if user_time_listened_in_the_last_24hrs >= 3600:
				hours = user_time_listened_in_the_last_24hrs / 3600
				minutes = ((user_time_listened_in_the_last_24hrs % 3600) / 60)
				seconds = ((user_time_listened_in_the_last_24hrs % 3600) % 60)
				if hours == 1:
					if minutes == 1:
						if seconds == 1:
							return str(hours) + " hr " + str(minutes) + " min " + str(seconds) + " sec"
						else:
							return str(hours) + " hr " + str(minutes) + " min " + str(seconds) + " secs"
					else:
						if seconds == 1:	
							return str(hours) + " hr " + str(minutes) + " mins " + str(seconds) + " sec"
						else:
							return str(hours) + " hr " + str(minutes) + " mins " + str(seconds) + " secs"
				else:
					if minutes == 1:
						if seconds == 1:
							return str(hours) + " hrs " + str(minutes) + " min " + str(seconds) + " sec"
						else:
							return str(hours) + " hrs " + str(minutes) + " min " + str(seconds) + " secs"
					else:
						if seconds == 1:	
							return str(hours) + " hrs " + str(minutes) + " mins " + str(seconds) + " sec"
						else:
							return str(hours) + " hrs " + str(minutes) + " mins " + str(seconds) + " secs"

	def get_total_time_listened_in_the_last_24hrs(self,obj):
		days = 1
		time = datetime.datetime.now() - datetime.timedelta(days=days)
		total_time_listened_in_the_last_24hrs = Listen.objects.filter(is_active=True,date_created__gte=time).aggregate(Sum('time_listened'))
		total_time_listened_in_the_last_24hrs = total_time_listened_in_the_last_24hrs['time_listened__sum']
		if total_time_listened_in_the_last_24hrs == None:
			return "0 secs"
		else:
			if total_time_listened_in_the_last_24hrs < 60:
				if total_time_listened_in_the_last_24hrs == 1:
					return str(total_time_listened_in_the_last_24hrs) + " sec"
				else:
					return str(total_time_listened_in_the_last_24hrs) + " secs"
			if total_time_listened_in_the_last_24hrs >= 60 and total_time_listened_in_the_last_24hrs < 3600:
				minutes = total_time_listened_in_the_last_24hrs / 60
				seconds = (total_time_listened_in_the_last_24hrs % 60)
				if minutes == 1:
					if seconds == 1:
						return str(minutes) + " min " + str(seconds) + " sec"
					else:
						return str(minutes) + " min " + str(seconds) + " secs"
				else:
					if seconds == 1:
						return str(minutes) + " mins " + str(seconds) + " sec"
					else:
						return str(minutes) + " mins " + str(seconds) + " secs"
			if total_time_listened_in_the_last_24hrs >= 3600:
				hours = total_time_listened_in_the_last_24hrs / 3600
				minutes = ((total_time_listened_in_the_last_24hrs % 3600) / 60)
				seconds = ((total_time_listened_in_the_last_24hrs % 3600) % 60)
				if hours == 1:
					if minutes == 1:
						if seconds == 1:
							return str(hours) + " hr " + str(minutes) + " min " + str(seconds) + " sec"
						else:
							return str(hours) + " hr " + str(minutes) + " min " + str(seconds) + " secs"
					else:
						if seconds == 1:	
							return str(hours) + " hr " + str(minutes) + " mins " + str(seconds) + " sec"
						else:
							return str(hours) + " hr " + str(minutes) + " mins " + str(seconds) + " secs"
				else:
					if minutes == 1:
						if seconds == 1:
							return str(hours) + " hrs " + str(minutes) + " min " + str(seconds) + " sec"
						else:
							return str(hours) + " hrs " + str(minutes) + " min " + str(seconds) + " secs"
					else:
						if seconds == 1:	
							return str(hours) + " hrs " + str(minutes) + " mins " + str(seconds) + " sec"
						else:
							return str(hours) + " hrs " + str(minutes) + " mins " + str(seconds) + " secs"






