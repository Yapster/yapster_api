from django.contrib.auth.models import User
from rest_framework import serializers
from location.models import *

class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		exclude = ["is_active","date_activated","date_deactivated"]

class USZIPCodeSerializer(serializers.ModelSerializer):

	class Meta:
		model = USZIPCode
		exclude = ["is_active","date_activated","date_deactivated"]

class USStateSerializer(serializers.ModelSerializer):

	class Meta:
		model = USState
		exclude = ["is_active","date_activated","date_deactivated"]

class CitySerializer(serializers.ModelSerializer):

	country = CountrySerializer
	usstates = USStateSerializer

	class Meta:
		model = City
		exclude = ["is_active","date_activated","date_deactivated"]
