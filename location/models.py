from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils import timezone
from itertools import chain
import ast
import datetime

class Country(models.Model):
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	def delete(self):
		self.is_active = False
		self.date_deactivated = timezone.now()
		self.save(update_fields=['is_active','date_deactivated'])

class USState(models.Model):
	name = models.CharField(max_length=255)
	abbreviation = models.CharField(max_length=2,blank=True,null=True)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	def delete(self):
		self.is_active = False
		self.date_deleted = timezone.now()
		self.save(update_fields=['is_active','date_deleted'])

	def load_all_usstates(self,country):
		if country.country == 'United States':
			us_states_list = USState.objects.filter(is_active=True)
			return us_states_list

class USZIPCode(models.Model):
	name = models.CharField(max_length=5)
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	def delete(self):
		self.is_active = False
		self.date_deleted = timezone.now()
		self.save(update_fields=['is_active','date_deleted'])

	def check_if_zip_code_exists(self,zipcode):
		if zipcode == USZIPCodes.objects.filter(us_zip_code=zipcode):
			return True
		else:
			return False

class City(models.Model):
	name = models.CharField(max_length=255)
	us_zip_code = models.ForeignKey(USZIPCode,related_name="city_us_zip_code",null=True,blank=True)
	us_state = models.ForeignKey(USState,related_name="city_us_state",null=True,blank=True)
	country = models.ForeignKey(Country,related_name="city_country")
	is_active = models.BooleanField(default=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)

	def delete(self):
		self.is_active = False
		self.date_deleted = timezone.now()
		self.save(update_fields=['is_active','date_deleted'])

class GeographicTarget(models.Model):
	geographic_countries_flag = models.BooleanField(default=False)
	geographic_countries = 	models.ManyToManyField(Country, related_name="geographic_countries",blank=True,null=True) #foreign key to Countries
	geographic_states_flag = models.BooleanField(default=False)
	geographic_states = models.ManyToManyField(USState,related_name="geographic_states",blank=True,null=True)
	geographic_zip_codes_flag = models.BooleanField(default=False)
	geographic_zip_codes = models.ManyToManyField(USZIPCode, related_name="geographic_zip_codes",blank=True,null=True)
	geographic_cities_flag = models.BooleanField(default=False) 
	geographic_cities = models.ManyToManyField(City, related_name="geographic_cities",blank=True,null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_deleted = models.DateTimeField(blank=True,null=True)
	is_active = models.BooleanField(default=True)

	def delete(self):
		self.is_active = False
		self.date_deleted = timezone.now()
		self.save(update_fields=['is_active','date_deleted'])











		