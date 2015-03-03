from django.conf.urls import patterns, include, url
from search.views_api import *

urlpatterns = patterns('search.views_api',
	url(r'^default/$',DefaultSearch.as_view()),

	url(r'^explore/top_12_popular_hashtags/$',Top12PopularHashtags.as_view()),
)