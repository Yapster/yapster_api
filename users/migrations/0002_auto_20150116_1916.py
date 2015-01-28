# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='gender',
            new_name='gender_abbreviation',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='gender',
            new_name='gender_abbreviation',
        ),
    ]
