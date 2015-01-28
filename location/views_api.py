from rest_framework.response import Response
from rest_framework.decorators import api_view
from location.serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from location.models import *
from django.utils import timezone
from yapster_utils import check_session

class LoadCountries(APIView):

	def get(self,request):
		countries = Country.objects.all()
		serialized = CountrySerializer(countries,many=True)
		return Response(serialized.data)

class LoadUSStates(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		country_id = request['country_id']
		us_country = Country.objects.get(country_name='United States')
		print us_country.pk
		if country_id == us_country.pk:
			us_states = USState.objects.all()
			serialized = USStateSerializer(us_states,many=True)
			return Response(serialized.data)
		else:
			return Response({"Mesage":"Request is invalid."})
'''
class FindCity(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		if 'us_state_id' in request and 'country_id' in request:
			country = Countries.objects.get(pk=request.pop('country_id'))
			us_state = USStates.objects.get(pk=request.pop('us_state_id'))
			city = Cities.objects.filter(city=request['city_name'],us_state=us_state,country=country)
			if len(city) == 1:
				return Response({"Valid":True,"city_id":city.pk})
			elif len(city) >= 2:
				return CitySerializer(city)
			elif len(city) >= 0:
				created_city = Cities.objects.create(city=request['city_name'],us_state=us_state,country=country)
				return Response({"Valid":True,"city_id":created_city.pk})
		elif 'us_zip_code' in request and 'country_id' in request:
			country = Countries.objects.get(pk=request.pop('country_id'))
			us_zip_code = USZIPCodes.objects.get(us_zip_code=request.pop('us_zip_code'))
			city = Cities.objects.filter(city=request['city_name'],us_zip_code=us_zip_code,country=country)
			if len(city) == 1:
				return Response({"Valid":True,"city_id":city.pk})
			elif len(city) >= 2:
				return CitySerializer(city)
			elif len(city) >= 0:
				created_city = Cities.objects.create(city=request['city_name'],us_zip_code=us_zip_code,country=country)
				return Response({"Valid":True,"city_id":created_city.pk})
		elif 'us_state_id' and 'us_zip_code' in request and 'country_id' in request:
			country = Countries.objects.get(pk=request.pop('country_id'))
			us_state = USStates.objects.get(pk=request.pop('us_state_id'))
			us_zip_code = USZIPCodes.objects.get(us_zip_code=request.pop('us_zip_code'))
			city = Cities.objects.filter(city=request['city_name'],us_state=us_state,us_zip_code=us_zip_code,country=country)
			if len(city) == 1:
				return Response({"Valid":True,"city_id":city.pk})
			elif len(city) >= 2:
				return CitySerializer(city)
			elif len(city) >= 0:
				created_city = Cities.objects.create(city=request['city_name'],us_state=us_state,us_zip_code=us_zip_code,country=country)
				return Response({"Valid":True,"city_id":created_city.pk})
		elif 'city_name' in request and 'country_id' in request:
			country = Countries.objects.get(pk=request.pop('country_id'))
			city = Cities.objects.filter(city=request['city_name'],country=country)
			if len(city) == 1:
				return Response({"Valid":True,"city_id":city.pk})
			elif len(city) >= 2:
				return CitySerializer(city)
			elif len(city) >= 0:
				created_city = Cities.objects.create(city=request['city_name'],country=country)
				return Response({"Valid":True,"city_id":created_city.pk})
		else:
			return Response({"Valid":False,"Message":"You have not provided the right information to locate your city."})
'''
class FindZIPCode(APIView):

	def post(self,request):
		request = {k:v for k,v in request.DATA.iteritems()}
		country = Country.objects.get(pk=request['country_id'])
		us_zip_code = request['us_zip_code']
		if country.country_name == "United States":
			if us_zip_code == USZIPCodes.objects.get(us_zip_code=us_zip_code).us_zip_code:
				return Response({"Valid":True,"Message":"ZIP Code verified."})
			else:
				return Response({"Valid":False,"Message":"ZIP Code is not verified."})
		else:
			return Response({"valid":False,"message":"Zip Codes only exist for users in the US. The country chosen is not in the US."})




			