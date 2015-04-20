from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from yap.models import *
from django.contrib.gis.db import models
from django.db.models import Q

class Search(models.Model):
	user = models.ForeignKey(User,related_name="searches", null=True,blank=True)
	origin_dashboard_subscribed_screen_flag = models.BooleanField(default=False)
	origin_dashboard_subscribed_view_all_users_screen_flag = models.BooleanField(default=False)
	origin_dashboard_subscribed_view_all_libraries_screen_flag = models.BooleanField(default=False)
	origin_dashboard_explore_screen_flag = models.BooleanField(default=False)
	origin_dashboard_explore_view_all_users_screen_flag = models.BooleanField(default=False)
	origin_dashboard_explore_view_all_libraries_screen_flag = models.BooleanField(default=False)
	origin_dashboard_channel_screen_flag = models.BooleanField(default=False)
	origin_dashboard_channel_searched = models.ForeignKey(Channel,related_name="in_searches",blank=True,null=True)
	origin_profile_screen_flag = models.BooleanField(default=False)
	origin_profile_searched = models.ForeignKey(User, related_name="in_searches",blank=True,null=True)
	origin_library_screen_flag = models.BooleanField(default=False)
	origin_library_searched = models.ForeignKey(Library, related_name="in_searches",blank=True,null=True)
	origin_web_screen_flag = models.BooleanField(default=False)
	text = models.CharField(max_length=255)
	latitude = models.FloatField(null=True,blank=True)
	longitude = models.FloatField(null=True,blank=True)
	point = models.PointField(srid=4326,null=True,blank=True)
	is_after_request = models.BooleanField(default=False)
	is_trending = models.BooleanField(default=False)
	is_recent = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	objects = models.GeoManager()

	class Meta:
		ordering = ['-date_created']


	def default_user_search(self,amount=None):
		# users = User.objects.filter(is_active=True)
		# search_results_1 = users.filter(first_name__istartswith=self.text)
		# search_results_2 = users.filter(last_name__istartswith=self.text)
		# search_results_3 = users.filter(username__istartswith=self.text)
		# search_result_list = set(chain(search_results_1,search_results_2,search_results_3))
		if amount == None:
			search_results_list = User.objects.filter((Q(first_name__istartswith=self.text) | Q(last_name__istartswith=self.text) | Q(username__istartswith=self.text)),is_active=True)
		else:
			search_results_list = User.objects.filter((Q(first_name__istartswith=self.text) | Q(last_name__istartswith=self.text) | Q(username__istartswith=self.text)),is_active=True)[:amount]
		return search_results_list

	def default_library_search(self,amount=None):
		# libraries = Library.objects.filter(is_active=True)
		# search_results_1 = libraries.filter(title__icontains=self.text)
		# search_results_2 = libraries.filter(description__icontains=self.text)
		# search_result_list = set(chain(search_results_1,search_results_2))
		if amount == None:
			search_results_list = Library.objects.filter((Q(title__icontains=self.text) | Q(description__icontains=self.text)),is_active=True)
		else:
			search_results_list = Library.objects.filter((Q(title__icontains=self.text) | Q(description__icontains=self.text)),is_active=True)[:amount]
		return search_results_list

	def default_yap_search(self,amount=None):
		# libraries = Library.objects.filter(is_active=True)
		# search_results_1 = libraries.filter(title__icontains=self.text)
		# search_results_2 = libraries.filter(description__icontains=self.text)
		# search_result_list = set(chain(search_results_1,search_results_2))
		if amount == None:
			search_results_list = Yap.objects.filter((Q(title__icontains=self.text) | Q(description__icontains=self.text)),is_active=True)
		else:
			search_results_list = Yap.objects.filter((Q(title__icontains=self.text) | Q(description__icontains=self.text)),is_active=True)[:amount]
		return search_results_list


# #Explore Hashtags Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_hashtags_recent_search(self,user,hashtags_searched,amount,after=None):
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return final_search_result_yaps
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(user=user,is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				if mutual_search_result_yaps == []:
# 					mutual_search_result_yaps.extend(search_result_yaps)
# 				elif mutual_search_result_yaps != []:
# 					mutual_search_result_yaps = [yap for yap in mutual_search_result_yaps if yap.hashtags == hashtag_searched]
# 			if mutual_search_result_yaps != []:
# 				search_result_list = sorted(set(chain(final_search_result_yaps,mutual_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				return search_result_list
# 			elif mutual_search_result_yaps == []:
# 				search_result_list = final_search_result_yaps
# 			return search_result_list
# 		elif number_of_hashtags_searched >= 4:
# 				return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 		elif number_of_hashtags_searched == 0:
# 			return 'This search is an error as this search requires a hashtag.'

# 	def explore_user_handles_recent_search(self,user,user_handles_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						return final_search_result_yaps
# 					else:
# 						return 'There are no yaps that match this user handle' + str(user_searched.username) + '.'
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						return final_search_result_yaps
# 					else:
# 						return 'There are no yaps that match this user handle' + str(user_searched.username) + '.'
# 		elif number_of_user_handles_searched == 2:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						return 'There are no yaps that match this user handle' + str(user_searched.username) + '.'
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						return 'There are no yaps that match this user handle' + str(user_searched.username) + '.'
# 				if mutual_search_result_yaps == []:
# 					mutual_search_result_yaps.extend(search_result_yaps)
# 				elif mutual_search_result_yaps != []:
# 					mutual_search_result_yaps = [yap for yap in mutual_search_result_yaps if yap.user_tags == user_searched]
# 			if mutual_search_result_yaps != []:
# 				search_result_list = sorted(set(chain(final_search_result_yaps,mutual_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				return search_result_list
# 			elif mutual_search_result_yaps == []:
# 				search_result_list = final_search_result_yaps
# 			return search_result_list

# 	def explore_user_handles_people_search(self,user,user_handles_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				if after is None:
# 					search_result_yaps = User.objects.filter(is_active=True,username__startswith=user_handle_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = User.objects.filter(is_active=True,username__startswith=user_handle_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return final_search_result_yaps
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_user_handles_searched == 2:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = User.objects.filter(is_active=True,username__startswith=user_handle_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = User.objects.filter(is_active=True,username__startswith=user_handle_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return final_search_result_yaps
# 			else:
# 				return 'There are no yaps that matched this search'


# 	def explore_hashtags_and_user_handles_recent_search(self,user,hashtags_searched,user_handles_searched,amount,after=None):
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched >= 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				if number_of_hashtags_searched == 1:
# 					for hashtag_searched_text in hashtags_searched:
# 						self.add_hashtags(hashtag_searched_text)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user=user_searched)[:amount]
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched)[:amount]
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 								return final_search_result_yaps
# 							else:
# 								return 'There are no yaps that match this hashtag.' + str(hashtag_searched.hashtag_name) + '.'
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user=user_searched,pk__lt=after)[:amount]
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,pk__lt=after)[:amount]
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 								return final_search_result_yaps
# 							else:
# 								return 'There are no yaps that match this hashtag.' + str(hashtag_searched.hashtag_name) + '.'
# 				elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtags_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user=user_searched)[:amount]
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched)[:amount]
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								return 'There are no yaps that match this hashtag.' + hashtag_searched.str + '.'
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user=user_searched,pk__lt=after)[:amount]
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,pk__lt=after)[:amount]
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								return 'There are no yaps that match this hashtag.' + hashtag_searched.str + '.'
# 						if mutual_search_result_yaps == []:
# 							mutual_search_result_yaps.extend(search_result_yaps)
# 						elif mutual_search_result_yaps != []:
# 							mutual_search_result_yaps = [yap for yap in mutual_search_result_yaps if yap.hashtags__hashtag_name == hashtag_searched]
# 					if mutual_search_result_yaps != []:
# 						search_result_list = sorted(set(chain(final_search_result_yaps,mutual_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 						return search_result_list
# 					elif mutual_search_result_yaps == []:
# 						search_result_list = final_search_result_yaps
# 					return search_result_list
# 				elif number_of_hashtags_searched >= 4:
# 					return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 				elif number_of_hashtags_searched == 0:
# 					return 'This search is an error as this search requires a hashtag.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'This search is an error as this search requires a channel.'

# 	#Explore General Search ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_text_recent_search(self,user,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			if after is None:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces)[:amount]
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right)[:amount]
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left)[:amount]
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=text_searched)[:amount]
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=text_searched)[:amount]
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=text_searched)[:amount]
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=text_searched)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return final_search_result_yaps
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'
# 			else:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=words_searched,pk__lt=after)[:amount]
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=words_searched,pk__lt=after)[:amount]
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=words_searched,pk__lt=after)[:amount]
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=words_searched,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return final_search_result_yaps
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'
# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces)[:amount]
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right)[:amount]
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left)[:amount]
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=list_of_words_searched[0])[:amount]
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=list_of_words_searched[1])[:amount]
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return final_search_result_yaps
# 				else:
# 					return 'There are no yaps related to:' + str(words_searched) + '.'
# 			else:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=list_of_words_searched[1],pk__lt=after)[:amount]
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return final_search_result_yaps
# 				else:
# 					return 'There are no yaps related to:' + str(words_searched) + '.'
# 		else:
# 			return 'Error: You must search a word for this search.'

# 	def explore_text_people_search(self,user,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_users = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			if after is None:
# 				search_result_users1 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces)[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,first_name__istartswith=string_of_words_searched_without_spaces)[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,last_name__istartswith=string_of_words_searched_without_spaces)[:amount]
# 				search_result_users = sorted(set(chain(search_result_users1,search_result_users2,search_result_users3)),key=attrgetter('username'), reverse=True)[:amount]
# 			else:
# 				search_result_users1 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,first_name__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,last_name__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_users = sorted(set(chain(search_result_users1,search_result_users2,search_result_users3)),key=attrgetter('username'), reverse=True)[:amount]
# 			if len(search_result_users) > 0:
# 				f_s_r_y = final_search_result_users.extend(search_result_users)
# 				return final_search_result_users
# 			else:
# 				return 'There are no yaps that match this user handle' + str(text_searched) + '.'
# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				search_result_users1 = User.objects.filter(is_active=True,username__istartswith=list_of_words_searched[0])[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,username__istartswith=list_of_words_searched[1])[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces)[:amount]
# 				search_result_users4 = User.objects.filter(is_active=True,first_name__istartswith=list_of_words_searched[0])[:amount]
# 				search_result_users5 = User.objects.filter(is_active=True,last_name__istartswith=list_of_words_searched[1])[:amount]

# 			else:
# 				search_result_users1 = User.objects.filter(is_active=True,username__istartswith=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,username__istartswith=list_of_words_searched[1],pk__lt=after)[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_users4 = User.objects.filter(is_active=True,first_name__istartswith=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_users5 = User.objects.filter(is_active=True,last_name__istartswith=list_of_words_searched[1],pk__lt=after)[:amount]

# 			search_result_users = sorted(set(chain(search_result_users1,search_result_users2,search_result_users3,search_result_users4,search_result_users5)),key=attrgetter('username'), reverse=True)[:amount]
# 			if len(search_result_users) > 0:
# 				return search_result_users
# 			else:
# 				return 'There are no yaps that matched this search'

# 	#Explore Channels Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_recent_search(self,user,channels_searched,amount,after=None):
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched == 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						return final_search_result_yaps
# 					else:
# 						return 'There are no yaps in this channel.' + str(channel_searched.channel_name) + '.'
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						return final_search_result_yaps
# 					else:
# 						return 'There are no yaps in this channel.' + str(channel_searched.channel_name) + '.'
# 		elif number_of_channels_searched >= 2:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				channel_searched = Channel.objects.get(pk=channel_searched)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						return 'There are no yaps in this channel.' + str(channel_searched.channel_name) + '.'
# 				else:
# 					search_result_yaps = Yap.objects.filter(user=user,is_active=True,is_private=False,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						return 'There are no yaps in this channel.' + str(channel_searched.channel_name) + '.'
# 				if mutual_search_result_yaps == []:
# 					mutual_search_result_yaps.extend(search_result_yaps)
# 				elif mutual_search_result_yaps != []:
# 					mutual_search_result_yaps = [yap for yap in mutual_search_result_yaps if yap.channel == channel_searched]
# 			if mutual_search_result_yaps != []:
# 				search_result_list = sorted(set(chain(final_search_result_yaps,mutual_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				return search_result_list
# 			elif mutual_search_result_yaps == []:
# 				search_result_list = final_search_result_yaps
# 			return search_result_list

# 	def explore_channels_and_user_handles_people_search(self,user,channels_searched,user_handles_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_users = []
# 		mutual_search_result_users = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				if number_of_channels_searched >= 1:
# 					for channel_searched in channels_searched:
# 						channel_searched = Channel.objects.get(pk=channel_searched)
# 						if after is None:
# 							yaps_in_channel_with_user = channel_searched.yaps.filter(user__username__istartswith=user_handle_searched,is_active=True)[:3 * amount]
# 							channel_users = [yap.user for yap in yaps_in_channel_with_user]
# 							channel_users = sorted(set(channel_users),key=attrgetter('username'))[:amount]
# 							if len(channel_users) > 0:
# 								f_s_r_y = final_search_result_users.extend(channel_users)
# 								return final_search_result_users
# 							else:
# 								return 'There are no yaps that match this user handle' + str(user_handle_searched) + '.'
# 						else:
# 							yaps_in_channel_with_user = channel_searched.yaps.filter(user__username__istartswith=user_handle_searched,is_active=True,pk__lt=after)[:3 * amount]
# 							channel_users = [yap.user for user in yaps_in_channel_with_user]
# 							channel_users = sorted(set(channel_users),key=attrgetter('username'))[:amount]
# 							if len(channel_users) > 0:
# 								f_s_r_y = final_search_result_users.extend(channel_users)
# 								return final_search_result_users
# 							else:
# 								return 'There are no yaps that match this user handle' + str(user_handle_searched) + '.'
# 				else:
# 					return 'This search requires you to at least search in one channel.'

# 		elif number_of_user_handles_searched == 2:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				if number_of_channels_searched >= 1:
# 					for channel_searched in channels_searched:
# 						channel_searched = Channel.objects.get(pk=channel_searched)
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						yaps_in_channel_with_user = channel_searched.yaps.filter(user__username__istartswith=user_handle_searched,is_active=True)[:3 * amount]
# 						channel_users = [yap.user for user in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'))[:amount]
# 						if len(channel_users) > 0:
# 							final_search_result_users.extend(channel_users)
# 						else:
# 							return 'There are no yaps that match this user handle' + str(user_handle_searched) + '.'
# 					else:
# 						yaps_in_channel_with_user = channel_searched.yaps.filter(user__username__istartswith=user_handle_searched,is_active=True,pk__lt=after)[:3 * amount]
# 						channel_users = [yap.user for user in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'))[:amount]
# 						if len(channel_users) > 0:
# 							final_search_result_users.extend(channel_users)
# 						else:
# 							return 'There are no yaps that match this user handle' + str(user_handle_searched) + '.'
# 				else:
# 					return 'This search requires you to at least search in one channel.'
# 			if len(final_search_result_users) > 0:
# 				return final_search_result_users
# 			else:
# 				return 'There are no yaps that matched this search'


# 	#Explore Channels General Search ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_and_text_recent_search(self,user,channels_searched,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = ' ' + str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		for channel_searched in channels_searched:
# 			try:
# 				self.add_channels(channel_searched)
# 				channel_searched = Channel.objects.get(pk=channel_searched)
# 			except ObjectDoesNotExist:
# 				continue
# 			if number_of_words_searched == 1:
# 				if after is None:
# 					search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces)[:amount]
# 					search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left)[:amount]
# 					search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right)[:amount]
# 					search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched)[:amount]
# 					search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched)[:amount]
# 					search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched)[:amount]
# 					search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched)[:amount]
# 					search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 					search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 					search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]
# 					search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched,pk__lt=after)[:amount]
# 					search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched,pk__lt=after)[:amount]
# 					search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched,pk__lt=after)[:amount]
# 					search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			elif number_of_words_searched == 2:
# 				list_of_words_searched = text_searched.split()
# 				string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 				if after is None:
# 					search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces)[:amount]
# 					search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left)[:amount]
# 					search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right)[:amount]
# 					search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces)[:amount]
# 					search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=list_of_words_searched[0])[:amount]
# 					search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=list_of_words_searched[1])[:amount]
# 					search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 					search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 					search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 					search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]
# 					search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 					search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=list_of_words_searched[0],pk__lt=after)[:amount]
# 					search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=list_of_words_searched[1],pk__lt=after)[:amount]
# 					search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 		if len(final_search_result_yaps) > 0:
# 			final_serch_result_yaps1 = sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			return final_serch_result_yaps1
# 		else:
# 			return 'There were no yaps that met this search.'


# 	def explore_channels_and_text_people_search(self,user,channels_searched,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_users = []
# 		mutual_search_result_users = []
# 		if number_of_words_searched == 1:
# 			if number_of_channels_searched >= 1:
# 				for channel_searched in channels_searched:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 					if after is None:
# 						users_in_channel_with_user1 = channel_searched.yaps.filter(user__username__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user2 = channel_searched.yaps.filter(user__first_name__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user3 = channel_searched.yaps.filter(user__last_name__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user4 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__username__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user5 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__first_name__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user6 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__last_name__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						yaps_in_channel_with_user = sorted(set(chain(users_in_channel_with_user1,users_in_channel_with_user2,users_in_channel_with_user3,users_in_channel_with_user4,users_in_channel_with_user5,users_in_channel_with_user6)),key=attrgetter('date_created'))[:amount]
# 						channel_users = [yap.user for yap in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'),reverse=True)[:amount]
# 						if len(channel_users) > 0:
# 							f_s_r_y = final_search_result_users.extend(channel_users)
# 						else:
# 							pass
# 					else:
# 						users_in_channel_with_user1 = channel_searched.yaps.filter(user__username__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user2 = channel_searched.yaps.filter(user__first_name__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user3 = channel_searched.yaps.filter(user__last_name__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user4 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__username__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user5 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__first_name__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user6 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__last_name__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						yaps_in_channel_with_user = sorted(set(chain(users_in_channel_with_user1,users_in_channel_with_user2,users_in_channel_with_user3,users_in_channel_with_user4,users_in_channel_with_user5,users_in_channel_with_user6)),key=attrgetter('date_created'))[:amount]
# 						channel_users = [yap.user for yap in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'),reverse=True)[:amount]
# 						if len(channel_users) > 0:
# 							f_s_r_y = final_search_result_users.extend(channel_users)
# 						else:
# 							pass
# 				if len(final_search_result_users) > 0:
# 					return final_search_result_users
# 				else:
# 					return 'There are no yaps that match this text search' + str(user_handle_searched) + '.'
# 			else:
# 				return 'This search requires you to at least search in 1 channel.'

# 		elif number_of_words_searched == 2 and number_of_words_searched == 3:
# 			if number_of_channels_searched >= 1:
# 				for channel_searched in channels_searched:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						users_in_channel_with_user1 = channel_searched.yaps.filter(user__username__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user2 = channel_searched.yaps.filter(user__first_name__istartswith=list_of_words_searched[0],is_active=True)[:amount]
# 						users_in_channel_with_user3 = channel_searched.yaps.filter(user__last_name__istartswith=list_of_words_searched[1],is_active=True)[:amount]
# 						users_in_channel_with_user4 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__username__istartswith=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 						users_in_channel_with_user5 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__first_name__istartswith=list_of_words_searched[0],is_active=True)[:amount]
# 						users_in_channel_with_user6 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__last_name__istartswith=list_of_words_searched[1],is_active=True)[:amount]
# 						yaps_in_channel_with_user = sorted(set(chain(users_in_channel_with_user1,users_in_channel_with_user2,users_in_channel_with_user3,users_in_channel_with_user4,users_in_channel_with_user5,users_in_channel_with_user6)),key=attrgetter('date_created'))[:amount]
# 						channel_users = [yap.user for yap in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'),reverse=True)[:amount]
# 						if len(channel_users) > 0:
# 							final_search_result_users.extend(channel_users)
# 						else:
# 							pass
# 					else:
# 						users_in_channel_with_user1 = channel_searched.yaps.filter(user__username__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user2 = channel_searched.yaps.filter(user__first_name__istartswith=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user3 = channel_searched.yaps.filter(user__last_name__istartswith=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user4 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__username__istartswith=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user5 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__first_name__istartswith=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 						users_in_channel_with_user6 = channel_searched.yaps.filter(user_tags_flag=True,user_tags__last_name__istartswith=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 						yaps_in_channel_with_user = sorted(set(chain(yaps_in_channel_with_user1,yaps_in_channel_with_user2,yaps_in_channel_with_user3,yaps_in_channel_with_user4,yaps_in_channel_with_user5,yaps_in_channel_with_user6)),key=attrgetter('date_created'))[:amount]
# 						channel_users = [yap.user for yap in yaps_in_channel_with_user]
# 						channel_users = sorted(set(channel_users),key=attrgetter('username'),reverse=True)[:amount]
# 						if len(channel_users) > 0:
# 							final_search_result_users.extend(channel_users)
# 						else:
# 							pass
# 				if len(final_search_result_users) > 0:
# 					return final_search_result_users
# 				else:
# 					return 'There are no yaps that matched this search'
# 			else:
# 				return 'This search requires you to at least search in one channel.'

# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please search for 3 or less users at one time.'


# 	#Explore Channels and Hashtags Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_and_hashtags_recent_search(self,user,hashtags_searched,channels_searched,amount,after=None):
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id.'
# 				if number_of_hashtags_searched == 1:
# 					for hashtag_searched_text in hashtags_searched:
# 						self.add_hashtags(hashtag_searched_text)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,channel_flag=True,channel=channel_searched)[:amount]
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtags_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,channel_flag=True,channel=channel_searched)[:amount]
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched >= 4:
# 					return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 				elif number_of_hashtags_searched == 0:
# 			 		return 'This search is an error as this search requires a hashtag.'
# 			if len(final_search_result_yaps) >= 1:
# 				search_result_list = sorted(set(chain(final_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				return search_result_list
# 			elif len(search_result_list) == 0:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_channels_searched == 0:
# 			return 'This search is an error as this search requires a channel.'


# 	def explore_channels_and_user_handles_recent_search(self,user,user_handles_searched,channels_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		for channel_searched in channels_searched:
# 			self.add_channels(channel_searched)
# 			try:
# 				channel_searched = Channel.objects.get(pk=channel_searched)
# 			except ObjectDoesNotExist:
# 				return 'There is no channel with this id.'
# 			if number_of_user_handles_searched == 1:
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						continue
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						search_result_yaps = Yap.objects.filter(user=user_searched,is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 					else:
# 						search_result_yaps = Yap.objects.filter(user=user_searched,is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 			elif number_of_user_handles_searched == 2:
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_tags()
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user handle:' + str(user_handle_searched) + '.'
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						search_result_yaps = Yap.objects.filter(user=user_searched,is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 						if len(search_result_yaps) > 0:
# 							final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 					else:
# 						search_result_yaps = Yap.objects.filter(user=user_searched,is_active=True,is_private=False,channel_flag=True,channel=channel_searched)[:amount]
# 						if len(search_result_yaps) > 0:
# 							final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 					return search_result_list
# 			elif number_of_user_handles_searched >= 3:
# 				return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 			elif number_of_user_handles_searched == 0:
# 				return 'This search is an error as this search requires a user_tag.'
# 			elif number_of_user_handles_searched == 0:
# 				return 'This search is an error as this search requires a channel.'
# 		if len(final_search_result_yaps) >= 1:
# 			search_result_list = sorted(set(chain(final_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 		else:
# 			return 'There are no yaps with this user.'

# 	def explore_channels_and_hashtags_and_user_handles_recent_search(self,user,channels_searched,hashtags_searched,user_handles_searched,amount,after=None):
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id:' + '.'
# 				if number_of_user_handles_searched >= 1 and number_of_user_handles_searched <=3:
# 					for user_handle_searched in user_handles_searched:
# 						self.add_user_handles(user_handle_searched)
# 						try:
# 							user_searched = User.objects.get(pk=user_handle_searched)
# 						except ObjectDoesNotExist:
# 							'There is no user with this user handle:' + str(user_handle_searched) + '.'
# 						if number_of_hashtags_searched == 1:
# 							for hashtag_searched in hashtags_searched:
# 								self.add_hashtags(hashtag_searched)
# 								hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 								#Here the hashtag already exists in the database.
# 								if after is None:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched)[:amount]
# 									if len(search_result_yaps) > 0:
# 										f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 								else:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 									if len(search_result_yaps) > 0:
# 										f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 						elif number_of_user_handles_searched == 2 or number_of_user_handles_searched == 3:
# 							for hashtag_searched in hashtags_searched:
# 								self.add_hashtags(hashtags_searched)
# 								hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 								#Here the hashtag already exists in the database.
# 								if after is None:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channels_flag=True,channel=channel_searched)[:amount]
# 									if len(search_result_yaps) > 0:
# 										final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 								else:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched,pk__lt=after)[:amount]
# 									if len(search_result_yaps) > 0:
# 										final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 						elif number_of_hashtags_searched >= 4:
# 							return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 						elif number_of_hashtags_searched == 0:
# 							return 'This search is an error as this search requires a hashtag.'
# 				elif number_of_user_handles_searched == 0:
# 					return 'This search is an error as this search requires a user_handle.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(chain(final_search_result_yaps,mutual_search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		else:
# 			return 'This search requires at least 1 channel searched.'

# #Profile Posts Hashtags Search

# 	def profile_posts_hashtags_search(self,user,profile_searched,hashtags_searched,amount,after_yap=None,after_reyap=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after_yap is None and after_reyap is None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				elif after_yap is None and after_reyap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_reyap)[:amount]
# 				elif after_reyap is None and after_yap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_reyap)[:amount]		
# 				search_result_yaps = sorted(set(chain(reyaps,yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no results that match this search.'
# 		elif number_of_hashtags_searched == 2 or number_of_hashtags_searched ==3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_seached = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				if after_yap is None and after_reyap is None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				elif after_yap is None and after_reyap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_reyap)[:amount]
# 				elif after_reyap is None and after_yap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after_reyap)[:amount]		
# 				search_result_yaps = sorted(set(chain(reyaps,yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					return 'There are no yaps that match this hashtag.' + str(hashtag_searched.hashtag_name) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no results that match this search.'
# 		elif number_of_hashtags_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_hashtags_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'
		
# 	def profile_posts_user_handles_search(self,user,profile_searched,user_handles_searched,amount,after_yap=None,after_reyap=None):
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				#Here the hashtag already exists in the database.
# 				if after_yap is None and after_reyap is None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 				elif after_yap is None and after_reyap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 				elif after_reyap is None and after_yap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after_reyap)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				if after_yap is None and after_reyap is None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 				elif after_yap is None and after_reyap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 				elif after_reyap is None and after_yap is not None:
# 					yaps = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after_reyap)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Yap.objects.filter(user=profile_searched,ser_tags_flag=True,user_tags=user_searched,is_active=True,pk__lt=after_yap)[:amount]
# 					reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__user=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 					reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after_reyap)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_posts_hashtags_and_user_handles_search(self,user,profile_searched,hashtags_searched,user_handles_searched,amount,after_yap=None,after_reyap=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					#Here the hashtag already exists in the database.
# 					if after_yap is None and after_reyap is None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					elif after_yap is None and after_reyap is not None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					elif after_reyap is None and after_yap is not None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					else:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					if after_yap is None and after_reyap is None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					elif after_yap is None and after_reyap is not None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					elif after_reyap is None and after_yap is not None:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					else:
# 						yaps = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 						reyaps1 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__user=user_searched,is_active=True)[:amount]
# 						reyaps2 = Reyap.objects.filter(reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user=user_searched,is_active=True)[:amount]
# 						reyaps3 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 						reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,reyap_reyap__yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_posts_text_search(self,user,profile_searched,text_searched,amount,after_yap=None,after_reyap=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			#Here the hashtag already exists in the database.
# 			if after_yap is None and after_reyap is None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			elif after_yap is None and after_reyap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			elif after_reyap is None and after_yap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			else:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,reyaps1,reyaps2,reyaps3,reyaps4,reyaps5,reyaps6,reyaps7,reyaps8,reyaps9,reyaps10,reyaps11,reyaps12,reyaps13,reyaps14,reyaps15,reyaps16,reyaps17)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no yaps that match this:' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_words_searched == 2:
# 			if after_yap is None and after_reyap is None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			elif after_yap is None and after_reyap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			elif after_reyap is None and after_yap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_yap)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			else:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,user_tags_flag=True,user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_yap)[:amount]
# 				yaps5 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps6 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps7 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps8 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,yap__user__username__iexact=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps7 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps8 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps9 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps10 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps11 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps12 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps13 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user_tags_flag=True,reyap_reyap__yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps14 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps15 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps16 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps17 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,reyaps1,reyaps2,reyaps3,reyaps4,reyaps5,reyaps6,reyaps7,reyaps8,reyaps9,reyaps10,reyaps11,reyaps12,reyaps13,reyaps14,reyaps15,reyaps16,reyaps17)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no yaps that match this text:' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this text:' + str(text_searched) + '.'
# 		elif number_of_words_searched == 3 or number_of_words_searched == 4:
# 			if after_yap is None and after_reyap is None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps1 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			elif after_yap is None and after_reyap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			elif after_reyap is None and after_yap is not None:
# 				yaps1 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			else:	
# 				yaps1 = Yap.objects.filter(user=profile_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps2 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps3 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_yap)[:amount]
# 				yaps4 = Yap.objects.filter(user=profile_searched,title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_yap)[:amount]
# 				reyaps1 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps2 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps3 = Reyap.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps4 = Reyap.objects.filter(user=profile_searched,reyap_flag=False,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps5 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 				reyaps6 = Reyap.objects.filter(user=profile_searched,reyap_flag=True,reyap_reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after_reyap)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,reyaps1,reyaps2,reyaps3,reyaps4,reyaps5,reyaps6)),key=attrgetter('date_created'), reverse=True)[:amount]
# 		elif number_of_user_handles_searched >= 5:
# 			return 'Please only search 3 or less words in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to search with a word.'

# #Profile Like Hashtags Search

# 	def profile_likes_hashtags_search(self,user,profile_searched,hashtags_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					yaps = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_hashtags_searched == 2 or number_of_hashtags_searched ==3:
# 			for hashtag_searched in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_seached)
# 				hashtag_seached = Hashtag.objects.get(hashtag_name=hashtag_seached)
# 				if after is None:
# 					yaps = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.' 
# 		elif number_of_hashtags_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_hashtags_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'
		
# 	def profile_likes_user_handles_search(self,user,profile_searched,user_handles_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True)[:amount]
# 					reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after)[:amount]
# 					yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 					reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				if after is None:
# 					yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True)[:amount]
# 					reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True,pk__lt=after)[:amount]
# 					yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 					reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_likes_hashtags_and_user_handles_search(self,user,profile_searched,hashtags_searched,user_handles_searched,amount,after):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					else:
# 						yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					if after is None:
# 						yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					else:
# 						yaps = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						yaps1 = Like.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						reyaps = Like.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_likes_text_search(self,user,profile_searched,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			#Here the hashtag already exists in the database.
# 			if after is None:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps7 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps8 = Like.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps9 = Like.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps10 = Like.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			else:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps5 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps6 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps7 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps8 = Like.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps9 = Like.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps10 = Like.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,yaps9,yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no liked yaps that match this : ' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps6 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				yaps7 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps8 = Like.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps9 = Like.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps10 = Like.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 			else:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps5 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 				yaps6 = Like.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 				yaps7 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps8 = Like.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps9 = Like.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 				yaps10 = Like.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,reyaps1,reyaps2,reyaps3,reyaps4,reyaps5,reyaps6,reyaps7,reyaps8,reyaps9,reyaps10,reyaps11)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no yaps that match this:' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_words_searched == 3 or number_of_words_searched == 4:
# 			if after is None:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 			else:
# 				yaps1 = Like.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Like.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no liked yaps that match this : ' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_words_searched >= 5:
# 			return 'Please only search 4 or less words in the search bar.'

# #Profile Listens Hashtags Search

# 	def profile_listens_hashtags_search(self,user,profile_searched,hashtags_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_hashtags_searched == 2 or number_of_hashtags_searched ==3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_seached = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				if after is None:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that meet this search.'
# 		elif number_of_hashtags_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_hashtags_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'
		
# 	def profile_listens_user_handles_search(self,user,profile_searched,user_handles_searched,amount,after_yap=None,after_reyap=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True)[:amount]
# 					reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True,pk__lt=after)[:amount]
# 					yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 					reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle'
# 				if after is None:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True)[:amount]
# 					yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True)[:amount]
# 					reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True)[:amount]
# 				else:
# 					yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,is_active=True,pk__lt=after)[:amount]
# 					yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 					reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_listens_hashtags_and_user_handles_search(self,user,profile_searched,hashtags_searched,user_handles_searched,amount,after_yap=None,after_reyap=None):
# 		#user = User.objects.get(pk=user_id)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					#Here the hashtag already exists in the database.
# 					if after is None:
# 						yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					else:
# 						yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'

# 		elif number_of_user_handles_searched == 2 or number_of_user_handles_searched ==3:
# 			for hashtag_searched in hashtags_searched:
# 				self.add_hashtags(hashtag_searched)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle'
# 					if after is None:
# 						yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True)[:amount]
# 						yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True)[:amount]
# 						reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True)[:amount]
# 					else:
# 						yaps = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,user_tags=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True,pk__lt=after)[:amount]
# 						yaps1 = Listen.objects.filter(user=profile_searched,yap__user=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True,pk__lt=after)[:amount]
# 						reyaps = Listen.objects.filter(user=profile_searched,reyap_flag=True,reyap__user=user_searched,hashtags_flag=True,hashtags=hashtag_searched,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(yaps,yaps1,reyaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_user_handles_searched >= 4:
# 			return 'Please only search 3 or less hashtags in the search bar.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'Error: This function requires you to yap with a hashtag.'

# 	def profile_listens_text_search(self,user,profile_searched,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			#Here the hashtag already exists in the database.
# 			if after is None:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps6 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps7 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps8 = Listen.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps9 = Listen.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps10 = Listen.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 			else:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps5 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps6 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps7 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps8 = Listen.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps9 = Listen.objects.filter(user=profile_searched,yap__user__first_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps10 = Listen.objects.filter(user=profile_searched,yap__user__last_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,yaps9,yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no yaps that match this text:' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this text.'

# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps5 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps6 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 				yaps7 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps8 = Listen.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps9 = Listen.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True)[:amount]
# 				yaps10 = Listen.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True)[:amount]
# 			else:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps5 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 				yaps6 = Listen.objects.filter(user=profile_searched,yap__user_tags_flag=True,yap__user_tags__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 				yaps7 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps8 = Listen.objects.filter(user=profile_searched,yap__user__username__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps9 = Listen.objects.filter(user=profile_searched,yap__user__first_name__iexact=list_of_words_searched[0],is_active=True,pk__lt=after)[:amount]
# 				yaps10 = Listen.objects.filter(user=profile_searched,yap__user__last_name__iexact=list_of_words_searched[1],is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,yaps3,yaps4,yaps5,yaps6,yaps7,yaps8,yaps9,yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no yaps that match this user_handle:' + str(user_handle_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_words_searched == 3 or number_of_words_searched == 4:
# 			if after is None:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True)[:amount]
# 			else:
# 				yaps1 = Listen.objects.filter(user=profile_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps2 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_spaces,is_active=True,pk__lt=after)[:amount]
# 				yaps3 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_left,is_active=True,pk__lt=after)[:amount]
# 				yaps4 = Listen.objects.filter(user=profile_searched,yap__title__icontains=text_searched_with_space_on_right,is_active=True,pk__lt=after)[:amount]
# 			search_result_yaps = sorted(set(chain(yaps1,yaps2,reyaps1,reyaps2,reyaps3,reyaps4)),key=attrgetter('date_created'), reverse=True)[:amount]
# 			if len(search_result_yaps) > 0:
# 				f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 			else:
# 				return 'There are no liked yaps that match this : ' + str(text_searched) + '.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no profile posts that match this search.'
# 		elif number_of_words_searched >= 5:
# 			return 'Please only search 4 or less words in the search bar.'
# 		elif number_of_words_searched == 0:
# 			return 'Error: This function requires you to search with a word.'

# 	def stream_hashtags_search(self,user,hashtags_searched,amount,after=None):
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1 or number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				if after is None:
# 					search_result_yaps = Stream.objects.filter(user=user,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 				else:
# 					search_result_yaps = Stream.objects.filter(user=user,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True, pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					final_search_result_yaps.extend(search_result_yaps)
# 			if len(search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no stream objects that match this search.'

# 	def stream_user_handles_search(self,user,user_handles_searched,amount,after=None):
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1 or number_of_user_handles_searched == 2 or number_of_user_handles_searched == 3:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this user_handle.'
# 				if after is None:
# 					search_result_yaps1 = Stream.objects.filter(user=user,yap__user=user_searched,is_active=True)[:amount]
# 					search_result_yaps2 = Stream.objects.filter(user=user,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True)[:amount]
# 					search_result_reyaps1 = Stream.objects.filter(user=user,reyap_flag=True,reyap__user=user_searched,is_active=True)[:amount]
# 				else:
# 					search_result_yaps1 = Stream.objects.filter(user=user,yap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps2 = Stream.objects.filter(user=user,yap__user_tags_flag=True,yap__user_tags=user_searched,is_active=True,pk__lt=after)[:amount]
# 					search_result_reyaps1 = Stream.objects.filter(user=user,reyap_flag=True,reyap__user=user_searched,is_active=True,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 					final_search_result_yaps.extend(search_result_yaps)
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no posts that match this search.'

# 	def stream_hashtags_and_user_handles_search(self,user,hashtags_searched,user_handles_searched,amount,after=None):
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1 or number_of_user_handles_searched == 2 or number_of_user_handles_searched == 3:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				for user_handle_searched in user_handles_searched:
# 					self.add_user_handles(user_handle_searched)
# 					try:
# 						user_searched = User.objects.get(username=user_handle_searched)
# 					except ObjectDoesNotExist:
# 						return 'There is no user with this user_handle.'
# 					if after is None:
# 						search_result_yaps1 = Stream.objects.filter(user=user,yap__user=user_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						search_result_yaps2 = Stream.objects.filter(user=user,yap__user_tags=user_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 						search_result_reyaps1 = Stream.objects.filter(user=user,reyap_flag=True,reyap__user=user_searched,reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True)[:amount]
# 					else:
# 						search_result_yaps1 = Stream.objects.filter(user=user,yap__user=user_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						search_result_yaps2 = Stream.objects.filter(user=user,yap__user_tags=user_searched,yap__hashtags_flag=True,yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 						search_result_reyaps1 = Stream.objects.filter(user=user,reyap_flag=True,reyap__user=user_searched,reyap__yap__hashtags_flag=True,reyap_reyap__yap__hashtags__hashtag_name__iexact=hashtag_searched_text,is_active=True,pk__lt=after)[:amount]
# 					search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)[:amount]
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 			else:
# 				return 'There are no posts that match this search.'

# #Stream Text Search ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# 	def stream_text_search(self,user,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			if after is None:
# 				search_result_yaps1 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_spaces)[:amount]
# 				search_result_yaps2 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_left)[:amount]
# 				search_result_yaps3 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_right)[:amount]
# 				search_result_yaps4 = Stream.objects.filter(is_active=True,yap__hashtags__hashtag_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps5 = Stream.objects.filter(is_active=True,yap__user_tags__first_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps6 = Stream.objects.filter(is_active=True,yap__user_tags__last_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps7 = Stream.objects.filter(is_active=True,yap__user_tags__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps8 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__first_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps9 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__last_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps10 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7,search_result_yaps8,search_result_yaps9,search_result_yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'
# 			else:
# 				search_result_yaps1 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 				search_result_yaps2 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 				search_result_yaps3 = Stream.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]
# 				search_result_yaps4 = Stream.objects.filter(is_active=True,yap__hashtags__hashtag_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps5 = Stream.objects.filter(is_active=True,yap__user_tags__first_name__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps6 = Stream.objects.filter(is_active=True,yap__user_tags__last_name__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps7 = Stream.objects.filter(is_active=True,yap__user_tags__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps8 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__first_name__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps9 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__last_name__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps10 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7,search_result_yaps8,search_result_yaps9,search_result_yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'
# 		elif number_of_words_searched == 2:
# 			list_of_words_searched = text_searched.split()
# 			string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 			if after is None:
# 				search_result_yaps1 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_spaces)[:amount]
# 				search_result_yaps2 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_left)[:amount]
# 				search_result_yaps3 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_right)[:amount]	
# 				search_result_yaps4 = Stream.objects.filter(is_active=True,yap__hashtags__hashtag_name__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps5 = Stream.objects.filter(is_active=True,yap__user_tags__first_name__icontains=list_of_words_searched[0])[:amount]
# 				search_result_yaps6 = Stream.objects.filter(is_active=True,yap__user_tags__last_name__icontains=list_of_words_searched[1])[:amount]
# 				search_result_yaps7 = Stream.objects.filter(is_active=True,yap__user_tags__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps8= Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__first_name__icontains=list_of_words_searched[0])[:amount]
# 				search_result_yaps9 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__last_name__icontains=list_of_words_searched[1])[:amount]
# 				search_result_yaps10= Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__username__icontains=string_of_words_searched_without_spaces)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7,search_result_yaps8,search_result_yaps9,search_result_yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'
# 			else:
# 				search_result_yaps1 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_spaces,pk__lt=after)[:amount]
# 				search_result_yaps2 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_left,pk__lt=after)[:amount]
# 				search_result_yaps3 = Listen.objects.filter(is_active=True,yap__title__icontains=text_searched_with_space_on_right,pk__lt=after)[:amount]	
# 				search_result_yaps4 = Stream.objects.filter(is_active=True,yap__hashtags__hashtag_name__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps5 = Stream.objects.filter(is_active=True,yap__user_tags__first_name__icontains=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_yaps6 = Stream.objects.filter(is_active=True,yap__user_tags__last_name__icontains=list_of_words_searched[1],pk__lt=after)[:amount]
# 				search_result_yaps7 = Stream.objects.filter(is_active=True,yap__user_tags__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps8= Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__first_name__icontains=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_yaps9 = Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__last_name__icontains=list_of_words_searched[1],pk__lt=after)[:amount]
# 				search_result_yaps10= Stream.objects.filter(is_active=True,reyap_flag=True,reyap__user__username__icontains=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7,search_result_yaps8,search_result_yaps9,search_result_yaps10)),key=attrgetter('date_created'), reverse=True)[:amount]
# 				if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							return sorted(set(final_search_result_yaps),key=attrgetter('date_created'), reverse=True)[:amount]
# 				else:
# 					return 'There are no yaps related to:' + str(text_searched) + '.'


# #TRENDING STARTS HERE ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# #Trending Explore Hashtags Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_hashtags_trending_search(self,user,hashtags_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_hashtags_searched == 1:
# 			for hashtag_searched_text in hashtags_searched:
# 				self.add_hashtags(hashtag_searched_text)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched_text)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 			for hashtag_searched in hashtags_searched:
# 				self.add_hashtags(hashtag_searched)
# 				hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(user=user,is_active=True,is_private=False,hashtags_flag=True,hashtags__hashtag_name__iexact=hashtag_searched_text,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_hashtags_searched >= 4:
# 				return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 		elif number_of_hashtags_searched == 0:
# 			return 'This search is an error as this search requires a hashtag.'

# 	def explore_user_handles_trending_search(self,user,user_handles_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_user_handles_searched == 2:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'

# 	def explore_hashtags_and_user_handles_trending_search(self,user,hashtags_searched,user_handles_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_user_handles_searched >= 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				try:
# 					user_searched = User.objects.get(username=user_handle_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no user with this handle.'
# 				if number_of_hashtags_searched == 1:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtag_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user=user_searched,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtags_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user=user_searched,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched >= 4:
# 					return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 				elif number_of_hashtags_searched == 0:
# 					return 'This search is an error as this search requires a hashtag.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_user_handles_searched == 0:
# 			return 'This search is an error as this search requires a channel.'

# 	#Explore General Search ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_text_trending_search(self,user,text_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			if after is None:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,date_created__gte=time)
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,date_created__gte=time)
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,date_created__gte=time)
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=text_searched,date_created__gte=time)
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=text_searched,date_created__gte=time)
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=text_searched,date_created__gte=time)
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=text_searched,date_created__gte=time)
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			else:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,pk__lt=after,date_created__gte=time)
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,pk__lt=after,date_created__gte=time)
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,pk__lt=after,date_created__gte=time)
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=text_searched,pk__lt=after,date_created__gte=time)
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,date_created__gte=time)
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,date_created__gte=time)
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,date_created__gte=time)
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,date_created__gte=time)
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=list_of_words_searched[0],date_created__gte=time)
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=list_of_words_searched[1],date_created__gte=time)
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=string_of_words_searched_without_spaces,date_created__gte=time)
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			else:
# 				search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_spaces,pk__lt=after,date_created__gte=time)
# 				search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_left,pk__lt=after,date_created__gte=time)
# 				search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,title__icontains=text_searched_with_space_on_right,pk__lt=after,date_created__gte=time)			
# 				search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,hashtags__hashtag_name__iexact=string_of_words_searched_without_spaces,pk__lt=after,date_created__gte=time)
# 				search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,user__first_name__icontains=list_of_words_searched[0],pk__lt=after,date_created__gte=time)
# 				search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,user__last_name__icontains=list_of_words_searched[1],pk__lt=after,date_created__gte=time)
# 				search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,user__username__icontains=string_of_words_searched_without_spaces,pk__lt=after,date_created__gte=time)
# 				search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 				if len(search_result_yaps) > 0:
# 					f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 				else:
# 					pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		else:
# 			return 'Error: You must search a word for this search.'

# 	#Explore Channels Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_trending_search(self,user,channels_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched == 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id.'
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		elif number_of_channels_searched >= 2:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				channel_searched = Channel.objects.get(pk=channel_searched)
# 				#Here the hashtag already exists in the database.
# 				if after is None:
# 					search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 				else:
# 					search_result_yaps = Yap.objects.filter(user=user,is_active=True,is_private=False,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 					if len(search_result_yaps) > 0:
# 						final_search_result_yaps.extend(search_result_yaps)
# 					else:
# 						pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There are no yaps that match this search.'
# 		else:
# 			return 'This search requires you to at least search in 1 channel.'

# 	#Explore Channels General Search ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_and_text_trending_search(self,user,channels_searched,text_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		text_searched_with_space_on_left = ' ' + str(text_searched)
# 		text_searched_with_space_on_right = str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				try:
# 					self.add_channels(channel_searched)
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no such channel.'
# 				if number_of_words_searched == 1:
# 					if after is None:
# 						search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,date_created__gte=time)
# 						search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,date_created__gte=time)
# 						search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,date_created__gte=time)
# 						search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched,date_created__gte=time)
# 						search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 					else:
# 						search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,pk__lt=after,date_created__gte=time)
# 						search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,pk__lt=after,date_created__gte=time)
# 						search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,pk__lt=after,date_created__gte=time)
# 						search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 				elif number_of_words_searched == 2:
# 					list_of_words_searched = text_searched.split()
# 					string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 					if after is None:
# 						search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,date_created__gte=time)
# 						search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,date_created__gte=time)
# 						search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,date_created__gte=time)
# 						search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched,date_created__gte=time)
# 						search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched,date_created__gte=time)
# 						search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 					else:
# 						search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_spaces,pk__lt=after,date_created__gte=time)
# 						search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_left,pk__lt=after,date_created__gte=time)
# 						search_result_yaps3 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,title__icontains=text_searched_with_space_on_right,pk__lt=after,date_created__gte=time)
# 						search_result_yaps4 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,hashtags__hashtag_name__iexact=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps5 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__first_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps6 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__last_name__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps7 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user__username__icontains=text_searched,pk__lt=after,date_created__gte=time)
# 						search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2,search_result_yaps3,search_result_yaps4,search_result_yaps5,search_result_yaps6,search_result_yaps7)),key=attrgetter('date_created'), reverse=True)
# 						if len(search_result_yaps) > 0:
# 							f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 						else:
# 							pass
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There were no yaps that met this search.'
# 		else:
# 			return 'For this function you must search at least 1 channel.'

# 	#Explore Channels and Hashtags Search ---------------------------------------------------------------------------------------------------------------------------------------

# 	def explore_channels_and_hashtags_trending_search(self,user,hashtags_searched,channels_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id.'
# 				if number_of_hashtags_searched == 1:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtag_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,channel_flag=True,channel=channel_searched,date_created__gte=time)
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 							if len(search_result_yaps) > 0:
# 								return final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched == 2 or number_of_hashtags_searched == 3:
# 					for hashtag_searched in hashtags_searched:
# 						self.add_hashtags(hashtags_searched)
# 						hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,channel_flag=True,channel=channel_searched,date_created__gte=time)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_hashtags_searched >= 4:
# 					return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 				elif number_of_hashtags_searched == 0:
# 					return 'This search is an error as this search requires a hashtag.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There were no yaps that met this search.'
# 		elif number_of_channels_searched == 0:
# 			return 'This search is an error as this search requires a channel.'


# 	def explore_channels_and_user_handles_trending_search(self,user,user_handles_searched,channels_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		number_of_channels_searched = len(channels_searched)
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id.'
# 				if number_of_user_handles_searched == 1:
# 					for user_handle_searched in user_handles_searched:
# 						self.add_user_handles(user_handle_searched)
# 						user_searched = User.objects.get(username=user_handle_searched)
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user=user_searched,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_user_handles_searched == 2:
# 					for user_handle_searched in user_handles_searched:
# 						self.add_user_tags()
# 						try:
# 							user_searched = User.objects.get(username=user_handle_searched)
# 						except ObjectDoesNotExist:
# 							return 'There is no user with this user handle:' + str(user_handle_searched) + '.'
# 						#Here the hashtag already exists in the database.
# 						if after is None:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user=user_searched,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user_tags_flag=True,user_tags=user_searched,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 						else:
# 							search_result_yaps1 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps2 = Yap.objects.filter(is_active=True,is_private=False,channel_flag=True,channel=channel_searched,user_tags_flag=True,user_tags=user_searched,pk__lt=after,date_created__gte=time)
# 							search_result_yaps = sorted(set(chain(search_result_yaps1,search_result_yaps2)),key=attrgetter('date_created'), reverse=True)
# 							if len(search_result_yaps) > 0:
# 								final_search_result_yaps.extend(search_result_yaps)
# 							else:
# 								pass
# 				elif number_of_user_handles_searched >= 3:
# 					return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 				elif number_of_user_handles_searched == 0:
# 					return 'This search is an error as this search requires a user_tag.'
# 				elif number_of_user_handles_searched == 0:
# 					return 'This search is an error as this search requires a channel.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There were no yaps that met this search.'
# 		else:
# 			return 'This search requires you to search at least 1 channel.'

# 	def explore_channels_and_hashtags_and_user_handles_trending_search(self,user,channels_searched,hashtags_searched,user_handles_searched,amount,after=None,minutes=2880):
# 		time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
# 		number_of_hashtags_searched = len(hashtags_searched)
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		number_of_channels_searched = len(channels_searched)
# 		final_search_result_yaps = []
# 		mutual_search_result_yaps = []
# 		if number_of_channels_searched >= 1:
# 			for channel_searched in channels_searched:
# 				self.add_channels(channel_searched)
# 				try:
# 					channel_searched = Channel.objects.get(pk=channel_searched)
# 				except ObjectDoesNotExist:
# 					return 'There is no channel with this id:' + '.'
# 				if number_of_user_handles_searched >= 1 and number_of_user_handles_searched <=3:
# 					for user_handle_searched in user_handles_searched:
# 						self.add_user_handles(user_handle_searched)
# 						try:
# 							user_searched = User.objects.get(pk=user_handle_searched)
# 						except ObjectDoesNotExist:
# 							'There is no user with this user handle:' + str(user_handle_searched) + '.'
# 						if number_of_hashtags_searched == 1:
# 							for hashtag_searched in hashtags_searched:
# 								self.add_hashtags(hashtag_searched)
# 								hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 								#Here the hashtag already exists in the database.
# 								if after is None:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched,date_created__gte=time)
# 									if len(search_result_yaps) > 0:
# 										f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 								else:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 									if len(search_result_yaps) > 0:
# 										f_s_r_y = final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 						elif number_of_user_handles_searched == 2 or number_of_user_handles_searched == 3:
# 							for hashtag_searched in hashtags_searched:
# 								self.add_hashtags(hashtags_searched)
# 								hashtag_searched = Hashtag.objects.get(hashtag_name=hashtag_searched)
# 								#Here the hashtag already exists in the database.
# 								if after is None:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channels_flag=True,channel=channel_searched,date_created__gte=time)
# 									if len(search_result_yaps) > 0:
# 										final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 								else:
# 									search_result_yaps = Yap.objects.filter(is_active=True,is_private=False,hashtags_flag=True,hashtags=hashtag_searched,user_tags_flag=True,user_tags=user_searched,channel_flag=True,channel=channel_searched,pk__lt=after,date_created__gte=time)
# 									if len(search_result_yaps) > 0:
# 										final_search_result_yaps.extend(search_result_yaps)
# 									else:
# 										pass
# 						elif number_of_hashtags_searched >= 4:
# 							return 'You cannot search for more than 3 hashtags. Please change your search query.'
# 						elif number_of_hashtags_searched == 0:
# 							return 'This search is an error as this search requires a hashtag.'
# 				elif number_of_user_handles_searched == 0:
# 					return 'This search is an error as this search requires a user_handle.'
# 			if len(final_search_result_yaps) > 0:
# 				return sorted(set(final_search_result_yaps),key=yap_trending_score, reverse=True)[:amount]
# 			else:
# 				return 'There were no yaps that met this search.'
# 		else:
# 			return 'This search requires you to search in at least one channel.'

# #Yap People Searches --------------------------------------------------------------------------------------------------------------------------------------------------

# 	def yap_text_people_search(self,user,text_searched,amount,after=None):
# 		list_of_words_searched = text_searched.split()
# 		string_of_words_searched_without_spaces = text_searched.replace(' ','')
# 		text_searched_with_spaces = ' ' + str(text_searched) + ' '
# 		number_of_words_searched = len(list_of_words_searched)
# 		final_search_result_users = []
# 		mutual_search_result_yaps = []
# 		if number_of_words_searched == 1:
# 			if after is None:
# 				search_result_users = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces)[:amount]
# 				if len(search_result_users) > 0:
# 					f_s_r_y = final_search_result_users.extend(search_result_users)
# 				else:
# 					pass
# 			else:
# 				search_result_users = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 				if len(search_result_users) > 0:
# 					f_s_r_y = final_search_result_users.extend(search_result_users)
# 				else:
# 					pass
# 		elif number_of_words_searched == 2:
# 			if after is None:
# 				search_result_users1 = User.objects.filter(is_active=True,first_name__istartswith=list_of_words_searched[0])[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,last_name__istartswith=list_of_words_searched[1])[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces)[:amount]
# 			else:
# 				search_result_users1 = User.objects.filter(is_active=True,first_name__istartswith=list_of_words_searched[0],pk__lt=after)[:amount]
# 				search_result_users2 = User.objects.filter(is_active=True,last_name__istartswith=list_of_words_searched[1],pk__lt=after)[:amount]
# 				search_result_users3 = User.objects.filter(is_active=True,username__istartswith=string_of_words_searched_without_spaces,pk__lt=after)[:amount]
# 			search_result_users = sorted(set(chain(search_result_users1,search_result_users2,search_result_users3)),key=attrgetter('username'), reverse=True)[:amount]
# 			if len(search_result_users) > 0:
# 				f_s_r_y = final_search_result_users.extend(search_result_users)
# 			else:
# 				pass
# 		elif number_of_words_searched >= 3:
# 			return 'Please only search one or two words.'
# 		elif number_of_words_searched == 0:
# 			return 'This search requires at least one word to be searched.'
# 		if len(final_search_result_users) > 0:
# 				return sorted(set(final_search_result_users),key=attrgetter('username'), reverse=True)[:amount]
# 		else:
# 			return 'There were no users that matched this search.'

# 	def yap_user_handles_people_search(self,user,user_handles_searched,amount,after=None):
# 		#user = User.objects.get(pk=user_id)
# 		#user_searched = User.objects.get(username=user_handle_searched)
# 		#Here the hashtag already exists in the database.
# 		number_of_user_handles_searched = len(user_handles_searched)
# 		final_search_result_yaps = []
# 		if number_of_user_handles_searched == 1:
# 			for user_handle_searched in user_handles_searched:
# 				self.add_user_handles(user_handle_searched)
# 				if after is None:
# 					search_result_users = User.objects.filter(is_active=True,username__istartswith=user_handle_searched)[:amount]
# 					if len(search_result_users) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_users)
# 					else:
# 						pass
# 				else:
# 					search_result_users = User.objects.filter(is_active=True,username__istartswith=user_handle_searched,pk__lt=after)[:amount]
# 					if len(search_result_users) > 0:
# 						f_s_r_y = final_search_result_yaps.extend(search_result_users)
# 					else:
# 						pass
# 			if len(search_result_users) > 0:
# 				return sorted(set(search_result_users),key=attrgetter('username'), reverse=False)[:amount]
# 			else:
# 				return 'There were no users that matched this search.'
# 		else:
# 			return 'You must at least search for one user handle for this search.'
