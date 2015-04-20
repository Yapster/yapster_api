# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yap', '0002_auto_20150116_0448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='library',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='libraryorder',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterModelOptions(
            name='libraryyaporder',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='yap',
            name='is_draft',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
