from yap.models import *
from users.models import *
import datetime
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db.models import Sum

def recommended_users_to_follow_according_to_questionaire(user):
	#a = datetime.datetime.now()
	#print a
	if Answer.objects.filter(user=user,is_active=True).exists() == True:
		if Answer.objects.filter(user=user,question__question_id=1,is_active=True).exists() == True:
			if Answer.objects.filter(user=user,question__question_id=2,is_active=True).exists() == True:
				answer_to_question_1 = Answer.objects.get(user=user,question__question_id=1,is_active=True)
				answers_to_question_2 = Answer.objects.filter(user=user,question__question_id=2,is_active=True)
				if answer_to_question_1.chosen_answer.question_possible_answer_id == 1 or answer_to_question_1.chosen_answer.question_possible_answer_id == 5:
					minimum_time_yapped = 15
				elif answer_to_question_1.chosen_answer.question_possible_answer_id == 2:
					minimum_time_yapped = 30
				elif answer_to_question_1.chosen_answer.question_possible_answer_id == 3:
					minimum_time_yapped = 60
				elif answer_to_question_1.chosen_answer.question_possible_answer_id == 4:
					minimum_time_yapped = 120
				else:
					pass
				channels_interested_in = []
				for answer_to_question_2 in answers_to_question_2:
					if answer_to_question_2.chosen_answer.question_possible_answer_id == 6:
						channels_interested_in_for_this_answer = [2,8]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					elif answer_to_question_2.chosen_answer.question_possible_answer_id == 7:
						channels_interested_in_for_this_answer = [4,5,23,13,14]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					elif answer_to_question_2.chosen_answer.question_possible_answer_id == 8:
						channels_interested_in_for_this_answer = [10,16]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					elif answer_to_question_2.chosen_answer.question_possible_answer_id == 9:
						channels_interested_in_for_this_answer = [11]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					elif answer_to_question_2.chosen_answer.question_possible_answer_id == 10:
						channels_interested_in_for_this_answer = [3,15,18]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					elif answer_to_question_2.chosen_answer.question_possible_answer_id == 11:
						channels_interested_in_for_this_answer = [20]
						channels_interested_in.extend(channels_interested_in_for_this_answer)
					else:
						continue
				#b = datetime.datetime.now()
				#print b, "time to check if answers exist", b-a
				users_to_recommend = []
				recommendations = Recommended.objects.filter(is_active=True)
				users_that_are_recommended = [recommendation.user for recommendation in recommendations]
				for user_recommended in users_that_are_recommended:
					time_yapped_in_channels_interested = 0
					#d = datetime.datetime.now()
					#print d, "time to finish first layer loop", d-b
					#f = b
					for channel_id in channels_interested_in:
						#e = datetime.datetime.now()
						#f = e
						#print e-f, "time to finish channel loop"
						channel = Channel.objects.get(pk=channel_id)
						if time_yapped_in_channels_interested == 0:
							if Yap.objects.filter(is_active=True,user=user_recommended).count() + Reyap.objects.filter(is_active=True,user=user_recommended).count() != 0:
								time_yapped_in_channels_interested = Yap.objects.filter(is_active=True,user=user_recommended,channel=channel).aggregate(Sum('length'))['length__sum'] + Reyap.objects.filter(is_active=True,user=user_recommended,yap__channel=channel).aggregate(Sum('length'))['yap__length__sum']
							else:
								continue
						else:
							if Yap.objects.filter(is_active=True,user=user_recommended).count() + Reyap.objects.filter(is_active=True,user=user_recommended).count() != 0:
								time_yapped_in_channels_interested = time_yapped_in_channels_interested + Yap.objects.filter(is_active=True,user=user_recommended,channel=channel).aggregate(Sum('length'))['length__sum'] + Reyap.objects.filter(is_active=True,user=user_recommended,yap__channel=channel).aggregate(Sum('length'))['yap__length__sum']
							else:
								continue
					if time_yapped_in_channels_interested >= minimum_time_yapped:
						users_to_recommend.append(user_recommended)
				#c = datetime.datetime.now()
				#print c, "time to finish loop", c-b
				if not users_to_recommend:
					users_to_recommend = users_that_are_recommended
				return users_to_recommend
			elif Answer.objects.filter(user=user,question__question_id=2,is_active=True).exists() == False:
				recommendations = Recommended.objects.filter(is_active=True)
				users_that_are_recommended = [recommendation.user for recommendation in recommendations]
				return users_that_are_recommended
				#User has not completed the questionaire so there is nothing to calculate results off of. 
		elif Answer.objects.filter(user=user,question__question_id=1,is_active=True).exists() == False:
			#User hasn't taken the questionaire yet. 
			recommendations = Recommended.objects.filter(is_active=True)
			users_that_are_recommended = [recommendation.user for recommendation in recommendations]
			return users_that_are_recommended
	elif Answer.objects.filter(user=user,is_active=True).exists() == False:
		#User hasn't taken the qustionaire yet.
		recommendations = Recommended.objects.filter(is_active=True)
		users_that_are_recommended = [recommendation.user for recommendation in recommendations]
		return users_that_are_recommended
		