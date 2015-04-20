# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('yap', '0003_auto_20150227_2224'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin_dashboard_subscribed_screen_flag', models.BooleanField(default=False)),
                ('origin_dashboard_explore_screen_flag', models.BooleanField(default=False)),
                ('origin_dashboard_channel_screen_flag', models.BooleanField(default=False)),
                ('origin_profile_screen_flag', models.BooleanField(default=False)),
                ('origin_library_screen_searched_flag', models.BooleanField(default=False)),
                ('origin_web_screen_searched_flag', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=255)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('is_after_request', models.BooleanField(default=False)),
                ('is_trending', models.BooleanField(default=False)),
                ('is_recent', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('origin_dashboard_channel_searched', models.ForeignKey(related_name='in_searches', blank=True, to='yap.Channel', null=True)),
                ('origin_library_searched', models.ForeignKey(related_name='in_searches', blank=True, to='yap.Library', null=True)),
                ('origin_profile_searched', models.ForeignKey(related_name='in_searches', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='searches', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=(models.Model,),
        ),
    ]
