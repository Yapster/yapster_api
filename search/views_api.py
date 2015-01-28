from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from yapster_utils import check_session
from users.models import *
from users.serializers import *
from search.models import *
from search.serializers import *
from yap.serializers import *
import datetime
from datetime import timedelta
from django.db.models import Count
from yapster_utils import hashtag_trending_score

#Explore Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreHashtagsRecentSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,is_recent=True,is_after_request=True)
				search_results = search.explore_hashtags_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,is_recent=True)
				search_results = search.explore_hashtags_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreHashtagsTrendingSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,is_trending=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_hashtags_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,is_trending=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_hashtags_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreUserHandlesRecentSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_recent=True,is_after_request=True)
				search_results = search.explore_user_handles_recent_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_recent=True)
				search_results = search.explore_user_handles_recent_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreUserHandlesTrendingSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_trending=True,is_after_request=True)
				search_results = search.explore_user_handles_trending_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_trending=True)
				search_results = search.explore_user_handles_trending_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreUserHandlesPeopleSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_people=True,is_after_request=True)
				search_results = search.explore_user_handles_people_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,is_people=True)
				search_results = search.explore_user_handles_people_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreHashtagsAndUserHandlesRecentSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_search_flag=True,user_handles_searched_flag=True,is_recent=True,is_after_request=True)
				search_results = search.explore_hashtags_and_user_handles_recent_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_search_flag=True,user_handles_searched_flag=True,is_recent=True)
				search_results = search.explore_hashtags_and_user_handles_recent_search(user=user,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreHashtagsAndUserHandlesTrendingSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_search_flag=True,user_handles_searched_flag=True,is_trending=True,is_after_request=True)
				search_results = search.explore_hashtags_and_user_handles_trending_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_search_flag=True,user_handles_searched_flag=True,is_trending=True)
				search_results = search.explore_hashtags_and_user_handles_trending_search(user=user,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


class ExploreTextRecentSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_recent=True,is_after_request=True)
				search_results = search.explore_text_recent_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_recent=True)
				search_results = search.explore_text_recent_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreTextTrendingSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		print ("text_searched",str(request['text_searched']))
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_trending=True,is_after_request=True)
				search_results = search.explore_text_trending_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_trending=True)
				search_results = search.explore_text_trending_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


class ExploreTextPeopleSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_people=True,is_after_request=True)
				search_results = search.explore_text_people_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_people=True)
				search_results = search.explore_text_people_search(user=user,text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


#Explore Channels Search ----------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsRecentSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,is_recent=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_recent_search(user=user,channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,is_recent=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_recent_search(user=user,channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels Search ----------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsTrendingSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,is_trending=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_trending_search(user=user,channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,is_trending=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_trending_search(user=user,channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndHashtagsRecentSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,channels_searched_flag=True,is_recent=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_and_hashtags_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,channels_searched_flag=True,is_recent=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.explore_channels_and_hashtags_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndHashtagsTrendingSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,channels_searched_flag=True,is_trending=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,channels_searched_flag=True,is_trending=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndUserHandlesRecentSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_recent=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_recent_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_recent=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_recent_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndUserHandlesTrendingSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_trending=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_trending_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_trending=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_trending_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreChannelsAndUserHandlesPeopleSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_people=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_people_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_people=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_user_handles_people_search(user=user,user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndHashtagsAndUserHandlesRecentSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_recent=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_and_user_handles_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_recent=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_and_user_handles_recent_search(user=user,hashtags_searched=kwargs['hashtags_searched'],user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Explore Channels and Hashtags Search -----------------------------------------------------------------------------------------------------------------------------------------------

class ExploreChannelsAndHashtagsAndUserHandlesTrendingSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_trending=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_and_user_handles_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,hashtags_searched_flag=True,user_handles_searched_flag=True,channels_searched_flag=True,is_trending=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.explore_channels_and_hashtags_and_user_handles_trending_search(user=user,hashtags_searched=kwargs['hashtags_searched'],user_handles_searched=kwargs['user_handles_searched'],channels_searched=kwargs['channels_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreChannelsAndTextRecentSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		print ("text_searched",str(request['text_searched']))
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_recent=True,is_after_request=True)
				search_results = search.explore_channels_and_text_recent_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_recent=True)
				search_results = search.explore_channels_and_text_recent_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


class ExploreChannelsAndTextTrendingSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_trending=True,is_after_request=True)
				search_results = search.explore_channels_and_text_trending_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_trending=True)
				search_results = search.explore_channels_and_text_trending_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExploreSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreChannelsAndTextPeopleSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_people=True,is_after_request=True)
				search_results = search.explore_channels_and_text_people_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,channels_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_people=True)
				search_results = search.explore_channels_and_text_people_search(user=user,channels_searched=request['channels_searched'],text_searched=str(request['text_searched']),amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ExplorePeopleSearchSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Posts Hashtag Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfilePostsHashtagsSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			after_yap = kwargs.get("after_yap",None)
			after_reyap = kwargs.get("after_reyap",None)
			profile_searched = User.objects.get(pk=kwargs['profile_searched_id'])
			if 'after_yap' in kwargs or 'after_reyap' in kwargs:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after_yap=kwargs['after_yap'],after_reyap=kwargs['after_reyap'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Posts User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfilePostsUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after_yap = request.get("after_yap",None)
			after_reyap = request.get("after_reyap",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after_yap' in request or 'after_reyap' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after_yap=request['after_yap'],request=request['after_reyap'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Posts Hashtags and User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfilePostsHashtagsAndUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after_yap = request.get("after_yap",None)
			after_reyap = request.get("after_reyap",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after_yap' in request or 'after_reyap' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'],after_yap=request['after_yap'],request=request['after_reyap'])
				if isinstance(search_results,str):
					return Response({"valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Posts Hashtags and User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfilePostsTextSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after_yap = request.get("after_yap",None)
			after_reyap = request.get("after_reyap",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after_yap' in request or 'after_reyap' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']),is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_posts_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'],after_yap=request['after_yap'],request=request['after_reyap'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_posts_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']))
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				print search
				search_results = search.profile_posts_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


#Profile Like Hashtags Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileLikesHashtagsSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			after = kwargs.get("after",None)
			profile_searched = User.objects.get(pk=kwargs['profile_searched_id'])
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Likes User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileLikesUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = request.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Likes Hashtags and User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileLikesHashtagsAndUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = request.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Likes Hashtags and User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileLikesTextSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = request.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']),is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_likes_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']))
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_likes_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Listens Hashtags Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileListensHashtagsSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			after = kwargs.get("after",None)
			profile_searched = User.objects.get(pk=kwargs['profile_searched_id'])
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_hashtags_search(user=user,profile_searched=profile_searched,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Listens User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileListensUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = kwargs.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_user_handles_search(user=user,profile_searched=profile_searched,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Listens Hashtags and User Handles Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileListensHashtagsAndUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = kwargs.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,user_handles_searched_flag=True,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_hashtags_and_user_handles_search(user=user,profile_searched=profile_searched,hashtags_searched=request['hashtags_searched'],user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

#Profile Listens Text Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class ProfileListensTextSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			after = request.get("after",None)
			profile_searched = User.objects.get(pk=request['profile_searched_id'])
			if 'after' in request:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']),is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response({"Valid":False,"Message":search_results})
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,profile_searched_flag=True,profile_listens_stream_searched_flag=True,profile_searched=profile_searched,general_searched_flag=True,text_searched=str(request['text_searched']))
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.profile_listens_text_search(user=user,profile_searched=profile_searched,text_searched=request['text_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ProfileSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


#Stream Hashtags Search ------------------------------------------------------------------------------------------------------------------------------------------------------------

class StreamHashtagsSearch(APIView):

	def post(self,request,format=None):
		kwargs = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=kwargs['user_id'])
		check = check_session(user,kwargs['session_id'])
		if check[1]:
			if 'after' in kwargs:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,hashtags_searched_flag=True,is_after_request=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.stream_hashtags_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'],after=kwargs['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,hashtags_searched_flag=True)
				#search_results = user.functions.hashtag_search(hashtag_searched=request['hashtag_searched'],amount=request['amount'],after=request['after'])
				search_results = search.stream_hashtags_search(user=user,hashtags_searched=kwargs['hashtags_searched'],amount=kwargs['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class StreamUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,user_handles_searched_flag=True,is_after_request=True)
				search_results = search.stream_user_handles_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,user_handles_searched_flag=True)
				search_results = search.stream_user_handles_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class StreamHashtagsAndUserHandlesSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,user_handles_searched_flag=True,is_after_request=True)
				search_results = search.stream_hashtags_and_user_handles_search(user=user,user_handles_searched=request['user_handles_searched'],hashtags_searched=request['hashtags_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,stream_searched_flag=True,user_handles_searched_flag=True)
				search_results = search.stream_hashtags_and_user_handles_search(user=user,user_handles_searched=request['user_handles_searched'],hashtags_searched=request['hashtags_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class StreamTextSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_after_request=True)
				search_results = search.stream_text_search(user=user,text_searched=request['text_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,explore_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']))
				search_results = search.stream_text_search(user=user,text_searched=request['text_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = StreamSearchResultsSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class YapUserHandlesPeopleSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,yap_searched_flag=True,user_handles_searched_flag=True,is_after_request=True)
				search_results = search.yap_user_handles_people_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = ListUserSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,yap_searched_flag=True,user_handles_searched_flag=True)
				search_results = search.yap_user_handles_people_search(user=user,user_handles_searched=request['user_handles_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ListUserSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])


class YapTextPeopleSearch(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			if 'after' in request:
				search = Search.objects.create(user_searching=user,yap_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']),is_after_request=True)
				search_results = search.yap_text_people_search(user=user,text_searched=request['text_searched'],amount=request['amount'],after=request['after'])
				if isinstance(search_results,str):
					return Response(search_results)
				else:
					serialized = ListUserSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
			else:
				search = Search.objects.create(user_searching=user,yap_searched_flag=True,general_searched_flag=True,text_searched=str(request['text_searched']))
				search_results = search.yap_text_people_search(user=user,text_searched=request['text_searched'],amount=request['amount'])
				if isinstance(search_results,str):
					return Response(None)
				else:
					serialized = ListUserSerializer(search_results,data=self.request.DATA,many=True,context={'user':user})
					return Response(serialized.data)
		else:
			return Response(check[0])

class ExploreScreenStatistics(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			serialized = ExploreScreenStatisticsSerializer(user)
			return Response(serialized.data)
		else:
			return Response(check[0])

class Top12PopularHashtags(APIView):

	def post(self,request,format=None):
		request = {k:v for k,v in request.DATA.iteritems()}
		user = User.objects.get(pk=request['user_id'])
		check = check_session(user,request['session_id'])
		if check[1]:
			minutes = 2880
			amount = 12
			time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
			yaps = Yap.objects.filter(hashtags_flag=True,is_active=True,is_private=False,date_created__gte=time)
			hashtags_list = Hashtag.objects.filter(yaps__in=yaps,is_blocked=False)
			hashtags = sorted(set(hashtags_list),key=hashtag_trending_score,reverse=True)[:amount]
			if isinstance(hashtags,str):
				return Response(None)
			else:
				serialized = HashtagSerializer(hashtags,data=self.request.DATA,many=True)
				return Response(serialized.data)
		else:
			return Response(check[0])


