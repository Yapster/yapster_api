from django.contrib.auth.models import User
from users.models import *
from yap.models import *
from notifications.models import *
from stream.models import *
from location.models import *
from operator import itemgetter
import random
import datetime
import time
import csv
def make_likes():
	users = list(User.objects.all())
	reyaps = list(Reyap.objects.all())
	for_checking = []
	user_copy = users
	for user in user_copy:
		num_likes = random.randint(10,20)
		possible_yaps = [post.yap.pk for post in Stream.objects.filter(user=user) if not post.reyap_flag]
		while num_likes > 0:
			if random.random() < 0.5:
				target = 'reyap'
			else:
				target = 'yap'
			print target
			if target == 'reyap':
				possible_reyaps = [post.yap.pk for post in Stream.objects.filter(user=user,is_active=True,reyap_flag=True)]
				print possible_reyaps
				if possible_reyaps == []:
					print ("possible_reyaps = empty = []")
					yap = None
					reyap = None
					reyap_flag = None
					like = {
					'yap'			:yap,
					'reyap_flag'	:reyap_flag,
					'reyap'			:reyap,
					'user'			:user
					}
					print user.pk, yap.pk
					#test = Like.objects.create(**like)
					#print user.pk, yap.pk, test.original_like
					print user.pk, yap.pk, like
					print ("num_likes")
					print num_likes
				else:
					print ("possible_reyaps are not empty")
					reyap_chosen = random.choice(possible_reyaps)
					if reyap_chosen in for_checking:
						reyap_chosen = random.choice(possible_reyaps)
					else:
						reyap = Reyap.objects.get(pk=reyap_chosen)
						print ("reyap")
						print reyap
						yap = reyap.yap
						reyap_flag = True
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
								'user'			:user
						}
						print user.pk, yap.pk
						#test = Like.objects.create(**like)
						#print user.pk, yap.pk, test.original_like
						print user.pk, yap.pk, like
						num_likes -= 1 
						print ("num_likes")
						print num_likes
			
		print(str(user.pk) + " has finished")
		gc.collect()

make_likes()
