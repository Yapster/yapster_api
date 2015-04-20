from yap.models import *

def create_yap(user,title,description,length,audio_path,library,picture_flag=False,picture_path=None,picture_cropped_flag=False,picture_cropped_path=None):
	yap_arguments = {}
	length_of_description = len(description)
	user_tags_for_this_yap = [word for word in description.split() if word.startswith('@')]
	hashtags_for_this_yap = [word for word in description.split() if word.startswith('#')]
	website_link_keywords = [".com",".co",".net","http://","https://"]
	website_links_for_this_yap = set([word for word in description.split() for website_link_keyword in website_link_keywords if website_link_keyword in word])
	if len(set(user_tags_for_this_yap)) == 0:
		user_tags_flag = False
	elif len(set(user_tags_for_this_yap)) > 0:
		user_tags_flag = True
		user_tags = []
		for user_tag_for_this_yap in user_tags_for_this_yap:
			user_tag = user_tag_for_this_yap[:0] + user_tag_for_this_yap[1:]
			user_tags.append(user_tag)
	if len(set(hashtags_for_this_yap)) == 0:
		hashtags_flag = False
	elif len(set(hashtags_for_this_yap)) > 0:
		hashtags_flag = True
		hashtags = []
		for hashtag_for_this_yap in hashtags_for_this_yap:
			hashtag = hashtag_for_this_yap[:0] + hashtag_for_this_yap[1:]
			hashtags.append(hashtag)
	if len(set(website_links_for_this_yap)) == 0:
		website_links_flag = False
	elif len(set(website_links_for_this_yap)) > 0:
		website_links_flag = True
		website_links = []
		for website_link_for_this_yap in website_links_for_this_yap:
			website_links.append(website_link_for_this_yap)
	yap_arguments['user'] = user
	yap_arguments['title'] = title
	yap_arguments['description'] = description
	yap_arguments['length'] = length
	yap_arguments['audio_path'] = audio_path
	if picture_flag == True:
		yap_arguments['picture_flag'] = True
		yap_arguments['picture_path'] = picture_path
	if picture_cropped_flag == True:
		yap_arguments['picture_cropped_flag'] = True
		yap_arguments['picture_cropped_path'] = picture_cropped_path
	yap = Yap.objects.create(**yap_arguments)
	if user_tags_flag == True:
		if kwargs.get('user_tags_flag') == True:
			yap.add_user_tags(user_tags)
		yap.add_user_tags(user_tags)
	if hashtags_flag == True:
		yap.add_hashtags(hashtags)
	if website_links_flag == True:
		yap.add_website_links(website_links)
	library.add_yap(yap)
	library_yap_order = LibraryYapOrder.objects.create(library=library,yap=yap)
	return yap


def create_library(user,title,description,picture_flag=False,picture_path=None,picture_cropped_flag=False,picture_cropped_path=None):
	library_arguments = {}
	library_arguments['user'] = user
	library_arguments['title'] = title
	library_arguments['description'] = description
	if picture_flag == True:
		library_arguments['picture_flag'] = True
		library_arguments['picture_path'] = picture_path
	if picture_cropped_flag == True:
		library_arguments['picture_cropped_flag'] = True
		library_arguments['picture_cropped_path'] = picture_cropped_path
	library = Library.objects.create(**library_arguments)
	library_order = LibraryOrder.objects.create(library=library,user=user)
	return library

