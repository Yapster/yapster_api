from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import datetime

def yap_trending_score(yap):
	yap_listen_count = yap.listens.count()
	yap_like_count = yap.likes.count()
	yap_reyap_count = yap.reyaps.count()
	yap_listen_score = yap_listen_count
	yap_like_score = yap_like_count * 2
	yap_reyap_score = yap_reyap_count * 4
	yap_trending_score = yap_listen_score + yap_like_score + yap_reyap_score
	return yap_trending_score

def hashtag_trending_score(hashtag):
	number_of_yaps_with_hashtag = Yap.objects.filter(hashtags=hashtag,is_active=True).count()
	return number_of_yaps_with_hashtag

def listening_score_for_user_based_on_subscribed_user(subscribe_user):
	amount_of_time_listened_query = Listen.objects.filter(user=subscribe_user.user,yap__user=subscribe_user.subscribed_user,is_active=True).annotate(amount_of_time_listened=Count('time_listened'))
	amount_of_time_listened = amount_of_time_listened_query[0].amount_of_time_listened
	return amount_of_time_listened

def listening_score_for_library_based_on_subscribed_user(subscribe_library):
	amount_of_time_listened_query = Listen.objects.filter(user=subscribe_library.user,yap__library=subscribe_library.subscribed_library,is_active=True).annotate(amount_of_time_listened=Count('time_listened'))
	amount_of_time_listened = amount_of_time_listened_query[0].amount_of_time_listened
	return amount_of_time_listened

def listening_score_for_users(user):
	amount_of_time_listened_query = Listen.objects.filter(yap__user=user,is_active=True).annotate(amount_of_time_listened=Count('time_listened'))
	amount_of_time_listened = amount_of_time_listened_query[0].amount_of_time_listened
	return amount_of_time_listened

def listening_score_for_libraries(library):
	amount_of_time_listened_query = Listen.objects.filter(yap__library=library,is_active=True).annotate(amount_of_time_listened=Count('time_listened'))
	amount_of_time_listened = amount_of_time_listened_query[0].amount_of_time_listened
	return amount_of_time_listened