from django.conf.urls import patterns, include, url
from search.views_api import *

urlpatterns = patterns('location.views_api',
	url(r'^explore/hashtags/recent_search/$',ExploreHashtagsRecentSearch.as_view()),
	url(r'^explore/hashtags/trending_search/$',ExploreHashtagsTrendingSearch.as_view()),

	url(r'^explore/user_handles/recent_search/$',ExploreUserHandlesRecentSearch.as_view()),
	url(r'^explore/user_handles/trending_search/$',ExploreUserHandlesTrendingSearch.as_view()),
	url(r'^explore/user_handles/people_search/$',ExploreUserHandlesPeopleSearch.as_view()),

	url(r'^explore/hashtags_and_user_handles/recent_search/$',ExploreHashtagsAndUserHandlesRecentSearch.as_view()),
	url(r'^explore/hashtags_and_user_handles/trending_search/$',ExploreHashtagsAndUserHandlesTrendingSearch.as_view()),

	url(r'^explore/text/recent_search/$',ExploreTextRecentSearch.as_view()),
	url(r'^explore/text/trending_search/$',ExploreTextTrendingSearch.as_view()),
	url(r'^explore/text/people_search/$',ExploreTextPeopleSearch.as_view()),

	url(r'^explore/channels/recent_search/$',ExploreChannelsRecentSearch.as_view()),
	url(r'^explore/channels/trending_search/$',ExploreChannelsTrendingSearch.as_view()),

	url(r'^explore/channels_and_hashtags/recent_search/$',ExploreChannelsAndHashtagsRecentSearch.as_view()),
	url(r'^explore/channels_and_hashtags/trending_search/$',ExploreChannelsAndHashtagsTrendingSearch.as_view()),

	url(r'^explore/channels_and_user_handles/search/$',ExploreChannelsAndUserHandlesRecentSearch.as_view()),
	url(r'^explore/channels_and_user_handles/trending_search/$',ExploreChannelsAndUserHandlesTrendingSearch.as_view()),
	url(r'^explore/channels_and_user_handles/people_search/$',ExploreChannelsAndUserHandlesPeopleSearch.as_view()),

	url(r'^explore/channels_and_hashtags_and_user_handles/recent_search/$',ExploreChannelsAndHashtagsAndUserHandlesRecentSearch.as_view()),
	url(r'^explore/channels_and_hashtags_and_user_handles/trending_search/$',ExploreChannelsAndHashtagsAndUserHandlesTrendingSearch.as_view()),

	url(r'^explore/channels_and_text/recent_search/$',ExploreChannelsAndTextRecentSearch.as_view()),
	url(r'^explore/channels_and_text/trending_search/$',ExploreChannelsAndTextTrendingSearch.as_view()),
	url(r'^explore/channels_and_text/people_search/$',ExploreChannelsAndTextPeopleSearch.as_view()),

	url(r'^profile/posts/hashtags/search/$',ProfilePostsHashtagsSearch.as_view()),
	url(r'^profile/posts/user_handles/search/$',ProfilePostsUserHandlesSearch.as_view()),
	url(r'^profile/posts/hashtags_and_user_handles/search/$',ProfilePostsHashtagsAndUserHandlesSearch.as_view()),
	url(r'^profile/posts/text/search/$',ProfilePostsTextSearch.as_view()),

	url(r'^profile/likes/hashtags/search/$',ProfileLikesHashtagsSearch.as_view()),
	url(r'^profile/likes/user_handles/search/$',ProfileLikesUserHandlesSearch.as_view()),
	url(r'^profile/likes/hashtags_and_user_handles/search/$',ProfileLikesHashtagsAndUserHandlesSearch.as_view()),
	url(r'^profile/likes/text/search/$',ProfileLikesTextSearch.as_view()),

	url(r'^profile/listens/hashtags/search/$',ProfileListensHashtagsSearch.as_view()),
	url(r'^profile/listens/user_handles/search/$',ProfileListensUserHandlesSearch.as_view()),
	url(r'^profile/listens/hashtags_and_user_handles/search/$',ProfileListensHashtagsAndUserHandlesSearch.as_view()),
	url(r'^profile/listens/text/search/$',ProfileListensTextSearch.as_view()),

	url(r'^stream/hashtags/search/$',StreamHashtagsSearch.as_view()),
	url(r'^stream/user_handles/search/$',StreamUserHandlesSearch.as_view()),
	url(r'^stream/hashtags_and_user_handles/search/$',StreamHashtagsAndUserHandlesSearch.as_view()),
	url(r'^stream/text/search/$',StreamTextSearch.as_view()),
	#url(r'^general/search/$',GeneralSearch.as_view()),

	url(r'^yap/text/people_search/$',YapTextPeopleSearch.as_view()),
	url(r'^yap/user_handles/people_search/$',YapUserHandlesPeopleSearch.as_view()),

	url(r'^explore/top_12_popular_hashtags/$',Top12PopularHashtags.as_view()),
	url(r'^explore/explore_screen_statistics/$',ExploreScreenStatistics.as_view()),
)