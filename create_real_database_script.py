from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from users.models import *
from yap.models import *
from notification.models import *
from stream.models import *
from location.models import *
from operator import itemgetter
from questionaire.models import *
import random
import datetime
import time
import csv

print("starting on countries")
with open('countries.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	countries = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states_a = [x[2] for x in reader]

print("starting cities")
with open('cities.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	cities = [x[2] for x in reader]

print("starting on zip_codes")
with open('zip_code_database.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	zip_codes = [x[0] for x in reader]

print("starting on blacklist")
with open('blacklist1.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	blacklist = [x[0] for x in reader]

'''
channels = [
	'Art',
	'Beauty',
	'Business',
	'Celebrity Gossip',
	'Comedy',
	'Education',
	'Family',
	'Fashion',
	'Finance',
	'Food and Drinks',
	'Health and Fitness',
	'Misc',
	'Movies',
	'Music',
	'News',
	'Night Life',
	'Organizations',
	'Politics',
	'Religion',
	'Sports',
	'Summer',
	'Technology',
	'TV',
]

print("starting channels")
total = len(channels)
print total
for i,channel in enumerate(channels):
	channel_string = channel.replace(" ","")
	print(channel + " " + str(i) + "/" + str(total))
	Channel.objects.create(channel_name=channel,
		channel_description=channel,
		icon_explore_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_clicked.png',
		icon_explore_path_unclicked ='yapsterchannels/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_unclicked.png',
		icon_yap_path_clicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_clicked.png',
		icon_yap_path_unclicked='yapsterchannels/' + str(channel_string.lower()) + '/yap/' + str(channel_string.lower()) + '_yap_unclicked.png')
#'''

def create_countries():
	print(countries)
	for country_name in countries:
		print country_name
		country = {
			'country_name':country_name
		}
		Country.objects.create(**country)

#create_countries()

def create_states():
	i = 0
	for state_name in states:
		#print state_name
		state_abr = states_a[i]
		#print state_abr
		state = {
			'us_state_name':state_name,
			'us_state_abbreviation':state_abr,
			}
		print state
		i += 1
		USState.objects.create(**state)

#create_states()

def create_cities():
	for city_string in cities:
		country = Country.objects.get(country_name="United States")
		city_string1 = city_string.strip().split(',')
		city_name = city_string1[0]
		city_us_state = city_string1[1]
		try:
			us_state = USState.objects.get(us_state_name=city_us_state)
			print us_state
		except ObjectDoesNotExist:
			print ("Object does not exist.", city_us_state)
			us_state = None
		city = {
			'city_name'	:city_name,
			'us_state' :us_state,
			'country' :country,
		}
		print city
		City.objects.create(**city)

#create_cities()

def create_zipcodes():
	for zip_code in zip_codes:
		print zip_code
		zipcode_number = {
			'us_zip_code':zip_code
		}
		USZIPCode.objects.create(**zipcode_number)

#create_zipcodes()

def yapster_channel_users():
	print 1
	channels = Channel.objects.filter(is_active=True)
	print channels
	for channel in channels:
		print 2
		print ("Channel", channel)
		first_name = "Yapster"
		last_name = str(channel.channel_name)
		channel_without_spaces = channel.channel_name.replace(' ', '')
		email = str(channel_without_spaces.lower()) + '@yapster.co'
		password = 'Yapster' + str(channel_without_spaces.lower()) + '1234'
		channel_without_spaces = channel.channel_name.replace(' ', '')
		print (channel_without_spaces)
		username = 'yapster' + str(channel_without_spaces.lower())
		date_of_birth = '1999-06-18'
		gender = 'O'
		country_id = 184
		country = Country.objects.get(pk=country_id)
		print ("country", country)
		us_state_id = 32
		us_state = USState.objects.get(pk=us_state_id)
		print ("us_state", us_state)
		city_name = 'New York'
		session_device_token = '<2a2062ef a4eeb196 f96fddcb 418fcdea 9bcfd269 b37752ff e7448e50 5faacae6>'
		city = City.objects.get_or_create(city_name=city_name,us_state=us_state,country=country)
		print ("city", city)
		user = {
			'first_name'		:first_name,
			'last_name'			:last_name,
			'username'			:username,
			'email'				:email,
			'password'			:password,
			'gender'			:gender,
			'user_city'			:city[0],
			'user_us_state'		:us_state,
			'user_country'		:country,
			'date_of_birth'		:date_of_birth,
			'session_device_token'	:session_device_token
		}
		UserFunctions.create(**user)
		print user

#yapster_channel_users()

def yapster_channel_users_verified():
	users = User.objects.filter(is_active=True,first_name="Yapster")
	for user in users:
		print user
		user.functions.verify_user()
		print("verified")

#yapster_channel_users_verified()

def yapster_channel_users_recommended():
	users = User.objects.filter(is_active=True,first_name="Yapster")
	for user in users:
		print ("user", user)
		date_will_be_deactived1 = "2020-06-18"
		date_will_be_deactived = datetime.datetime.strptime(date_will_be_deactived1,"%Y-%m-%d").date()
		user.functions.recommend_user(date_will_be_deactived)
		print("recommended")

#yapster_channel_users_recommended()

#def channel_users_following_everyone_else():
#	users = User.objects.all()
#	for user in users:


def creating_blacklist():
	print blacklist
	blacklist1 = set(blacklist)
	for username_blacklisted in blacklist1:
		u1 = username_blacklisted.replace(' ','')
		u2 = u1.replace('\'','')
		u3 = u2.replace('-','')
		u4 = u3.replace('.','')
		u5 = u4.lower()
		print u5
		BlackList.objects.get_or_create(username=u5)

#creating_blacklist()

def deleting_blacklist():
	all_blacklist_items = BlackList.objects.all()
	for blacklist_item in all_blacklist_items:

		print blacklist_item.username
		blacklist_item.delete()

#deleting_blacklist()

def changing_channel_accounts_passwords():
	channel_users = User.objects.filter(pk__lt=24)
	for channel_user in channel_users:
		print channel_user.username
		channel_user.set_password('Yapster1234')
		channel_user.save(update_fields=['password'])

#changing_channel_accounts_passwords()

def create_no_yap_in_stream_questionaire():
	question_type1 = QuestionType.objects.get_or_create(question_type_name="Multiple Choice",question_type_description="A multiple choice question where users have to choose one answer from a group of options.")
	print question_type1[0]
	question_possible_answer1 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="0 - 15 minutes")
	print question_possible_answer1[0]
	question_possible_answer2 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="16 - 30 minutes")
	question_possible_answer3 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="31 - 60 minutes")
	question_possible_answer4 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="over 60 minutes")
	question_possible_answer5 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="not sure")
	question1 = Question.objects.get_or_create(question_type=question_type1[0],question_title="Question 1",question_text="How long do you plan to listen to audio content daily?",no_yaps_in_stream_questionaire_flag=True)
	#question1[0].question_possible_answers.add(question_possible_answer1[0],question_possible_answer2[0],question_possible_answer3[0],question_possible_answer4[0],question_possible_answer5[0])
	#question1[0].save()
	print question1[0].question_possible_answers.all()
	question_type2 = QuestionType.objects.get_or_create(question_type_name="Choose Two Of The Listen Below",question_type_description="A question which gives the user a set of options that the user must choose two answers ")
	print question_type2[0]	
	question_possible_answer6 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="Beauty/Fashion")
	print question_possible_answer6[0]
	question_possible_answer7 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="Entertainment (Celebrity Gossip/TV/Movies/Music)")
	question_possible_answer8 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="Food & Drinks")
	question_possible_answer9 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="Health & Fitness ")
	question_possible_answer10 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="News/Politics/Business")
	question_possible_answer11 = QuestionPossibleAnswer.objects.get_or_create(question_possible_answer_text="Sports")
	question2 = Question.objects.get_or_create(question_type=question_type2[0],question_title="Question 2",question_text="Which two categories of audio content listed below interests you most? (Please choose two categories below)",no_yaps_in_stream_questionaire_flag=True)
	#question2[0].question_possible_answers.add(question_possible_answer6[0],question_possible_answer7[0],question_possible_answer8[0],question_possible_answer9[0],question_possible_answer10[0],question_possible_answer11[0])
	#question2[0].save()
	print question2[0].question_possible_answers.all()

#create_no_yap_in_stream_questionaire()

def make_all_channels_follow_each_other():
	users = User.objects.filter(is_active=True)
	for user1 in users:
		for user2 in users:
			if user1 == user2:
				continue
			else:
				user1.functions.follow_request(user2.pk)

make_all_channels_follow_each_other()


