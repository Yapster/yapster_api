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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class DefaultSearch(APIView):

	def post(self,request,**kwargs):
		request = {k:v for k,v in request.DATA.iteritems()}
		if 'user_id' in request:
			user = User.objects.get(pk=request['user_id'])
			check = check_session(user,request['session_id'])
			if check[1]:
				pass
			else:
				Response({"valid":False,"message":check[0]})
		else:
			user = None
		if "search_id" in request:
			search_id = request['search_id']
			search = Search.objects.get(pk=search_id)
		else:
			screen = request.get("screen")
			text = request.get("text")
			longitude = request.get("longitude", None)
			latitude = request.get("latitude", None)
			if screen == "dashboard_subscribed":
				search = Search.objects.create(user=user,origin_dashboard_subscribed_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_subscribed_view_all_users":
				search = Search.objects.create(user=user,origin_dashboard_subscribed_view_all_users_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_subscribed_view_all_libraries":
				search = Search.objects.create(user=user,origin_dashboard_subscribed_view_all_libraries_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_explore":
				search = Search.objects.create(user=user,origin_dashboard_explore_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_explore_view_all_users":
				search = Search.objects.create(user=user,origin_dashboard_explore_view_all_users_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_explore_view_all_libraries":
				search = Search.objects.create(user=user,origin_dashboard_explore_view_all_libraries_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "dashboard_explore_view_all":
				search = Search.objects.create(user=user,origin_dashboard_explore_view_all_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "profile":
				search = Search.objects.create(user=user,origin_profile_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "library_details":
				search = Search.objects.create(user=user,origin_profile_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
			elif screen == "web":
				search = Search.objects.create(user=user,origin_web_screen_flag=True,text=text,latitude=latitude,longitude=longitude)
		search_type = request.get("search_type","all")
		page = request.get('page',1)
		amount = request.get('amount',5)
		if search_type == "all":
			serialized = SearchResultsSerializer(search,context={'user':user})
			return Response({"valid":True,"search_id":search.pk,"data":serialized.data})
		elif search_type == "users":
			search_results = search.default_user_search()
		elif search_type == "libraries":
			search_results = search.default_library_search()
		elif search_type == "yaps":
			search_results = search.default_yap_search()
		paginator = Paginator(object_list=search_results,per_page=amount,allow_empty_first_page=False)
		try:
			results = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			return Response({"valid":False,"message":"Page is not an integer."})
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			return Response({"valid":True,"data":None})
		if search_type == "users":
			serialized = UserSerializer(results,many=True,context={'user':user})
		elif search_type == "libraries":
			serialized = LibraryPreviewSerializer(results,many=True,context={'user':user})
		elif search_type == "yaps":
			serialized = AbstractYapSerializer(results,many=True,context={'user':user})
		return Response({"valid":True,"search_id":search.pk,"data":serialized.data})

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


