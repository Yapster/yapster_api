from rest_framework import serializers
from users.serializers import *
from search.models import *
from location.serializers import *
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
from django.db.models import Sum

class SearchResultsSerializer(serializers.Serializer):

	users = serializers.SerializerMethodField("get_users_searched")
	libraries = serializers.SerializerMethodField("get_libraries_searched")
	yaps = serializers.SerializerMethodField("get_yaps_searched")

	def get_users_searched(self,obj):
		print obj
		return UserSerializer(obj.default_user_search(amount=5),many=True,context={'user':self.context['user']}).data

	def get_libraries_searched(self,obj):
		return LibraryPreviewSerializer(obj.default_library_search(amount=5),many=True,context={'user':self.context['user']}).data

	def get_yaps_searched(self,obj):
		return YapSerializer(obj.default_yap_search(amount=5),many=True,context={'user':self.context['user']}).data


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






