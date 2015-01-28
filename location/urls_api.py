from django.conf.urls import patterns, include, url
from location.views_api import *

urlpatterns = patterns('location.views_api',
	url(r'^countries/load/$',LoadCountries.as_view()),
	url(r'^us_states/load/$',LoadUSStates.as_view()),
	#url(r'^city/find/$',FindCity.as_view()),
	url(r'^zipcode/find/$',FindZIPCode.as_view()),
)