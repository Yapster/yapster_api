from django.conf.urls import patterns, include, url
from users.views_api import *

urlpatterns = patterns('users.views_api',

	url(r'^sign_up/verify_email/$',SignUpVerifyEmail.as_view()),
	url(r'^sign_up/verify_username/$',SignUpVerifyUsername.as_view()),
	url(r'^sign_up/$',SignUp.as_view()),
	url(r'^sign_in/$',SignIn.as_view()),
	url(r'^automatic_sign_in/$',AutomaticSignIn.as_view()),
	url(r'^sign_out/$',SignOut.as_view()),
	url(r'^load/dashboard/subscribed/users/$',LoadDashboardSubscribedUsers.as_view()),
	url(r'^load/dashboard/subscribed/libraries/$',LoadDashboardSubscribedLibraries.as_view()),
	url(r'^load/dashboard/explore/users/$',LoadDashboardExploreUsers.as_view()),
	url(r'^load/dashboard/explore/libraries/$',LoadDashboardExploreLibraries.as_view()),
	url(r'^load/profile/$',LoadProfile.as_view()),
	url(r'^load/settings/$',LoadProfile.as_view()),
	url(r'^edit/profile/$',EditProfile.as_view()),
	url(r'^edit/profile_picture/$',EditProfilePicture.as_view()),
	url(r'^edit/settings/$',EditSettings.as_view()),
	url(r'^delete/profile_picture/$',DeleteProfilePicture.as_view()),
	url(r'^disconnect/facebook_account/$',DisconnectFacebookAccount.as_view()),
	url(r'^disconnect/twitter_account/$',DisconnectTwitterAccount.as_view()),
	url(r'^forgot_password/request_for_email/$',ForgotPasswordRequestForEmail.as_view()),
	url(r'^forgot_password/request_for_reset_password/$',ForgotPasswordRequestForResetPassword.as_view()),
	)