from django.contrib.auth.models import User
from users.models import *
from yap.models import *
from location.models import *
from operator import itemgetter
import random
import datetime
import time
import csv
import requests
import json
from django.core.exceptions import MultipleObjectsReturned

"""
IMPORTANT NOTE

when looking at likes, listens, and reyaps, always look at original_object
because reyap will not be null in order to keep the information of where 
it came from, but even though it will not be null, the action does not count
as a reyap action because it is placed on a like...ORIGINAL_OBJECT = FALSE IS 
ALWAYS ABOUT A YAP BUT FROM A REYAP
"""

user_created_date = datetime.datetime.now()
user_requested_date = user_created_date + datetime.timedelta(days=1)
miminum_yap_date = user_created_date + datetime.timedelta(seconds=300)
minimum_yap_action_date = user_requested_date + datetime.timedelta(seconds=300)

print("starting first names")
with open('CSV_Database_of_First_Names.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	first_names = [x[0] for x in reader]

print("starting last names")
with open('CSV_Database_of_Last_Names.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	last_names = [x[0] for x in reader]

print("starting cities")
with open('cities.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	cities = [x[1] for x in reader]

print("starting on countries")
with open('countries.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	countries = [x[1] for x in reader]

print("starting on states")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states_names = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states_abbreviations = [x[2] for x in reader]

print("starting on states_abbreviations")
with open('state_table.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	states = [x[1] for x in reader]

print("starting on states_abbreviations")
with open('zip_code_database.csv','Ur') as f:
	reader = csv.reader(f)
	header = reader.next()
	zipcodes = [x[0] for x in reader]

print("starting words")
with open("/usr/share/dict/words","r") as f:
	words = [x.strip() for x in f.readlines()]

print len(words)

print(words[:10])

print "Starting hashtags"
with open('hashtags.csv','r') as f:
	reader = csv.reader(f)
	header = reader.next()
	hashtags = [x[1] for x in reader]


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


'''
print("starting channels")

total = len(channels)
print total
for i,channel in enumerate(channels):
	channel_string = channel.replace(" ","")
	print(channel + " " + str(i) + "/" + str(total))
	Channel.objects.create(name=channel,
		description=channel,
		picture_flag='misc/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_clicked.png',
		picture_path ='misc/' + str(channel_string.lower()) + '/explore/' + str(channel_string.lower()) + '_explore_unclicked.png')

#'''

import gc
profile_pictures = [
	'misc/twins1.jpg',
	'misc/twins2.jpg',
	'misc/twins3.jpg',
	'misc/twins4.jpg',	
]

profile_pictures_cropped = [
	'misc/twins1.jpg',
	'misc/twins2.jpg',
	'misc/twins3.jpg',
	'misc/twins4.jpg',	
]

yap_images = [
	'misc/twins1.jpg',
	'misc/twins2.jpg',
	'misc/twins3.jpg',
	'misc/twins4.jpg',	
]

web_cover_pictures = [
	'misc/webcoverpicture1.jpg',
	'misc/webcoverpicture2.jpg',
	'misc/webcoverpicture3.jpg',
	'misc/webcoverpicture4.jpg',	
]

audio_paths = [
	'misc/ashlee_1.mp3', 
	'misc/gurkaran_1.mp3',
]

device_types = [
	'computer',
	'android',
	'ios',
]


def date_time_between(start,end):
	between = end - start
	seconds = (between.days * 24 * 60 * 60) + between.seconds
	random_seconds = random.randrange(seconds)
	return start + datetime.timedelta(seconds=random_seconds)

def date_between(start,end):
	between = end - start
	random_days = random.randint(0,between.days)
	return start + datetime.timedelta(days=random_days)

def rand(options,times=20):
	probabilities = options.values()
	while times > 0:
		random_number = random.random()
		threshold = 0
		answer = None
		for item in options.iteritems():
			threshold += item[1]
			if random_number <= threshold:
				answer = item[0]
				break
		print(answer)
		times -= 1

def incremented(item):
	#returns a dictionary with values that are probabilities'''
	range_ids = range(1,len(item)+1)
	size = len(range_ids)
	#x/1 + x/2 + ... + x/size = 1
	#x * sum([1/i for i in range_ids]) = 1
	x = 1.0/sum([1/float(i) for i in range_ids])
	#check to make sure it's right
	probabilities = [x/float(i) for i in range_ids]
	return dict(zip(range_ids,probabilities))

'''
def create_countries():
	print(countries)
	for country in countries:
		print country
		country_name = {
			'name':country
		}
		Country.objects.create(**country_name)

create_countries()

def create_states():
	print(states)
	for state in states:
		print state
		state_name = {
			'name':state
		}
		USState.objects.create(**state_name)

create_states()
def create_zipcodes():
	print(zipcodes)
	for zipcode in zipcodes:
		print zipcode
		zipcode_number = {
			'name':zipcode
		}
		USZIPCode.objects.create(**zipcode_number)

create_zipcodes()

#'''
'''
def create_users():
	limit=30
	initial = limit
	user_hold = []
	while limit > 0:
		limit -= 1
		print limit
		payload = {}
		seed1 = random.randint(0,len(first_names)-1)
		seed2 = random.randint(0,len(last_names)-1)
		#seed3 = random.randint(0,len(states)-1)
		#seed4 = random.randint(0,len(cities)-1)
		first_name = first_names[seed1]
		payload['first_name'] = first_name
		last_name = last_names[seed2]
		payload['last_name'] = last_name
		full_name = (first_name,last_name)
		same_name_number = user_hold.count(full_name)
		user_hold.append(full_name)
		if same_name_number < 1:
			username = first_name.lower() + '_' + last_name.lower()
		else:
			username = first_name.lower() + '_' + last_name.lower() + '_' + str(same_name_number)
		payload['username'] = username
		email = username + "@yapster.co"
		payload['email'] = email
		print limit
		password = 'ABCD1234'
		payload['password'] = password		
		gender_list = ['M','F','O']
		gender = random.choice(gender_list)
		payload['gender'] = gender
		phone_number = ''
		if random.random() < 0.15:
			for x in range(10):
				phone_number += str(random.randint(0,9))
			payload['phone_number'] = phone_number
		if random.random() < 0.9:
			country_id = 184
			payload['country_id'] = country_id
			us_state_id = 32
			payload['us_state_id'] = us_state_id
			city_name = "New York"
			payload['city_name'] = city_name
		else:
			city_name = None
			us_state_id = None
			country_id = None
		print limit
		#random bday calculator
		date_of_birth = "1993-05-14"
		payload['date_of_birth'] = date_of_birth
		#create description
		description = 'HAHAHAHAHAHAHAHAHHA This is a test.'
		payload['description'] = description
		print limit
		num_words = random.randint(10,20)
		print limit
		# while num_words > 0:
		# 	description += words[random.randint(0,len(words)-1)]
		# 	if num_words > 1:
		# 		description += " "
		# 	num_words -= 1
		print limit
		profile_picture_flag = True
		profile_picture_path = random.choice(profile_pictures)
		profile_cropped_picture_flag = True
		profile_cropped_picture_path = random.choice(profile_pictures)
		payload['profile_picture_flag'] = profile_picture_flag
		payload['profile_picture_path'] = profile_picture_path
		payload['profile_cropped_picture_flag'] = profile_cropped_picture_flag
		payload['profile_cropped_picture_path'] = profile_cropped_picture_path
		print limit
		image_cropped = profile_pictures_cropped[random.randint(0,len(profile_pictures_cropped)-1)]
		print limit
		pk = initial - limit
		device_type = random.choice(device_types)
		payload['device_type'] = device_type
		device_computer_ip = ""
		device_android_registration_id = ""
		device_ios_token =  ""
		if device_type == "computer":
			device_computer_ip = "65.209.60.146"
			payload['device_computer_ip'] = device_computer_ip
		elif device_type == "android":
			device_android_registration_id = "3635D0D6229162A0"
			payload['device_android_registration_id'] = device_android_registration_id
		elif device_type == "ios":
			device_ios_token = "FE66489F304DC75B8D6E8200DFF8A456E8DAEACEC428B427E9518741C92C6660"
			payload['device_ios_token'] = device_ios_token
		print limit
		url = 'http://localhost:8000/users/sign_up/'
		headers = {'Content-type': 'application/json'}
		print payload
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		print r.status_code

create_users()

#'''
'''
def make_user_subscriptions():
	users = list(User.objects.all())
	user_ids = [user.pk for user in users]
	if SubscribeUser.objects.all().exists() == True:
		requesters = [l.user for l in SubscribeUser.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	for i,user in enumerate(user_copy):
		user_ids_copy = list(user_ids)
		user_ids_copy.remove(user.pk)
		#print len(user_keys)
		number_seed = random.randint(10,20)
		original_seed = number_seed
		print number_seed
		while number_seed > 0:
			seed = random.randint(0,len(user_ids_copy)-1)
			requested_user = user_ids_copy.pop(seed)
			url = 'http://localhost:8000/yap/subscribe/user/'
			headers = {'Content-type': 'application/json'}
			payload = {}
			print "user.pk  :  " + str(user.pk)
			payload['user_id'] = user.pk
			session = Session.objects.get(user=user,is_active=True)
			payload['session_id'] = session.pk
			payload['subscribing_user_id'] = requested_user
			print payload
			r = requests.post(url, data=json.dumps(payload), headers=headers)
			print r.status_code
			print(i, user.pk, number_seed, original_seed)
			number_seed -= 1
		print(str(user.pk) + " has finished")
		gc.collect()

make_user_subscriptions()

#'''
'''
def make_library_subscriptions():
	users = list(User.objects.all())
	user_ids = [user.pk for user in users]
	if SubscribeLibrary.objects.all().exists() == True:
		requesters = [l.user for l in SubscribeLibrary.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	for i,user in enumerate(user_copy):
		user = User.objects.get(pk=1)
		libraries = list(Library.objects.all())
		library_ids = [library.pk for library in libraries]
		#print len(user_keys)
		number_seed = random.randint(10,20)
		original_seed = number_seed
		print number_seed
		while number_seed > 0:
			seed = random.randint(0,len(library_ids)-1)
			subscribing_library_id = library_ids.pop(seed)
			url = 'http://localhost:8000/yap/subscribe/library/'
			headers = {'Content-type': 'application/json'}
			payload = {}
			print "user.pk  :  " + str(user.pk)
			payload['user_id'] = user.pk
			session = Session.objects.get(user=user,is_active=True)
			payload['session_id'] = session.pk
			payload['subscribing_library_id'] = subscribing_library_id
			print payload
			r = requests.post(url, data=json.dumps(payload), headers=headers)
			print r.status_code
			print(i, user.pk, number_seed, original_seed)
			number_seed -= 1
		print(str(user.pk) + " has finished")
		gc.collect()

make_library_subscriptions()

#'''



'''

print("starting yaps")

def make_yaps():
	if Yap.objects.all().exists():
		#requesters = [yap.user for yap in Yap.objects.all()]
		#user_copy = [user for user in users if user not in requesters]
		libraries = Library.objects.all()
	else:
		libraries = Library.objects.all()
	print ("starting yaps")
	for library in libraries:
		num_yaps = random.randint(5,10)
		print ("num_yaps",num_yaps)
		while num_yaps > 0:
			payload = {}
			payload['library_id'] = library.pk
			print ("num_yaps",num_yaps)
			#hashtag creation
			print ("user",library.user.pk, num_yaps)
			#title creation
			num_words = random.randint(2,10)
			title = ""
			while num_words > 0:
				seed = random.randint(0,len(words)-1)
				word = words[seed]
				if num_words == 1:
					title += word
				elif num_words > 1:
					title +=  word + " "
				num_words -= 1
			payload['title'] = title
			description = title
			if random.random() < 1.0:
				num_hashtags = random.randint(1,6)
				hashtags_flag = True
				list_of_hashtags = list(hashtags)
				yap_hashtags = random.sample(list_of_hashtags,num_hashtags)
				for yap_hashtag in yap_hashtags:
					description = description + " #" + yap_hashtag
					print ("THis is the description : " + description)
			else:
				hashtags_flag = False
			payload['description'] = description
			if random.random() < 0.7:
				picture_flag = True
				picture_path = random.choice(yap_images)
				picture_cropped_flag = True
				picture_cropped_path = picture_path
				payload['picture_flag'] = picture_flag
				payload['picture_path'] = picture_path
				payload['picture_cropped_flag'] = picture_cropped_flag
				payload['picture_cropped_path'] = picture_cropped_path
			else:
				picture_path = None
				picture_flag = False
				payload['picture_flag'] = picture_flag
			audio_path = random.choice(audio_paths)
			payload['audio_path'] = audio_path
			length = random.randint(10,600)
			payload['length'] = length
			#date_created = date_time_between(miminum_yap_date,datetime.datetime(2014,3,1,0,0,0))
			url = 'http://localhost:8000/yap/create/yap/'
			headers = {'Content-type': 'application/json'}
			print "user.pk  :  " + str(library.user.pk)
			payload['user_id'] = library.user.pk
			session = Session.objects.get(user=library.user,is_active=True)
			payload['session_id'] = session.pk
			print json.dumps(payload)
			r = requests.post(url, data=json.dumps(payload), headers=headers)
			print r.status_code
			num_yaps -= 1

		print str(user.pk) + " has finished"

	gc.collect()

make_yaps()

#'''

yaps = list(Yap.objects.all())
users = list(User.objects.all())
'''
def make_reyaps():
	for_checking = []
	if Reyap.objects.all().exists():
		requesters = [reyap.user for reyap in Reyap.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	print ("starting reyaps")
	for user in user_copy:
		num_reyaps = random.randint(25,50)
		print ("num_reyaps", num_reyaps)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_reyaps > 0:
			print("user", user)
			print ("num_reyaps", num_reyaps)
			print ("possible_reyaps", possible_reyaps)
			print ("possible_yaps", possible_yaps)
			if random.random() < 0.5 and len(possible_reyaps) > 0:
				target = 'reyap'
			else:
				if len(possible_yaps) > 0:
					target = 'yap'
				else:
					target = "reyap"
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				#print ("possible_yaps", possible_yaps)
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:   
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					new_reyap = {
						'yap'				:yap,
						'user'				:user,
						'reyap_flag'		:reyap_flag,
						'reyap_reyap'		:reyap
					}
					print ("new_reyap", new_reyap)
					Reyap.objects.create(**new_reyap)
					num_reyaps -= 1
			elif target == 'reyap' and possible_reyaps != []:				
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				print ("reyap", reyap)
				#print ("user.pk, yap.pk", user.pk, yap.pk)
				#print ("new_reyap", new_reyap)
				reyap.reyap(user)
				num_reyaps -= 1
			#print num_reyaps
			elif possible_reyaps == []:
				print("the possible_reyaps queryset is empty.") 
		print ("num_reyaps", num_reyaps)
			#print num_reyaps
	print(str(user.pk) + " has finished")
	gc.collect()


start = datetime.datetime.now()
end = datetime.datetime.now()
make_reyaps()
print("Reyaps created in " + str(end-start))
#'''
users = list(User.objects.all())

'''
def make_likes():
	for_checking = []
	if Like.objects.all().exists():
		requesters = [like.user for like in Like.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		reyaps = list(Reyap.objects.all())
		user_copy = users
	for user in user_copy:
		num_likes = random.randint(50,75)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_likes > 0:
			if random.random() < 0.5:
				target = 'reyap'
			else:
				target = 'yap'
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				print possible_yaps
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:	
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					like = {
					'yap'			:yap,
					'reyap_flag'	:reyap_flag,
					'reyap'			:reyap,
					'user'			:user
					}
					print user.pk, yap.pk
					print like
					Like.objects.create(**like)
			elif target == 'reyap' and possible_reyaps != []:
				#possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
				
				print possible_reyaps
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				like = {
				'yap'			:yap,
				'reyap_flag'	:reyap_flag,
				'reyap'			:reyap,
				'user'			:user,
				}
				print user.pk, yap.pk
				print like
				reyap.like(user)
			num_likes -= 1 
			print ("num_likes")
			print num_likes
		print(str(user.pk) + " has finished")
		gc.collect()

make_likes()

#	sorted_listens = sorted(listens)
#	final = []
#	for pk,listen in enumerate(sorted_listens):
#		actual_listen = listen[1]
#		actual_listen['id'] = pk
#		final.append(actual_listen)
#	return final

start = datetime.datetime.now()
end = datetime.datetime.now()
print("Likes created in " + str(end-start))

#'''
users = list(User.objects.all())

'''
def make_listens():
	for_checking = []
	if Listen.objects.all().exists():
		requesters = [listen.user for listen in Listen.objects.all()]
		user_copy = [user for user in users if user not in requesters]
	else:
		user_copy = users
	for user in user_copy:
		num_listens = random.randint(100,150)
		#userlikes = [like.yap.pk for like in user.likes.all()]
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
		while num_listens > 0:
			if random.random() < 0.5:
				target = 'reyap'
			else:
				target = 'yap'
			print target
			if target == 'yap':
				seed = random.choice(possible_yaps)
				print possible_yaps
				print ("seed", seed)
				yap = Yap.objects.get(pk=seed)
				if (yap.pk,user.pk) in for_checking:
					continue
				else:	
					for_checking.append((yap.pk,user.pk))
					reyap = None
					reyap_flag = False
					listen = {
					'yap'			:yap,
					'reyap_flag'	:reyap_flag,
					'reyap'			:reyap,
					'user'			:user
					}
					print user.pk, yap.pk
					print listen
					Listen.objects.create(**listen)
			elif target == 'reyap' and possible_reyaps != []:
				#possible_reyaps = [post.reyap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
				print possible_reyaps
				reyap_chosen = random.choice(possible_reyaps)
				reyap = Reyap.objects.get(pk=reyap_chosen)
				yap = reyap.yap
				if (yap.pk,user.pk) in for_checking:
					continue
				reyap_flag=True
				if not (yap.pk,user.pk) in for_checking:
					for_checking.append((yap.pk,user.pk))
					fake_needed = True
					try:
						possible_yaps.remove(reyap.yap.pk)
					except:
						pass
				else:
					fake_needed = False
				listen = {
				'yap'			:yap,
				'reyap_flag'	:reyap_flag,
				'reyap'			:reyap,
				'user'			:user,
				}
				print user.pk, yap.pk
				print listen
				reyap.listen(user)
			num_listens -= 1 
			print ("num_listens")
			print num_listens
		print(str(user.pk) + " has finished")
		gc.collect()

make_listens()

start = datetime.datetime.now()
listens = make_listens()
end = datetime.datetime.now()
print("Listens created in " + str(end-start))

#'''
'''
def fix_user_profile_pictures():

	users = User.objects.all()
	for user in users:
		print str(user.pk) + " , " + user.username
		user.profile.profile_picture_flag = True
		user.profile.profile_picture_path = random.choice(yap_images)
		user.profile.profile_cropped_picture_flag = True
		user.profile.profile_cropped_picture_path = user.profile.profile_picture_path
		user.profile.save()
		print "part 1 done"
		info = UserInfo.objects.get(user_id=user.pk)
		info.profile_picture_flag = True
		info.profile_picture_path = random.choice(yap_images)
		info.profile_cropped_picture_flag = True
		info.profile_cropped_picture_path = user.profile.profile_picture_path
		info.save()
		print "part 2 done"
		print user.profile.profile_picture_flag
		print user.profile.profile_picture_path
		print user.profile.profile_cropped_picture_flag
		print user.profile.profile_cropped_picture_path
		print info.profile_picture_flag
		print info.profile_picture_path
		print info.profile_cropped_picture_flag
		print info.profile_cropped_picture_path

fix_user_profile_pictures()

#'''
'''
def correct_subscriptions_library():

	users = list(User.objects.all())
	user_ids = [user.pk for user in users]
	libraries = list(Library.objects.all())
	library_ids = [library.pk for library in libraries]
	user = User.objects.get(pk=1)
	#print len(user_keys)
	number_seed = random.randint(10,20)
	original_seed = number_seed
	print number_seed
	while number_seed > 0:
		seed = random.randint(0,len(library_ids)-1)
		subscribing_library_id = library_ids.pop(seed)
		url = 'http://localhost:8000/yap/subscribe/library/'
		headers = {'Content-type': 'application/json'}
		payload = {}
		print "user.pk  :  " + str(user.pk)
		payload['user_id'] = user.pk
		session = Session.objects.get(user=user,is_active=True)
		payload['session_id'] = session.pk
		payload['subscribing_library_id'] = subscribing_library_id
		print payload
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		print r.status_code
		number_seed -= 1
	print(str(user.pk) + " has finished")
	gc.collect()

correct_subscriptions_library()

#'''
'''
def change_path_of_all_yap():
	print "in the function"
	if random.random() < 0.50:
		users = User.objects.all()
		for user in users:
			print user.pk
			user.profile.web_cover_picture_1_flag = True
			user.profile.web_cover_picture_1_path = random.choice(profile_pictures)
			user.profile.save()
			userInfo = UserInfo.objects.get(pk=user.pk)
			userInfo.web_cover_picture_1_flag = True
			userInfo.web_cover_picture_1_path = user.profile.web_cover_picture_1_path
			userInfo.save()
			print "done"

change_path_of_all_yap()
#'''
