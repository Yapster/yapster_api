from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
import datetime
from users.models import Session

def check_session(user,session_id):
	try:
		session = Session.objects.get(pk=session_id,is_active=True)
	except ObjectDoesNotExist:
		return ("There is no such session_id",False)
	check = session.check_session(user=user,session_id=session_id)
	if isinstance(check,str):
		return (check,False)
	elif isinstance(check,bool):
		return (check,True)

def automatic_sign_in_check_session_id_and_device(user,session_id,device_type,identifier):
		try:
			session = Session.objects.get(pk=session_id,is_active=True)
		except ObjectDoesNotExist:
			return("There is no active session with this session_id.",False)
		check = session.automatic_sign_in_check_session_id_and_device(user=user,identifier=identifier)
		if isinstance(check,str):
			return (check,False)
		elif isinstance(check,bool):
			return (check,True)

def sign_in_check_session_id_and_device(user,device_type,identifier):
	if device_type == "computer":
		check = Session.objects.filter(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True).exists()
	elif device_type == "ios":
		check = Session.objects.filter(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True).exists()
	elif device_type == "android":
		check = Session.objects.filter(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True).exists()
	if check == True:
		try:
			if device_type == "computer":
				session = Session.objects.get(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True)
			elif device_type == "ios":
				session = Session.objects.get(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True)
			elif device_type == "android":
				session = Session.objects.get(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True)
		except MultipleObjectsReturned:
			if device_type == "computer":
				active_sessions = Session.objects.filter(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True)
			elif device_type == "ios":
				active_sessions = Session.objects.filter(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True)
			elif device_type == "android":
				active_sessions = Session.objects.filter(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True)
			for active_session in active_sessions:
				active_session.close_session()
				if device_type == "computer":
					new_session = Session.objects.get_or_create(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True)[0]
				elif device_type == "ios":
					new_session = Session.objects.get_or_create(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True)[0]
				elif device_type == "android":
					new_session = Session.objects.get_or_create(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True)[0]
				check = new_session.sign_in_check_session_id_and_device_token(session_device_token=session_device_token)
				return (new_session.pk,True)
		time_check = session.sign_in_check_session_id()
		if time_check == True:
			return (session.pk,True)
		elif time_check == False:
			if device_type == "computer":
				new_session = Session.objects.get_or_create(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True)[0]
			elif device_type == "ios":
				new_session = Session.objects.get_or_create(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True)[0]
			elif device_type == "android":
				new_session = Session.objects.get_or_create(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True)[0]
			return (new_session.pk,True)
	elif check == False:
		if device_type == "computer":
			new_session = Session.objects.get_or_create(user=user,device_computer_flag=True,device_computer_ip=identifier,is_active=True)[0]
		elif device_type == "ios":
			new_session = Session.objects.get_or_create(user=user,device_ios_flag=True,device_ios_token=identifier,is_active=True)[0]
		elif device_type == "android":
			new_session = Session.objects.get_or_create(user=user,device_android_flag=True,device_android_registration_id=identifier,is_active=True)[0]
		return(new_session.pk,True)




#When you're filtering and try to aggregate numbers and that we created fake likes, listens, reyaps.