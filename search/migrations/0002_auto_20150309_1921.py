# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='origin_library_screen_searched_flag',
            new_name='origin_dashboard_explore_view_all_libraries_screen_flag',
        ),
        migrations.RenameField(
            model_name='search',
            old_name='origin_web_screen_searched_flag',
            new_name='origin_dashboard_explore_view_all_users_screen_flag',
        ),
        migrations.AddField(
            model_name='search',
            name='origin_dashboard_subscribed_view_all_libraries_screen_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='origin_dashboard_subscribed_view_all_users_screen_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='origin_library_screen_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='origin_web_screen_flag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
