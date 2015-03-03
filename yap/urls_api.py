from django.conf.urls import patterns, include, url
from yap.views_api import *

urlpatterns = patterns('yap.views_api',
	url(r'^load/library/info/$',LoadLibraryInfo.as_view()),
	url(r'^load/library/yaps/$',LoadLibraryYaps.as_view()),
	url(r'^create/yap/$',CreateYap.as_view()),
	url(r'^create/library/$',CreateLibrary.as_view()),
	url(r'^delete/yap/$',DeleteYap.as_view()),
	url(r'^delete/library/$',DeleteLibrary.as_view()),
	url(r'^subscribe/user/$',SubscribeUser.as_view()),
	url(r'^subscribe/library/$',SubscribeLibrary.as_view()),
	url(r'^unsubscribe/user/$',UnsubscribeUser.as_view()),
	url(r'^unsubscribe/library/$',UnsubscribeLibrary.as_view()),
	url(r'^listen/$',Listen.as_view()),
	url(r'^listen/set_time_listened/$',ListenSetTimeListened.as_view()),
	url(r'^listen/skip_clicked/$',ListenSkipClicked.as_view()),
)
