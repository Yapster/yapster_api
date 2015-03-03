from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
import yapster_api.views

urlpatterns = patterns('',
                       url(r'^$',"yapster_api.views.aws_index"),
                       url(r'users/',include('users.urls_api')),
                       url(r'yap/',include('yap.urls_api')),
                       url(r'location/',include('location.urls_api')),
                       url(r'search/',include('search.urls_api')),
                       url(r'^download/ios/$', RedirectView.as_view(url='https://itunes.apple.com/us/app/yapster/id899766051?mt=8')),
                       )