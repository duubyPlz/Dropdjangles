# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0028_auto_20151013_0736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='full_name',
        ),
    ]
