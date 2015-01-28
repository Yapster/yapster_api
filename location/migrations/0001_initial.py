# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeographicTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geographic_countries_flag', models.BooleanField(default=False)),
                ('geographic_states_flag', models.BooleanField(default=False)),
                ('geographic_zip_codes_flag', models.BooleanField(default=False)),
                ('geographic_cities_flag', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('geographic_cities', models.ManyToManyField(related_name='geographic_cities', null=True, to='location.City', blank=True)),
                ('geographic_countries', models.ManyToManyField(related_name='geographic_countries', null=True, to='location.Country', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='USState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=2, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='USZIPCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=5)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='geographictarget',
            name='geographic_states',
            field=models.ManyToManyField(related_name='geographic_states', null=True, to='location.USState', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='geographictarget',
            name='geographic_zip_codes',
            field=models.ManyToManyField(related_name='geographic_zip_codes', null=True, to='location.USZIPCode', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(related_name='city_country', to='location.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='us_state',
            field=models.ForeignKey(related_name='city_us_state', blank=True, to='location.USState', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='us_zip_code',
            field=models.ForeignKey(related_name='city_us_zip_code', blank=True, to='location.USZIPCode', null=True),
            preserve_default=True,
        ),
    ]
